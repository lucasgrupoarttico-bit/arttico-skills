# Auditoria semanal — Tastto

Rodar **depois** de montar a tabela e **antes** de escrever os próximos passos.

A auditoria tem duas camadas:

- **Camada A — checks de tendência desta conta.** Rodam sobre a série inteira do
  `historico.json`. São os checks que a série 1–7 não tinha e que deixaram passar
  problemas reais.
- **Camada B — Quality Gates genéricos.** Carregar
  `.claude/skills/ads-ratos/references/quality-gates.md` e
  `.claude/skills/ads-ratos/references/benchmarks-br.md`.

Cada check devolve `PASS` / `ATENÇÃO` / `FAIL` e, quando não for PASS, o número que
justifica e a ação recomendada.

---

## Camada A — Checks de tendência da conta

### A1. Deriva de CPL (3 semanas)

**Por que existe:** entre as semanas 4 e 7 o CPL subiu de R$17,81 → 22,80 → 25,78 →
48,73. Cada relatório chamou o próprio número de "dentro da meta". Ninguém olhou a
série. O mensal fechou em R$25,30 e chamou de "praticamente em cima da meta" — verdade
na média, falso na tendência.

**Regra:** comparar o CPL de BoF das últimas 3 semanas **cheias**.

| Condição | Status |
|---|---|
| CPL subiu nas 3 últimas semanas cheias | `FAIL` — deriva confirmada |
| CPL subiu em 2 das 3 | `ATENÇÃO` |
| Estável ou caindo | `PASS` |

Semanas parciais entram na conta com o CPL como está, mas marcadas — nunca são a
única base de uma conclusão.

**Ação quando FAIL:** olhar o que mudou nas 3 semanas (criativo novo, verba, público)
e propor uma reversão testável, não um ajuste genérico.

### A2. CPL full-funnel

**Por que existe:** o CPL reportado divide só o gasto de BoF pelos leads. No acumulado
das semanas 1–7 isso deu R$27,89, enquanto o custo real por lead — verba total dividida
por leads — foi R$100,73. ToF e MoF existem pra alimentar o BoF; excluí-los faz a meta
parecer batida.

**Cálculo:**
```
cpl_bof         = gasto_bof / leads
cpl_full_funnel = gasto_total / leads
```

| Condição | Status |
|---|---|
| `cpl_full_funnel` > 2x `cpl_full_funnel_referencia` | `FAIL` |
| `cpl_full_funnel` > `cpl_full_funnel_referencia` | `ATENÇÃO` |
| Dentro da referência | `PASS` |

**Sempre reportar os dois números lado a lado.** Nunca só o de BoF.

### A3. Concentração de criativo

**Por que existe:** o AD 01 "T. Clientes NRA" gerou 13 dos 18 leads de julho. Quando
ficou 5 dias sem converter, o BoF inteiro produziu 1 lead. Ponto único de falha.

**Regra:** por etapa, calcular a fatia do criativo líder no resultado da etapa.

| Fatia do líder | Status |
|---|---|
| > 70% | `FAIL` — dependência crítica |
| 50–70% | `ATENÇÃO` |
| < 50% | `PASS` |

**Ação quando FAIL:** subir criativo de teste na mesma etapa antes que o líder canse.
Não esperar a queda pra reagir.

### A4. Variação de verba diária

**Por que existe:** na semana 7 a verba diária caiu de ~R$53 pra ~R$32 (-40%) e nenhum
relatório mencionou. O CPL de R$48,73 dessa semana foi lido como problema de criativo
quando era, em boa parte, efeito de volume.

**Regra:** comparar `gasto_total / dias` com a média das 3 semanas anteriores.

| Variação | Status |
|---|---|
| Fora de ±25% | `FAIL` — normalizar antes de comparar qualquer métrica |
| Fora de ±10% | `ATENÇÃO` |
| Dentro de ±10% | `PASS` |

**Ação quando FAIL:** reportar tudo em base diária nessa semana e dizer explicitamente
que a comparação semana a semana está contaminada.

### A5. Suficiência de amostra

**Por que existe:** as conclusões de BoF vêm de 1 a 6 leads por semana. A diferença
entre "melhor CPL da campanha" (R$17,81, n=6) e "acima da meta" (R$25,78, n=5) é um
lead. A semana 2 acertou ao chamar R$93,06 de ruído; as seguintes pararam de aplicar
o critério quando o número virou favorável.

**Regra:**

| Leads na semana | O que pode ser afirmado |
|---|---|
| < 3 | Nada sobre CPL. Só reportar o número com ressalva explícita |
| 3–9 | Tendência só via média móvel de 3 semanas |
| >= 10 | Comparação semana a semana é válida |

Aplicar o critério nos dois sentidos — inclusive quando o número for bom.

### A6. Fadiga de criativo no ToF

**Por que existe:** o CTR do ToF caiu monotonicamente de 1,82% (S1) a 1,13% (S5) antes
de alguém trocar o criativo. A vida útil de criativo de topo é de 3 a 4 semanas
(benchmarks-br.md).

**Regra:** por criativo ativo no ToF, comparar CTR dos últimos 7 dias com os 7 anteriores.

| Condição | Status |
|---|---|
| Queda > 20% em 14 dias, ou > 4 semanas no ar | `FAIL` — renovar |
| Queda de 10–20% | `ATENÇÃO` — preparar substituto |
| Estável | `PASS` |

### A7. Reconciliação de janelas

**Por que existe:** a série antiga usava segunda a domingo (20–26/07), mas o relatório
de 28/07 usou 21–27/07. As duas fontes nunca reconciliaram. E o parcial de 31/07 foi
fechado com o dia em curso, subestimando o ToF em R$ 6,30.

**Regra:** conferir que a janela tem 7 dias, termina em D-1 (nunca no dia da geração) e
encaixa exatamente após o `fim` da última entrada do `historico.json`. Qualquer buraco ou
sobreposição vira `ATENÇÃO` e é declarado no corpo do relatório.

**Exceção conhecida:** a troca de cadência de 06/08/2026 (segunda-a-domingo → quinta-a-quarta)
gera uma sobreposição única de 4 dias entre a S7 (27/07–02/08) e a primeira janela nova
(30/07–05/08). Essa é esperada, fica registrada em `sobrepoe` e não conta como falha —
mas **os acumulados da série precisam subtrair os dias repetidos**, senão o gasto desses
4 dias entra duas vezes.

### A8. Dias sem entrega

**Por que existe:** na semana de 27/07 a 02/08, o MoF e o BoF ficaram **quatro dias em
R$ 0,00** enquanto o ToF rodou os sete. O total semanal escondia isso por completo: a
conta aparecia como "gastando menos", quando na verdade dois terços do funil estavam
fora do ar. O CPL de R$ 48,73 foi lido como problema de criativo e não era.

**Regra:** para cada etapa, contar os dias da janela com gasto igual a zero
(vem de `entrega_por_dia` / `dias_sem_entrega`, ou da chamada 2.2 do MCP).

| Dias sem entrega na etapa | Status |
|---|---|
| >= 2 | `FAIL` — investigar antes de qualquer outra análise |
| 1 | `ATENÇÃO` |
| 0 | `PASS` |

**Ação quando FAIL:** puxar o nível de conjunto (chamada 2.4) e separar a causa:

| Sinal no conjunto | Diagnóstico | O que fazer |
|---|---|---|
| `delivery.status = off` | Pausado de propósito ou por engano | Confirmar se foi intencional e desde quando |
| `delivery.status = active` com 0 impressão | **Falha de entrega** | Investigar público, leilão, aprovação de anúncio |
| `substatuses = in_learning_phase` e gasto zero | Conjunto novo que ainda não subiu | Verificar orçamento e data de início |
| Conjunto substituto criado depois da parada | Buraco de cobertura | Contar os dias entre a pausa e o substituto entrar |

**Este check tem precedência sobre A1, A2 e A4.** Não faz sentido discutir CPL ou
deriva de custo numa semana em que a etapa não entregou. Resolver entrega primeiro,
medir depois.

**Quantificar sempre:** dias parados × orçamento diário do conjunto = verba não
investida. Com o CPL histórico, estimar os leads não gerados e **rotular como
estimativa**, nunca como dado.

---

## Camada B — Quality Gates (ads-ratos)

Aplicar na ordem da hierarquia de decisão: **converte → é lucrativo → é escalável →
é eficiente.** Nunca otimizar eficiência antes de resolver lucratividade.

Checks obrigatórios nesta conta:

| Gate | Fonte | Nota para a Tastto |
|---|---|---|
| 3x Kill Rule | quality-gates.md | CPA > R$75 (3x a meta de R$25) → pausar |
| Zero conversões | quality-gates.md | Gasto > R$50 sem lead → revisar |
| Frequência tóxica | quality-gates.md | Prospecção > 5,0 |
| CTR morto | benchmarks-br.md | CTR (leads) < 1,0% = crítico |
| Limite estatístico | quality-gates.md | Gasto mensal ~R$1,5k → decisões por campanha, não granulares |

O último importa: com R$1.400–1.500/mês a conta está na faixa "R$1.000–5.000 = mudanças
por campanha". **Não propor otimização por horário, device ou posicionamento** — não há
volume que sustente a decisão.

---

## Saída da auditoria

Tabela no relatório, ordenada por severidade (FAIL primeiro):

```markdown
| Check | Status | Número | Ação |
|---|---|---|---|
| A1 Deriva de CPL | FAIL | 17,81 → 22,80 → 25,78 (3 semanas subindo) | {ação} |
| A3 Concentração BoF | FAIL | AD 01 = 72% dos leads | {ação} |
| A2 CPL full-funnel | ATENÇÃO | R$ 100,73 vs referência R$ 78 | {ação} |
```

Checks em PASS não entram na tabela — só contam no resumo (`5 de 7 checks OK`).
