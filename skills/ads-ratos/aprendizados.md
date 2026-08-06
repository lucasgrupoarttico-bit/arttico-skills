# Aprendizados — Ads Ratos

Regras gerais aprendidas durante o uso. O Claude DEVE ler este arquivo no início de qualquer comando.
Regras específicas de plataforma ficam no `aprendizados.md` de cada skill de execução.

---

<!-- Aprendizados serão adicionados conforme o uso -->

## 2026-07-20 — Meta: conversão só é legível no nível adset

Contas com múltiplas janelas de atribuição retornam `results: "Not available"`
no nível `campaign`. O Meta não soma resultados de atribuições diferentes.

Verificado na Click Cirurgia: a campanha devolve "Not available", mas os
4 ad sets ativos devolvem os 66 leads normais (CPL R$5,57 a R$9,20).

**Regra:** auditar CPA/conversão sempre em `adset`. Auditar por campanha
faria o agente ler "zero conversões" numa conta saudável e propor pausá-la.

## 2026-07-20 — Nunca comparar resultado entre optimization_goal diferentes

Rafael Medeiros tem ad set `PROFILE_VISIT` com custo por resultado R$0,09,
contra R$1,41 e R$2,70 dos `OFFSITE_CONVERSIONS`. R$0,09 são visitas ao
perfil, não leads.

**Regra:** agrupar por `optimization_goal` antes de ranquear, comparar ou
calcular baseline. Sempre nomear o tipo de resultado no relatório.

## 2026-07-20 — CPM se lê decomposto, nunca isolado

`CPA = CPM ÷ (1000 × CTR × taxa_conversão)` — identidade exata, conferida.

Serve pra dizer **por que** o CPA mudou: CPM (mídia/saturação), CTR
(criativo) ou taxa de conversão (público/LP). CPM alto com frequência alta
é saturação; CPM alto com frequência baixa pode ser só público caro e
lucrativo (65+ da Click Cirurgia: CPM R$34 e o melhor CPA da conta).

## 2026-07-20 — Validar plausibilidade da taxa de conversão ANTES de usar o CPA

Pinheiro Borges (Google, PMax 90d): 5.850 conversões para 5.554 cliques = 105%.
Mais de uma conversão por clique é impossível numa venda 1:1.

**Regra:** calcular `conversões ÷ cliques` em toda auditoria. Acima de ~50%
para venda, ou acima de 100% para qualquer objetivo, tratar como problema de
medição e **invalidar o CPA** em vez de reportá-lo. Sinalizar para conferência
manual em Ferramentas › Conversões (o `read.py` não lista quais ações estão
marcadas como principais).

Um CPA bonito calculado sobre conversão inflada é pior que nenhum CPA — leva a
escalar no escuro.

## 2026-07-20 — `read.py quality-scores` e `search-terms` ignoram período

Diferente de `campaigns` e `keywords`, esses dois subcomandos não aceitam
`--date-range` / `--since` / `--until` e retornam números vitalícios.

Causou contradição aparente: campanha pausada há 90+ dias aparecendo com
milhares de cliques em `quality-scores` mas R$0 em `campaigns`. Não é erro de
dado — são janelas diferentes.

## 2026-07-20 — `campaign_name` não existe no nível adset

Dois auditores perderam chamadas com esse erro. Para associar ad set à
campanha, usar `campaign_id` e fazer uma chamada separada no nível campaign
para pegar os nomes.

## 2026-07-20 — Google Ads: não usar `read.py accounts`

O MCC `4102537076` (GOOGLE_ADS_LOGIN_CUSTOMER_ID) está desativado e sempre
retorna `CUSTOMER_NOT_ENABLED`. Isso dá falsa impressão de que a credencial
quebrou — mas o OAuth está válido.

**Regra:** consultar sempre direto pelo `customer_id` do cliente
(`read.py campaigns --customer-id <ID>`). Os 4 clientes cadastrados
respondem normalmente por essa via.

## 2026-07-20 — As skills moram em dois níveis

Credenciais (`.env`) e `contas.yaml` preenchidos ficam em `~/.claude/skills/`.
As cópias dentro do projeto têm `contas.yaml` vazio.

**Regra:** ler dados de conta sempre do nível usuário. Não concluir que
"não está configurado" olhando só a cópia do projeto.
