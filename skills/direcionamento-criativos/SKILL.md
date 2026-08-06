---
name: direcionamento-criativos
description: >
  Cria o Direcionamento de Criativos de um cliente: uma apresentação em folha vertical (retrato)
  no padrão da Arttico, em dois layouts a escolher ("Disciplina Ártica": navy + branco, ou
  "Aurora Ártica": gradiente navy > teal + accent gelo; ambos Montserrat + Inter), com
  briefing técnico das peças, avatar (boneco line-art + dores e desejos) e roteiros de criativo
  por etapa de funil (topo, meio e fundo). Os roteiros são cena a cena, em tabela
  Arte | Texto | Imagem | Observações, prontos pra gravar e editar. O fundo de funil sempre traz
  pelo menos um UGC em vídeo (roteiro "E eu que...") e um estático formato notícia. Gera o PDF e
  depois exporta pro Canva. Use quando o usuário disser "direcionamento de criativos", "roteiro
  de criativos", "monta os criativos do cliente X", "novas peças pro cliente", "solicitação de
  criativo", "roteiro de vídeo pra Meta". Também dispara com /direcionamento-criativos.
---

# /direcionamento-criativos — Direcionamento de Criativos

## Contexto
Ler antes de começar (se existirem): `_contexto/empresa.md`, `_contexto/preferencias.md`,
`_contexto/estrategia.md` e `marca/design-guide.md`. Tom: estratégico, direto, persuasivo,
orientado a conversão. **Sem travessões.** Sem promessas vagas.

Esta skill é a camada **upstream** de criativos: define a estratégia e o roteiro (o que gravar /
desenhar). Quem produz a peça final é `carrossel` (carrossel) e `criativo-estatico` (estático).
O `plano-acao` é independente: ele entrega o plano de mídia e o avatar; aqui detalhamos as peças.

## Parâmetros
- **cliente** — nome da pasta do cliente (ex: `mateus-medeiros`). Se não vier, perguntar e listar
  as pastas de `clientes/` (exceto `_modelo-cliente`).

---

## Fluxo

### 1. Ler o contexto do cliente
- Ler `clientes/[cliente]/briefing.md`: `Cliente`, `Segmento`/nicho, `Objetivo principal`,
  `Público-alvo`, `Opera em`, produto(s) e oferta/preço, diferenciais e prova social.
- Se existir, ler `clientes/[cliente]/plano-acao/*_plano-acao.html` pra reaproveitar o **avatar**
  (dores e desejos) já definido. Se não existir, montar o avatar do briefing.
- Se faltar informação crítica (oferta, produto foco, prova social, voz da marca), perguntar
  antes de seguir. Não inventar oferta nem preço.

### 2. CHECKPOINT — Definir produto, oferta e peças (pra aprovação)
Antes de roteirizar, confirmar com o usuário:
- **Produto/oferta** que os criativos vão vender (ex: TQB · R$ 79,90). Se o cliente tem mais de um
  produto, perguntar qual é o foco.
- **Quantidade e mix de peças** (ex: 3 vídeos + 1 estático).
- **Formato e veiculação** (padrão: Story 1080x1920, Meta Ads).
- **Layout do deck** — perguntar qual dos dois usar (ver seção 4):
  - **Disciplina Ártica** (padrão) — navy chapado, branco como único destaque.
  - **Aurora Ártica** — gradiente navy > teal, accent gelo, tabela com header sólido.

Apresentar assim e parar pra aprovação:

> **Direcionamento de Criativos — [Cliente]**
> Produto/oferta: [...] · Peças: [...] · Formato: [Story 1080x1920] · Veiculação: [Meta Ads]
> Layout: [Disciplina Ártica | Aurora Ártica]
>
> Aprova essa direção ou quer ajustar?

### 3. Montar o conteúdo (mostrar em texto antes do PDF)
Com base em **dores + desejos do avatar + briefing**, montar e mostrar pro usuário:
- **Avatar**: ficha (Idade, Perfil, Onde/Decisor, Momento) + dores e desejos.
- **Solicitações**: uma por peça, cada uma é um **roteiro cena a cena**. Marcar a etapa de funil
  no pill da solicitação (ex: Topo, Fundo).

Ajustar se o usuário pedir antes de gerar o PDF.

### 4. Montar o deck (formato oficial)
Dois layouts disponíveis, mesma folha vertical 1080x1528, mesma estrutura e **os mesmos tokens**.
A escolha foi feita no checkpoint 2:

| Layout | Arquivo | Cara |
|---|---|---|
| **Disciplina Ártica** (padrão) | `SKILL_FILES/template-criativos.html` | Navy `#00002c` chapado, cards `#0a0a3d`, branco como único destaque. Sóbrio. |
| **Aurora Ártica** | `SKILL_FILES/template-criativos-aurora.html` | Gradiente navy > teal, accent gelo `#a9e2f2`, capa com logo + seta, tabela com header sólido gelo, anexo na horizontal. |

**Identidade ARTTICO sempre**, nos dois, mesmo quando o cliente tem marca própria: o design-guide
do cliente vale só pras peças/anexos, nunca pro deck.

O Aurora tem três tokens a mais, todos com fallback simples:
- `{{COVER_FRENTES}}` (capa, ex: "Pacientes Modelo · Corpo Clínico"; sem frentes, usar
  "Topo · Meio · Fundo de funil").
- `{{AVATAR_NOME}}` (ex: "a paciente"). Com um avatar só, usar "dores e desejos". Com mais de um,
  duplicar o slide de Avatar, um por frente.
- `{{SOL_FRENTE}}` no eyebrow da Solicitação (ex: " · Pacientes Modelo"); sem frentes, deixar vazio.

> **Modelos prontos:** `SKILL_FILES/referencia-direcionamento.html` (Disciplina Ártica, exemplo
> real: Garagem do Particular, 11 solicitações) e `SKILL_FILES/referencia-aurora.html` +
> `.pdf` (Aurora Ártica, exemplo: Clínica Velleza, com anexo de vídeo e de estático).
> Deck enxuto nos dois: Capa, Briefing, Avatar, Solicitações e Fechamento. Padrões que estabelecem:
> - **Estático é Solicitação** também, no mesmo formato de tabela (Arte | Texto | Imagem |
>   Observações): 1 linha com headline + detalhes + CTA na coluna Texto.
> - **Moldura de anexo abaixo do roteiro** nas solicitações que **têm referência** (o usuário
>   indica quais). No Disciplina Ártica, vídeo (`.attach.v`) e estático (`.attach.s`) são ambos
>   **1080x1920**; no Aurora, vídeo é 9:16 e estático é 3:4, com a moldura na horizontal
>   (rótulo "Vídeo referência" + divisor + thumb + link).
>   Preencher o token `{{SOL_ANEXO}}` com a moldura; sem referência, deixar vazio. Quando a
>   referência já existe (arquivo/link), a moldura vira a **thumb clicável** que redireciona ao link
>   (vídeo: frame de capa + selo de play; imagem: a própria arte).
> - **NÃO existe "Visão por funil" nem seções de "Copy" no deck.** Não incluir em hipótese nenhuma.

Estrutura:

1. **Capa.**
2. **Briefing técnico** (ficha): `{{BRIEF_PECAS}}` (ex: "3 vídeos e 1 estático"),
   `{{BRIEF_OBJETIVO}}`, `{{BRIEF_TOM}}` (ex: "Objetiva, clara, amigável e persuasiva"),
   `{{BRIEF_FORMATO}}` (ex: "Story · 1080x1920"), `{{BRIEF_VEICULACAO}}` (ex: "Meta Ads"),
   `{{BRIEF_ORIENTACOES}}`.
3. **Avatar**: boneco line-art (persona) + ficha `{{AVATAR_FICHA}}` (linhas
   `<div class="pf"><span class="pk">Rótulo</span><span class="pv">Valor</span></div>`, ~4) e as
   listas `{{AVATAR_DORES}}`/`{{AVATAR_DESEJOS}}` (`<li>` de `ul.list`).
4. **Solicitações** — duplicar o slide de Solicitação, **um por peça**. Tokens por slide:
   `{{SOL_TITULO}}` (ex: "Solicitação 01"), `{{SOL_ETAPA}}` (ex: "Fundo · UGC"), `{{SOL_FORMATO}}`
   (ex: "Story · 1080x1920"), `{{SOL_CENAS}}` (linhas `<tr>`). Cada cena:
   - **Arte** = número da cena.
   - **Texto** = a fala/legenda **exata** daquela cena.
   - **Imagem** = como captar ("Mateus falando", "caixa de perguntas", "aluno falando").
   - **Observações** = grafismo ("Lettering no R$ 79,90", "legenda na tela").
   Manter ~5 a 7 cenas por roteiro pra caber no slide. Se passar, dividir a Solicitação em 2
   slides com o mesmo cabeçalho.
5. **Fechamento** (`{{FRASE_FINAL}}`).

**Formatos de apoio para o FUNDO** (usar quando fizer sentido, não são obrigatórios):
- **UGC em vídeo** — roteiro cena a cena no padrão "E eu que...": **gancho na dor** →
  **conflito** (o que tentou e não funcionou) → **virada** (o mecanismo do produto) →
  **resultado** (transformação concreta) → **CTA** (ex: "clica no link da bio e vem fazer parte
  da tropa"). Coluna Imagem = "aluno falando" / "Mateus falando". Adaptar dor, mecanismo e oferta
  ao cliente real.
- **Estático formato notícia** — Solicitação com formato estático: nas linhas usar os **elementos
  da arte** (Manchete / Linha fina / Selo "leia mais" / Oferta / CTA) no lugar de cenas. Coluna
  Imagem indica o layout de portal; Observações marca tarja, fonte serifada e lettering.

Exemplos de cena e das Solicitações UGC e notícia estão no rodapé do template em comentário:
copiar, adaptar e **remover o comentário do arquivo final**.

**Sistema de design (não desviar):**
- Comum aos dois: display Montserrat ExtraBold; corpo Inter; serif (Lora) só no selo ARTTICO.
  Linha de horizonte com o traço `.run` de progresso. **Sem travessões.**
- **Disciplina Ártica:** fundo `#00002c`, cards `#0a0a3d`, branco `#FFFFFF` é o único destaque.
- **Aurora Ártica:** gradiente noite > teal, accent gelo `#a9e2f2` (subtítulo do avatar, header da
  tabela, seta da capa, destaque do fechamento). **Nunca empilhar camadas de gradiente com
  `rgba()`/`transparent` no fundo:** o Chromium exporta gradiente com alpha como shading + SMask
  e a máscara corrompe a cor na conversão do PDF (o teal vira magenta). Um único gradiente
  **opaco** por slide, como está no template.

**Passo final obrigatório — numeração e progresso:** contar o total de slides `N` (após duplicar)
e, em cada slide, preencher `.pageno` com `P / N` e `.run` com `style="width:<P/N×100>%"`.

### 5. Renderizar e salvar
- Salvar o HTML em `clientes/[cliente]/direcionamento-criativos/[YYYY-MM-DD]_direcionamento.html`
  (criar a pasta `direcionamento-criativos/` se não existir).
- Renderizar em **folha vertical** passando largura/altura ao script:
  ```
  node ".claude/skills/direcionamento-criativos/SKILL_FILES/render-pdf.js" "<html>" "<pdf>" 1080 1528
  ```
- Se Playwright não estiver instalado: `npx playwright install chromium`.
- PDF final: `clientes/[cliente]/direcionamento-criativos/[YYYY-MM-DD]_direcionamento.pdf`.

### 6. Exportar para o Canva (após o PDF)
Subir o PDF pro Canva via importação (Canva Connect API — *design import*), gerando um design
editável com a mesma cara dos slides.
- **Pré-requisito:** o MCP do Canva precisa estar conectado a este ambiente. Checar se há uma
  ferramenta do Canva (ex: `mcp__*canva*`). Se **não** houver, avisar o usuário que o MCP do
  Canva não está conectado e pular esta etapa (não falhar o fluxo) — o PDF já está salvo.
  Comando pra conectar: `claude mcp add canva --transport http https://mcp.canva.com/mcp`.
- **Após importar:** informar o link de edição/visualização do design no Canva.

### 7. Confirmar
Informar o caminho do PDF e o link do Canva (se exportado). Perguntar se quer ajustar alguma
Solicitação, trocar uma peça ou já está pronto pra produção (passar pro `carrossel` /
`criativo-estatico` ou pra gravação).

---

## Vídeo institucional (peça "quem somos")
Quando o cliente pedir um **vídeo institucional / de apresentação da empresa** (e não peças de
funil), usar o template `SKILL_FILES/roteiro-institucional-modelo.md`. É um roteiro clássico em
**6 tempos** (gancho + definição da categoria → como funciona + dores → opções/diferenciais →
produto complementar → localização → fechamento de marca), no mesmo formato de tabela
Arte | Texto | Imagem | Observações. O arquivo traz a estrutura, um esqueleto com placeholders pra
preencher por cliente e um exemplo real preenchido (Garagem do Particular). Salvar o roteiro final
em `clientes/[cliente]/conteudo/roteiros/`.

## Observações
- Calibrar copy, ângulos e oferta pelo nicho real do cliente e pela região (`Opera em`). Pra
  clientes da América Latina, adaptar pro espanhol mantendo especificidade e persuasão.
- O UGC e a notícia no fundo são **obrigatórios**. Os demais formatos são livres (Reels, carrossel,
  estático de reposicionamento, prova social etc).
- Reaproveitar a voz real da marca (CTAs, bordões, oferta) quando o cliente já tiver referência.
- Nada de travessão em copy. CTA e linguagem orientada a conversão.
