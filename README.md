# GF Monitor - Monitor de Comandos GM

Monitor em tempo real de comandos GM executados nos servidores do jogo, com notificações automáticas no Discord.

## 📋 Funcionalidades

- ✅ Monitora múltiplos canais/zonas simultaneamente
- ✅ Envia notificações formatadas para Discord via webhook
- ✅ Ignora comandos `sii 1` e `sii 0`
- ✅ Rate limiting inteligente para evitar bloqueios
- ✅ Processamento de histórico opcional
- ✅ Execução como serviço systemd (auto-restart e boot automático)

## 🚀 Instalação

1. Configure o webhook do Discord no arquivo `gfmonitor.py`:
```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/SEU_WEBHOOK_AQUI"
```

2. Ajuste as zonas monitoradas conforme necessário:
```python
ZONES = [
    {"path": "/root/gf_server/ZoneServer101", "canal": "Canal 1"},
    {"path": "/root/gf_server/ZoneServer102", "canal": "Canal 2"},
    # ... adicione mais canais aqui
]
```

3. Instale o serviço:
```bash
sudo cp /root/gfmonitor/gfmonitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gfmonitor
sudo systemctl start gfmonitor
```

## 🎮 Comandos de Gerenciamento

### Ver status do serviço
```bash
sudo systemctl status gfmonitor
```

### Parar o serviço
```bash
sudo systemctl stop gfmonitor
```

### Iniciar o serviço
```bash
sudo systemctl start gfmonitor
```

### Reiniciar o serviço
```bash
sudo systemctl restart gfmonitor
```

### Ver logs em tempo real
```bash
sudo journalctl -u gfmonitor -f
```

### Ver últimas 100 linhas de log
```bash
sudo journalctl -u gfmonitor -n 100
```

### Desabilitar inicialização automática
```bash
sudo systemctl disable gfmonitor
```

### Habilitar inicialização automática
```bash
sudo systemctl enable gfmonitor
```

## ⚙️ Configurações

### Principais parâmetros em `gfmonitor.py`:

- **ZONES**: Lista de caminhos e nomes dos canais a monitorar
- **LOG_PATTERN**: Padrão de arquivos de log (`GMCommand*.log*`)
- **DISCORD_WEBHOOK_URL**: URL do webhook do Discord
- **RATE_LIMIT_MESSAGES**: Limite de mensagens por janela (padrão: 25)
- **RATE_LIMIT_WINDOW**: Janela de tempo em segundos (padrão: 60)
- **SKIP_HISTORY**: Se True, ignora histórico ao iniciar (padrão: True)

## 📊 Formato das Notificações

As notificações no Discord incluem:
- 👮 **Game Master**: Nome do GM que executou o comando
- 📍 **Local**: Canal/zona onde foi executado
- ⚙️ **Comando Utilizado**: O comando GM específico
- 🕒 **Timestamp**: Data e hora da execução

## 🔧 Troubleshooting

### Serviço não inicia
```bash
sudo journalctl -u gfmonitor -n 50
```

### Webhook retorna erro 403
Verifique se a URL do webhook está correta e se o webhook não foi deletado no Discord.

### Comandos não aparecem
- Confirme que os caminhos em `ZONES` estão corretos
- Verifique se os arquivos de log existem
- Use `journalctl` para ver mensagens de erro

### Aplicar alterações no código
Após editar `gfmonitor.py`, reinicie o serviço:
```bash
sudo systemctl restart gfmonitor
```

## 📝 Notas

- O serviço reinicia automaticamente se cair (intervalo: 10 segundos)
- Comandos `sii 1` e `sii 0` são ignorados por padrão
- O monitor verifica novos comandos a cada 2 segundos
- Rate limiting previne bloqueios do Discord (limite interno de ~30 msgs/min)

## 📄 Arquivos

- `gfmonitor.py` - Script principal do monitor
- `gfmonitor.service` - Arquivo de serviço systemd
- `README.md` - Esta documentação
