---
name: pagespeed
description: Analisa velocidade, comportamento via GA4 e copy de landing pages dos clientes. Lê prints ou PDFs do PageSpeed Insights, cria plano de ação priorizado e implementa mudanças para atingir 90+ performance. Audita LPs como especialista em copy e estrutura TSL. Integra com ga4-ratos para comportamento. Gera relatório HTML com design do Grupo Arttico. Use quando o usuário mencionar pagespeed, velocidade do site, performance, core web vitals, lighthouse, GA4, analytics, comportamento de usuário, relatório de UX, carregamento lento, copy de landing page, auditoria de LP, TSL. Também dispara com /pagespeed.
---

# PageSpeed Ratos

Análise de performance, comportamento via GA4 e copy de landing pages para os clientes da agência.

## O que esta skill faz

| Módulo | O que faz |
|---|---|
| **PageSpeed** | Lê screenshot/PDF/URL do PageSpeed Insights e cria plano de ação para atingir 90+ performance e 100 acessibilidade/SEO |
| **GA4** | Integra com ga4-ratos para analisar sessões, bounce rate, tempo de sessão, landing pages e conversões |
| **Landing Page** | Audita copy, informações e estrutura da LP — infoprodutos usam estrutura TSL, negócios locais usam versão adaptada |
| **Relatório** | Gera relatório HTML com design do Grupo Arttico consolidando PageSpeed + GA4 + LP |

## Setup

Na primeira vez, rodar:
```
/pagespeed setup
```

## Comandos

| Comando | O que faz | Quando usar |
|---|---|---|
| `/pagespeed setup` | Cadastra clientes e sites | Primeira vez |
| `/pagespeed pagespeed` | Analisa PageSpeed e implementa melhorias | Ao receber print/PDF ou URL |
| `/pagespeed ga4` | Analisa comportamento via Google Analytics 4 | Check semanal de comportamento |
| `/pagespeed lp` | Audita copy e estrutura da landing page | Ao revisar ou criar uma LP |
| `/pagespeed relatorio` | Gera relatório HTML completo | Entrega mensal pro cliente |

## Tipos de cliente

Cada cliente tem um `tipo` definido no `contas.yaml` que determina a estrutura de LP usada:

| Tipo | Clientes atuais | Estrutura de LP |
|---|---|---|
| `infoproduto` | Cliente Exemplo B, Cliente Exemplo A | TSL completa (11 seções) |
| `negocio_local` | Negócio Local Exemplo, Clínica Exemplo | TSL adaptada sem seções de oferta (8 seções) |

## Estrutura TSL — Infoprodutos

1. **Headline com promessa + Benefício + 4Us** (Urgente, Único, Ultra-específico, Útil)
2. **Explicação do Mecanismo do Problema** — por que o problema existe na raiz
3. **Explicação do Mecanismo da Solução** — como o produto resolve de forma única
4. **Bloco da Prova** — depoimentos com resultado específico, prints, mídia
5. **Identificação** (pra quem serve) — 1º botão de CTA
6. **Transição de Oferta** — ponte do conteúdo educacional para a oferta
7. **Explicação da Oferta** — o que está incluso, valor percebido — Botão de compra
8. **Bônus** — o que vem a mais — Botão de compra
9. **Resumo da Oferta** com todos os entregáveis e valor total
10. **Garantia** — prazo claro, remoção do risco
11. **FAQ** — responde as principais objeções

## Estrutura TSL — Negócios Locais

Versão sem as seções de oferta (itens 6–9 da TSL completa):

1. **Headline com promessa + Benefício + 4Us**
2. **Explicação do Mecanismo do Problema**
3. **Explicação do Mecanismo da Solução**
4. **Bloco da Prova** — avaliações Google, fotos do serviço, cases reais
5. **Identificação** (pra quem serve) — 1º CTA (WhatsApp, formulário, ligação)
6. **Apresentação dos Serviços/Entregáveis** — o que está incluso, como funciona o atendimento
7. **Garantia** (se o negócio oferece)
8. **FAQ**

## Papel do especialista em landing pages

Ao analisar qualquer LP, Claude atua como especialista em copy e estrutura. Deve:
- Mapear quais seções da estrutura existem, estão fracas ou ausentes
- Avaliar a headline pelos 4Us e sugerir versão mais forte se score < 3
- Checar se o mecanismo do problema e da solução estão claros e únicos
- Verificar se há prova social suficiente com números e nomes reais
- Analisar se os CTAs são específicos e orientados à ação
- Identificar objeções não tratadas no FAQ
- Verificar match entre o anúncio (se conhecido) e o copy da LP

## Dois modos de entrada no PageSpeed

**Modo visual** — usuário envia screenshot ou PDF do PageSpeed Insights:
- Claude lê visualmente as notas e oportunidades

**Modo API** — usuário fornece a URL do site:
- Script Python chama a Google PageSpeed Insights API
- Extrai Core Web Vitals, oportunidades e diagnósticos automaticamente

## Arquivo de contas (contas.yaml)

Localização: `~/.claude/skills/pagespeed/contas.yaml`

Antes de qualquer análise, Claude DEVE ler este arquivo para resolver
o nome do cliente, URL, tipo (infoproduto/negocio_local) e API keys.

## Design do relatório

O relatório HTML usa o design guide do Grupo Arttico:
- Fundo: `#00002c` | Cards: `#0a0a3d` | Texto: `#FFFFFF`
- Fonte títulos: Montserrat ExtraBold | Corpo: Inter
- Border-radius: 12px | Sem bordas visíveis
- Template em: `templates/relatorio.html`

## Referências (carregar sob demanda)

| Arquivo | Quando carregar |
|---|---|
| `references/pagespeed-fixes.md` | Ao gerar plano de ação do PageSpeed |
