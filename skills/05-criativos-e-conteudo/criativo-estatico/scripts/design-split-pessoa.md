# Regras de Design — Split Pessoa

> Frame dividido em duas metades horizontais. Metade superior: conteúdo clean
> (headline, subheadline e CTA). Metade inferior: só a foto da pessoa, sem texto.

---

## Conceito

Separação limpa entre mensagem e rosto. Em cima, o argumento em tipografia
elegante sobre fundo claro; embaixo, a pessoa "olhando pra fora" da peça. Passa
seriedade e autoridade sem sobrepor texto na cara de ninguém. Ótimo pra
especialista, consultor, médico, profissional que vende confiança.

---

## Dimensões

- **Story:** 1080×1920 (`criativo.html`)
- **Feed:** 1080×1440 (`criativo-feed.html`)

Divisão 50/50 padrão. Ajustar pra 45/55 (top menor) se o conteúdo for muito curto.

---

## Estrutura

```
body (flex-direction: column, height: 1920px)
  ├── .top-half         ← height: 50%, bg: #F5F0E8 ou #F5F4F1, padding: 80px 90px 70px
  │     │                  justify-content: space-between
  │     ├── .brand-bar   ← logo esquerda + label produto direita (small caps, opacidade 35%)
  │     └── .top-content ← display: flex, flex-direction: column, gap: 28px
  │           ├── .headline    ← Playfair Display ExtraBold, ~92px, cor #0D0D0D
  │           ├── .subtitle    ← Inter regular, ~34px, opacidade 50%
  │           └── .cta-outlined ← outlined pill, cor da marca, align-self: flex-start
  └── .bottom-half      ← height: 50%, position: relative, overflow: hidden
        └── .person-photo ← position: absolute, inset: 0, object-fit: cover, object-position: center top
```

---

## Cores

- **Fundo do topo:** nunca branco puro — usar `#F5F0E8` (quente) ou `#F5F4F1` (neutro)
- **Headline:** `#0D0D0D` (preto suave)
- **Subtitle:** preto a 50% de opacidade
- **CTA e label:** cor da marca

---

## Tipografia

- **Headline:** Playfair Display ExtraBold — **nunca sans-serif neste layout**
- **Subtitle:** Inter regular
- **Label da brand-bar:** small caps, opacidade 35%

---

## Regras

- **Metade inferior contém APENAS a foto** — sem CTA, sem texto sobreposto, sem overlay
- Todo o conteúdo (headline, subheadline, CTA) fica na metade superior
- Topo: nunca fundo branco puro (`#F5F0E8` ou `#F5F4F1`)
- `.top-half` usa `justify-content: space-between` — brand-bar no topo, conteúdo embaixo
- CTA: outlined pill (`border: 2.5px solid [cor-marca]`, `background: transparent`),
  `align-self: flex-start`
- Foto: `object-position: center top` pra manter o rosto visível ao cortar
- Divisão 50/50 padrão; 45/55 se o conteúdo for curto
- Sem travessões em nenhum texto
- Logo base64, nunca `src` relativo ou com espaços

---

## Imagem

- Foto de pessoa, retrato preferencialmente vertical
- `object-fit: cover`, `object-position: center top` — evita cortar a cabeça
- Base64 ou caminho absoluto `file:///`. Nunca relativo

---

## Adaptação por cliente

1. Ler o design guide pra cor primária (CTA, label) e conferir se a marca aceita
   Playfair na headline; se a marca tiver serifada própria, usar a dela
2. Foto real do cliente/especialista, vertical, com o rosto no terço superior
3. Fundo do topo: escolher `#F5F0E8` se a paleta for quente (dourado/terracota),
   `#F5F4F1` se for neutra/fria
4. Label da brand-bar: nome do produto/serviço do cliente

---

## O que ajustar

- **Conteúdo curto:** mudar divisão pra 45/55 (top menor, foto maior)
- **Cabeça cortada na foto:** ajustar `object-position` pra `center top` ou `top`
- **Marca não combina com Playfair:** trocar pela serifada do design guide (nunca sans)

Pede pro Claude: "muda a regra X no design split pessoa" e ele edita este arquivo.
