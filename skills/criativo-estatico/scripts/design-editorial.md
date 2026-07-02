# Regras de Design — Editorial

> Fundo claro, muito espaço em branco, tipografia dominante. Sensação de matéria
> de revista ou post de autoridade. O texto é o design.

---

## Conceito

Sofisticação por subtração. Sem foto obrigatória, sem elementos gráficos
pesados: só tipografia elegante, respiro e uma ou duas linhas de acento. Passa
autoridade e bom gosto. Ideal pra posicionamento, frase de impacto, manifesto de
marca, conteúdo de topo que vende ideia antes de vender produto.

---

## Dimensões

- **Story:** 1080×1920 (`criativo.html`)
- **Feed:** 1080×1440 (`criativo-feed.html`)

Conteúdo centralizado verticalmente, âncora decorativa no terço inferior.

---

## Estrutura

```
body (flex-direction: column, padding: 100px 100px 120px, bg: #F5F0E8 ou #F5F4F1)
  ├── .brand-bar        ← logo esquerda + label produto direita (uppercase, opacidade 40%)
  │                        flex-shrink: 0
  ├── .content          ← flex: 1, display: flex, flex-direction: column
  │     │                  justify-content: center, gap: 52px
  │     ├── .divider-line ← 60px × 2px, cor da marca, opacidade 70%
  │     ├── .headline    ← Playfair Display ExtraBold, ~116px, line-height 1.04, #0D0D0D
  │     ├── .accent-line ← Playfair Display italic regular, ~66px, cor da marca (tom mais escuro)
  │     ├── .subtitle    ← Inter regular, ~36px, line-height 1.65, opacidade 50%
  │     └── .cta-outlined ← border 2.5px cor da marca, transparent, border-radius 100px, padding 24px 56px
  ├── .decorative-block ← flex-shrink: 0, gap: 32px — âncora visual no terço inferior
  │     ├── .deco-rule   ← linha horizontal sólida 1px, cor da marca, opacidade 25%
  │     └── .deco-tags   ← pills com categorias/atributos, borda fina, texto opaco
  │                         border: 1px solid rgba(0,0,0,0.12), border-radius: 100px
  └── .footer           ← flex-shrink: 0, justify-content: space-between, margin-top: 40px
                           texto uppercase pequeno, opacidade 28%
```

---

## Cores

- **Fundo:** `#F5F0E8` (tom quente, combina com dourado/terracota) ou `#F5F4F1` (neutro)
- **Headline:** `#0D0D0D`
- **Accent line:** cor da marca em tom **mais escuro** que o primário
  (ex: dourado `#F1B835` → usar `#C49A28` no claro)
- **Subtitle:** preto a 50% de opacidade
- **Dividers/tags:** cor da marca em baixa opacidade

---

## Tipografia

- **Headline:** obrigatoriamente **Playfair Display** ou Lora — nunca sans-serif no editorial
- **Accent line:** Playfair Display italic, regular, na cor da marca (tom escuro)
- **Subtitle:** Inter regular, line-height generoso (1.65)
- **Brand-bar / footer:** uppercase, opacidade baixa

---

## Regras

- Fundo nunca branco puro: `#F5F0E8` (quente) ou `#F5F4F1` (neutro)
- Headline em Playfair Display ou Lora — **nunca sans-serif**
- `.content` com `flex: 1` e `justify-content: center` — centraliza verticalmente
  sem `margin-top` fixo
- `.decorative-block` âncora o terço inferior: elimina o vazio sem foto
- `.deco-rule`: usar `1px solid rgba([cor-marca], 0.25)` — gradiente pode sumir no Playwright
- CTA outlined: **nunca fundo sólido no editorial** — sempre transparente com borda
- Se houver foto/screenshot: inserir entre `.subtitle` e `.cta-outlined` com
  `border-radius: 12px`, `max-height: 600px`
- Sem travessões em nenhum texto
- Logo base64, nunca `src` relativo ou com espaços

---

## Adaptação por cliente

1. Ler o design guide pra cor primária (dividers, accent, CTA) e conferir se a
   marca aceita Playfair; se tiver serifada própria, usar a dela
2. Fundo: `#F5F0E8` pra paleta quente, `#F5F4F1` pra neutra/fria
3. Accent line: derivar um tom mais escuro da cor primária pra contrastar no fundo claro
4. Deco-tags: usar categorias/atributos reais da marca
5. Brand-bar/footer: nome do produto/serviço do cliente

---

## O que ajustar

- **Accent line sumindo no fundo:** escurecer mais o tom da cor da marca
- **Deco-rule invisível no Playwright:** trocar gradiente por `1px solid rgba(...)`
- **Marca não combina com Playfair:** usar a serifada do design guide (nunca sans)
- **Com foto:** inserir entre subtitle e CTA, `border-radius: 12px`, `max-height: 600px`

Pede pro Claude: "muda a regra X no design editorial" e ele edita este arquivo.
