---
name: plano-acao
description: >
  Cria o plano de ação (planejamento de campanha) para um cliente novo e gera o PDF no padrão
  da Arttico. Diagnostica nicho + verba, recomenda plataforma (Meta / Google / ambos) pra
  aprovação e, depois de aprovado, detalha a campanha: no Google (objetivo, palavras-chave,
  títulos, descrições, sitelinks) e/ou no Meta (objetivo e criativos por funil), o avatar
  (público-alvo com boneco, dores e desejos), além do funil do lead até o comercial. Gera um deck
  de slides 16:9 no padrão visual da Arttico, em dois layouts a escolher ("Disciplina Ártica":
  navy + branco, ou "Aurora Ártica": gradiente navy > teal + accent gelo; ambos Montserrat +
  Inter) em PDF e depois exporta pro Canva. O deck só inclui a plataforma escolhida.
  O direcionamento de criativos (roteiros de peça por funil) é uma skill separada:
  `direcionamento-criativos`.
  Use quando o usuário disser "plano de ação", "planejamento de campanha", "monta o plano pro
  cliente X", "cliente novo, faz o planejamento", "plano de mídia". Também dispara com /plano-acao.
---

# /plano-acao — Plano de Ação (Planejamento de Campanha)

## Contexto
Ler antes de começar: `_contexto/empresa.md`, `_contexto/preferencias.md`, `_contexto/estrategia.md`
e `marca/design-guide.md`. Tom: estratégico, direto, persuasivo, orientado a conversão. Sem
travessões. Sem promessas vagas.

## Parâmetros
- **cliente** — nome da pasta do cliente (ex: `igor-flor`). Se não vier, perguntar e listar as
  pastas de `clientes/` (exceto `_modelo-cliente`).

---

## Fluxo

O fluxo tem **dois checkpoints de aprovação**. Não pular nenhum.

### 1. Ler o briefing do cliente
- Ler `clientes/[cliente]/briefing.md`.
- Extrair: `Cliente`, `Segmento`/nicho, `Objetivo principal`, `Público-alvo`, `Budget mensal`,
  `Opera em`, `Site`.
- Se o briefing estiver incompleto nos campos críticos (nicho, objetivo, verba, público),
  perguntar o que faltar antes de seguir. Não inventar.

### 2. CHECKPOINT 1 — Recomendar plataforma (pra aprovação)
Com base em **nicho + verba + objetivo**, recomendar **Meta**, **Google** ou **ambos**, com
justificativa curta e específica. Considerar:

- **Google** quando há demanda ativa / intenção de busca (a pessoa procura a solução): serviços
  locais, urgência, comparação, B2B de nicho, ticket alto com pesquisa. Captura quem já está
  procurando.
- **Meta** quando é demanda latente / descoberta: produto/serviço que precisa ser apresentado,
  apelo visual, público definido por interesse e comportamento, topo de funil e remarketing.
- **Ambos** quando a verba comporta dividir sem pulverizar (regra prática: abaixo de ~R$2k/mês
  evitar dividir; concentrar onde o retorno é mais provável) e o objetivo justifica capturar
  demanda ativa (Google) + gerar demanda (Meta).

Apresentar assim e **parar pra aprovação**:

> **Recomendação de plataforma — [Cliente]**
> Nicho: [...] · Verba: [R$ ...] · Objetivo: [...]
> **Plataforma sugerida: [Meta / Google / Ambos]**
> Por quê: [2-3 linhas]
> Distribuição de verba (se ambos): [ex: 60% Meta / 40% Google]
> Layout do deck: [Disciplina Ártica | Aurora Ártica]
>
> Aprova essa direção ou quer ajustar?

Perguntar também **qual layout** usar (ver seção 4):
- **Disciplina Ártica** (padrão) — navy chapado, branco como único destaque.
- **Aurora Ártica** — gradiente navy > teal, accent gelo.

Não montar o conteúdo detalhado antes da aprovação.

### 3. Após aprovação — montar o conteúdo (condicional à plataforma)

Montar **somente** os blocos da(s) plataforma(s) aprovada(s).

**Sempre (independente da plataforma):**
- **Estratégia + plataforma**: diagnóstico do nicho/verba, plataforma escolhida + justificativa,
  distribuição de verba e objetivo geral.
- **Avatar (público-alvo)**: quem é a pessoa que vai ser impactada. O slide tem um **boneco
  line-art** (persona) com uma **ficha** ao lado e duas listas. A ficha (`{{AVATAR_FICHA}}`) são
  ~4 linhas `<div class="pf"><span class="pk">Rótulo</span><span class="pv">Valor</span></div>`
  (ex: Idade, Perfil, Decisor/Onde, Momento). As listas são **dores** (o que incomoda, o medo, a
  frustração, o que tentou e não funcionou) e **desejos** (o que quer de verdade, a transformação).
  No deck 16:9 os itens de dores/desejos precisam caber em **1 linha** (texto curto, ~30 caracteres),
  senão estouram. Tirar do briefing (`Público-alvo`, objetivo, segmento) e do nicho real. Esse
  avatar é a base do direcionamento de criativos (skill `direcionamento-criativos`). Ser
  específico, nada genérico.

**Se Google (só Google ou ambos):**
- **Objetivo de campanha** (ex: Geração de leads / Vendas / Ligações).
- **Palavras-chave** organizadas por grupo de anúncios/tema, com a correspondência sugerida
  (ampla modificada / frase / exata). Incluir lista de **negativas** óbvias.
- **Títulos** (RSA — até 15, 30 caracteres cada).
- **Descrições** (até 4, 90 caracteres cada).
- **Sitelinks** (4-6) e **callouts**.

**Se Meta (só Meta ou ambos):**
- **Objetivo de campanha** (ex: Leads / Conversões / Mensagens).
- **Criativos por funil** — Topo (Reconhecimento) · Meio (Relacionamento) · Fundo (Remarketing).
  **Padrão (não descrever copy no deck):** os criativos entram como **molduras 1080x1920 vazias**
  pro cliente anexar as peças que já existem no perfil. No conteúdo em texto do Checkpoint 2, só
  confirmar as **etapas do funil** e **quantas peças por etapa** (ex: 3 por etapa). Não escrever
  headline/ângulo/CTA de cada peça, a menos que o cliente peça explicitamente. Ver o padrão
  montado em `SKILL_FILES/referencia-meta.html`.

**Sempre:**
- **Funil do lead ao comercial**: o caminho completo do lead, da entrada (anúncio/LP/form/DM)
  até a chegada no comercial. Etapas: captação → qualificação → nutrição/contato → handoff pro
  comercial. Indicar ferramentas/automação se conhecidas (ex: form, WhatsApp, CRM).

Mostrar esse conteúdo pro usuário em texto **antes** de gerar o PDF (CHECKPOINT 2). Ajustar se
ele pedir.

### 4. CHECKPOINT 2 — Montar o deck (formato oficial)
Depois do conteúdo aprovado, montar o **deck de slides 16:9**. É uma apresentação, não um
documento A4. Dois layouts, mesma estrutura, **mesmos tokens e mesmos blocos**
`BLOCO_GOOGLE_*` / `BLOCO_META_*` — troca só a pele. A escolha foi feita no checkpoint 1:

| Layout | Arquivo | Cara |
|---|---|---|
| **Disciplina Ártica** (padrão) | `SKILL_FILES/template-plano.html` | Navy `#00002c` chapado, cards `#0a0a3d`, branco como único destaque. |
| **Aurora Ártica** | `SKILL_FILES/template-plano-aurora.html` | Gradiente navy > teal, accent gelo `#a9e2f2`, capa com logo + seta, tabela com header sólido, cards com contorno. |

No Aurora, a classe `.dim` dos títulos vale como accent gelo (não precisa reescrever slide
nenhum: "Resultados <span class="dim">esperados</span>" já sai branco + gelo). O mesmo layout
existe na skill `direcionamento-criativos` (`template-criativos-aurora.html`), então os dois
documentos do mesmo cliente ficam com a mesma cara.

Modelo pronto do Aurora: `SKILL_FILES/referencia-aurora.html` + `.pdf` (17 slides, Meta e Google,
todos os componentes preenchidos: divider, avatar, tabela de keywords, verba, funil, criativos).

> **Padrão Meta (usar sempre que a plataforma incluir Meta):** o modelo de referência é
> `SKILL_FILES/referencia-meta.html` (exemplo real: Garagem do Particular, 3 produtos). Vale
> pra **1 produto ou vários**. Os criativos entram como **molduras 1080x1920**, nunca como
> cards com copy. Dois modos:
> - **Placeholder** (peças ainda não existem): molduras 9:16 vazias pro cliente anexar depois.
> - **Thumb clicável pro Instagram** (peça já publicada): a moldura vira a arte real (frame de
>   capa do vídeo + selo de play, ou a imagem direto) e um **link** que abre o post/Reels; a
>   legenda vira "Ver no Instagram ↗". O PDF preserva o hyperlink como anotação clicável.
>   Para gerar os thumbnails de vídeo (mp4/H.264), rodar `SKILL_FILES/extract-video-thumbs.js`
>   (usa o Chrome/Edge do sistema, pois o Chromium do Playwright não decodifica H.264). As
>   thumbs vão pra `clientes/<cliente>/plano-acao/assets/` e são referenciadas por caminho
>   relativo; não apagar essa pasta.
> - **1 produto:** uma seção de produto (avatar + slide de criativos com molduras); pode
>   dispensar o divider numerado por produto e o slide de verba por produto.
> - **Vários produtos:** um deck só, uma seção por produto (divider numerado + avatar +
>   criativos), sem misturar avatares, + estratégia geral e distribuição de verba por produto.
>
> O cabeçalho do `referencia-meta.html` detalha a estrutura das molduras (`.ph-row` > `.ph-group`
> > `.ph-frames` > `.ph-frame`) e como ajustar a quantidade de peças por etapa.

**Sistema de design (não desviar):**
- Comum aos dois layouts: display Montserrat ExtraBold; corpo Inter; serif (Lora) **só** no selo
  ARTTICO (é o logo). Assinatura: a **linha de horizonte** com o traço `.run` que avança a cada
  slide (= progresso). Numerais contornados gigantes (`.bignum`) só nos slides divisores.
- **Disciplina Ártica:** fundo `#00002c`, cards `#0a0a3d`, **branco `#FFFFFF` é o único
  destaque**. Sem cor vibrante, sem gradiente colorido (regra do `marca/design-guide.md`).
- **Aurora Ártica:** gradiente noite > teal, accent gelo `#a9e2f2`. **Nunca empilhar camadas de
  gradiente com `rgba()`/`transparent` no fundo do `.slide`:** o Chromium exporta gradiente com
  alpha como shading + SMask e a máscara corrompe a cor na conversão do PDF (o teal vira
  magenta). Um único gradiente **opaco** por slide, como está no template.
- **Apagar o comentário do topo do template** no arquivo final. Ele contém `-->`, que fecha o
  comentário cedo e faz o texto vazar como conteúdo na capa (e cria uma página extra no PDF).

**Regra crítica de plataforma:** o deck só contém a(s) plataforma(s) escolhida(s).
- Só Meta → remover o bloco `<!-- BLOCO_GOOGLE_INICIO -->...<!-- BLOCO_GOOGLE_FIM -->`.
- Só Google → remover o bloco `<!-- BLOCO_META_INICIO -->...<!-- BLOCO_META_FIM -->`.
- Ambos → manter os dois e ajustar os números de Seção (Google = 03, Meta = 04).

**Montagem:**
- **Criativos no Meta:** montar como o `referencia-meta.html` — um slide de criativos por produto,
  com molduras `.ph-*` (Topo/Meio/Fundo, N molduras 1080x1920 por etapa). Não usar os cards
  `.creative` com copy, a menos que o cliente peça.
- Slides repetíveis: no Google, duplicar as linhas `<tr>` da tabela de palavras-chave. Em
  multi-produto, duplicar a seção do produto (divider + avatar + criativos) por produto.
- Tokens a substituir: `{{CLIENTE}}`, `{{CLIENTE_CURTO}}`, `{{PLATAFORMA}}`, `{{DATA}}`,
  `{{RESULTADOS_CURTO}}`/`{{RESULTADOS_MEDIO}}` (itens `<li>`), `{{ACESSOS}}` (`<li>`),
  `{{ESTRATEGIA}}` (parágrafos `.para` + `.duo` de `.kcard`),
  `{{AVATAR_FICHA}}` (linhas `.pf` da persona), `{{AVATAR_DORES}}`/`{{AVATAR_DESEJOS}}` (itens
  `<li>` de `ul.list`, curtos pra caber em 1 linha), `{{FRASE_FINAL}}`, `{{FUNIL_FLOW}}` (caixas
  `.fbox` em `.frow`).
  - Google: `{{GOOGLE_OBJETIVO}}`, `{{GOOGLE_KEYWORDS_ROWS}}` (`<tr>`), `{{GOOGLE_TITULOS}}`,
    `{{GOOGLE_DESCRICOES}}` (`<li>`), `{{GOOGLE_SITELINKS}}`.
  - Meta: `{{META_VERBA_VALOR}}`, `{{META_VERBA_NOTE}}`, `{{META_FUNIL_LEGEND}}` (`.leg`),
    `{{ETAPA_NOME}}`/`{{ETAPA_TAG}}`/`{{ETAPA_CRIATIVOS}}` (`.creative`) por slide de criativo.
- **Passo final obrigatório — numeração e progresso:** contar o total de slides `N` (após
  remover/duplicar) e, em cada slide, preencher `.pageno` com `P / N` e `.run` com
  `style="width:<P/N×100>%"`. O traço tem que crescer do primeiro ao último slide.
- **Sem travessões (—)** em nenhum texto.

### 5. Renderizar e salvar (deck do plano)
- Salvar o HTML em `clientes/[cliente]/plano-acao/[YYYY-MM-DD]_plano-acao.html`
  (criar a pasta `plano-acao/` se não existir).
- Renderizar o PDF com Playwright usando o script `SKILL_FILES/render-pdf.js`:
  ```
  node ".claude/skills/plano-acao/SKILL_FILES/render-pdf.js" "<caminho-absoluto-do-html>" "<caminho-absoluto-do-pdf>"
  ```
- Se Playwright não estiver instalado: `npx playwright install chromium`.
- PDF final: `clientes/[cliente]/plano-acao/[YYYY-MM-DD]_plano-acao.pdf`.

### 6. Exportar para o Canva (após o PDF)
Depois de gerar o PDF, **sempre** subir esse mesmo PDF para o Canva via importação, gerando um
design editável com a mesma cara dos slides.

- **Pré-requisito:** o MCP do Canva precisa estar conectado a este ambiente (Claude Code). Checar
  se há uma ferramenta do Canva disponível (ex: `mcp__*canva*`). Se **não** houver, avisar o
  usuário que o MCP do Canva não está conectado aqui e pular esta etapa (não falhar o fluxo) —
  o PDF já está salvo. Comando pra conectar: `claude mcp add canva --transport http https://mcp.canva.com/mcp`.
- **Mecanismo:** importação de design (Canva Connect API — *design import*). Enviar o
  `[YYYY-MM-DD]_plano-acao.pdf` e aguardar o job de importação concluir. O Canva converte cada
  página do PDF em uma página do design.
- **Após importar:** informar ao usuário o link de edição/visualização do design no Canva.
- Observação: a importação preserva o visual; o texto fica pouco editável (cada slide entra
  rasterizado/achatado). Para edição nativa total seria necessário Brand Template + autofill —
  fora do escopo padrão.

### 7. Confirmar
Informar o caminho do PDF gerado e o link do design no Canva (se exportado). Perguntar se quer
ajustar algum bloco ou já está pronto pra enviar ao cliente.

Como o avatar já está montado, **oferecer o próximo passo**: gerar o direcionamento de criativos
(roteiros de peça por funil) com a skill `direcionamento-criativos`. Não montar os criativos
aqui — essa skill é independente.

---

## Observações
- Calibrar keywords, títulos, descrições e criativos pelo nicho real do cliente e pela região
  (`Opera em`). Pra clientes da América Latina, adaptar pro espanhol mantendo especificidade.
- Respeitar limites de caracteres do Google (títulos 30 / descrições 90).
- Nada de travessão em copy. CTA e linguagem orientada a conversão.
