# Regras de Design — Comparação

> Dois estados lado a lado: tradicional vs marca, antes/depois, com vs sem. Dois
> cards sobre um fundo de cor única. O contraste vem do card vencedor elevado +
> tratamento da foto + ícones, nunca de cores de fundo diferentes.

---

## Conceito

Mostra a escolha óbvia. A pessoa bate o olho e vê dois caminhos: o comum
(apagado, cinza) e o da marca (vivo, elevado, com brilho sutil). O design faz o
trabalho de persuasão antes mesmo da leitura. Ideal pra vender diferencial claro
contra o "jeito tradicional" ou concorrente genérico.

---

## Dimensões

- **Story:** 1080×1920 (`criativo.html`)
- **Feed:** 1080×1440 (`criativo-feed.html`)

Duas variações da mesma base:
- **Com foto** — cada card tem a foto do respectivo estado entre o header e a lista
- **Sem foto** — mesma estrutura sem o bloco de foto (cards mais curtos, ganham
  banda de oferta opcional acima do CTA)

---

## Estrutura

```
body (flex-direction: column, align-items: center, justify-content: center,
      bg: cor primária da marca, padding ~44px 52px)
  ├── .kicker          ← pílula "Pode comparar" — fundo cor de acento, texto na cor do fundo
  ├── .headline        ← título uppercase centralizado (fonte de título da marca)
  ├── .cards           ← display: flex, gap: 20px, align-items: stretch
  │     ├── .card.lose ← estado negativo: bg levemente mais claro que o fundo, borda fraca
  │     │     ├── .card-head   ← chip(✕) + título; min-height fixo p/ alinhar fotos entre cards
  │     │     ├── .card-photo  ← (só com foto) foto do estado negativo, DESSATURADA + escurecida
  │     │     └── .rows         ← 5 itens, ícone ✕ apagado + texto ~55% opacidade, divisória fina
  │     └── .card.win  ← estado positivo (VENCEDOR): elevado
  │           ├── .card-head   ← chip(✓ cor de acento) + título na cor de acento
  │           ├── .card-photo  ← (só com foto) foto do estado positivo, natural
  │           └── .rows         ← 5 itens, ícone ✓ na cor de acento + texto cheio
  └── .cta             ← CTA na base (ver regras de estilo)
```

---

## Regra crítica da foto (com foto)

- O container `.card-photo` deve ter **a mesma proporção da imagem original**
  (`aspect-ratio`) para que `object-fit: cover` mostre a foto **inteira, sem
  cortar pessoas**. Retrato de estúdio (4000×6000) → `aspect-ratio: 2/3`. Checar
  a proporção real do arquivo antes (PowerShell `System.Drawing` ou similar) e
  espelhar no container
- **Nunca** forçar proporção paisagem (4/5, 16/9) num retrato — corta cabeça/pés
- **Cada lado usa a SUA foto** — nunca a mesma foto vazando atrás dos dois
- Lado negativo: `filter: grayscale(0.55) brightness(0.82)` — comunica o "pior"
  sem precisar de cor

---

## Card vencedor (elevado)

```css
.card.win {
  background: linear-gradient(180deg, [primária+5%], [primária-2%]);
  border: 1.5px solid rgba([acento], 0.5);
  box-shadow: 0 24px 70px rgba([acento], 0.10);   /* glow sutil */
}
.card.lose { background: [primária+4%]; border: 1px solid rgba([acento], 0.08); }
```

---

## Ícones / marcadores

- ✓ positivo: chip preenchido na cor de acento (texto na cor do fundo); marcadores
  das linhas na cor de acento
- ✕ negativo: chip **vazado/apagado** (borda + texto a ~30-55% de opacidade);
  marcadores das linhas apagados
- **Só usar X vermelho `#E53935` se o design guide permitir cores vibrantes.**
  Marcas com paleta restrita (ex: Outlier) → usar o acento da marca apagado,
  nunca vermelho néon

---

## Cores

- **Fundo:** cor primária da marca (única — sem contraste de cor no fundo)
- **Card lose:** primária +4% (levemente mais claro)
- **Card win:** gradiente primária +5% → -2%
- **Acento:** cor de destaque da marca (✓, título do card win, kicker, CTA)

---

## CTA

- Estilo **linear (contorno)** quando a marca for premium/sóbria:
  `background: transparent; border: 2px solid [acento]; color: [acento]`,
  `align-self: center`, largura automática, fonte de título ~30px
- Estilo **pílula preenchida** (acento sólido, texto na cor do fundo) quando a
  marca pedir CTA forte. Máx 1 por criativo

---

## Regras gerais

- **5 itens por lado** (padrão aprovado). Texto direto; pode passar de uma linha
- `.card-head` com `min-height` fixo (~80px) pra as fotos começarem na mesma
  altura nos dois cards mesmo com títulos de tamanhos diferentes
- `align-items: stretch` nos cards mantém os dois com a mesma altura
- Conteúdo centralizado verticalmente (`justify-content: center`) — sem espaço
  morto; se sobrar respiro, aumentar foto/tipografia antes de deixar vazio
- Logo/foto base64 ou caminho absoluto — nunca relativo nem com espaços
- Gerar via script Node que lê as imagens, faz base64 e escreve o HTML (evita o
  problema de `file:///` com espaços no caminho). Renderizar com `npx playwright
  screenshot` passando o **nome relativo** do HTML
- Sem travessões em nenhum texto

---

## Adaptação por cliente

1. Ler o design guide pra cor primária (fundo) e cor de acento (✓, CTA, kicker)
2. Verificar se a paleta permite cores vibrantes — se não, X apagado no acento,
   nunca vermelho
3. Com foto: usar a foto de cada estado (marca vs tradicional) na proporção real
4. Escrever 5 itens por lado no tom do cliente, comparando o diferencial real

---

## O que ajustar

- **Foto cortando pessoa:** conferir `aspect-ratio` do container = proporção real do arquivo
- **Marca sem cores vibrantes:** trocar X vermelho pelo acento apagado
- **Sem foto disponível:** usar a variação sem foto (cards mais curtos + banda de oferta)
- **CTA fraco demais pra marca:** trocar outlined por pílula preenchida (máx 1)

Pede pro Claude: "muda a regra X no design comparação" e ele edita este arquivo.
