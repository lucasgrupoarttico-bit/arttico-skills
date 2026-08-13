# 08 — Relatórios de performance

**Quando usar:** fechamento de semana ou de mês, hora de entregar os números pro cliente.

| Skill | O que faz | Chame assim |
|-------|-----------|-------------|
| [`relatorio-cliente`](relatorio-cliente/) | Relatório de tráfego pago (Meta e/ou Google) de um cliente ou de todos. Salva o HTML na pasta do cliente com a data no nome. | "gera o relatório do cliente X dos últimos 7 dias" |
| [`relatorio-semanal-tastto`](relatorio-semanal-tastto/) | Relatório semanal no formato da série histórica de um cliente específico: tabela ToF/MoF/BoF, auditoria com Quality Gates e próximos passos priorizados. | "fecha a semana da Tastto" |

## Instalação

```bash
cp -r skills/08-relatorios-de-performance/relatorio-cliente ~/.claude/skills/
```

> A pasta numerada só organiza este repositório. Copie **a pasta da skill**, nunca a pasta da categoria.
> `relatorio-semanal-tastto` é o exemplo de relatório sob medida pra um cliente. Use como molde pra criar o de outro: troque `conta.yaml`, `templates/relatorio.html` e o formato em `references/`.
