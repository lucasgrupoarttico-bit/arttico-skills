# Regras de Design — Criativo Notícia

> Replica o visual de uma matéria de portal de notícias local. Tarja "NOVIDADE"
> no topo, manchete preta pesada sobre fundo branco, linha de apoio (deck) em
> cinza e foto full-bleed embaixo. Gera autoridade por parecer cobertura de imprensa.

---

## Conceito

O criativo finge ser uma reportagem, não um anúncio. A pessoa lê o título como
se fosse notícia da cidade dela, baixa a guarda e absorve a mensagem antes de
perceber que é publicidade. Funciona muito bem pra negócio local (clínica,
serviço, comércio de cidade pequena) e pra lançamento/novidade.

A credibilidade vem de imitar o padrão editorial de portal: fonte pesada de
manchete, hierarquia jornalística (tarja › título › deck › foto), zero elemento
de "propaganda" (sem CTA botão, sem selo de oferta, sem preço gritando).

---

## Dimensões

- **Story:** 1080×1920 (`criativo.html`)
- **Feed:** 1080×1440 (`criativo-feed.html`)
- **Quadrado:** 1080×1080 (`criativo-square.html`) — **muda o layout**, ver seção abaixo

No story e no feed, layout vertical em blocos empilhados de cima pra baixo, sem
centralização vertical. No quadrado, a pilha não cabe: usar o layout de sobreposição
descrito em "Formato quadrado (1080×1080)".

---

## Estrutura

```
body (flex-direction: column, bg: #FFFFFF, height: 1920px)
  ├── .tarja           ← faixa full-width no topo, bg vermelho (ou cor da marca)
  │                       texto "NOVIDADE" uppercase, branco, extrabold, centralizado
  ├── .texto           ← bloco de texto, padding lateral ~52px, padding top ~48px
  │     ├── .manchete  ← sans-serif pesada (800/900), preto #111, ~92px, line-height 1.05
  │     └── .deck      ← sans-serif regular, cinza #333/#444, ~46px, line-height 1.3
  └── .foto            ← imagem full-bleed no rodapé, width 100%, object-fit: cover
                          ocupa a área restante (flex: 1) ou altura fixa ~55% do frame
```

### Tarja (topo)

- Full-width, sem margem lateral, encostada nas bordas
- Altura ~130px (story) / ~110px (feed)
- Fundo **vermelho `#E11515`** por padrão (é o código visual de "urgente/notícia")
- Alternativa: cor primária da marca, se o design guide pedir consistência de marca
- **Texto mutável.** Dois usos possíveis, escolher conforme a intenção:
  - **Chamada de urgência:** `NOVIDADE`, `URGENTE`, `ATENÇÃO`, `EXCLUSIVO` — quando o
    foco é lançamento/prazo/alerta
  - **Editoria/categoria:** `EDUCAÇÃO`, `ESPORTES`, `SAÚDE`, `ECONOMIA`, `TECNOLOGIA`,
    `NEGÓCIOS` — quando o foco é parecer a seção de um portal do nicho do cliente
  - Adaptar sempre ao cliente: clínica → `SAÚDE`; escola/curso → `EDUCAÇÃO`;
    academia/time → `ESPORTES`; consultoria → `NEGÓCIOS`. Uma palavra, uppercase
- Fonte: extrabold/black, branco, letter-spacing ~2px, font-size ~72px
- Centralizado horizontal e vertical

### Manchete

- Fonte **sans-serif pesada** (peso 800-900): Montserrat, Inter, Arial Black ou a
  fonte de título da marca. Nunca serifada — portal de notícia usa sans pesada
- Cor `#111111` (preto quase puro, nunca `#000`)
- `font-size` ~92px story / ~76px feed, `line-height` 1.05, `font-weight` 800
- Alinhada à esquerda, `letter-spacing: -1px` (aperta como manchete real)
- Máx ~14 palavras. Escrever no tom jornalístico, terceira pessoa:
  "Clínica traz para [cidade]...", "[Empresa] chega em [cidade] com..."
- Nome do serviço/cidade pode aparecer no título (ancora local)

### Deck (linha de apoio)

- Fonte sans-serif regular (400), cor `#3A3A3A`
- `font-size` ~46px story / ~38px feed, `line-height` 1.3
- Máx ~30 palavras. Explica o benefício em tom de lide de jornal:
  "Nova opção promete beneficiar pacientes que enfrentam longas filas..."
- Sem ponto de exclamação, sem CTA, sem "clique aqui"

### Foto (rodapé)

- Full-bleed: encosta nas bordas laterais e inferior, sem border-radius
- `object-fit: cover`, `object-position: center`
- Ocupa a faixa inferior do frame (~50-58% da altura no story)
- Deve ter pessoas/contexto reais do serviço (equipe, atendimento, ambiente)
- Se a marca tiver logo discreta, pode aparecer marca d'água no canto da foto
- Embutir como base64 ou caminho absoluto `file:///` — nunca relativo

---

## Formato quadrado (1080×1080)

No quadrado o canvas é baixo demais pra empilhar tarja + texto + foto sem cortar o
rosto ou sobrar branco. Inverte-se a lógica: **a foto ocupa o frame inteiro** e a
copy vai **por cima**, na base, sobre um **degradê escuro**. Vira uma capa de
revista/portal — a foto aparece completa e a copy preenche o vazio.

### Estrutura

```
body (position:relative, 1080×1080, bg escuro de fallback)
  ├── .foto     ← position:absolute; inset:0 — foto full-frame, object-fit:cover
  ├── .overlay  ← position:absolute; inset:0 — degradê transparente→escuro na base
  ├── .tarja    ← faixa vermelha no topo (igual story/feed), z-index acima
  └── .painel   ← ancorado embaixo (bottom:0): manchete + deck em BRANCO
```

### Regras específicas do quadrado

- **Foto completa:** `object-fit:cover`, `object-position:center top`. Se a foto for
  1:1 e o degradê cobrir o rosto, dar leve zoom (`height:~118-132%`) e ajustar
  `object-position` (ex.: `center 34%`) pra enquadrar do topo da cabeça até a boca
  acima do degradê. Nunca cortar o rosto na altura dos olhos.
- **Degradê na base** (não é painel branco opaco — isso cobriria a foto):
  ```css
  background:linear-gradient(to bottom,
    rgba(6,20,10,0) 34%,
    rgba(6,20,10,0.45) 52%,
    rgba(6,20,10,0.82) 70%,
    rgba(6,20,10,0.95) 100%);
  ```
  Ajustar a cor-base do degradê ao fundo da foto (verde escuro pra fundo verde,
  `rgba(0,0,0,...)` pra fundo neutro).
- **Copy em branco**, ancorada na base, preenchendo a largura:
  - manchete: `#FFFFFF`, 800, `text-shadow:0 2px 18px rgba(0,0,0,.55)`, `line-height:1.04`,
    tamanho ~82% do story
  - deck: `rgba(255,255,255,.92)`, `text-shadow:0 2px 14px rgba(0,0,0,.5)`
  - padding: ~60px laterais e base
- **Tarja** vermelha `#E11515` continua no topo, full-width, encostada na borda.
- Preencher a base sem sobrar vão: a copy é grande e ancorada embaixo; quanto mais
  longa a manchete, mais alto o degradê deve começar pra manter contraste.

Referência de implementação testada: `clientes/mateus-medeiros/conteudo/criativos/tqb-noticia/gen-square.mjs`.

---

## Cores

- **Fundo:** `#FFFFFF` (branco puro — é papel de jornal)
- **Tarja:** `#E11515` vermelho (padrão) ou cor primária da marca
- **Manchete:** `#111111`
- **Deck:** `#3A3A3A`
- **Texto da tarja:** `#FFFFFF`

Regra: o resto do criativo é preto e branco. A única cor é a tarja. Isso mantém
a leitura "editorial" e joga o olho pra faixa vermelha e pra foto.

---

## Tipografia

- **Manchete:** sans pesada 800-900. Prioridade: fonte de título da marca; se não
  combinar (ex.: marca usa serifada elegante), usar Montserrat ExtraBold como
  fonte neutra de "portal"
- **Deck:** sans regular 400, mesma família da manchete
- **Tarja:** mesma sans, peso 800, uppercase
- Nunca serifada, nunca condensada extrema, nunca decorativa

---

## Regras

- **Sem CTA botão, sem selo de oferta, sem preço em destaque** — quebra a ilusão
  de notícia. O CTA fica na legenda/copy do post, não na arte
- **Sem travessões** em nenhum texto
- Tarja sempre encostada no topo, full-width, sem cantos arredondados
- Manchete sempre alinhada à esquerda, tom jornalístico em terceira pessoa
- Foto sempre no rodapé, full-bleed, com pessoas/contexto real
- Manter alto contraste: preto sobre branco. Não usar cinza claro na manchete
- A palavra da tarja é mutável e adapta ao contexto. Duas famílias:
  - Urgência: `NOVIDADE` (lançamento), `URGENTE` (prazo), `ATENÇÃO` (alerta),
    `EXCLUSIVO` (diferencial)
  - Editoria do nicho: `SAÚDE`, `EDUCAÇÃO`, `ESPORTES`, `ECONOMIA`, `TECNOLOGIA`,
    `NEGÓCIOS` — reforça a leitura de "seção de portal"

---

## Adaptação por cliente

O layout é o mesmo pra qualquer cliente — muda só o conteúdo e (opcionalmente) a
cor da tarja:

1. Ler o design guide do cliente pra pegar a fonte de título e a cor primária
2. Manchete no tom jornalístico, citando o serviço + cidade do cliente
3. Foto: usar imagem real do cliente (equipe, ambiente, atendimento). Se não
   tiver, gerar/pedir uma que combine com o serviço
4. Tarja: manter vermelho `#E11515` (mais crível como notícia) OU trocar pela cor
   primária da marca se o cliente pedir consistência visual
5. Deck: benefício em linguagem de lide, sem promessa vaga

**Exemplos de manchete por nicho:**
- Clínica: "Clínica traz para [cidade] cirurgias de [X] com parcelamento em até 24x"
- Engenharia: "[Empresa] chega em [cidade] com AVCB, CLCB e projetos contra incêndio"
- Serviço local: "Nova [empresa] promete resolver [dor] de [público] em [cidade]"

---

## O que ajustar

- **Quer a cor da marca na tarja:** trocar `#E11515` pela primária no `.tarja`
- **Manchete muito longa:** reduzir `font-size` da manchete pra caber sem cortar a foto
- **Sem foto:** não recomendado — o layout depende da foto de contexto pra parecer
  matéria. Se realmente não tiver, aumentar o bloco de texto e usar fundo cinza claro
  `#F0F0F0` na área da foto com a logo centralizada
- **Palavra da tarja:** trocar `NOVIDADE` por outra de urgência (`URGENTE`,
  `ATENÇÃO`, `EXCLUSIVO`) ou pela editoria do nicho (`SAÚDE`, `EDUCAÇÃO`,
  `ESPORTES`, `ECONOMIA`, `NEGÓCIOS`)

Pede pro Claude: "muda a regra X no design de notícia" e ele edita este arquivo.
