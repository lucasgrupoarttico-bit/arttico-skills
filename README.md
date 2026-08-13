# Arttico Skills — Claude Code OS

Coleção de **skills para o [Claude Code](https://claude.com/claude-code)** usadas no dia a dia de uma agência de marketing digital de performance. São fluxos prontos para tráfego pago, análise de dados, produção de conteúdo e automação de operação.

> Mantido pelo [Grupo Arttico](https://ratosdeia.com.br) / Ratos de IA. Os arquivos de configuração (`contas.yaml`, `.env.example`) vêm **apenas com exemplos e placeholders** — preencha com os seus próprios dados.

## Como achar a skill certa

As 23 skills estão em [`skills/`](skills/), organizadas na ordem do ciclo de um cliente. Comece pela etapa em que você está:

| Pasta | Use quando | Skills |
|-------|------------|--------|
| [`00-descobrir-novas-skills`](skills/00-descobrir-novas-skills/) | Não sabe se já existe skill pro que você quer fazer | 1 |
| [`01-planejamento-de-cliente`](skills/01-planejamento-de-cliente/) | Entrou cliente novo e falta o planejamento de campanha | 1 |
| [`02-pesquisa-e-concorrencia`](skills/02-pesquisa-e-concorrencia/) | Precisa saber o que o mercado já está rodando | 3 |
| [`03-campanhas-meta-e-google`](skills/03-campanhas-meta-e-google/) | Vai subir, editar, pausar ou puxar números de campanha | 2 |
| [`04-otimizacao-e-auditoria`](skills/04-otimizacao-e-auditoria/) | A conta travou e você precisa decidir onde mexer | 2 |
| [`05-direcionamento-de-criativos`](skills/05-direcionamento-de-criativos/) | Precisa dizer ao time o que gravar e o que escrever | 1 |
| [`06-criativos-e-conteudo`](skills/06-criativos-e-conteudo/) | O roteiro existe e falta produzir e publicar a peça | 3 |
| [`07-landing-pages-e-sites`](skills/07-landing-pages-e-sites/) | A página está lenta, a copy não converte ou falta publicar | 2 |
| [`08-medicao-e-tagueamento`](skills/08-medicao-e-tagueamento/) | Vai instalar a medição ou entender o que rolou no site | 2 |
| [`09-relatorios-de-performance`](skills/09-relatorios-de-performance/) | Fechamento de semana ou de mês pro cliente | 2 |
| [`10-google-meu-negocio`](skills/10-google-meu-negocio/) | Cliente com ponto físico que vive de busca local | 1 |
| [`11-apps-e-interfaces`](skills/11-apps-e-interfaces/) | O entregável é um produto, não uma campanha | 3 |

Cada pasta tem um `README.md` com a lista das skills, o que cada uma faz e como chamar. A lista completa está em [`skills/README.md`](skills/README.md).

## Como instalar

Copie a skill desejada para a pasta de skills do Claude Code:

- **Global (todos os projetos):** `~/.claude/skills/`
- **Só neste projeto:** `.claude/skills/`

```bash
# exemplo: instalar a skill de Meta Ads globalmente
cp -r skills/03-campanhas-meta-e-google/meta-ads-ratos ~/.claude/skills/
```

> **Importante:** a pasta numerada existe só pra organizar este repositório. Copie **a pasta da skill** (`meta-ads-ratos`), nunca a pasta da categoria — o Claude Code espera cada skill direto na raiz de `skills/`.

Cada skill traz um `SKILL.md` com as instruções e, quando precisa de credenciais, um `.env.example` para você renomear para `.env` e preencher.

## Aviso

Estas skills foram construídas para o fluxo de trabalho de uma agência específica. Trate-as como ponto de partida: revise, adapte e substitua os exemplos pelos seus próprios dados e credenciais antes de usar em produção.

## Licença

MIT
