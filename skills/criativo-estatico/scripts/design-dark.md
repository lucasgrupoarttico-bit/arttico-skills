# Regras de Design — Dark

> Fundo escuro sólido, hierarquia tipográfica forte, sem foto. Um elemento
> oversized decorativo dá textura. Impacto por contraste e tamanho de fonte.

---

## Conceito

Sem foto, sem distração: só a mensagem em fundo escuro. A força vem da hierarquia
tipográfica (label pequena › headline gigante › divider › subtitle › CTA) e de um
símbolo oversized da marca quase invisível por trás, que quebra o fundo chapado.
Ideal pra frase de impacto, dado forte, anúncio direto sem imagem.

---

## Dimensões

- **Story:** 1080×1920 (`criativo.html`)
- **Feed:** 1080×1440 (`criativo-feed.html`)

Conteúdo centralizado verticalmente (`.content` com `flex: 1` + `justify-content: center`).

---

## Estrutura

```
body (flex-direction: column, padding: 100px 90px 120px, bg: cor primária escura, position: relative)
  ├── .bg-letter        ← position: absolute, font-size: 900px, opacity: 0.06, cor da marca
  │                        top: -80px, right: -120px — elemento oversized decorativo
  ├── .logo-area        ← logo no topo, 150-200px largura, position: relative, z-index: 2
  ├── .content          ← flex: 1, display: flex, flex-direction: column, justify-content: center
  │     │                  gap: 40px, position: relative, z-index: 2
  │     ├── .label      ← uppercase, letra espaçada, cor da marca, opacidade 75%
  │     ├── .headline   ← Montserrat ExtraBold (ou fonte de título da marca), ~100px, line-height 1.05
  │     ├── .divider    ← linha fina 80px, cor da marca, opacidade 80%
  │     ├── .subtitle   ← Inter regular, ~38px, opacidade 65%
  │     └── .cta-button ← fundo cor da marca, texto escuro, border-radius: 8px, margin-top: 8px
  └── (sem spacer separado — .content com flex:1 e justify-content:center resolve o espaço)
```

---

## Elemento oversized (obrigatório)

Letra inicial ou símbolo da marca que quebra o fundo chapado:

- `position: absolute`, `font-size: 900px`, `opacity: 0.06`, `overflow: hidden`
- Cor da marca, posicionado no canto (ex: `top: -80px; right: -120px`)
- **Sempre incluir** — evita fundo sólido vazio

---

## Cores

- **Fundo:** cor primária escura da marca (nunca `#000` puro se a marca tiver um escuro próprio)
- **Headline:** branco ou cor clara de alto contraste
- **Label / divider:** cor da marca
- **Subtitle:** branco a 65% de opacidade
- **CTA:** fundo na cor da marca, texto escuro

Sem gradientes coloridos, sem bordas visíveis.

---

## Tipografia

- **Headline:** Montserrat ExtraBold ou fonte de título da marca, ~100px, line-height 1.05
- **Subtitle:** Inter regular, ~38px
- **Label:** uppercase, letter-spacing largo, ~28px

---

## Regras

- `.content` com `flex: 1` e `justify-content: center` — centraliza verticalmente
  sem spacers manuais
- CTA dentro do bloco `.content`, **nunca no rodapé separado**
- Logo `position: relative; z-index: 2` pra ficar acima do elemento oversized
- Logo embutida como base64 no `src` da tag `<img>`
- Sem bordas visíveis, sem gradientes coloridos
- Elemento oversized sempre presente (`opacity: 0.06`)
- Sem travessões em nenhum texto
- Máximo 1 CTA

---

## Adaptação por cliente

1. Ler o design guide pra cor primária escura (fundo), cor da marca (label,
   divider, CTA) e fonte de título
2. Se a marca não tiver um escuro próprio, usar o mais escuro da paleta — evitar
   `#000` puro, que achata
3. Elemento oversized: usar a inicial do nome do cliente ou o símbolo da marca
4. Headline e subtitle no tom do cliente

---

## O que ajustar

- **Fundo achatado:** garantir que o elemento oversized esteja presente com opacidade 0.06
- **Headline não cabe:** reduzir font-size antes de tirar palavras
- **Contraste baixo:** clarear o texto ou escurecer mais o fundo
- **Marca com escuro próprio:** trocar o bg pela cor escura do design guide

Pede pro Claude: "muda a regra X no design dark" e ele edita este arquivo.
