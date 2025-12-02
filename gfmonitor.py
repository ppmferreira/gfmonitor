import os
import glob
import time
import json
import urllib.request
from collections import deque
from datetime import datetime, timedelta

# Carrega variáveis de ambiente do arquivo .env
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

# ================== CONFIGURAÇÕES ==================

# Mapeamento pasta -> nome do canal
ZONES = [
    {"path": "/root/gf_server/ZoneServer101", "canal": "Canal 1"},
    {"path": "/root/gf_server/ZoneServer102", "canal": "Canal 2"},
    {"path": "/root/gf_server/ZoneServer103", "canal": "Canal 3"},
    {"path": "/root/gf_server/ZoneServer109", "canal": "Canal 9"},
]

# Padrão de nome dos arquivos GMCommand dentro de cada pasta
# ex: GMCommand1011.log.1116.2016
LOG_PATTERN = "GMCommand*.log*"

# URL de webhook carregada do arquivo .env
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')

# Se quiser forçar outro nome/avatar diferente do webhook,
# preencha aqui. Se deixar None, usa o padrão do webhook.
DISCORD_USERNAME = None      # ex: "GM Watcher"
DISCORD_AVATAR = None        # ex: "https://..."

# Rate limiting (Discord permite ~30 msgs/min, vamos ser conservadores)
RATE_LIMIT_MESSAGES = 25     # mensagens por janela
RATE_LIMIT_WINDOW = 60       # segundos

# Processar histórico sem enviar para Discord (True = não envia histórico)
SKIP_HISTORY = True


# ================== RATE LIMITER ==================

class RateLimiter:
    """Controla a taxa de envio para evitar HTTP 429/403"""
    def __init__(self, max_messages, window_seconds):
        self.max_messages = max_messages
        self.window_seconds = window_seconds
        self.timestamps = deque()
    
    def can_send(self):
        """Verifica se pode enviar mensagem agora"""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window_seconds)
        
        # Remove timestamps antigos
        while self.timestamps and self.timestamps[0] < cutoff:
            self.timestamps.popleft()
        
        return len(self.timestamps) < self.max_messages
    
    def record_send(self):
        """Registra que uma mensagem foi enviada"""
        self.timestamps.append(datetime.now())
    
    def wait_time(self):
        """Retorna quantos segundos esperar antes de poder enviar"""
        if self.can_send():
            return 0
        
        cutoff = datetime.now() - timedelta(seconds=self.window_seconds)
        while self.timestamps and self.timestamps[0] < cutoff:
            self.timestamps.popleft()
        
        if self.timestamps:
            oldest = self.timestamps[0]
            wait = (oldest + timedelta(seconds=self.window_seconds) - datetime.now()).total_seconds()
            return max(0, wait)
        return 0


rate_limiter = RateLimiter(RATE_LIMIT_MESSAGES, RATE_LIMIT_WINDOW)


# ================== FUNÇÕES ==================


def send_to_discord(text: str, skip=False):
    """Envia uma mensagem simples para o webhook do Discord."""
    if skip:
        return  # Modo silencioso (histórico)
    
    if not DISCORD_WEBHOOK_URL or "COLE_AQUI" in DISCORD_WEBHOOK_URL:
        print("[ERRO] DISCORD_WEBHOOK_URL não configurada.")
        return

    # Verifica rate limit
    if not rate_limiter.can_send():
        wait = rate_limiter.wait_time()
        print(f"[WARN] Rate limit atingido. Aguardando {wait:.1f}s...")
        time.sleep(wait + 0.5)

    data = {
        "embeds": [text]  # text agora é um embed dict
    }

    # Só sobrescreve nome/avatar se você tiver configurado
    if DISCORD_USERNAME:
        data["username"] = DISCORD_USERNAME
    if DISCORD_AVATAR:
        data["avatar_url"] = DISCORD_AVATAR

    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; GMMonitor/1.0)"
        },
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status in (200, 204):
                    rate_limiter.record_send()
                    return
                else:
                    print(f"[ERRO] Discord retornou status {resp.status}")
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"[ERRO] Webhook bloqueado (403 Forbidden). Verifique a URL ou permissões.")
                return  # Não tentar reenviar 403
            elif e.code == 429:
                # Rate limit do Discord
                retry_after = int(e.headers.get('Retry-After', 5))
                print(f"[WARN] Rate limit do Discord (429). Aguardando {retry_after}s...")
                time.sleep(retry_after)
            else:
                print(f"[ERRO] HTTP {e.code}: {e.reason}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Backoff exponencial
        except Exception as e:
            print(f"[ERRO] Falha ao enviar pro Discord: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return


def parse_gm_line(line: str):
    """
    Esperado algo assim:
    578245,2025/11/16 23:57:21-03,P:200000274:KombSemPorta,Z:42:琉璃山脈:367:512,ci 16225
    """
    parts = line.split(",")
    if len(parts) < 5:
        return None

    timestamp = parts[1].strip()
    p_field = parts[2].strip()  # P:playerId:Nome
    command = parts[4].strip()  # ex: "ci 16225"

    # pega o nome do personagem/GM
    char_name = "Desconhecido"
    p_parts = p_field.split(":")
    if len(p_parts) >= 3:
        char_name = p_parts[2]

    return {
        "timestamp": timestamp,
        "char_name": char_name,
        "command": command,
    }


def process_line(line: str, filename: str, canal: str, skip_discord=False):
    line = line.strip()
    if not line:
        return

    info = parse_gm_line(line)
    if not info:
        return

    char_name = info["char_name"]
    command = info["command"]
    timestamp = info["timestamp"]
    
    # Ignora comandos sii (todas as variações)
    if command.lower().startswith("sii ") or "recv gm cmd[sii" in command.lower():
        return

    # Cria embed bonitinho
    embed = {
        "title": "🛡️ Comando GM Detectado",
        "color": 0xFF5733,  # Cor laranja/vermelha
        "fields": [
            {
                "name": "👮 Game Master",
                "value": f"**{char_name}**",
                "inline": True
            },
            {
                "name": "📍 Local",
                "value": f"**{canal}**",
                "inline": True
            },
            {
                "name": "⚙️ Comando Utilizado",
                "value": f"`{command}`",
                "inline": False
            }
        ],
        "footer": {
            "text": f"🕒 {timestamp}"
        }
    }
    
    if not skip_discord:
        msg_summary = f"[GM] {char_name} → {command} ({canal})"
        print(msg_summary)
        send_to_discord(embed, skip=skip_discord)
    # Sem print para histórico silencioso


def listar_arquivos():
    """
    Retorna lista de tuplas (path, canal) para todos os GMCommand
    encontrados em todas as ZONES.
    """
    arquivos = []
    for z in ZONES:
        base = z["path"]
        canal = z["canal"]
        pattern = os.path.join(base, LOG_PATTERN)
        for path in glob.glob(pattern):
            arquivos.append((path, canal))
    arquivos.sort(key=lambda x: x[0])
    return arquivos


def main():
    # offsets[path] = {"pos": int, "canal": str}
    offsets = {}

    print("Iniciando monitor de GMCommand...\nZonas configuradas:")
    for z in ZONES:
        print(f"  - {z['path']}  ->  {z['canal']}")
    print()

    # 1) Processa TODO o histórico existente (todas as linhas de todos os arquivos)
    if SKIP_HISTORY:
        print("Modo SKIP_HISTORY ativado - pulando histórico e monitorando apenas novos comandos.\n")
    
    arquivos = listar_arquivos()
    for path, canal in arquivos:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    process_line(line, path, canal, skip_discord=SKIP_HISTORY)
                offsets[path] = {"pos": f.tell(), "canal": canal}
        except FileNotFoundError:
            print(f"[WARN] Arquivo não encontrado (histórico): {path}")

    print("\nHistórico inicial processado. Agora monitorando novas entradas...\n")

    # 2) Loop infinito: monitora novas linhas e novos arquivos
    try:
        while True:
            arquivos = listar_arquivos()

            # novos arquivos que aparecerem depois
            for path, canal in arquivos:
                if path not in offsets:
                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as f:
                            for line in f:
                                process_line(line, path, canal, skip_discord=False)
                            offsets[path] = {"pos": f.tell(), "canal": canal}
                        print(f"[INFO] Novo arquivo monitorado: {path}")
                    except FileNotFoundError:
                        print(f"[WARN] Arquivo sumiu antes de abrir: {path}")
                        continue

            # arquivos já conhecidos: verifica se cresceram
            for path in list(offsets.keys()):
                meta = offsets[path]
                canal = meta["canal"]
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        f.seek(meta["pos"])
                        for line in f:
                            process_line(line, path, canal, skip_discord=False)
                        meta["pos"] = f.tell()
                except FileNotFoundError:
                    print(f"[INFO] Arquivo removido/rotacionado: {path}")
                    offsets.pop(path, None)

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nEncerrando monitor...")


if __name__ == "__main__":
    main()
