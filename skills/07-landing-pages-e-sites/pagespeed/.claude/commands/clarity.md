# /pagespeed clarity

Lê dados do Microsoft Clarity e analisa o comportamento dos usuários no site:
scroll depth, rage clicks, dead clicks, heatmaps, sessões. Gera análise de UX com
insights acionáveis.

## Dois modos de entrada

**Modo visual** (usuário envia screenshot do Clarity):
- Claude lê visualmente as métricas do painel
- Analisa o que está visível: sessões, scroll depth, clicks, bot traffic

**Modo API** (Clarity API Key configurada no contas.yaml):
- Script Python chama a Clarity API automaticamente
- Mais completo: dados por página, sessões por período, etc.

Se o usuário não especificar, perguntar:
> "Prefere me enviar um print do Clarity, ou tem a API Key configurada para eu puxar os dados automaticamente?"

## Instruções para execução

### PASSO 0 — Identificar cliente e período

1. Ler `contas.yaml` da skill
2. Se houver mais de um cliente, perguntar qual
3. Perguntar período (padrão: últimos 30 dias)
4. Definir modo: **visual** ou **API**

### PASSO 1A — Modo visual: ler screenshot(s) do Clarity

O usuário pode enviar prints de várias telas do Clarity. Extrair de cada uma:

**Dashboard principal:**
```
Sessões totais:     X.XXX
Páginas por sessão: X.X
Duração média:      X min Xs
Taxa de bot:        X.X%
Dead clicks:        X.X%
Rage clicks:        X.X%
Scroll rápido:      X.X%
```

**Heatmap / Scroll Map (se enviado):**
```
Página analisada: /caminho
- X% dos usuários chegou até o fold principal
- X% chegou até [seção]
- X% chegou até o rodapé
- Elementos mais clicados: [listar]
- Dead clicks identificados em: [área]
```

**Gravações (se enviado):**
```
- Páginas com mais rage clicks: /caminho (X%)
- Páginas com mais dead clicks: /caminho (X%)
- Fluxo de saída mais comum: /entrada → /saída
```

### PASSO 1B — Modo API: chamar script Python

```bash
# Métricas gerais do projeto
python3 ~/.claude/skills/pagespeed/scripts/clarity_api.py metrics \
  --project-id "PROJECT_ID" \
  --api-key "API_KEY" \
  --start-date "DATA_INICIO" \
  --end-date "DATA_FIM"

# Páginas com mais sessões
python3 ~/.claude/skills/pagespeed/scripts/clarity_api.py pages \
  --project-id "PROJECT_ID" \
  --api-key "API_KEY" \
  --start-date "DATA_INICIO" \
  --end-date "DATA_FIM"
```

### PASSO 2 — Classificar métricas de comportamento

| Métrica | ÓTIMO | NORMAL | ATENÇÃO |
|---|---|---|---|
| Dead clicks | <2% | 2-5% | >5% |
| Rage clicks | <1% | 1-3% | >3% |
| Scroll rápido | <10% | 10-25% | >25% |
| Taxa de bot | <5% | 5-15% | >15% |
| Duração média | >2min | 1-2min | <1min |
| Páginas/sessão | >2.5 | 1.5-2.5 | <1.5 |

### PASSO 3 — Gerar análise de UX

**Formato da análise:**

```
═══════════════════════════════════════════════════════════
 CLARITY — {CLIENTE}
 Período: {DATA_INICIO} a {DATA_FIM}
═══════════════════════════════════════════════════════════

 MÉTRICAS DE SESSÃO
─────────────────────────────────────────────────────────
 Sessões:           X.XXX
 Duração média:     X:XX  ⚠️ BAIXO (usuário sai rápido)
 Páginas/sessão:    X.X   ✅ BOM
 Taxa de bot:       X.X%  ✅ OK

 SINAIS DE FRUSTRAÇÃO
─────────────────────────────────────────────────────────
 Rage clicks:   X.X%  🔴 ALTO — usuário clicando com raiva
 Dead clicks:   X.X%  ⚠️ MÉDIO — cliques em elementos não clicáveis
 Scroll rápido: X.X%  ✅ OK

 ANÁLISE POR PÁGINA (TOP 5)
─────────────────────────────────────────────────────────
 1. /         — XXX sessões | XX% saem sem interagir
 2. /oferta   — XXX sessões | rage clicks: X.X% ⚠️
 3. /sobre    — XXX sessões | scroll médio: XX%

 SCROLL DEPTH (página principal)
─────────────────────────────────────────────────────────
 100% chegou: acima do fold
  75% chegou: [seção]
  50% chegou: [seção]
  25% chegou: [seção abaixo]
  10% chegou: rodapé

 INSIGHTS E AÇÕES PRIORITÁRIAS
─────────────────────────────────────────────────────────

 🔴 URGENTE

 1. [INSIGHT COM NÚMERO ESPECÍFICO]
    Dado: X.X% rage clicks em /oferta — acima de 3% = frustração real
    Causa provável: [botão, formulário ou elemento com problema]
    Ação: [o que fazer]

 ⚠️ ATENÇÃO

 2. [INSIGHT]
    Dado: [número]
    Causa provável: [análise]
    Ação: [recomendação]

 💡 OPORTUNIDADES

 3. [INSIGHT]
    Dado: [número]
    Ação: [sugestão de melhoria]

═══════════════════════════════════════════════════════════
```

### PASSO 4 — Perguntar sobre relatório

Ao final da análise, SEMPRE perguntar:

> "Quer que eu gere um relatório HTML completo com esses dados do Clarity + PageSpeed para o cliente? Usa o design do Grupo Arttico."

- Se sim: executar `/pagespeed relatorio`
- Se não: encerrar com a análise em texto

## Regras importantes

- Cada insight DEVE ter um número específico — nunca dizer "muitos rage clicks", sempre "X.X% de rage clicks"
- Identificar a página com problema, não apenas a métrica geral
- Dead clicks em elementos de decoração (ícones, imagens sem link) são menos críticos que em CTAs
- Rage clicks em formulários geralmente indicam erro de validação ou submit quebrado
- Scroll depth abaixo de 50% na landing page é sinal de que o conteúdo não está engajando
- Se a taxa de bot estiver >20%, investigar antes de tirar conclusões sobre comportamento humano
