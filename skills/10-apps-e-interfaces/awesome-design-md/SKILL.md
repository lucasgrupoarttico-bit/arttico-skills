---
name: awesome-design-md
description: Apply a DESIGN.md from the VoltAgent/awesome-design-md collection to guide UI generation with the visual identity of a real brand (Stripe, Notion, Apple, Figma, etc.). Use this skill when the user wants to build interfaces inspired by or consistent with a specific brand's design system, or when asked to "make it look like X", "use the design of Y", or "build with the Stripe/Notion/Apple aesthetic".
source: https://github.com/VoltAgent/awesome-design-md
---

This skill fetches and applies DESIGN.md files from the `VoltAgent/awesome-design-md` collection — a curated library of 72 plain-text design system documents extracted from real-world products. Each file encodes a brand's visual identity so AI agents can generate consistent, on-brand UI without requiring Figma access or CSS inspection.

The user provides a brand name and a UI to build. You fetch the corresponding DESIGN.md, absorb its rules, and then generate the interface according to those rules.

## How to Use

### Step 1 — Identify the brand

Match the user's request to one of the available brands. The collection is organized in categories:

- **AI & LLM**: Claude, Cohere, ElevenLabs, Mistral AI, Ollama, Replicate, Runway, Together AI, VoltAgent, xAI
- **Dev Tools & IDEs**: Cursor, Expo, Lovable, Raycast, Superhuman, Vercel, Warp
- **Backend / DevOps**: ClickHouse, Composio, HashiCorp, MongoDB, PostHog, Sanity, Sentry, Supabase
- **Productivity & SaaS**: Cal.com, Intercom, Linear, Mintlify, Notion, Resend, Zapier
- **Design & Creative**: Airtable, Clay, Figma, Framer, Miro, Webflow
- **Fintech & Crypto**: Binance, Coinbase, Kraken, Mastercard, Revolut, Stripe, Wise
- **E-commerce & Retail**: Airbnb, Meta, Nike, Shopify, Starbucks
- **Media & Consumer Tech**: Apple, HP, IBM, NVIDIA, Pinterest, PlayStation, SpaceX, Spotify, The Verge, Uber, Vodafone, WIRED
- **Automotive**: BMW, BMW M, Bugatti, Ferrari, Lamborghini, Renault, Tesla
- **Retro Web**: Dell (1996)

### Step 2 — Fetch the DESIGN.md

Construct the raw GitHub URL using the pattern:

```
https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/sites/<brand-slug>/DESIGN.md
```

Examples:
- Stripe → `.../stripe/DESIGN.md`
- Notion → `.../notion/DESIGN.md`
- Apple → `.../apple/DESIGN.md`

Fetch the file and read all nine sections it contains:
1. Visual Theme & Atmosphere
2. Color Palette & Roles
3. Typography Rules
4. Component Stylings
5. Layout Principles
6. Depth & Elevation
7. Do's and Don'ts
8. Responsive Behavior
9. Agent Prompt Guide

### Step 3 — Build the UI

Generate the requested interface strictly following the DESIGN.md rules. Respect:
- The exact color tokens and roles defined (primary, surface, accent, etc.)
- Typography scale, font families, weights, and line-height rules
- Component patterns (buttons, cards, inputs, nav) described in the file
- Layout principles: spacing system, grid, alignment
- Do's and Don'ts — treat violations as hard constraints, not suggestions
- The tone from the Agent Prompt Guide section

## Landing Page Structure (obrigatória)

Sempre que o output for uma landing page, a estrutura de seções é fixa e não negociável — independente do design system aplicado:

### Seção 01 — Promessa + Mecanismo Único (4U's)
Captura a atenção com a promessa principal usando os 4U's: **Útil, Urgente, Único, Ultra-específico**.
- **Headline**: A transformação prometida em 1 frase (o que o usuário ganha, não o que o produto faz)
- **Subheadline**: Explica o mecanismo único — como/por que isso é possível
- **CTA primário**: Botão de ação acima da dobra
- Sem distrações — zero links de navegação, zero texto de suporte desnecessário

### Seção 02 — Identificação do Problema
Faz o visitante se sentir compreendido antes de apresentar qualquer solução.
- Nomeia a dor específica com linguagem do ICP (não linguagem de produto)
- Agita as consequências de não resolver
- Termina criando abertura para a solução

### Seção 03 — Soluções em Blocos
Apresenta os benefícios/features em blocos visuais escaneáveis.
- Cada bloco: ícone ou visual + título curto + 1–2 linhas de descrição
- Foco em transformação, não em funcionalidade
- Mínimo 3, máximo 6 blocos

### Seção 04 — Provas Sociais
Elimina objeções com evidências de terceiros.
- Depoimentos reais com foto, nome e contexto (cargo/empresa ou resultado obtido)
- Pode incluir logos de clientes, números de impacto ou selos de credibilidade
- Tom: específico e crível, nunca genérico

### Seção 05 — FAQ
Destrói as últimas objeções antes da decisão.
- 4 a 6 perguntas que refletem dúvidas reais do ICP
- Respostas diretas, sem enrolação
- Última pergunta deve reforçar a urgência ou o risco de não agir
- Seguida de CTA final repetindo o botão da Seção 01

## Edge Cases

- **Brand not in collection**: Tell the user the brand isn't available and suggest the closest visual match from the list above.
- **Ambiguous brand name**: Ask for clarification before fetching.
- **Fetch fails**: Fall back to describing what you know about the brand's visual identity and proceed with best effort.
- **User wants a custom twist**: Apply the DESIGN.md as a base, then layer the user's customization on top — never discard the base rules entirely.

## Output Format

Always confirm which DESIGN.md you used at the top of your response:

```
> Using DESIGN.md: [Brand] — VoltAgent/awesome-design-md
```

Then deliver the working code (HTML/CSS/JS, React, or whatever the user requested).
