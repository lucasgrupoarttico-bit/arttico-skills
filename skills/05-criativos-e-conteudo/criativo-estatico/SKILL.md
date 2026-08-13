---
name: criativo-estatico
description: >
  Cria criativos estáticos (PNG nos três formatos: story 1080x1920, feed 1080x1440 e quadrado 1080x1080) para Arttico ou clientes.
  Dois modos: direcionamento (usuário envia briefing) ou pauta em alta (Claude pesquisa assuntos em alta no nicho).
  Lê o design guide da marca antes de gerar qualquer visual.
  Use quando o usuário disser "cria um criativo", "faz um criativo estático",
  "busca pautas pra criativo", "gera criativo para [cliente]", ou enviar um direcionamento de criativo.
---

# /criativo-estatico — Criação de Criativo Estático

## Dependências

- **Design guide:** `marca/design-guide.md` (Arttico) ou informado pelo usuário (cliente)
- **Contexto:** `_contexto/empresa.md`
- **Tom de voz:** `_contexto/preferencias.md`
- **Template HTML:** `.claude/skills/criativo-estatico/template.html`
- **Playwright CLI:** `npx playwright screenshot`

## Setup (primeira vez)

Verificar se Playwright está instalado:

```bash
npx playwright screenshot --help 2>$null && echo "OK" || echo "INSTALAR"
```

Se precisar instalar:

```bash
npx playwright install chromium
```

---

## Modo 1 — Direcionamento

Ativado quando o usuário envia um briefing, texto, PDF ou direcionamento de criativo.

### Passo a passo

1. Identificar para quem é o criativo:
   - Se o usuário não disser, perguntar: "Esse criativo é pra Arttico ou pra qual cliente?"
   - Se for cliente, ler `clientes/[cliente]/marca/design-guide.md`. Se não existir, pedir: "Me passa as cores, logo e fonte da marca deles."

2. Extrair do direcionamento:
   - **Headline** (texto principal, max 8 palavras)
   - **Subtítulo** (complemento, max 15 palavras)
   - **CTA** (chamada pra ação, max 5 palavras)

   Se o direcionamento vier em PDF, ler com a ferramenta de leitura nativa do Claude Code.
   Se vier como texto colado, extrair diretamente.

3. Perguntar qual layout usar (numa mensagem só):
   > "Qual layout você quer pra esse criativo?
   >
   > 1. **Dark** — fundo escuro, título grande, sem foto
   > 2. **Foto fundo** — foto de pessoa como fundo full-bleed, texto sobreposto
   > 3. **Split pessoa** — conteúdo clean em cima, foto da pessoa embaixo
   > 4. **Comparação** — dois cards lado a lado (com ou sem foto), tradicional vs marca / antes/depois
   > 5. **Editorial** — fundo claro, tipografia elegante, espaço em branco
   > 6. **Tweet** — simula post do Twitter/X
   > 7. **Referência** — replicar layout de um anúncio enviado
   > 8. **Notícia** — parece matéria de portal: tarja NOVIDADE, manchete e foto embaixo
   > 9. **Preço topo** — comparação COM × SEM (2x1): preços grandes no topo, foto do produto full-bleed embaixo
   > 10. **Preço base** — foto do produto herói no centro, selos no topo e preços COM × SEM na base
   >
   > Se tiver imagem pra usar, já manda o arquivo ou coloca na pasta `marca/` e me diz o nome."

4. Confirmar os elementos antes de gerar:
   > "Vou gerar com:
   > - Layout: [X]
   > - Headline: [X]
   > - Subtítulo: [X]
   > - CTA: [X]
   > - Imagem: [nome do arquivo ou 'sem imagem']
   >
   > Posso gerar?"

   Aguardar confirmação. Só avançar quando aprovado.

5. Gerar o HTML seguindo as regras do layout escolhido (seções abaixo).
   - Arttico → salvar em `conteudo/criativos/arttico/[tema]/criativo.html`
   - Cliente → salvar em `clientes/[cliente]/conteudo/criativos/[tema]/criativo.html`

6. Renderizar **sempre nos três formatos**: story (1080×1920), feed (1080×1440) e quadrado (1080×1080).

   **Story:**
   ```bash
   npx playwright screenshot --viewport-size=1080,1920 "file:///[caminho-absoluto]/criativo.html" "[mesmo-diretório]/criativo.png"
   ```

   **Feed:** gerar variante do HTML com os ajustes abaixo e renderizar:
   ```bash
   npx playwright screenshot --viewport-size=1080,1440 "file:///[caminho-absoluto]/criativo-feed.html" "[mesmo-diretório]/criativo-feed.png"
   ```

   **Ajustes do HTML para o formato feed (1080×1440):**
   - `height: 1920px` → `height: 1440px`
   - Padding do `.content`: reduzir top de 96px→72px e bottom de 108px→80px
   - Fontes de headline: escalar ~82% (ex: 108px → 88px, 118px → 96px)
   - Fontes de subtítulo/bullets/CTA: reduzir ~18% (ex: 36px → 30px, 34px → 28px)
   - Gradiente do overlay (Layout 2): aumentar cobertura para compensar canvas menor
     `rgba(0,0,0,0.82) 30%, rgba(0,0,0,0.06) 58%, transparent 74%`

   **Quadrado:** gerar variante do HTML e renderizar:
   ```bash
   npx playwright screenshot --viewport-size=1080,1080 "file:///[caminho-absoluto]/criativo-square.html" "[mesmo-diretório]/criativo-square.png"
   ```

   **Ajustes do HTML para o formato quadrado (1080×1080):**
   - `height` → `1080px`. É o canvas mais baixo: o texto tem que preencher sem sobrar
     vão branco e sem estourar. Nunca deixar área vazia grande.
   - **Layouts com foto full-bleed / foto de pessoa / split** (foto-fundo, notícia,
     split-pessoa, referência): no quadrado a pilha "texto em cima, foto embaixo" não
     cabe. Usar **foto ocupando o frame inteiro** (`position:absolute; inset:0; object-fit:cover`)
     + **degradê escuro na base** (transparente no topo → ~0.95 no rodapé) + **copy em
     branco** ancorada embaixo. Assim a pessoa aparece inteira e a copy preenche o vazio.
     Se a foto for 1:1 e cortar o rosto, dar leve zoom/`object-position` pra enquadrar
     rosto até a boca acima do degradê. Regras detalhadas em `scripts/design-noticia.md`.
   - **Layouts sem foto de pessoa** (tweet, comparação, editorial, minimalista, dark,
     preço): manter o layout, só reescalar. Headline ~82% do story, corpo ~85%, paddings
     laterais ~52px e verticais ~46px. Centralizar verticalmente (`justify-content:center`)
     pra não sobrar vão.
   - Manter tarja/faixa/selo encostados nas bordas, sem cantos arredondados.

   **Converter feed PNG para JPG** (quando o cliente pede JPG):
   ```powershell
   Add-Type -AssemblyName System.Drawing
   $bmp = New-Object System.Drawing.Bitmap("criativo-feed.png")
   $ep  = New-Object System.Drawing.Imaging.EncoderParameters(1)
   $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, 92L)
   $ci  = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object {$_.MimeType -eq 'image/jpeg'}
   $bmp.Save("criativo-feed.jpg", $ci, $ep)
   $bmp.Dispose()
   ```

7. Mostrar os três PNGs gerados pro usuário e perguntar se quer ajuste.
   - Se pedir ajuste: editar o HTML base e re-renderizar os três
   - Se aprovar: confirmar onde foram salvos

---

## Modo 2 — Pauta em Alta

Ativado quando o usuário diz "busca pautas" ou "cria criativo sobre assuntos em alta para [cliente/Arttico]".

### Passo a passo

1. Identificar para quem é:
   - Se não informado, perguntar: "Esse criativo é pra Arttico ou pra qual cliente?"

2. Identificar o nicho:
   - Arttico: tráfego pago, marketing digital, performance, Meta Ads, Google Ads, conversão
   - Cliente: ler `clientes/[cliente]/briefing.md` pra entender o nicho

3. Pesquisar pautas em alta:
   - Usar WebSearch com termos do nicho + "tendência 2025", "novidade", "atualização"
   - Buscar 2-3 fontes diferentes

4. Propor 3 a 5 direcionamentos no formato:
   > "Encontrei essas pautas em alta pro nicho [X]:
   >
   > **1. [Assunto]**
   > Headline: [max 8 palavras]
   > Subtítulo: [max 15 palavras]
   > CTA: [max 5 palavras]
   > Layout sugerido: [nome do layout]
   >
   > **2. [Assunto]**
   > ...
   >
   > Qual você quer desenvolver?"

5. Aguardar o usuário escolher um.

6. A partir da escolha, seguir o Modo 1 a partir do passo 3.

---

## Layouts

### Layout 1 — Dark

Fundo escuro sólido, hierarquia tipográfica forte, sem foto. Regras completas em `scripts/design-dark.md`.

**Estrutura:**
```
body (flex-direction: column, padding: 100px 90px 120px, bg: cor primária escura, position: relative)
  ├── .bg-letter        ← position: absolute, font-size: 900px, opacity: 0.06, cor da marca
  │                        top: -80px, right: -120px — elemento oversized decorativo
  ├── .logo-area        ← logo no topo, 150-200px largura, position: relative, z-index: 2
  ├── .content          ← flex: 1, display: flex, flex-direction: column, justify-content: center
  │     │                  gap: 40px, position: relative, z-index: 2
  │     ├── .label      ← uppercase, letra espaçada, cor da marca, opacidade 75%
  │     ├── .headline   ← Montserrat ExtraBold, ~100px, line-height: 1.05
  │     ├── .divider    ← linha fina 80px, cor da marca, opacidade 80%
  │     ├── .subtitle   ← Inter regular, ~38px, opacidade 65%
  │     └── .cta-button ← fundo cor da marca, texto escuro, border-radius: 8px, margin-top: 8px
  └── (sem spacer separado — .content com flex:1 e justify-content:center resolve o espaço)
```

**Elemento oversized:** letra inicial ou símbolo da marca, `position: absolute`, `font-size: 900px`, `opacity: 0.06`, `overflow: hidden`, cor da marca. Sempre incluir — evita fundo sólido vazio.

**Regras:**
- `.content` com `flex: 1` e `justify-content: center` — centraliza verticalmente sem spacers manuais
- CTA dentro do bloco `.content`, nunca no rodapé separado
- Logo `position: relative; z-index: 2` para ficar acima do elemento oversized
- Logo embutida como base64 no `src` da tag `<img>`
- Sem bordas visíveis, sem gradientes coloridos

---

### Layout 2 — Foto Fundo

Foto de pessoa ou ambiente como fundo full-bleed. Texto sobreposto com overlay. Regras completas em `scripts/design-foto-fundo.md`.

**Estrutura:**
```
body (position: relative, overflow: hidden)
  ├── .bg-photo         ← position: absolute, top/left: 0, width/height: 100%, object-fit: cover
  ├── .overlay          ← position: absolute, top/left: 0, 100%x100%, gradient ou rgba
  └── .content          ← position: relative, z-index: 2, padding: 100px 90px 120px
        ├── .logo-area
        ├── .spacer-top ← flex: 1 (empurra conteúdo pra baixo)
        ├── .label
        ├── .headline
        ├── .subtitle
        └── .cta-button
```

**Overlay (gradiente suave — padrão obrigatório):**
```css
background:
  linear-gradient(to bottom, rgba(0,0,0,0.30) 0%, transparent 18%),
  linear-gradient(to top, rgba(0,0,0,0.82) 30%, rgba(0,0,0,0.06) 58%, transparent 74%);
```
- Parte superior: leve escurecimento para o logo ficar legível
- Parte inferior: gradiente âncora o texto sem apagar a foto
- **Nunca usar opacidade acima de 0.85 no gradiente inferior** — foto deve permanecer visível e com cores naturais
- Para overlay com cor da marca no lugar do preto: substituir `rgba(0,0,0,...)` pela cor primária em rgba, mantendo as mesmas opacidades

**Posição do texto:** âncora no terço inferior (spacer-top empurra o conteúdo pra baixo). A foto "respira" acima.

**Elemento oversized opcional:** número, letra ou ícone da marca posicionado atrás do conteúdo (z-index: 1, opacidade 10-15%, cor da marca ou branco).

**Imagem:** embutir como base64 ou usar caminho absoluto `file:///`. Nunca caminho relativo.

---

### Layout 3 — Split Pessoa

Frame dividido em duas metades horizontais. Metade superior: conteúdo clean (headline, subheadline e CTA). Metade inferior: somente a foto da pessoa, sem texto sobreposto. Regras completas em `scripts/design-split-pessoa.md`.

**Estrutura:**
```
body (flex-direction: column, height: 1920px)
  ├── .top-half         ← height: 50%, bg: #F5F0E8 ou #F5F4F1, padding: 80px 90px 70px
  │     ├── .brand-bar  ← logo esquerda + label produto direita (small caps, opacidade 35%)
  │     └── .top-content ← display: flex, flex-direction: column, gap: 28px
  │           ├── .headline   ← Playfair Display ExtraBold, ~92px, cor #0D0D0D
  │           ├── .subtitle   ← Inter regular, ~34px, opacidade 50%
  │           └── .cta-outlined ← outlined pill, cor da marca, align-self: flex-start
  └── .bottom-half      ← height: 50%, position: relative, overflow: hidden
        └── .person-photo ← position: absolute, inset: 0, object-fit: cover, object-position: center top
```

**Regras:**
- **Metade inferior contém APENAS a foto** — sem CTA, sem texto sobreposto, sem overlay
- Todo o conteúdo (headline, subheadline, CTA) fica na metade superior
- Top: nunca fundo branco puro — usar `#F5F0E8` (quente) ou `#F5F4F1` (neutro)
- `.top-half` usa `justify-content: space-between` — brand-bar no topo, conteúdo embaixo
- CTA: outlined pill (`border: 2.5px solid [cor-marca]`, `background: transparent`), `align-self: flex-start`
- Fonte headline: Playfair Display ExtraBold — nunca sans-serif neste layout
- Divisão: 50/50 padrão. Ajustar para 45/55 (top menor) se o conteúdo for muito curto

---

### Layout 4 — Comparação

Dois estados lado a lado: tradicional vs marca, antes/depois, com vs sem. **Estrutura única de dois cards** sobre um fundo de cor única (sem contraste de cor no fundo). O contraste vem do **card vencedor elevado** + tratamento da foto + ícones, nunca de cores de fundo diferentes. Regras completas em `scripts/design-comparacao.md`.

Mesma base para as duas versões — a única diferença é a presença da foto dentro do card:
- **Com foto** — cada card tem a foto do respectivo estado entre o header e a lista
- **Sem foto** — mesma estrutura, sem o bloco de foto (cards mais curtos, ganham banda de oferta opcional acima do CTA)

**Estrutura:**
```
body (flex-direction: column, align-items: center, justify-content: center,
      bg: cor primária da marca, padding ~44px 52px)
  ├── .kicker          ← pílula "Pode comparar" — fundo cor de acento, texto na cor do fundo
  ├── .headline        ← título uppercase centralizado (fonte de título da marca)
  ├── .cards           ← display: flex, gap: 20px, align-items: stretch
  │     ├── .card.lose ← estado negativo: bg levemente mais claro que o fundo, borda fraca
  │     │     ├── .card-head   ← chip(✕) + título; min-height fixo p/ alinhar fotos entre cards
  │     │     ├── .card-photo  ← (só com foto) foto do estado negativo, DESSATURADA + escurecida
  │     │     └── .rows         ← 5 itens, ícone ✕ apagado + texto a ~55% de opacidade, divisória fina entre linhas
  │     └── .card.win  ← estado positivo (VENCEDOR): elevado
  │           ├── .card-head   ← chip(✓ cor de acento) + título na cor de acento
  │           ├── .card-photo  ← (só com foto) foto do estado positivo, natural
  │           └── .rows         ← 5 itens, ícone ✓ na cor de acento + texto cheio
  └── .cta             ← CTA na base (ver regras de estilo abaixo)
```

**Regra crítica da foto (com foto):**
- O container `.card-photo` deve ter **a mesma proporção da imagem original** (`aspect-ratio`) para que `object-fit: cover` mostre a foto **inteira, sem cortar pessoas**. Para retrato de estúdio (4000×6000) usar `aspect-ratio: 2/3`. Checar a proporção real do arquivo antes (PowerShell `System.Drawing` ou similar) e espelhar no container.
- **Nunca** forçar uma proporção paisagem (ex: 4/5, 16/9) num retrato — corta cabeça/pés. Foi o erro do layout antigo.
- **Cada lado usa a SUA foto** — nunca a mesma foto vazando atrás dos dois (erro do layout antigo).
- Lado negativo: `filter: grayscale(0.55) brightness(0.82)` — comunica o "pior" sem precisar de cor.

**Card vencedor (elevado):**
```css
.card.win {
  background: linear-gradient(180deg, [primária+5%], [primária-2%]);
  border: 1.5px solid rgba([acento], 0.5);
  box-shadow: 0 24px 70px rgba([acento], 0.10);   /* glow sutil */
}
.card.lose { background: [primária+4%]; border: 1px solid rgba([acento], 0.08); }
```

**Ícones / marcadores:**
- ✓ positivo: chip preenchido na cor de acento (texto na cor do fundo); marcadores das linhas na cor de acento
- ✕ negativo: chip **vazado/apagado** (borda + texto a ~30-55% de opacidade); marcadores das linhas apagados
- **Só usar X vermelho `#E53935` se o design guide da marca permitir cores vibrantes.** Marcas com paleta restrita (ex: Outlier) → usar o acento da marca apagado, nunca vermelho néon.

**CTA:**
- Estilo **linear (contorno)** quando a marca for premium/sóbria: `background: transparent; border: 2px solid [acento]; color: [acento]`, `align-self: center`, largura automática (não full-width), fonte de título ~30px. Mantém leve, não "exagerado".
- Estilo **pílula preenchida** (acento sólido, texto na cor do fundo) quando a marca pedir CTA forte. Máx 1 por criativo.

**Regras gerais:**
- **5 itens por lado** (padrão aprovado). Texto direto; pode passar de uma linha
- `.card-head` com `min-height` fixo (~80px) para que as fotos comecem na mesma altura nos dois cards mesmo com títulos de tamanhos diferentes
- `align-items: stretch` nos cards mantém os dois com a mesma altura
- Conteúdo centralizado verticalmente (`justify-content: center`) — sem espaço morto; se sobrar respiro, aumentar a foto/tipografia antes de deixar vazio
- Logo/foto embutida como base64 ou caminho absoluto — nunca relativo nem com espaços
- Gerar via script Node que lê as imagens, faz base64 e escreve o HTML (evita o problema de `file:///` com espaços no caminho). Renderizar com `npx playwright screenshot` passando o **nome relativo** do HTML

---

### Layout 5 — Editorial

Fundo claro, muito espaço em branco, tipografia dominante. Sensação de matéria de revista ou post de autoridade. Regras completas em `scripts/design-editorial.md`.

**Estrutura:**
```
body (flex-direction: column, padding: 100px 100px 120px, bg: #F5F0E8 ou #F5F4F1)
  ├── .brand-bar        ← logo esquerda + label produto direita (uppercase, opacidade 40%)
  │                        flex-shrink: 0
  ├── .content          ← flex: 1, display: flex, flex-direction: column
  │     │                  justify-content: center, gap: 52px
  │     ├── .divider-line ← 60px × 2px, cor da marca, opacidade 70%
  │     ├── .headline   ← Playfair Display ExtraBold, ~116px, line-height: 1.04, cor #0D0D0D
  │     ├── .accent-line ← Playfair Display italic regular, ~66px, cor da marca (tom mais escuro)
  │     ├── .subtitle   ← Inter regular, ~36px, line-height: 1.65, opacidade 50%
  │     └── .cta-outlined ← border 2.5px cor da marca, cor da marca, background transparent,
  │                          border-radius: 100px, padding: 24px 56px
  ├── .decorative-block ← flex-shrink: 0, gap: 32px — âncora visual no terço inferior
  │     ├── .deco-rule  ← linha horizontal sólida 1px, cor da marca, opacidade 25%
  │     └── .deco-tags  ← pills com categorias/atributos da marca, borda fina, texto opaco
  │                        border: 1px solid rgba(0,0,0,0.12), border-radius: 100px
  └── .footer           ← flex-shrink: 0, justify-content: space-between, margin-top: 40px
                           texto uppercase pequeno, opacidade 28%
```

**Regras:**
- Fundo: `#F5F0E8` (tom quente, combina com dourado/terracota) ou `#F5F4F1` (neutro)
- Headline obrigatoriamente em **Playfair Display** ou Lora — nunca sans-serif no editorial
- Accent line: italic na cor da marca em tom ligeiramente mais escuro que o primário (ex: dourado `#F1B835` → usar `#C49A28` no claro)
- `.content` com `flex: 1` e `justify-content: center` — centraliza verticalmente sem `margin-top` fixo
- `.decorative-block` âncora o terço inferior: elimina o vazio sem foto
- `.deco-rule`: usar `1px solid rgba([cor-marca], 0.25)` — gradiente pode sumir no Playwright
- CTA outlined: nunca fundo sólido no editorial — sempre transparente com borda
- Se houver foto/screenshot: inserir entre `.subtitle` e `.cta-outlined` com `border-radius: 12px`, `max-height: 600px`

---

### Layout 6 — Tweet

Visual de tweet real capturado como Story. Deve parecer autêntico, não um post desenhado.

**Visual:**
- **Fundo:** `#F0F2F5` (cinza levíssimo — nunca branco puro). Sem card ou wrapper branco
- **Avatar:** logo do cliente como foto de perfil (base64, `object-fit: cover`, padding 10px no círculo). Fallback: iniciais
- **Nome:** negrito, 30-32px, `#0F1419`
- **Handle:** regular, 26-28px, `#536471`
- **Badge verificado:** SVG azul `#1D9BF0` com check branco, sempre ao lado do nome
- **Layout:** conteúdo centralizado verticalmente no frame (`justify-content: center`)
- **Corpo do tweet:** 38-44px, regular, `#0F1419`, line-height 1.5. System fonts
- **Palavras em destaque:** `font-weight: 700` apenas. Não trocar cor
- **Botão de CTA:** não incluir na arte (Meta insere automaticamente)

**Estrutura do copy:**
```
[Hook: 1-2 frases curtas e diretas]

[Emoji] [item 1 com dado específico]
[Emoji] [item 2 com dado específico]
[Emoji] [item 3 com dado específico]

[Insight ou virada em 1-2 frases]

👇 [CTA textual]
```

**Regras:**
- Emojis com intenção: 📊 dados, ✅ lista positiva, 📡 tech
- **Último bloco SEMPRE começa com 👇** — sem exceção
- Tom conversacional, direto. Não parece copy de anúncio
- Sem ponto final no hook, sem travessões

---

### Layout 7 — Referência

Replica o layout de um anúncio enviado pelo usuário. Adapta ao design guide do cliente — não copia cor ou estilo do concorrente. Regras completas em `scripts/design-referencia.md`.

**Visual:**
- **Fundo:** cor primária do cliente — nunca preto ou cor genérica
- **Com imagem:** foto no lado direito inferior; overlay `linear-gradient(to right, [cor-primária] 25%, rgba([rgb], 0.25) 100%)`
- **Sem imagem:** fundo sólido na cor primária
- **Banner de atenção:** pílula/tag uppercase com fundo semitransparente no topo do conteúdo (`rgba(255,255,255,0.15)`)
- **Logo:** topo do frame, base64 embedded

**CTA:**
- Dentro do bloco de conteúdo, logo abaixo do subtítulo (`margin-top: 24px`)
- Nunca no rodapé separado do texto principal
- Estilo sugerido: outlined (`border: 3px solid #FFFFFF; color: #FFFFFF; background: transparent`) ou fundo branco com texto na cor primária

---

### Layout 8 — Notícia

Replica uma matéria de portal de notícias. Tarja "NOVIDADE" no topo, manchete preta pesada sobre fundo branco, deck em cinza e foto full-bleed embaixo. Gera autoridade por parecer cobertura de imprensa — ideal pra negócio local e lançamento. Regras completas em `scripts/design-noticia.md`.

**Estrutura:**
```
body (flex-direction: column, bg: #FFFFFF, height: 1920px)
  ├── .tarja           ← faixa full-width no topo, bg vermelho #E11515 (ou cor da marca)
  │                       texto uppercase, branco, extrabold ~72px, centralizado (palavra mutável)
  ├── .texto           ← padding lateral ~52px, top ~48px
  │     ├── .manchete  ← sans pesada 800, #111, ~92px, line-height 1.05, tom jornalístico
  │     └── .deck      ← sans regular 400, #3A3A3A, ~46px, line-height 1.3 (lide de jornal)
  └── .foto            ← full-bleed no rodapé, width 100%, object-fit: cover, flex: 1 (~55%)
```

**Regras:**
- **Sem CTA botão, sem selo de oferta, sem preço** — quebra a ilusão de notícia. O CTA vai na legenda, não na arte
- Tarja: vermelho `#E11515` por padrão (mais crível como notícia) ou cor primária da marca se pedir consistência. Full-width, sem cantos arredondados, encostada no topo
- Manchete: sans-serif pesada (Montserrat ExtraBold ou fonte de título da marca) — **nunca serifada**. Alinhada à esquerda, terceira pessoa, cita serviço + cidade
- Deck: benefício em linguagem de lide, sem promessa vaga, sem exclamação
- Foto no rodapé, full-bleed, com pessoas/contexto real do serviço. Base64 ou caminho absoluto
- Alto contraste: o resto é preto e branco, a única cor é a tarja
- Palavra da tarja é mutável: chamada de urgência (`NOVIDADE` / `URGENTE` / `ATENÇÃO` / `EXCLUSIVO`) ou editoria do nicho do cliente (`SAÚDE` / `EDUCAÇÃO` / `ESPORTES` / `ECONOMIA` / `NEGÓCIOS`)

**Adaptação por cliente:** ler o design guide pra fonte de título e cor primária; manchete no tom de portal citando serviço + cidade do cliente; usar foto real do cliente. Reprodutível pra qualquer cliente trocando só conteúdo e (opcional) cor da tarja.

---

### Layout 9 — Preço Topo

Comparação de preço COM × SEM a marca (oferta 2x1): a headline "COM O [MARCA] ✕ SEM O [MARCA]", uma tarja dourada de contexto e os **dois preços em destaque no topo**, com a foto do produto full-bleed embaixo. Formato agressivo e direto. Ideal pra clube de desconto, cupom, 2x1, combo. Regras completas em `scripts/design-preco-topo.md`.

**Estrutura:**
```
body (flex-direction: column, bg: cor primária escura da marca)
  ├── .top (text-align: center)
  │     ├── .brand-logo   ← logo da marca, ~88px, circular, centralizado
  │     ├── .headline     ← "COM O [MARCA]" / "✕ SEM O [MARCA]" — Montserrat 800 ~84px, "✕" no acento
  │     └── .subtarja     ← pílula na cor de acento (texto escuro): "na compra de dois [item] no [parceiro]"
  ├── .prices (flex, gap ~22px)
  │     ├── .col.com  → label branco + card fundo acento, preço ~82px escuro
  │     └── .col.sem  → label branco + card claro #f4f2ee, preço ~82px escuro
  ├── .photo (flex: 1)  ← foto do produto full-bleed + gradiente sutil topo/base
  └── .footer          ← "*valores aproximados"
```

**Regras:**
- Movido a dado real: parceiro + preço COM + preço SEM. Sempre citar o parceiro
- Preços **exagerados** (queixa comum é ficarem pequenos): `.val` ~82px Montserrat 800
- Acento em 3 pontos só: o "✕", a tarja e o card COM
- Foto base64 via script Node; placeholder escuro se não houver foto
- Sem travessões

---

### Layout 10 — Preço Base

Mesma oferta 2x1, versão premium: **foto do produto herói no centro**, selos no topo ("EXCLUSIVIDADE ◆ ECONOMIA" com a logo diamante) e a comparação COM × SEM na base. Ideal quando a foto é forte e a marca é sóbria/high ticket. Regras completas em `scripts/design-preco-base.md`.

**Estrutura:**
```
body (flex-direction: column, bg: cor primária escura da marca)
  ├── .mini           ← "EXCLUSIVIDADE" · logo diamante · "ECONOMIA" (selos mutáveis)
  ├── .head-block
  │     ├── .headline ← "2 [ITEM] NO [PARCEIRO]" — Montserrat 800 ~78px, número no acento
  │     └── .subline  ← pílula acento (texto escuro): "ECONOMIA CERTA DE R$X"
  ├── .photo          ← foto herói (feed: flex:1 | story: altura fixa + objY 62%)
  └── .prices (flex, base)
        ├── .col.com  → "COM [MARCA]" (acento ~60px) + box contorno acento
        └── .col.sem  → "SEM [MARCA]" (branco ~60px) + box contorno branco
```

**Regras:**
- **Story ≠ feed:** no story **nunca** usar `flex: 1` na foto (estica e cria vão entre headline e preços). Usar altura fixa (~1040px) + `body { justify-content: center }` + `object-position: center 62%` pra focar o produto. No feed a foto pode ser `flex: 1`
- Labels e preços **exagerados** (`.lbl` ~60px, `.box` ~56px)
- Pílula de economia dourada destaca o gatilho principal
- Foto base64 via script Node; placeholder escuro se não houver foto
- Sem travessões

---

## Padrões de CTA

Referência rápida para escolher o estilo de botão conforme o layout:

| Estilo | Quando usar | CSS base |
|--------|------------|----------|
| Pílula branca | Universal, qualquer fundo escuro | `background: #FFFFFF; color: #000; border-radius: 100px; padding: 24px 56px` |
| Outlined | Fundos escuros premium, editorial | `background: transparent; border: 2px solid #FFFFFF; color: #FFFFFF; border-radius: 100px` |
| Pílula cor marca | Fundo claro ou neutro | `background: [cor-marca]; color: #FFFFFF; border-radius: 100px` |
| Flutuante | Dentro de split ou editorial, posição lateral | `background: rgba(0,0,0,0.15); border-radius: 50px; backdrop-filter: blur(4px)` |

**Regra geral:** máximo 2 CTAs por criativo (1 flutuante no meio + 1 pílula na base). Nunca 3.

---

## Uso de imagens

- **Logo:** sempre base64 embedded no `src` da `<img>`. Caminhos com espaço não carregam via `file:///`
- **Foto de pessoa:** base64 ou caminho absoluto com `file:///`. Nunca caminho relativo
- **Screenshot de produto/app:** mostrar dentro de container com `border-radius: 12px` e `box-shadow: 0 8px 32px rgba(0,0,0,0.3)`
- **Elemento oversized decorativo:** letra inicial, número ou símbolo da marca em `opacity: 0.08-0.15`, `position: absolute`, `font-size: 800-1000px`, `overflow: hidden` — cria textura sem poluir

---

## Output final

Sempre gerar os três formatos:

| Arquivo | Formato | Dimensão | Uso |
|---------|---------|----------|-----|
| `criativo.html` + `criativo.png` | Story | 1080×1920 | Reels, Stories |
| `criativo-feed.html` + `criativo-feed.png` | Feed | 1080×1440 | Feed Instagram |
| `criativo-square.html` + `criativo-square.png` | Quadrado | 1080×1080 | Feed quadrado, Facebook |

- **Arttico:** `conteudo/criativos/arttico/[tema]/`
- **Cliente:** `clientes/[cliente]/conteudo/criativos/[tema]/`

---

## Regras

- Sempre confirmar headline + subtítulo + CTA + layout + imagem antes de gerar o HTML
- **Sempre gerar os três formatos: story (1080×1920), feed (1080×1440) e quadrado (1080×1080)** — sem exceção
- Sempre mostrar os três PNGs gerados antes de encerrar
- Se pedir ajuste, re-renderizar os três formatos
- Se o usuário não informar para quem é o criativo, perguntar antes de qualquer coisa
- Se for cliente e não tiver design guide, pedir antes de gerar
- Uma pergunta por vez — não listar várias dúvidas de uma vez
- **Nunca usar travessões (—) em qualquer texto de criativo**, em nenhum estilo
- Logo sempre embutida como base64 — nunca `src` com caminho relativo ou com espaços
- **No Layout Foto Fundo: sempre usar o gradiente suave documentado** — nunca overlay acima de 0.85 de opacidade. A foto deve manter suas cores naturais; o efeito de fundo fica apenas na área do texto
