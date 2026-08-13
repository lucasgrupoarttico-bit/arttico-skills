# Regras de Design — Foto Fundo

> Foto de pessoa ou ambiente como fundo full-bleed. Texto sobreposto ancorado no
> terço inferior, com overlay em gradiente suave que mantém a foto viva.

---

## Conceito

A foto é a protagonista. O texto entra por cima, mas nunca "mata" a imagem: o
overlay escurece só o necessário pra dar legibilidade na área do texto e deixa a
foto respirar em cima. É o layout mais direto pra transmitir contexto humano
(rosto, ambiente, situação) com uma mensagem curta e forte.

---

## Dimensões

- **Story:** 1080×1920 (`criativo.html`)
- **Feed:** 1080×1440 (`criativo-feed.html`)

Texto ancorado no terço inferior. A foto ocupa o frame inteiro por baixo.

---

## Estrutura

```
body (position: relative, overflow: hidden)
  ├── .bg-photo         ← position: absolute, top/left: 0, width/height: 100%, object-fit: cover
  ├── .overlay          ← position: absolute, top/left: 0, 100%x100%, gradiente (ver abaixo)
  └── .content          ← position: relative, z-index: 2, padding: 100px 90px 120px
        ├── .logo-area   ← logo no topo, base64
        ├── .spacer-top  ← flex: 1 (empurra o conteúdo pra baixo)
        ├── .label       ← uppercase, letra espaçada, cor da marca ou branco
        ├── .headline    ← peso alto, branco, ~100px, line-height 1.05
        ├── .subtitle    ← regular, branco 85%, ~38px
        └── .cta-button  ← pílula branca ou outlined branco
```

---

## Overlay (padrão obrigatório)

```css
background:
  linear-gradient(to bottom, rgba(0,0,0,0.30) 0%, transparent 18%),
  linear-gradient(to top, rgba(0,0,0,0.82) 30%, rgba(0,0,0,0.06) 58%, transparent 74%);
```

- Parte superior: leve escurecimento pro logo ficar legível
- Parte inferior: gradiente âncora o texto sem apagar a foto
- **Nunca opacidade acima de 0.85 no gradiente inferior** — a foto tem que
  permanecer visível e com cores naturais
- Para overlay na cor da marca no lugar do preto: trocar `rgba(0,0,0,...)` pela
  cor primária em rgba, mantendo as mesmas opacidades

**Ajuste feed (1080×1440):** o canvas é menor, então aumentar a cobertura do
gradiente inferior pra compensar:
`rgba(0,0,0,0.82) 30%, rgba(0,0,0,0.06) 58%, transparent 74%`

---

## Posição do texto

- Âncora no terço inferior (o `.spacer-top` com `flex: 1` empurra o conteúdo pra baixo)
- A foto respira acima do texto
- Todo o bloco (label, headline, subtitle, CTA) fica junto na base, sem espalhar

---

## Cores

- **Texto:** branco `#FFFFFF` (headline) e branco 85% (subtitle) — quase sempre,
  porque o texto fica sobre foto escurecida
- **Label:** cor da marca ou branco
- **Overlay:** preto em rgba (padrão) ou cor primária em rgba
- **CTA:** pílula branca (texto na cor primária) ou outlined branco

---

## Tipografia

- **Headline:** fonte de título da marca, peso alto (800/900), ~100px
- **Subtitle:** fonte de corpo, regular, ~38px, branco 85%
- **Label:** uppercase, letter-spacing largo, ~28px

---

## Imagem

- Embutir como base64 ou usar caminho absoluto `file:///`. **Nunca caminho relativo**
- `object-fit: cover`, `object-position` ajustado pra manter o rosto/foco visível
  na parte de cima (que fica limpa)
- Escolher foto com "respiro" na metade superior — se a pessoa estiver no topo,
  o texto embaixo não compete

---

## Elemento oversized (opcional)

Número, letra ou ícone da marca atrás do conteúdo: `z-index: 1`, `opacity: 10-15%`,
cor da marca ou branco. Cria textura sem poluir.

---

## Regras

- **Sempre usar o gradiente suave documentado** — nunca overlay acima de 0.85 de
  opacidade. A foto tem que manter cores naturais; o escurecimento fica só na área
  do texto
- Sem travessões em nenhum texto
- Logo sempre base64, nunca `src` relativo ou com espaços
- Texto ancorado embaixo, nunca centralizado no meio da foto
- Máximo 1 CTA

---

## Adaptação por cliente

1. Ler o design guide pra fonte de título e cor primária (usada no label e no CTA)
2. Escolher foto real do cliente com espaço livre na parte superior
3. Se a marca pedir, trocar o overlay preto pela cor primária em rgba
4. Texto branco funciona pra qualquer marca sobre foto escurecida

---

## O que ajustar

- **Foto muito clara:** aumentar a opacidade do gradiente inferior até no máx 0.85
- **Texto competindo com a foto:** subir o `.spacer-top` ou trocar por foto com
  mais respiro no topo
- **Quer cor da marca no overlay:** trocar `rgba(0,0,0,...)` pela primária em rgba

Pede pro Claude: "muda a regra X no design foto fundo" e ele edita este arquivo.
