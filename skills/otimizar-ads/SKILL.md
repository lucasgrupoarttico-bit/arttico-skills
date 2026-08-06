---
name: otimizar-ads
description: Agente de gestão e otimização de tráfego pago. Varre as contas Meta e Google Ads de todos os clientes, aplica as Quality Gates e entrega um plano de ações pra aprovação. Não muda nada sem OK. Use quando o usuário disser "otimizar", "varre as contas", "o que precisa de ação hoje", "rodar otimização", "como estão as contas". Também dispara com /otimizar.
---

# Otimizar Ads

Loop diário de gestão de tráfego pago. Cruza métrica com regra, e entrega
**um plano de ações pra aprovação**.

## Regra fundamental

**Este agente propõe. Ele não executa.**

Nada é pausado, alterado ou escalado sem o Lucas aprovar explicitamente.
Depois do OK, a execução vai pras skills `meta-ads-ratos` e `google-ads-ratos`.

Motivo: são contas de cliente com verba real. Um erro de leitura de métrica
vira dinheiro queimado ou campanha vencedora morta.

## Onde as coisas ficam (importante)

A stack está fragmentada em dois níveis. Vale saber:

| O quê | Onde |
|---|---|
| Inteligência (quality gates, benchmarks) | `.claude/skills/ads-ratos/` (projeto) |
| Metas de CPA por cliente | `.claude/skills/otimizar-ads/metas.yaml` (projeto) |
| Credenciais e IDs de conta | `~/.claude/skills/*/` (**usuário**) |

As cópias de `meta-ads-ratos` e `google-ads-ratos` dentro do projeto têm
`contas.yaml` **vazio**. Os dados reais estão no nível usuário. Sempre ler de lá.

## Fluxo

### 1. Definir escopo

Sem argumento → todos os clientes de `metas.yaml`.
Com argumento (`/otimizar segantini`) → só aquele.

### 2. Auditar

Disparar o subagente `auditor-conta` — **um por cliente, em paralelo**.
Cada um lê a própria conta e devolve achados estruturados.

Rodar em paralelo importa: 15 clientes em sequência leva muito tempo e
estoura contexto. Em paralelo, cada auditoria é isolada e o orquestrador
só recebe a conclusão.

### 3. Consolidar

Juntar tudo num plano único, ordenado por **dinheiro em risco**, não por
ordem alfabética nem por cliente.

```markdown
# Otimização — <data>

## 🔴 Ação hoje (R$ X em risco)
| Cliente | Plataforma | Achado | Ação proposta | Impacto |

## 🟡 Ação esta semana
| ... |

## 🟢 Oportunidades de escala
| ... |

## ⚪ Contas saudáveis
<lista simples, sem detalhe — não ocupar espaço com o que está bem>

## ⚠️ Não avaliado
<cliente + motivo: sem meta, conta disabled, sem dados>
```

### 4. Apresentar e aguardar

Mostrar o plano e perguntar o que aprovar. Aceitar aprovação parcial
("aprova os críticos, deixa o resto").

**Não executar nada antes da resposta.**

### 5. Executar o aprovado

Só o que foi aprovado, via:
- Meta → skill `meta-ads-ratos`
- Google → skill `google-ads-ratos`

Confirmar cada execução com o resultado real da API. Se uma falhar,
reportar a falha — nunca dar como feito o que não foi.

### 6. Registrar

Salvar o plano em `clientes/_relatorios/otimizacao-<data>.md`.
Anotar o que foi aprovado, o que foi recusado e o que falhou.

Se o Lucas recusar uma proposta, perguntar o porquê e gravar em
`.claude/skills/ads-ratos/aprendizados.md`. É assim que o agente para
de repetir sugestão ruim.

## O calcanhar de aquiles: metas

As Quality Gates são todas relativas à meta do cliente
(*"CPA > 3x a meta"*). Hoje **nenhum cliente tem `cpa_meta` preenchida**
em `metas.yaml`.

Sem meta, o agente cai no benchmark do nicho — que serve pra detectar
absurdo (CTR 0,2%, frequência 8.0), mas **não** pra dizer se um CPA de
R$ 47 é bom pro Click Cirurgia. Isso depende do ticket e da margem.

Enquanto estiver assim: marcar todo achado desse cliente como
**"régua = benchmark, confiança baixa"**, e não propor ação irreversível
(pausar campanha) baseado só em benchmark. Sinalizar pro Lucas decidir.

Cada `cpa_meta` preenchida tira um cliente desse modo degradado.

## Cadência

Roda diariamente de manhã. Pra agendar, usar a skill `schedule`.

Numa rodada diária, ser econômico: se nada mudou desde ontem, dizer
"sem novidade em 12 das 15 contas" e detalhar só o que mudou.
Relatório diário que repete tudo todo dia vira ruído e para de ser lido.
