# 07 — Landing pages e sites

**Quando usar:** a página do cliente está lenta, a copy não converte, ou você precisa publicar o site.

| Skill | O que faz | Chame assim |
|-------|-----------|-------------|
| [`pagespeed`](pagespeed/) | Audita velocidade (Core Web Vitals), comportamento via GA4 e copy da LP. Cria plano priorizado, implementa os fixes pra chegar em 90+ e gera relatório HTML. | "analisa a velocidade do site do cliente X" |
| [`github-deploy`](github-deploy/) | Configura deploy automático via FTP com GitHub Actions: cria o repo, gera o workflow, orienta os secrets e monitora os runs. A cada push a página publica sozinha. | "configura o deploy automático dessa LP" |

## Instalação

```bash
cp -r skills/07-landing-pages-e-sites/pagespeed ~/.claude/skills/
```

> A pasta numerada só organiza este repositório. Copie **a pasta da skill**, nunca a pasta da categoria.
> `pagespeed` se integra com `ga4-ratos` ([`08-medicao-e-tagueamento`](../08-medicao-e-tagueamento/)) pra ler comportamento real de usuário.
