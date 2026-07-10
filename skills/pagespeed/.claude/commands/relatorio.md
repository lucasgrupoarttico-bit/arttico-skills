# /pagespeed relatorio

Gera um relatório HTML completo consolidando dados de PageSpeed Insights e
Microsoft Clarity para o cliente. Usa o design guide do Grupo Arttico.

## O que este comando faz

1. Pergunta qual cliente e período
2. Coleta dados de PageSpeed (roda API ou usa dados já coletados nessa sessão)
3. Coleta dados de Clarity (roda API ou usa dados já analisados nessa sessão)
4. Preenche o template `templates/relatorio.html` com os dados reais
5. Salva o HTML no diretório do cliente no CC-OS RATOS
6. Exibe o caminho do arquivo gerado

## Instruções para execução

### PASSO 0 — Identificar contexto

1. Ler `contas.yaml` da skill
2. Perguntar qual cliente (se houver mais de um)
3. Verificar se já há dados do PageSpeed e/ou Clarity nessa conversa:
   - Se sim, usar esses dados — não rodar novamente
   - Se não, perguntar: "Tem algum print do PageSpeed ou Clarity pra incluir no relatório?"

### PASSO 1 — Coletar dados PageSpeed (se não coletados ainda)

```bash
# Mobile (obrigatório)
python3 ~/.claude/skills/pagespeed/scripts/pagespeed_api.py analyze \
  --url "URL_DO_CLIENTE" --strategy mobile

# Desktop (opcional, mas enriquece o relatório)
python3 ~/.claude/skills/pagespeed/scripts/pagespeed_api.py analyze \
  --url "URL_DO_CLIENTE" --strategy desktop
```

### PASSO 2 — Coletar dados Clarity (se não coletados ainda)

Se Clarity API Key estiver configurada:
```bash
python3 ~/.claude/skills/pagespeed/scripts/clarity_api.py metrics \
  --project-id "PROJECT_ID" --api-key "API_KEY" \
  --start-date "DATA_INICIO" --end-date "DATA_FIM"
```

Se não tiver API Key: pular seção Clarity no relatório (ou usar prints enviados).

### PASSO 3 — Preparar dados para o template

Organizar todas as variáveis necessárias para substituição no HTML:

```
{{CLIENTE}}              → nome do cliente
{{SITE_URL}}             → URL do site
{{PERIODO}}              → ex: "01/05 a 31/05/2026"
{{DATA_GERACAO}}         → data de hoje

PageSpeed Mobile:
{{PS_MOB_PERF}}          → score performance (0-100)
{{PS_MOB_ACESS}}         → score acessibilidade
{{PS_MOB_BP}}            → score boas práticas
{{PS_MOB_SEO}}           → score SEO
{{PS_MOB_LCP}}           → valor LCP (ex: "2.4s")
{{PS_MOB_TBT}}           → valor TBT (ex: "150ms")
{{PS_MOB_CLS}}           → valor CLS (ex: "0.05")
{{PS_MOB_FCP}}           → valor FCP (ex: "1.8s")
{{PS_MOB_STATUS}}        → "90+ ✅" ou "Abaixo de 90 ⚠️"

PageSpeed Desktop (se disponível):
{{PS_DESK_PERF}}         → score performance desktop
{{PS_DESK_STATUS}}       → status

Plano de ação (até 5 itens principais):
{{PLANO_ITEM_1_TITULO}}
{{PLANO_ITEM_1_DESC}}
{{PLANO_ITEM_1_IMPACTO}}
... (repetir para itens 2-5)

Clarity:
{{CL_SESSOES}}           → total de sessões
{{CL_DURACAO}}           → duração média
{{CL_PAGINAS}}           → páginas por sessão
{{CL_RAGE}}              → % rage clicks
{{CL_DEAD}}              → % dead clicks
{{CL_SCROLL}}            → % scroll rápido
{{CL_BOT}}               → % bot traffic

Insights Clarity (até 3):
{{CL_INSIGHT_1}}
{{CL_INSIGHT_2}}
{{CL_INSIGHT_3}}
```

### PASSO 4 — Ler template e substituir variáveis

1. Ler o arquivo `~/.claude/skills/pagespeed/templates/relatorio.html`
2. Substituir TODAS as variáveis `{{...}}` pelos dados reais
3. Para métricas ausentes (ex: Clarity sem API Key), substituir por `"—"` ou remover a seção

**Lógica de cor para scores:**
- Score >= 90: classe `score-bom` (verde `#22c55e`)
- Score >= 50: classe `score-medio` (âmbar `#f59e0b`)
- Score < 50: classe `score-ruim` (vermelho `#ef4444`)

**Lógica de cor para Core Web Vitals:**
- Dentro do threshold: classe `cwv-bom`
- Melhoria necessária: classe `cwv-medio`
- Ruim: classe `cwv-ruim`

### PASSO 5 — Salvar o arquivo

Salvar em:
```
ccos-ratos/clientes/{slug-cliente}/relatorios/pagespeed_{YYYY-MM-DD}.html
```

Onde `slug-cliente` é o nome do cliente em kebab-case (ex: `segantini-consultoria`).

Se o diretório não existir, criar antes de salvar.

### PASSO 6 — Exibir resultado

```
═══════════════════════════════════════════════════════════
 RELATÓRIO GERADO — {CLIENTE}
═══════════════════════════════════════════════════════════

 Arquivo: ccos-ratos/clientes/{slug}/relatorios/pagespeed_{data}.html

 Conteúdo:
   ✅ PageSpeed Mobile: XX/100
   ✅ PageSpeed Desktop: XX/100 (se disponível)
   ✅ Core Web Vitals
   ✅ Plano de ação (X itens)
   [✅/⚠️] Clarity: X.XXX sessões (se disponível)

 Para visualizar: abrir o arquivo HTML no navegador

═══════════════════════════════════════════════════════════
```

## Regras

- O relatório é para o CLIENTE — usar linguagem clara, sem jargão técnico excessivo
- Títulos das seções em português
- Sempre incluir a data de geração no relatório
- Se Clarity não estiver disponível, o relatório ainda deve ser gerado (só PageSpeed)
- Não inventar dados — se uma métrica não estiver disponível, omitir a seção
- O HTML deve ser auto-contido (sem dependências externas que possam quebrar) — fontes via Google Fonts com fallback
