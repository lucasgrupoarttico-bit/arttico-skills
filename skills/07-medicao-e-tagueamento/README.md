# 07 — Medição e tagueamento

**Quando usar:** cliente novo entrando (instalar a medição) ou dúvida sobre o que aconteceu no site depois do clique.

| Skill | O que faz | Chame assim |
|-------|-----------|-------------|
| [`gtm-setup`](gtm-setup/) | Setup completo de Google Tag Manager: contêiner WEB e SERVER, tags GA4/Meta/Clarity, triggers de conversão e domínio no Stape. | "configura o GTM do cliente X" |
| [`ga4-ratos`](ga4-ratos/) | Consulta o Google Analytics 4: sessões, usuários, bounce, conversões, fontes de tráfego, landing pages, campanhas UTM, geo e realtime. | "quais landing pages converteram mais esse mês?" |

## Ordem natural

`gtm-setup` (instala a medição) → `ga4-ratos` (lê o que foi medido)

## Instalação

```bash
cp -r skills/07-medicao-e-tagueamento/ga4-ratos ~/.claude/skills/
```

> A pasta numerada só organiza este repositório. Copie **a pasta da skill**, nunca a pasta da categoria.
> `ga4-ratos` reaproveita o OAuth do `google-ads-ratos` se já estiver configurado. Rode `/ga4-ratos setup` na primeira vez.
