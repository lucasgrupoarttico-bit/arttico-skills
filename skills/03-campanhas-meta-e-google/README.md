# 03 — Campanhas Meta e Google

**Quando usar:** operação do dia a dia da conta — subir, editar, pausar, duplicar e puxar números de campanha.

| Skill | O que faz | Chame assim |
|-------|-----------|-------------|
| [`meta-ads-ratos`](meta-ads-ratos/) | Campanhas Meta Ads (Facebook/Instagram) via SDK oficial: lê, cria, edita, pausa, duplica e deleta. Busca interesses e geolocalização, troca `url_tags`. | "pausa a campanha X do cliente Y" |
| [`google-ads-ratos`](google-ads-ratos/) | Campanhas Google Ads com GAQL: campanhas, ad groups, keywords, search terms, RSA, sitelinks, negativas e quality score. | "quais termos de busca gastaram sem converter?" |

## Onde continuar

Pra decidir **o que** mudar antes de mexer, veja [`04-otimizacao-e-auditoria`](../04-otimizacao-e-auditoria/).

## Instalação

```bash
cp -r skills/03-campanhas-meta-e-google/meta-ads-ratos ~/.claude/skills/
```

> A pasta numerada só organiza este repositório. Copie **a pasta da skill**, nunca a pasta da categoria.
> As duas skills precisam de credenciais: rode `/meta-ads-ratos setup` ou `/google-ads-ratos setup` na primeira vez.
