# Arttico Skills — Claude Code OS

Coleção de **skills para o [Claude Code](https://claude.com/claude-code)** usadas no dia a dia de uma agência de marketing digital de performance. São fluxos prontos para tráfego pago, análise de dados, produção de conteúdo e automação de operação.

> Mantido pelo [Grupo Arttico](https://ratosdeia.com.br) / Ratos de IA. Os arquivos de configuração (`contas.yaml`, `.env.example`) vêm **apenas com exemplos e placeholders** — preencha com os seus próprios dados.

## Como instalar

Copie a skill desejada para a pasta de skills do Claude Code:

- **Global (todos os projetos):** `~/.claude/skills/`
- **Só neste projeto:** `.claude/skills/`

```bash
# exemplo: instalar a skill de Meta Ads globalmente
cp -r skills/meta-ads-ratos ~/.claude/skills/
```

Cada skill traz um `SKILL.md` com as instruções e, quando precisa de credenciais, um `.env.example` para você renomear para `.env` e preencher.

## Skills disponíveis

| Skill | O que faz |
|-------|-----------|
| `meta-ads-ratos` | Gerencia campanhas Meta Ads (ler, criar, editar, pausar, duplicar) via SDK oficial |
| `google-ads-ratos` | Gerencia campanhas Google Ads com GAQL (campanhas, keywords, search terms, RSA) |
| `ads-ratos` | Diagnóstico, auditoria e Health Score de contas de tráfego com benchmarks BR |
| `ga4-ratos` | Consulta dados do Google Analytics 4 (sessões, conversões, fontes, UTM, realtime) |
| `pagespeed` | Auditoria de velocidade + copy de landing pages, com plano de ação priorizado |
| `gtm-setup` | Setup completo de Google Tag Manager (WEB + SERVER) e domínio no Stape |
| `apify` | Coleta de dados via Apify (leads Google Maps, Instagram, TikTok, Facebook Ad Library) |
| `analise-concorrentes` | Análise de concorrentes no Meta Ads, Google Ads, Instagram e TikTok |
| `gmb-ratos` | Automação mensal de otimização de ficha do Google Meu Negócio |
| `relatorio-cliente` | Gera relatório de performance de tráfego pago em HTML |
| `carrossel` | Cria carrosséis para Instagram/TikTok com identidade visual da marca |
| `criativo-estatico` | Cria criativos estáticos (PNG 1080x1920) a partir de briefing ou pauta em alta |
| `direcionamento-criativos` | Monta o direcionamento de criativos por etapa de funil (PDF) |
| `plano-acao` | Cria o plano de ação / planejamento de campanha de um cliente novo (deck 16:9) |
| `publicar-instagram` | Publica carrosséis e posts no Instagram e TikTok |
| `yt-research` | Pesquisa de mercado no YouTube com análise via NotebookLM |
| `github-deploy` | Deploy automático de sites estáticos via FTP com GitHub Actions |
| `frontend-design` | Direção de design visual para novas interfaces |
| `awesome-design-md` | Aplica um DESIGN.md de marcas reais (Stripe, Notion, Apple…) na geração de UI |
| `find-skills` | Ajuda a descobrir e instalar novas skills |
| `criar-app` | Cria um app/SaaS do zero: entrevista, plano de ação, banco, telas e deploy |
| `otimizar-ads` | Varre as contas de todos os clientes e entrega plano de otimização para aprovação |
| `relatorio-semanal-tastto` | Relatório semanal de tráfego pago no formato da série histórica do cliente |

## Aviso

Estas skills foram construídas para o fluxo de trabalho de uma agência específica. Trate-as como ponto de partida: revise, adapte e substitua os exemplos pelos seus próprios dados e credenciais antes de usar em produção.

## Licença

MIT
