# 06 — Criativos e conteúdo

**Quando usar:** o roteiro já existe e agora é hora de produzir a peça — do PNG pronto até a publicação.

| Skill | O que faz | Chame assim |
|-------|-----------|-------------|
| [`criativo-estatico`](criativo-estatico/) | Gera criativo estático em PNG nos três formatos (story, feed e quadrado), a partir de briefing ou de pauta em alta no nicho. | "cria um criativo pro cliente X" |
| [`carrossel`](carrossel/) | Cria carrossel completo pra Instagram e TikTok com a identidade visual da marca: texto editorial, HTML e render em PNG. | "faz um carrossel sobre X" |
| [`publicar-instagram`](publicar-instagram/) | Publica os carrosséis e posts direto no Instagram e TikTok, via Post for Me ou Graph API. | "publica esse carrossel" |

## Ordem natural

[`direcionamento-criativos`](../05-direcionamento-de-criativos/) (o roteiro) → `criativo-estatico` ou `carrossel` → `publicar-instagram`

## Instalação

```bash
cp -r skills/06-criativos-e-conteudo/carrossel ~/.claude/skills/
```

> A pasta numerada só organiza este repositório. Copie **a pasta da skill**, nunca a pasta da categoria.
> As skills de imagem usam Playwright pra renderizar. `publicar-instagram` pede credenciais no primeiro uso.
