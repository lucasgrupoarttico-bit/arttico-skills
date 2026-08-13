# Regras de Design — Preço Base

> Foto do produto como herói no centro, selos no topo e a comparação de preço
> COM × SEM a marca na base. Versão mais sofisticada/premium da oferta 2x1.
> Nasceu de referências validadas da Prime Gourmet (Casa Moscou).

---

## Conceito

Mesma lógica de "você paga metade" do Preço Topo, mas com a **foto do produto no
centro como herói** e os preços ancorados na base. Os selos ("EXCLUSIVIDADE ◆
ECONOMIA") e a pílula de economia dão ar de clube premium. Ideal quando a foto é
forte e a marca é sóbria/high ticket.

---

## Dimensões

- **Story:** 1080×1920 (`layout-b-story.html`)
- **Feed:** 1080×1440 (`layout-b-feed.html`)

**Diferença crítica entre os formatos** (aprendizado da Prime):
- **Feed:** foto `flex: 1` preenchendo o meio — funciona porque o canvas é curto
- **Story:** **NÃO** deixar a foto `flex: 1` (estica e cria um vão enorme entre a
  headline no topo e os preços na base). Em vez disso: foto com **altura fixa**
  (~1040px), `body { justify-content: center }` pra agrupar tudo no centro, e
  `object-position: center 62%` pra focar o produto (corta o fundo vazio). As
  sobras viram margem preta equilibrada em cima/embaixo, não um vão esticado

---

## Estrutura

```
body (flex-direction: column, bg: cor primária escura da marca)
  ├── .mini (flex, center, gap)   ← "EXCLUSIVIDADE" · logo diamante da marca · "ECONOMIA"
  │                                  selos uppercase brancos, mutáveis
  ├── .head-block (text-align: center)
  │     ├── .headline   ← "2 [ITEM] NO / [PARCEIRO]" — Montserrat 800 ~78px
  │     │                  o número/palavra-chave ("2") na cor de acento
  │     └── .subline    ← PÍLULA cor de acento, texto escuro: "ECONOMIA CERTA DE R$X"
  ├── .photo            ← foto herói (feed: flex:1 | story: height fixa + objY 62%)
  │     ├── .photo-img  ← object-fit: cover
  │     └── ::after     ← gradiente fundindo topo e base com o fundo
  └── .prices (display: flex, na base)
        ├── .col.com  → .lbl "COM [MARCA]" (acento, ~60px) + .box preço (contorno acento)
        └── .col.sem  → .lbl "SEM [MARCA]" (branco, ~60px) + .box preço (contorno branco)
```

---

## Preços (exagerados)

- `.lbl` "COM/SEM [MARCA]": Montserrat 800, ~60px, uppercase. COM na cor de acento,
  SEM em branco
- `.box` do preço: `font-size ~56px`, Montserrat 800, `border-radius: 12px`,
  `padding ~24px`
  - COM: `border: 3px solid [acento]; color: [acento]; background: rgba([acento], 0.10)`
  - SEM: `border: 3px solid rgba(255,255,255,0.45); color: #fff`
- Boxes **subidos da margem** — dar `padding-bottom` generoso (~96px) pra
  respirarem embaixo, como na referência

---

## Selos e pílula de economia

- **Mini-header:** dois selos brancos uppercase ("EXCLUSIVIDADE" / "ECONOMIA")
  flanqueando a **logo diamante** da marca (circular, ~74px). Selos mutáveis
- **Pílula de economia:** fundo cor de acento, texto na cor do fundo, uppercase
  ~20px, weight 700, logo abaixo da headline. Destaca o gatilho principal (economia)

---

## Cores

- **Fundo:** cor primária escura da marca (ex: Prime `#010300`)
- **Acento:** cor de destaque (ex: dourado `#F1B835`) — número da headline, pílula,
  "COM [MARCA]", contorno do box COM, logo
- **Branco:** selos, headline, "SEM [MARCA]", contorno do box SEM

---

## Regras gerais

- **Preços movidos a dado real** — parceiro, preço COM, preço SEM, economia
- Foto herói base64 via script Node (nunca caminho relativo/com espaços)
- Placeholder escuro se não houver foto; dropar a imagem em `marca/` e re-rodar
- Story: **nunca** `flex: 1` na foto (ver Dimensões) — usar altura fixa + centralizar
- Sem travessões em nenhum texto

---

## Adaptação por cliente

1. Ler o design guide pra cor primária (fundo), acento e logo
2. Headline "2 [ITEM] NO [PARCEIRO]" com o número no acento
3. Pílula "ECONOMIA CERTA DE R$X" com o valor economizado
4. Selos do mini-header no tom da marca ("EXCLUSIVIDADE / ECONOMIA / VANTAGEM")
5. Foto real do produto do parceiro no centro
6. Reaproveitável: trocar parceiro + foto + valores pros próximos

---

## O que ajustar

- **Story com vão/espaço esticado:** foto com altura fixa + `justify-content: center`
  no body + `object-position` focando o produto (NÃO usar `flex: 1` no story)
- **Preço/label pouco visível:** aumentar `.lbl` e `.box` (queixa comum — exagerar)
- **Muito espaço em branco no topo:** aumentar a headline
- **Item específico:** trocar "pratos" pelo item real ("hambúrgueres")

Pede pro Claude: "muda a regra X no design preço base" e ele edita este arquivo.
