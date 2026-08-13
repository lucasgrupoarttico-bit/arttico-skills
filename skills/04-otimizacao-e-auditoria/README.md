# 04 — Otimização e auditoria

**Quando usar:** a conta está travada, o custo subiu, ou é dia de decidir onde mexer. Estas skills dizem **o que** fazer; a execução é em [`03-campanhas-meta-e-google`](../03-campanhas-meta-e-google/).

| Skill | O que faz | Chame assim |
|-------|-----------|-------------|
| [`otimizar-ads`](otimizar-ads/) | Varre as contas Meta e Google de **todos** os clientes, aplica as Quality Gates e entrega um plano de ações pra aprovação. Não muda nada sem OK. | "o que precisa de ação hoje?" |
| [`ads-ratos`](ads-ratos/) | Diagnóstico e auditoria de **uma** conta, com Health Score e benchmarks brasileiros por nicho. Base de Quality Gates usada pelas outras skills. | "faz o diagnóstico da conta do cliente X" |

## Instalação

```bash
cp -r skills/04-otimizacao-e-auditoria/ads-ratos ~/.claude/skills/
```

> A pasta numerada só organiza este repositório. Copie **a pasta da skill**, nunca a pasta da categoria.
> As duas dependem das skills de [`03-campanhas-meta-e-google`](../03-campanhas-meta-e-google/) pra ler os dados das contas.
