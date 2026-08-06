---
name: relatorio-semanal-tastto
description: Gera o relatório semanal de tráfego pago da Tastto (conta Meta "CA - Reserva"). Puxa os dados da semana fechada, monta a tabela ToF/MoF/BoF no formato da série histórica, roda auditoria com Quality Gates do ads-ratos mais os checks de tendência da conta, sugere próximos passos priorizados e gera o HTML com o design guide da Tastto. Use quando o usuário mencionar relatório semanal da Tastto, relatório da Tastto, semanal do tráfego da Tastto, fechar a semana da Tastto, relatório de tráfego Tastto. Também dispara com /relatorio-semanal-tastto.
---

# Relatório Semanal — Tastto

Gera o relatório semanal de tráfego pago da conta **CA - Reserva** (`act_2751474615165051`),
mantendo a continuidade da série histórica que começou em 15/06/2026.

Entrega quatro coisas, nessa ordem:

1. **Relatório** — tabela ToF/MoF/BoF no formato exato da série
2. **Auditoria** — Quality Gates do `ads-ratos` + checks de tendência específicos da conta
3. **Próximos passos** — priorizados por impacto financeiro
4. **HTML** — dashboard com o design guide da Tastto

## Uso

```
/relatorio-semanal-tastto                      # última semana fechada (seg–dom)
/relatorio-semanal-tastto 03/08 a 09/08        # janela específica
/relatorio-semanal-tastto --só-auditoria       # pula a geração de arquivos
```

---

## Passo 0 — Pré-check de credenciais (OBRIGATÓRIO)

Antes de qualquer coisa, confirmar que dá pra ler a conta. Duas rotas, nessa ordem:

**Rota A — MCP oficial (preferencial):**
```
mcp__claude_ai_Meta__ads_get_ad_accounts
```
Se responder, usar o MCP pra tudo (`ads_get_ad_entities` com `time_range` e `level=ad`).

**Rota B — SDK Python (fallback):**
```bash
python .claude/skills/meta-ads-ratos/scripts/read.py accounts
```

Se as duas falharem, **parar e reportar**. Não inventar número, não estimar, não
reaproveitar dados de semana anterior como se fossem da semana atual. Diagnósticos:

| Erro | Causa | O que dizer ao usuário |
|---|---|---|
| MCP Meta não autorizado | Conector sem OAuth | "Autoriza o conector Meta nas configurações do claude.ai" |
| `code 190` / `Session has expired` | Token do `.env` vencido | "Gera token novo no Graph API Explorer e atualiza `~/.claude/skills/meta-ads-ratos/.env`" |
| `(#200)` / permissão | Token sem `ads_read` | "O token precisa do escopo `ads_read` nessa conta" |

## Passo 1 — Resolver a janela e a continuidade da série

**A skill roda toda quinta e cobre os 7 dias fechados que terminam na véspera.**

```
janela = [D-7, D-1]   onde D = dia da geração
```

Gerando na quinta 06/08 → janela **30/07 a 05/08** (quinta a quarta).
Gerando na quinta 13/08 → janela **06/08 a 12/08**. E assim por diante, sem buraco.

O nome do arquivo usa a **data final** da janela.

**Por que termina em D-1:** nenhum dia entra com o dia ainda em curso. Foi exatamente
esse o erro do relatório parcial de 31/07, que capturou o último dia pela metade e
subestimou o ToF em R$ 6,30 e 23 visitas.

Fluxo:

1. Ler `historico.json` — contém todas as semanas já fechadas.
2. Calcular a janela padrão (D-7 a D-1). Se o usuário passou uma janela explícita, usar essa.
3. Se o dia da geração **não for quinta**, seguir mesmo assim com a janela D-7 a D-1,
   mas avisar no início: *"Hoje é {dia}, não quinta. A janela fica {início} a {fim}."*
4. **Se a janela sobrepõe uma entrada existente**, avisar antes de gerar e registrar
   `sobrepoe` na entrada nova (ver abaixo).
5. Nunca gerar relatório de janela em aberto sem marcar `parcial: true` e escrever
   no corpo: *"Janela parcial (N dias), não comparar diretamente com as janelas cheias."*

### Transição de cadência (evento único, 06/08/2026)

Até a Semana 7 a série era **segunda a domingo**. A partir de 06/08 passa a ser
**quinta a quarta**. Isso cria uma sobreposição de **4 dias** entre a S7 (27/07–02/08)
e a primeira janela nova (30/07–05/08): os dias 30, 31/07 e 01, 02/08 aparecem nas duas.

Como tratar:

- A entrada nova leva `"sobrepoe": {"semana": 7, "dias": 4}`.
- O corpo do relatório declara a sobreposição em uma linha.
- **Acumulados da série (gasto total, leads totais, CPL do período) precisam subtrair
  os dias repetidos.** Somar as entradas cruas contaria esses 4 dias duas vezes.
- Comparação semana a semana continua válida sem ajuste: ambas as janelas têm 7 dias.

Depois dessa transição, as janelas voltam a ser contíguas e o problema desaparece.

## Passo 2 — Coletar os dados

### Rota A — MCP oficial (preferencial)

O MCP resolve `results` / `cost_per_result` por objetivo de campanha, que é exatamente
a coluna "Resultados" do Ads Manager. Não precisa mapear `action_type` na mão.

São **quatro chamadas**, todas com `time_range: {"since": ..., "until": ...}`. Nenhuma
é opcional.

**2.1 — Campanhas (a tabela do relatório):**
```
ads_get_ad_entities  level=campaign
fields: ["name","objective","effective_status","daily_budget","spend","impressions",
         "clicks","ctr","cpm","reach","frequency","results","cost_per_result",
         "landing_page_view","lead","onsite_conversion_lead_grouped",
         "instagram_profile_follow_v2","actions:link_click","cost_per_link_click"]
```

**2.2 — Quebra diária (OBRIGATÓRIA):**
```
ads_get_ad_entities  level=campaign  time_increment=1
fields: ["name","spend","impressions","clicks","ctr","results","cost_per_result"]
filtering: [{"field":"campaign.spend","operator":"GREATER_THAN","value":["0"]}]
```
É esta chamada que revela parada de entrega. Foi ela que mostrou que MoF e BoF ficaram
4 dias em R$ 0,00 na semana de 27/07 — algo que o total semanal escondia completamente.
**Nunca pular.**

**2.3 — Criativos:**
```
ads_get_ad_entities  level=ad  sort=spend_descending
fields: ["name","effective_status","spend","impressions","clicks","ctr","cpm",
         "frequency","results","cost_per_result","landing_page_view","lead"]
```

**2.4 — Conjuntos (só se 2.2 mostrar dia zerado em alguma etapa):**
```
ads_get_ad_entities  level=adset  sort=spend_descending
fields: ["name","effective_status","delivery","daily_budget","lifetime_budget",
         "start_time","stop_time","spend","impressions","results","cost_per_result"]
```
Serve pra separar as três causas possíveis de parada: conjunto **pausado**
(`delivery.status = off`), conjunto **ativo sem entregar** (`delivery.status = active`
com 0 impressão — é falha de entrega, não pausa), ou conjunto **novo em aprendizado**
(`substatuses = in_learning_phase`).

Notas de campo aprendidas na prática:
- `spend` volta como `amount_spent`, formatado (`"R$48,73 BRL"`). Parsear.
- `actions` **não** é aceito em `level=campaign`. Use `actions:link_click` etc.
- Se um campo for rejeitado, a mensagem de erro lista todos os válidos daquele nível.

### Rota B — Script Python (fallback, quando o MCP não estiver na sessão)

```bash
python .claude/skills/relatorio-semanal-tastto/scripts/coletar.py \
  --desde 2026-07-30 --ate 2026-08-05 \
  --saida .claude/skills/relatorio-semanal-tastto/.cache/semana.json
```

Faz o mesmo trabalho: agrega por etapa, traz nível de ad e a quebra diária com
`dias_sem_entrega`. Classifica primeiro por `campanha_ids` do `conta.yaml` e só depois
por regex.

Se aparecer linha em `nao_classificados` (só entram linhas com gasto ou impressão),
rodar a descoberta e atualizar o `conta.yaml`:
```bash
python .claude/skills/relatorio-semanal-tastto/scripts/coletar.py --descobrir
```

**Nunca atribuir gasto a uma campanha sem ter quebrado por campanha.** (Regra 8 do
`meta-ads-ratos`.)

## Passo 3 — Montar o relatório

Ler `references/formato-relatorio.md` e seguir o template **literalmente** — a série
tem sete edições no mesmo formato e a consistência é o valor dela.

## Passo 4 — Auditoria

Carregar, nesta ordem:

1. `references/auditoria-semanal.md` — os checks de tendência desta conta (obrigatório)
2. `.claude/skills/ads-ratos/references/quality-gates.md` — Kill Rules, escala, orçamento
3. `.claude/skills/ads-ratos/references/benchmarks-br.md` — classificação por benchmark BR

A auditoria roda sobre a **série inteira** do `historico.json`, não só sobre a semana.
É isso que separa esta skill de um dump de métricas: os relatórios antigos erraram
justamente por só olharem a própria semana.

## Passo 5 — Próximos passos

Ordenar por impacto financeiro (maior economia/ganho primeiro). Cada item precisa de:
número específico, ação concreta e critério de sucesso. Nada de "melhorar o criativo".

Formato:
```
1. [AÇÃO] {o que fazer} — {número que justifica} → {resultado esperado}
```

## Passo 6 — Gerar os arquivos

| Arquivo | Caminho |
|---|---|
| Markdown | `clientes/tastto/trafego/relatorios/{mes}-{ano}/{DD-MM-AAAA}.md` |
| HTML | `clientes/tastto/trafego/relatorios/{mes}-{ano}/{DD-MM-AAAA}.html` |

O `{DD-MM-AAAA}` é a **data final** da janela. O `{mes}` é o mês da data final, em
português minúsculo (`agosto-2026`).

Pro HTML: ler `templates/relatorio.html` e substituir os placeholders `{{...}}`.
As cores já vêm do design guide da Tastto e a paleta de séries já foi validada pra
daltonismo — **não trocar as cores das etapas** sem revalidar.

## Passo 7 — Atualizar o histórico

Adicionar a semana ao `historico.json`. É o que alimenta os checks de tendência da
próxima execução. Sem isso a skill perde a memória da conta.

## Passo 8 — Publicar no repositório

**Faz parte do fluxo.** Todo relatório gerado sobe pro `Piv-09/tastto-mkt-interno`,
em `trafego/relatorios/{mes}-{ano}/`. Autorizado pelo usuário em 05/08/2026.

```bash
# repo é privado; o token vem do Git Credential Manager
git clone https://github.com/Piv-09/tastto-mkt-interno.git <tmp>   # ou git pull se já existir
```

**Sobem sempre os dois arquivos, juntos:**

| Arquivo | O que é | Como o time consome |
|---|---|---|
| `{DD-MM-AAAA}.md` | Relatório no formato da série + as três adições (CPL full-funnel, Auditoria, Próximos passos) | Renderiza direto no GitHub |
| `{DD-MM-AAAA}.html` | Dashboard com o design da Tastto | **Precisa baixar e abrir no navegador** |

1. Copiar o `.md` e o `.html` pra `trafego/relatorios/{mes}-{ano}/`
2. No topo do `.md`, logo abaixo do cabeçalho, incluir a linha:
   `> 📊 **Dashboard visual:** [{DD-MM-AAAA}.html](./{DD-MM-AAAA}.html) — baixe o arquivo pra abrir, o GitHub não renderiza HTML.`
3. Atualizar a seção **"Relatórios semanais do mês"** do `mensal-{mes}-{ano}.md`,
   com link pro `.md` e pro `.html` da nova edição
4. Commitar e dar push na `main`

Commit: `relatorio semanal tastto: {DD/MM} a {DD/MM}`

**Identidade e sintaxe do commit** (as duas coisas que quebraram no teste de 05/08):

- O clone novo não herda `user.name` / `user.email`. Configurar **no repo clonado**
  antes de commitar, com a mesma identidade dos commits existentes:
  ```bash
  git config user.name "Lucas Felipe | Grupo Arttico"
  git config user.email "lucas.grupoarttico@gmail.com"
  ```
- Mensagem multilinha vai por **heredoc do bash**, nunca por here-string do PowerShell:
  ```bash
  git commit -F - <<'MSG'
  relatorio semanal tastto: 29/07 a 04/08
  ...
  MSG
  ```
  Usar `@'...'@` dentro da ferramenta Bash faz o `@` virar a primeira linha da mensagem,
  ou seja, o título do commit no GitHub vira `@`.

**Sobre o HTML no GitHub:** repositório privado não renderiza HTML nem serve por
GitHub Pages (exige plano pago) nem por htmlpreview. Quem abrir o `.html` pelo site
vê o código-fonte. Por isso o `.md` é a peça de leitura e o `.html` é o anexo pra
baixar. Se um dia a Tastto quiser o dashboard com URL clicável, o caminho é publicar
num host à parte (Netlify, como já é feito nas LPs) — decisão do usuário, não da skill.

**Limites que valem sempre:**

- Mexer **somente** em `trafego/relatorios/`. Nenhum outro caminho do repo.
- **Nunca** `push --force`, nunca reescrever histórico.
- Se o arquivo de destino **já existir**, parar e perguntar antes de sobrescrever —
  pode ser uma edição feita à mão por outra pessoa.
- Se o push falhar por conflito, dar `pull --rebase` e tentar de novo. Se ainda
  falhar, reportar e não insistir.
- Ao final, informar o commit e a URL dos arquivos publicados.

## Passo 9 — Avisar a Maria Eduarda no ClickUp

Último passo. Avisar na **DM** que o relatório dos últimos 7 dias saiu e **pedir que
ela cheque os números contra o Go High Level**.

A skill **não acessa o CRM**. A comparação é dela; a mensagem é o pedido.

```
clickup_send_chat_message
  channel_id: {notificacao.clickup.channel_id do conta.yaml}
  content: {mensagem abaixo}
```

Modelo (curta — o detalhe está no relatório, não na mensagem):

```
Oi Duda! Saiu o relatório de tráfego da Tastto dos últimos 7 dias ({DD/MM} a {DD/MM}).

Investimento R$ {x} · {n} lead(s) · CPL de BoF R$ {x} · CPL full-funnel R$ {x}

{Uma frase com o achado principal da semana.}

Consegue comparar esses números com o que aparece no Go High Level? Principalmente
quantos desses {n} leads viraram contato lá dentro.
```

**Quando a janela fechar com zero lead**, trocar o parágrafo do CRM por:

```
Não teve lead nessa janela, então não tem o que comparar do lado da Meta. Mas se
aparecer contato novo da Tastto no Go High Level nesse período, me avisa, porque aí
tem algo chegando por outro caminho.

Relatório: {link do .md no repo}
Dashboard: {link do .html} (baixa pra abrir, o GitHub não renderiza HTML)
```

Regras:

- **Não resolver o destinatário por nome.** `clickup_find_member_by_name` depende de
  `clickup_get_workspace_members`, que vem vazio nesta conexão. Usar o `channel_id`
  fixo do `conta.yaml`.
- **Nunca inventar ID de canal ou de usuário.** Se `notificacao.clickup.ativo` for
  `false` ou faltar `channel_id`, pular o passo e avisar o usuário.
- Mensagem em tom de conversa, sem travessão, sem jargão. É DM, não relatório.
- Mandar **depois** da publicação, pra que os links já funcionem.
- **Uma mensagem por relatório.** Se a execução for repetida no mesmo dia (correção,
  regeração), não mandar de novo sem o usuário pedir.

### Quando ela responder

Se a Maria Eduarda devolver os números do GHL, registrar a comparação no `historico.json`
da semana correspondente, em `crm`:

```json
"crm": { "fonte": "Go High Level", "contatos": 0, "informado_em": "AAAA-MM-DD" }
```

Com dois ou três pontos acumulados, isso vira base pra um check de reconciliação
Meta × CRM. Hoje ainda não há série suficiente pra definir limite.

---

## Regras da conta (não negociáveis)

1. **CPL de BoF e CPL full-funnel andam juntos.** Todo relatório mostra os dois. O CPL
   isolado de BoF ignora ~70% da verba e faz a meta parecer batida quando não foi.
   Ver `references/auditoria-semanal.md`.
2. **PT-BR sempre.** Usar a tabela de terminologia do `ads-ratos` (gasto, alcance, etc).
3. **Sem travessão em texto de criativo/legenda.** Regra geral da Arttico.
4. **Amostra pequena é ruído.** Com menos de 10 leads na semana, não declarar tendência
   de CPL sem olhar a média móvel de 3 semanas.
5. **Números específicos.** Nenhum alerta vago. Todo alerta tem valor, período e ação.
6. **Não inventar dado.** Se a API não devolveu, o campo vai como `sem dados`.

## Arquivos da skill

| Arquivo | Papel |
|---|---|
| `conta.yaml` | Conta, metas, mapeamento de etapas e de `action_type` |
| `historico.json` | Série semanal acumulada (semeada com as Semanas 1–7) |
| `references/formato-relatorio.md` | Template exato do markdown da série |
| `references/auditoria-semanal.md` | Os checks de tendência desta conta |
| `scripts/coletar.py` | Coleta + classificação + agregação |
| `templates/relatorio.html` | Dashboard com o design guide da Tastto |
