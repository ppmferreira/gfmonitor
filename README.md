# 🛡️ GF Monitor - Sistema Profissional de Monitoramento GM

> **Solução empresarial completa para monitoramento em tempo real de atividades de Game Masters, com notificações automáticas e inteligentes no Discord.**

Mantenha total controle e transparência sobre todas as ações administrativas executadas em seus servidores de jogo. O GF Monitor é um sistema robusto, confiável e totalmente automatizado que garante a segurança e auditoria completa das operações dos seus Game Masters.

---

## ✨ Por que escolher o GF Monitor?

### 🎯 Recursos Principais

- **✅ Monitoramento Multi-Canal**: Acompanhe simultaneamente todos os seus servidores e zonas em tempo real
- **✅ Notificações Instantâneas**: Receba alertas formatados e profissionais diretamente no Discord
- **✅ Filtragem Inteligente**: Sistema de filtros configurável que ignora comandos irrelevantes (como `sii 0` e `sii 1`)
- **✅ Proteção Anti-Spam**: Rate limiting inteligente que evita bloqueios e garante entrega de todas as notificações
- **✅ Alta Disponibilidade**: Executa como serviço systemd com reinicialização automática e inicialização no boot
- **✅ Auditoria Completa**: Registra timestamp, nome do GM, comando executado e localização exata
- **✅ Configuração Segura**: Credenciais protegidas em arquivo `.env` separado
- **✅ Zero Dependências Externas**: Utiliza apenas bibliotecas nativas do Python

### 🔒 Segurança e Confiabilidade

- Logs detalhados via systemd journal para auditoria completa
- Retry automático com backoff exponencial em caso de falhas temporárias
- Tratamento robusto de erros e exceções
- Proteção contra perda de dados em caso de rotação de logs
- Monitoramento contínuo sem interrupções

---

## 🚀 Guia de Instalação Rápida

### Passo 1: Configurar o Webhook do Discord

Edite o arquivo `.env` e adicione sua URL de webhook:

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/SEU_WEBHOOK_AQUI
```

### Passo 2: Configurar Zonas de Monitoramento

Edite o arquivo `gfmonitor.py` e ajuste as zonas conforme seus servidores:

```python
ZONES = [
    {"path": "/root/gf_server/ZoneServer101", "canal": "Canal 1"},
    {"path": "/root/gf_server/ZoneServer102", "canal": "Canal 2"},
    {"path": "/root/gf_server/ZoneServer103", "canal": "Canal 3"},
    # Adicione quantos canais precisar...
]
```

### Passo 3: Instalar e Ativar o Serviço

Execute os comandos abaixo para instalar o monitor como serviço do sistema:

```bash
# Copiar arquivo de serviço
sudo cp /root/gfmonitor/gfmonitor.service /etc/systemd/system/

# Recarregar configurações do systemd
sudo systemctl daemon-reload

# Ativar inicialização automática
sudo systemctl enable gfmonitor

# Iniciar o serviço
sudo systemctl start gfmonitor

# Verificar status
sudo systemctl status gfmonitor
```

✅ **Pronto!** Seu sistema de monitoramento está ativo e operacional.

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
