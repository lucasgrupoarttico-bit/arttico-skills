# 02 — Pesquisa e concorrência

**Quando usar:** antes de criar oferta, criativo ou campanha, pra saber o que o mercado já está rodando e captar dados de fora.

| Skill | O que faz | Chame assim |
|-------|-----------|-------------|
| [`analise-concorrentes`](analise-concorrentes/) | Varre Meta Ad Library, Google Ads, Instagram e TikTok dos concorrentes. Detecta criativo validado (2+ anúncios iguais) e sugere ângulos, palavras-chave e headlines. | "analisa os concorrentes de X" |
| [`apify`](apify/) | Coleta dados via Apify: leads do Google Maps, perfis e posts do Instagram, vídeos do TikTok e anúncios da Facebook Ad Library. | "coleta leads de X em Y" |
| [`yt-research`](yt-research/) | Pesquisa vídeos do YouTube sobre um tema e devolve dores, hooks e objeções pra alimentar copy. | "pesquisa no youtube sobre X" |

## Instalação

```bash
cp -r skills/02-pesquisa-e-concorrencia/apify ~/.claude/skills/
```

> A pasta numerada só organiza este repositório. Copie **a pasta da skill**, nunca a pasta da categoria.
> `apify` precisa de token: renomeie `.env.example` para `.env` e preencha.
