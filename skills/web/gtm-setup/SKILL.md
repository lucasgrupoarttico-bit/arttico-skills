---
name: gtm-setup
description: Automação completa de setup GTM para novos clientes — cria contêiner WEB e SERVER, configura tags GA4/Meta/Clarity, triggers de conversão e domínio no Stape.
---

# GTM Setup Automático

Cria e publica contêineres GTM (WEB + SERVER) para novos clientes da Arttico em um único comando.

## O que cria automaticamente

**Contêiner WEB:**
- Google Tag com GA4 ID + server_container_url (Stape)
- GA4 page_view (DOM Ready)
- Meta Pixel PageView (se Meta ativado)
- Microsoft Clarity (se Clarity ID informado)
- Tags de conversão: click_whatsapp e/ou generate_lead (GA4 + Meta)
- Todos os triggers e variáveis correspondentes

**Contêiner SERVER:**
- GA4 Client
- GA4 Tag (todos os eventos)
- Facebook CAPI (todos os eventos, se Meta ativado)

**Stape:**
- Cria contêiner vinculado ao GTM SERVER
- Configura domínio: `stape.{domínio do cliente}`

## Como usar

```bash
cd .claude/skills/gtm-setup/scripts
python setup_gtm.py
```

## Pré-requisito

Ver `COMO_CONFIGURAR.md` para configurar o Google Cloud Console na primeira vez.
