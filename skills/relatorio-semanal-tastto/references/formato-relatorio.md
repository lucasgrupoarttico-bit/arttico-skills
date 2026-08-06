# Formato do relatório semanal — Tastto

A série tem sete edições no mesmo esqueleto. **Manter o formato é parte da entrega.**
Não reordenar seções, não renomear títulos, não adicionar emoji.

---

## Template do markdown

````markdown
# Relatório de Tráfego — Semana {N}
**Período:** {DD/MM} a {DD/MM/AAAA}
**Gerado em:** {DD/MM/AAAA}
**Conta:** CA - Reserva | ID: 2751474615165051

---

## Resumo da semana

| Etapa | Investimento | Resultado | Custo | CTR |
|---|---|---|---|---|
| ToF — Visitas ao perfil | R$ {x} | {n} visitas | R$ {x} | {x}% |
| MoF — Visitas à LP | R$ {x} | {n} visitas LP | R$ {x} | {x}% |
| BoF — Formulário | R$ {x} | {n} leads | R$ {x} | {x}% |
| **Total** | **R$ {x}** | **{n} leads** | — | — |

**CPL de BoF:** R$ {x} (meta R$ 25) · **CPL full-funnel:** R$ {x}

## Entrega por dia
<!-- SEÇÃO CONDICIONAL: só entra quando o check A8 acusar pelo menos um dia
     de entrega zerada em alguma etapa. Sem dia zerado, omitir por completo. -->

| Dia | ToF | MoF | BoF | Total |
|---|---|---|---|---|
| {DD/MM} {abrev} | R$ {x} | R$ {x} | R$ {x} | R$ {x} |

{Uma a três frases: quais etapas pararam, em quais dias, e a causa apurada no
nível de conjunto (pausado / ativo sem entregar / novo em aprendizado).}

## Criativos e insights

**ToF:** {criativo líder com CTR e volume, criativos que entraram ou saíram}

**MoF:** {idem}

**BoF:** {idem, sempre citando quantos leads vieram de cada criativo}

## Auditoria da semana

{tabela de checks — ver auditoria-semanal.md}

## Próximos passos

1. [AÇÃO] {o que fazer} — {número que justifica} → {resultado esperado}
2. ...

## Insight da semana
{uma a três frases. O que mudou e o que isso significa pra próxima semana.}

*{responsavel do conta.yaml}*
````

---

## Regras de formatação

| Item | Regra |
|---|---|
| Moeda | `R$ 1.234,56` — ponto de milhar, vírgula decimal, espaço após `R$` |
| Percentual | `1,82%` — vírgula decimal, duas casas |
| Custo unitário | `R$ 0,26` — duas casas sempre |
| Data no corpo | `27/07 a 02/08/2026` — ano só na segunda data |
| Nome de criativo | `AD 05 "Ninguém quer mais trabalhar!"` — número, espaço, aspas |
| Semana parcial | Linha em itálico logo abaixo da tabela avisando o número de dias |
| Sem dados | Escrever `sem dados` e `—` na célula. Nunca `0` nem estimativa |
| Plural | Concordar: `1 lead` / `4 leads`, `1 visita` / `509 visitas` |

## Seções fixas vs condicionais

| Seção | Quando aparece |
|---|---|
| Cabeçalho, Resumo da semana, linha de CPL | Sempre |
| **Entrega por dia** | **Só se o check A8 acusar dia zerado** |
| Criativos e insights | Sempre |
| Auditoria da semana | Sempre |
| Próximos passos | Sempre |
| Insight da semana, assinatura | Sempre |

**Não inventar seção nova nem renomear título.** Se um achado não couber em nenhuma
seção existente, ele vai no corpo da seção mais próxima. Título descritivo do tipo
"O que aconteceu: dois terços do funil pararam de entregar" pode até ler melhor numa
edição isolada, mas quebra a comparabilidade da série — que é o valor dela.

## Diferenças em relação à série original (melhorias deliberadas)

A série 1–7 não tinha estas duas coisas. Elas foram adicionadas porque a leitura
conjunta das sete semanas mostrou que a ausência delas escondia problemas reais:

1. **Linha de CPL full-funnel** logo abaixo da tabela. O CPL de BoF sozinho divide
   o gasto de BoF pelos leads e ignora o ToF e o MoF, que existem justamente pra
   alimentar o BoF. Nas semanas 1–7 isso fez um CPL real de ~R$100 aparecer como
   R$25. Os dois números convivem: a meta contratada é sobre BoF, mas o custo de
   aquisição verdadeiro precisa estar visível.

2. **Seções de Auditoria e Próximos passos.** Os semanais originais eram descritivos
   e só o mensal tinha ação. Um relatório sem próximo passo não é um documento de
   decisão.

## Continuidade da numeração

`N` vem de `historico.json`: último `n` + 1. Se o usuário pedir uma janela que
sobrepõe uma semana já registrada, perguntar antes (ver Passo 1 do SKILL.md).
