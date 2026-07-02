---
name: relatorio-cliente
description: >
  Gera relatório de performance de tráfego pago (Meta Ads e/ou Google Ads) para um ou todos os
  clientes. Salva HTML na pasta do cliente com data no nome.
  Use quando o usuário pedir: "relatório do cliente X", "gera relatório", "relatório semanal",
  "relatório mensal", "relatório de todos os clientes", "relatório dos últimos 7 dias".
---

# /relatorio-cliente — Relatório de Tráfego Pago

## Contexto
Ler `_contexto/empresa.md`, `_contexto/preferencias.md` e `marca/design-guide.md` antes de começar.

## Parâmetros

- **cliente** — nome da pasta do cliente (ex: `pinheiro-borges`) ou `todos`
- **período** — `7d` (padrão) ou `mes-anterior`
- **plataforma** — `meta`, `google` ou `ambas` (padrão: ler do briefing do cliente)

Se nenhum parâmetro for fornecido, perguntar em sequência:
1. "Pra qual cliente?" (listar pastas em `clientes/` excluindo `_modelo-cliente`)
2. "Período: últimos 7 dias ou mês anterior?"

---

## Fluxo

### 1. Identificar clientes

**Se `todos`:**
- Listar pastas em `clientes/` exceto `_modelo-cliente`
- Para cada uma, ler `briefing.md` e verificar campo `Plataformas:`
- Processar em sequência

**Se cliente específico:**
- Ler `clientes/[cliente]/briefing.md`
- Verificar campo `Plataformas:` para saber quais APIs chamar

### 2. Definir período

- `7d` → data de hoje menos 7 dias até ontem
- `mes-anterior` → primeiro ao último dia do mês anterior

### 3. Puxar dados

**Meta Ads** (se `Plataformas:` inclui Meta):
- Usar o MCP oficial do Meta (`claude.ai Meta` — mcp.facebook.com/ads) para puxar insights da conta do cliente
- Identificar a conta do cliente pelo campo `Conta Meta Ads:` do briefing
- Métricas principais: results, cost_per_result, ctr, spend
- Métricas secundárias: cpm, reach, impressions, frequency, roas, quality_ranking

**Google Ads** (se `Plataformas:` inclui Google):
- Usar `/google-ads-ratos` para puxar relatório da conta
- Identificar a conta pelo campo `Conta Google Ads:` do briefing
- Métricas principais: conversions, cost_per_conversion, ctr, cost
- Métricas secundárias: quality_score, avg_cpc, impression_share, search_impression_share

### 4. Analisar métricas secundárias

Para cada métrica secundária, avaliar:
- Está dentro dos benchmarks brasileiros do setor?
- Tem anomalia vs período anterior (queda ou alta >20%)?
- Qual é a ação recomendada?

Tom: direto, específico, orientado a ação. Sem jargões. Frases curtas.

Exemplos de análise:
- "Frequência 4.2 — acima do ideal (1.5–3.0). Expanda o público ou renove os criativos."
- "CTR 0.8% — abaixo da média BR (1.2–2%). Teste novos hooks nas primeiras cenas."
- "Quality Score 4/10 — melhore a relevância do anúncio e a velocidade da landing page."
- "CPM R$42 — elevado pra esse segmento. Revise a segmentação de público."

### 5. Gerar HTML

Usar o template em `SKILL_FILES/template-report.html` como base.

Substituir os placeholders:
- `{{CLIENTE}}` — nome do cliente (campo `Cliente:` do briefing)
- `{{PERIODO_LABEL}}` — ex: "19/05 a 25/05/2026" ou "Abril 2026"
- `{{PLATAFORMA}}` — "Meta Ads", "Google Ads" ou "Meta Ads + Google Ads"
- `{{DATA_GERACAO}}` — data e hora de geração
- `{{METRICAS_PRINCIPAIS}}` — linhas da tabela com os valores reais
- `{{METRICAS_SECUNDARIAS}}` — cards gerados com análise
- `{{SUGESTOES}}` — lista numerada de ações recomendadas
- `{{COMPARACAO}}` — variação % vs período anterior (se disponível; se não, omitir essa seção)

### 6. Salvar

Para Meta Ads:
`clientes/[cliente]/meta.ads/relatorios/[YYYY-MM-DD]_[periodo].html`

Para Google Ads:
`clientes/[cliente]/google.ads/relatorios/[YYYY-MM-DD]_[periodo].html`

Exemplos:
- `clientes/pinheiro-borges/meta.ads/relatorios/2026-05-25_7d.html`
- `clientes/pinheiro-borges/google.ads/relatorios/2026-05-01_abril.html`

### 7. Confirmar

Ao finalizar, informar o caminho do arquivo gerado.
Se gerou pra todos, mostrar a lista completa ao final.

---

## Configuração (primeira vez por cliente)

**Meta Ads:** MCP oficial já conectado (`claude.ai Meta`). Basta ter o ID da conta de anúncios preenchido no `briefing.md` do cliente (`Conta Meta Ads:`).

**Google Ads:** Se google-ads-ratos não estiver configurado pra esse cliente:
> "Preciso das credenciais do Google Ads de [cliente]. Rode `/google-ads-ratos setup` primeiro."
