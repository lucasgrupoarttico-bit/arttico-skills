# 05 — Direcionamento de criativos

**Quando usar:** o plano está aprovado e agora é preciso dizer ao time **o que gravar e o que escrever** — antes de qualquer peça sair.

| Skill | O que faz | Chame assim |
|-------|-----------|-------------|
| [`direcionamento-criativos`](direcionamento-criativos/) | Monta o Direcionamento de Criativos do cliente em apresentação vertical no padrão Arttico: briefing técnico das peças, avatar (dores e desejos) e roteiros cena a cena por etapa de funil, em tabela Arte \| Texto \| Imagem \| Observações. Gera o PDF e exporta pro Canva. | "monta o direcionamento de criativos do cliente X" |

## O que sai daqui

Um documento pronto pra entregar a quem grava e edita, com roteiro por etapa de funil:

- **Topo** — atração e problema
- **Meio** — prova e diferencial
- **Fundo** — sempre com pelo menos um UGC em vídeo (roteiro "E eu que...") e um estático em formato notícia

Dois layouts disponíveis: **Aurora Ártica** (padrão, gradiente navy → teal) e **Disciplina Ártica** (navy + branco).

## Onde continuar

Com o roteiro em mãos, a produção da peça é em [`06-criativos-e-conteudo`](../06-criativos-e-conteudo/). O plano que antecede este documento está em [`01-planejamento-de-cliente`](../01-planejamento-de-cliente/).

## Instalação

```bash
cp -r skills/05-direcionamento-de-criativos/direcionamento-criativos ~/.claude/skills/
```

> A pasta numerada só organiza este repositório. Copie **a pasta da skill**, nunca a pasta da categoria.
> A geração do PDF usa Playwright (`SKILL_FILES/render-pdf.js`).
