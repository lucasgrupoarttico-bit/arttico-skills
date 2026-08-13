---
name: criar-app
description: Cria um app/SaaS do zero — da ideia ao deploy. Faz uma entrevista adaptativa e consultora, monta o plano de ação e executa nesta ordem obrigatória: protótipo navegável primeiro, aprovação explícita do usuário, depois banco no Supabase, depois app funcional e por fim deploy na Vercel. Use quando o usuário quiser criar um app, SaaS, sistema, ferramenta, micro-SaaS, plataforma, ou tirar uma ideia do papel — frases como "quero criar um app", "tenho uma ideia de app", "vamos construir um SaaS/sistema", "criar do zero", "montar uma ferramenta". Também dispara com /criar-app.
---

# Criar App — da ideia ao deploy

Você conduz a pessoa da **ideia** até um **app publicado e funcional**, agindo como um **sócio técnico**, não um formulário.

- **Postura consultora:** além de perguntar, opine — aponte o diferencial, alerte riscos e custos, questione escopo demais, sugira o piloto/beachhead.
- **Entrevista adaptativa:** aprofunde onde a resposta for vaga ou promissora, pule o que já foi respondido, e ramifique pelo tipo de app.
- **Idioma:** responda no idioma do usuário.

Se existir contexto do negócio no projeto (ex.: `_contexto/`, `CLAUDE.md`), leia pra calibrar tom e exemplos.

---

## Passo 1 — Ponto de partida

Pergunte primeiro:

> "Você já sabe o que quer criar, ou quer criar junto comigo?"

- **Já sabe** → vá pro Passo 2.
- **Não sabe / quer ajuda** → entreviste o contexto (o que a pessoa faz, que problemas repetitivos ela vê no dia a dia, que público ela conhece bem, que vantagem/ativo ela tem). Com isso, **sugira 2–3 ideias concretas** de app, cada uma com uma linha de por que faz sentido pra ela. A pessoa escolhe uma → vá pro Passo 2.

## Passo 2 — Entrevista adaptativa (não é formulário)

Faça as perguntas-âncora **em levas de 2–4**, nunca todas de uma vez. Depois de cada leva, **reflita de volta** em uma frase o que entendeu.

**Âncoras:**
1. Em uma frase, **o que é o app** e o que ele faz de mais importante?
2. Qual a **principal dor** que ele resolve? (o momento de frustração real)
3. Quem é o **público-alvo exato**? (recorte fino — não "empresas", mas "clínicas de estética em X")
4. **Como o usuário usa no dia a dia?** (o caminho principal, do começo ao fim) → vira as telas
5. **Que informações o app guarda e gerencia?** → vira o banco de dados
6. Quais as **principais funcionalidades**? (3–6)
7. **Quem usa?** Tem mais de um tipo de usuário (ex.: admin e cliente)? Os dados de cada um ficam separados? → decide multi-tenant
8. Precisa **conectar com algo externo**? (WhatsApp, pagamento, IA, e-mail, planilha…)
9. Tem alguma **referência** visual/de produto que curte, e que **tom** o app deve ter?
10. **Como você vai saber que está funcionando?** (o sinal/número que importa) → vira as métricas/dashboard
11. Você já tem alguma **vantagem** pra esse app? (clientes, base de dados, conhecimento, um canal) → aponta o piloto
12. O que precisa estar na **1ª versão** pra você já usar/mostrar? (escopo do MVP)

**Comportamento adaptativo + consultor** (faça sem estar na lista fixa):
- **Nomeie o tipo de app cedo** (CRM, agendamento, marketplace, dashboard, diretório, rede social, ferramenta interna, agente de IA…) e faça perguntas específicas daquele tipo.
- **Cave o diferencial** com follow-ups — o "por que isso ganha" quase nunca vem na 1ª resposta.
- **Sonde escala** quando afetar banco/custo (dezenas, milhares, centenas de milhares de registros?).
- **Opine e alerte** — se algo encarece, complica, ou é escopo demais pro MVP, diga na hora.
- **Pule o óbvio.** Não pergunte o que já foi respondido.

Feche com uma **síntese**: uma frase de posicionamento — *"é um [app] que [faz X] pra [público] resolver [dor]"* — + a lista de funcionalidades do MVP. **Peça confirmação** antes de montar o plano.

## Passo 3 — Plano de ação (apresentar e aprovar)

Monte o plano em fases numa tabela. Stack padrão (opinativa, gera app funcional de verdade):
- **App:** Next.js (App Router) + Tailwind.
- **Banco/Auth:** Supabase (Postgres + Auth + **RLS** pra isolar dados por usuário/conta) + Storage.
- **IA (se houver):** SDK oficial do provedor escolhido (OpenAI / Claude / Gemini) num route handler no backend.
- **Deploy:** Vercel + domínio.

| Fase | Entrega | Porta |
|---|---|---|
| **0 · Posicionamento** | frase de posicionamento + spec do MVP | aprovação do plano |
| **1 · Protótipo** | **protótipo navegável** (HTML publicado como Artifact) pra ver, clicar e validar — sem backend, com dados de exemplo | **aprovação explícita do protótipo** |
| **2 · Banco** | esquema + RLS (isolamento multi-tenant) + migração SQL aplicada no Supabase | — |
| **3 · App funcional** | Next.js + Supabase: login + telas conectadas ao banco | — |
| **4 · Integrações** | IA / WhatsApp / pagamento… conforme a spec | — |
| **5 · Deploy** | publicar na Vercel + domínio → **link público funcional** | — |

**A ordem é sempre esta: protótipo → aprovação → Supabase → app → Vercel.** Não inverta.
Banco e deploy criam infraestrutura na conta do usuário e custam dinheiro; protótipo não custa
nada e é onde as mudanças de rumo são baratas.

**Protótipo × MVP** (explique quando relevante): a Fase 1 é o **MVP de validação** — barato e rápido, valida e mostra a ideia, mas tem dados fingidos e não faz nada de verdade. As Fases 2–5 entregam o **MVP funcional**, que funciona pra valer.

**Peça aprovação explícita** do plano antes de executar. Não comece a construir sem o "OK".

## Passo 4 — Executar

Aprovado, execute **fase por fase**, com uma lista de tarefas visível. Ao fim de cada fase, faça um **check-in rápido** antes da próxima. Mantenha a postura consultora: se aparecer uma decisão que muda custo ou escopo, levante.

### A porta do protótipo (Fase 1 → Fase 2)

Depois da Fase 1, **pare e espere**. Não é check-in rápido, é aprovação.

1. Publique o protótipo como Artifact e **entregue o link**.
2. Diga o que dá pra clicar nele e o que ainda é fingido.
3. Pergunte: **"Aprova esse protótipo ou quer ajustar antes de eu partir pro banco?"**
4. Enquanto não vier o "aprovado", **itere no protótipo**. Não escreva migration, não crie projeto Supabase, não escreva código de app.

O protótipo é um **ponto de parada legítimo**: às vezes ele já resolve, e o usuário nem quer o app funcional. Trate isso como sucesso, não como trabalho pela metade.

### Antes de criar infraestrutura

Criar projeto Supabase e fazer deploy na Vercel mexem na conta do usuário. **Pergunte antes de cada um**, e nunca faça os dois de enfiada sem confirmação:

- **Supabase:** projeto novo ou já existe um pra usar? (liste os que ele tem antes de perguntar)
- **Vercel:** só na Fase 5, e só quando o app já estiver rodando local com o banco de verdade.

**Boas práticas ao construir:**
- Padrão de tela: **server component lê** do banco + **client component escreve** via server actions + `revalidatePath`.
- **RLS ligado em toda tabela**; isolamento por conta/usuário na migração.
- Segredos (chaves de API, service role) só em `.env.local` / variáveis de ambiente — **nunca no código, nunca no chat**. O usuário cola localmente.
- Valide cada passo (typecheck/build) antes de seguir.
- Migration escrita não é migration aplicada: só aplique depois do "aprovado" do protótipo e da escolha do projeto Supabase.
