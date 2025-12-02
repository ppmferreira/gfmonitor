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

---

## 🎮 Gerenciamento do Sistema

### Comandos Essenciais

#### Verificar Status
```bash
sudo systemctl status gfmonitor
```
Exibe o estado atual do serviço, uptime, PID e últimas mensagens de log.

#### Parar o Monitoramento
```bash
sudo systemctl stop gfmonitor
```
Interrompe temporariamente o monitoramento.

#### Iniciar o Monitoramento
```bash
sudo systemctl start gfmonitor
```
Inicia ou reinicia o serviço de monitoramento.

#### Reiniciar o Serviço
```bash
sudo systemctl restart gfmonitor
```
Útil após fazer alterações nas configurações.

#### Desabilitar Inicialização Automática
```bash
sudo systemctl disable gfmonitor
```
O serviço não iniciará automaticamente no boot.

#### Habilitar Inicialização Automática
```bash
sudo systemctl enable gfmonitor
```
Garante que o serviço inicie automaticamente com o sistema.

---

## 📊 Visualização de Logs

### Ver Logs em Tempo Real
```bash
sudo journalctl -u gfmonitor -f
```
Acompanhe todas as atividades do monitor em tempo real.

### Ver Últimas Entradas
```bash
sudo journalctl -u gfmonitor -n 100
```
Exibe as últimas 100 linhas de log.

### Logs de Hoje
```bash
sudo journalctl -u gfmonitor --since today
```
Visualize todas as atividades do dia atual.

### Logs de um Período Específico
```bash
sudo journalctl -u gfmonitor --since "2025-12-01" --until "2025-12-02"
```
Consulte logs de um intervalo de datas específico.

---

## 📨 Formato das Notificações Discord

Cada comando executado por um GM gera uma notificação elegante e informativa:

**🛡️ Comando GM Detectado**

```
👮 Game Master: NomeDoGM
📍 Local: Canal 1
⚙️ Comando Utilizado: ci 16225
🕒 2025/12/02 14:35:21-03
```

### Informações Incluídas:
- **Nome do Game Master**: Identifica quem executou a ação
- **Canal/Zona**: Localização exata do servidor
- **Comando Completo**: O comando GM exato que foi executado
- **Timestamp Preciso**: Data e hora com fuso horário

---

## ⚙️ Configurações Avançadas

### Arquivo `.env`

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

**🔐 Segurança**: Nunca compartilhe ou versione este arquivo publicamente.

### Parâmetros em `gfmonitor.py`

#### Configurações de Monitoramento
```python
# Zonas a serem monitoradas
ZONES = [...]

# Padrão de arquivos de log
LOG_PATTERN = "GMCommand*.log*"
```

#### Configurações de Discord
```python
# Personalizar nome do bot (opcional)
DISCORD_USERNAME = "GM Monitor"

# Personalizar avatar do bot (opcional)
DISCORD_AVATAR = "https://..."
```

#### Configurações de Rate Limiting
```python
# Máximo de mensagens por janela de tempo
RATE_LIMIT_MESSAGES = 25

# Janela de tempo em segundos
RATE_LIMIT_WINDOW = 60
```

#### Configurações de Histórico
```python
# True = ignora comandos antigos ao iniciar
# False = processa todo o histórico
SKIP_HISTORY = True
```

**💡 Recomendação**: Mantenha `SKIP_HISTORY = True` para evitar spam de notificações antigas ao reiniciar o serviço.

---

## 🔧 Solução de Problemas

### ❌ Serviço Não Inicia

**Problema**: O serviço falha ao iniciar.

**Solução**:
```bash
# Verifique os logs de erro
sudo journalctl -u gfmonitor -n 50 --no-pager

# Verifique permissões do arquivo
ls -la /root/gfmonitor/gfmonitor.py

# Teste manualmente
python3 /root/gfmonitor/gfmonitor.py
```

### ❌ Erro 403 no Webhook

**Problema**: Discord retorna "403 Forbidden".

**Possíveis Causas**:
- URL do webhook incorreta ou inválida
- Webhook foi deletado no Discord
- Permissões insuficientes no canal

**Solução**:
1. Verifique se a URL no arquivo `.env` está correta
2. Teste a URL diretamente com um curl:
```bash
curl -X POST https://SEU_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{"content":"Teste"}'
```
3. Recrie o webhook no Discord se necessário

### ❌ Comandos Não Aparecem

**Problema**: Comandos GM não geram notificações.

**Diagnóstico**:
```bash
# Verifique se os caminhos existem
ls -la /root/gf_server/ZoneServer*/GMCommand*

# Verifique logs do monitor
sudo journalctl -u gfmonitor -f

# Verifique se novos logs estão sendo criados
watch -n 2 'ls -lht /root/gf_server/ZoneServer101/GMCommand* | head -5'
```

**Soluções**:
- Confirme que os caminhos em `ZONES` estão corretos
- Verifique se os arquivos de log existem e têm permissão de leitura
- Confirme que o padrão `LOG_PATTERN` corresponde aos nomes dos arquivos

### ❌ Rate Limit Constante

**Problema**: Muitas mensagens "Rate limit atingido".

**Solução**:
```python
# Ajuste os limites em gfmonitor.py
RATE_LIMIT_MESSAGES = 20  # Reduza para ser mais conservador
RATE_LIMIT_WINDOW = 60
```

### ⚡ Aplicar Alterações

Após qualquer modificação nos arquivos de configuração:
```bash
sudo systemctl restart gfmonitor
sudo systemctl status gfmonitor
```

---

## 📋 Requisitos do Sistema

- **Sistema Operacional**: Linux com systemd
- **Python**: 3.6 ou superior
- **Permissões**: Acesso root para instalação do serviço
- **Rede**: Conexão com a internet para enviar notificações
- **Armazenamento**: Aproximadamente 50MB de espaço livre

---

## 🎯 Casos de Uso

### 🏢 Gestão de Servidores Comerciais
Mantenha auditoria completa de todas as ações administrativas, garantindo transparência e accountability.

### 👥 Monitoramento de Equipes
Supervisione múltiplos GMs trabalhando simultaneamente em diferentes canais.

### 🔍 Investigação de Incidentes
Logs completos com timestamp para rastrear ações específicas e resolver disputas.

### 📈 Análise de Atividades
Acompanhe padrões de uso de comandos GM para otimização de processos.

---

## 📝 Estrutura de Arquivos

```
/root/gfmonitor/
├── gfmonitor.py           # Script principal do monitor
├── gfmonitor.service      # Arquivo de serviço systemd
├── .env                   # Configurações sensíveis (webhook)
└── README.md              # Esta documentação
```

---

## 🔄 Atualizações e Manutenção

### Atualizar o Sistema

1. Pare o serviço:
```bash
sudo systemctl stop gfmonitor
```

2. Faça backup das configurações:
```bash
cp /root/gfmonitor/.env /root/gfmonitor/.env.backup
```

3. Atualize os arquivos necessários

4. Reinicie o serviço:
```bash
sudo systemctl restart gfmonitor
```

### Backup Regular

Recomendamos fazer backup periódico dos seguintes arquivos:
- `.env` (contém webhook)
- `gfmonitor.py` (contém suas configurações de ZONES)

---

## 💡 Dicas de Otimização

### Performance
- O monitor consome recursos mínimos (~5-10MB RAM)
- Intervalo de verificação padrão: 2 segundos (ajustável no código)
- Suporta monitoramento de dezenas de canais simultaneamente

### Escalabilidade
- Adicione novos canais simplesmente editando a lista `ZONES`
- Não há limite prático de canais monitorados
- Rate limiting automático previne sobrecarga

### Personalização
- Customize cores dos embeds modificando o valor `color` em hexadecimal
- Adicione campos extras nos embeds conforme necessidade
- Implemente filtros adicionais para comandos específicos

---

## 🆘 Suporte

Para problemas técnicos:
1. Consulte a seção "Solução de Problemas" acima
2. Verifique os logs com `journalctl`
3. Teste manualmente o script Python
4. Verifique permissões e caminhos de arquivos

---

## 📄 Licença e Notas

- **Desenvolvido para**: Servidores Grand Fantasia
- **Compatibilidade**: Testado em Ubuntu/Debian Linux
- **Manutenção**: Sistema pronto para produção com auto-recuperação
- **Documentação**: Mantida e atualizada regularmente

---

## ✅ Checklist de Implantação

- [ ] Webhook do Discord configurado no `.env`
- [ ] Zonas corretas configuradas em `ZONES`
- [ ] Serviço instalado via systemd
- [ ] Serviço habilitado para inicialização automática
- [ ] Teste de notificação bem-sucedido
- [ ] Logs sendo gerados corretamente
- [ ] Backup das configurações realizado

---

**🎉 Sistema Pronto para Produção!**

O GF Monitor está agora protegendo e auditando seus servidores 24/7. Todas as ações de GM são monitoradas e registradas automaticamente, garantindo transparência total e controle administrativo completo.
