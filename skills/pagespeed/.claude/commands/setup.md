# /pagespeed setup

Configura a skill para os clientes da agência: cadastra sites, API keys e IDs do Clarity.

## O que este comando faz

1. Detecta o contexto CC-OS RATOS (empresa e clientes já cadastrados)
2. Pergunta quais sites/clientes cadastrar
3. Salva `contas.yaml` com URLs, Clarity project IDs e configurações
4. Testa a conexão com a PageSpeed API
5. Exibe resumo e próximos passos

## Instruções para execução

### PASSO 0 — Detectar contexto existente

```bash
cat ~/.claude/skills/pagespeed/contas.yaml 2>/dev/null || echo "SEM_CONTAS"
ls ccos-ratos/_contexto/empresa.md 2>/dev/null && echo "CCOS_OK"
```

Se o CC-OS RATOS estiver instalado, ler `ccos-ratos/_contexto/empresa.md` e listar os clientes conhecidos. Informar ao usuário:
> "Encontrei os clientes: [lista]. Quais sites/domínios você quer cadastrar?"

### PASSO 1 — Coletar dados dos clientes

Para cada cliente, perguntar:

1. **Nome do cliente** (ex: "Consultoria Exemplo")
2. **URL do site principal** (ex: "https://consultoriaexemplo.com.br")
3. **URL da landing page de tráfego pago** (se diferente do site, pode ser a mesma)
4. **Microsoft Clarity — Project ID** (encontrado no painel Clarity > Settings > Project ID)
5. **Google PageSpeed API Key** (opcional — sem key funciona mas com limites de quota)

Perguntar se quer cadastrar mais clientes antes de salvar.

### PASSO 2 — Salvar contas.yaml

Salvar em `~/.claude/skills/pagespeed/contas.yaml`:

```yaml
pagespeed_api_key: ""  # opcional — https://developers.google.com/speed/docs/insights/v5/get-started

clientes:

  nome-do-cliente:
    nome: "Nome do Cliente"
    site: "https://exemplo.com.br"
    landing_page: "https://exemplo.com.br/oferta"  # URL que recebe o tráfego pago
    clarity:
      project_id: "XXXXXXXXXXXXX"
      api_key: ""  # opcional — Clarity API Key para dados automáticos
    notas: ""  # observações sobre o site (CMS, hospedagem, etc.)
```

### PASSO 3 — Testar PageSpeed API

```bash
python3 ~/.claude/skills/pagespeed/scripts/pagespeed_api.py analyze \
  --url "https://exemplo.com.br" --strategy mobile
```

Se funcionar, exibir o score de performance. Se der erro, investigar e orientar.

### PASSO 4 — Resumo final

```
═══════════════════════════════════════════════════════════
 PAGESPEED RATOS — Setup completo
═══════════════════════════════════════════════════════════

 Clientes cadastrados:
   ✅ Nome do Cliente — exemplo.com.br
   ✅ Clarity: PROJETO_ID

 API Keys:
   ⚠️  PageSpeed API Key: não configurada (funciona sem ela)
   ⚠️  Clarity API Key: não configurada (usar modo visual)

 Próximos passos:
   /pagespeed pagespeed  → analisar performance do site
   /pagespeed clarity    → analisar comportamento no Clarity
   /pagespeed relatorio  → gerar relatório HTML para o cliente

═══════════════════════════════════════════════════════════
```

## Regras

- NUNCA assumir qual cliente o usuário quer — sempre perguntar se houver mais de um
- Se o usuário não souber o Clarity Project ID, orientar: Clarity > Settings > Project ID
- PageSpeed API Key é opcional mas recomendada para evitar limite de 25 req/dia
- Se `contas.yaml` já existir, perguntar se quer adicionar novo cliente ou sobrescrever
