# 05 — Criativos e conteúdo

**Quando usar:** hora de produzir a peça — do roteiro ao PNG pronto e à publicação.

| Skill | O que faz | Chame assim |
|-------|-----------|-------------|
| [`direcionamento-criativos`](direcionamento-criativos/) | Monta o direcionamento de criativos do cliente em PDF: briefing técnico, avatar e roteiros cena a cena por etapa de funil (topo, meio e fundo). | "monta o direcionamento de criativos do cliente X" |
| [`criativo-estatico`](criativo-estatico/) | Gera criativo estático em PNG nos três formatos (story, feed e quadrado), a partir de briefing ou de pauta em alta no nicho. | "cria um criativo pro cliente X" |
| [`carrossel`](carrossel/) | Cria carrossel completo pra Instagram e TikTok com a identidade visual da marca: texto editorial, HTML e render em PNG. | "faz um carrossel sobre X" |
| [`publicar-instagram`](publicar-instagram/) | Publica os carrosséis e posts direto no Instagram e TikTok, via Post for Me ou Graph API. | "publica esse carrossel" |

## Ordem natural

`direcionamento-criativos` → `criativo-estatico` ou `carrossel` → `publicar-instagram`

## Instalação

```bash
cp -r skills/05-criativos-e-conteudo/carrossel ~/.claude/skills/
```

> A pasta numerada só organiza este repositório. Copie **a pasta da skill**, nunca a pasta da categoria.
> As skills de imagem usam Playwright pra renderizar. `publicar-instagram` pede credenciais no primeiro uso.
