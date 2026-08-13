---
name: gmb-ratos
description: Automacao mensal de otimizacao de fichas do Google Meu Negocio. Executa 4 modulos todo dia 01: auditoria da ficha, publicacao de posts mensais (adaptados do Instagram via Meta MCP), respostas automaticas a avaliacoes (sem emojis, sem travessoes) e relatorio mensal salvo como task no ClickUp. Use quando o usuario mencionar google meu negocio, gmb, ficha do google, otimizacao de ficha, posts gmb, avaliacoes google, relatorio gmb. Tambem dispara com /gmb-ratos.
---

# GMB Ratos

Automacao completa de otimizacao mensal de fichas do Google Meu Negocio para os clientes do Grupo Arttico.

## Credenciais

Arquivo: `~/.claude/skills/gmb-ratos/.env`

```
GMB_CLIENT_ID=
GMB_CLIENT_SECRET=
GMB_REFRESH_TOKEN=
```

Antes de qualquer operacao, verificar se o .env existe e esta preenchido.

## Modulos (rodam dia 01 de cada mes)

### Modulo 1 — Auditoria da Ficha

Verificar via GMB API os seguintes campos para cada cliente:
- Nome, categoria primaria e secundarias
- Descricao (existe? tem palavras-chave locais?)
- Horario de funcionamento (preenchido?)
- Fotos (quantas? atualizadas?)
- Website, telefone, endereco

Gerar score de completude 0-100 por campo.
Registrar gaps encontrados na task do ClickUp ao final.

### Modulo 2 — Posts Mensais (via Instagram)

Fluxo:
1. O usuario envia a imagem + legenda dos posts do Instagram do mes
2. Claude seleciona os melhores para GMB (maximo 4 posts)
3. Adapta o conteudo:
   - Remove hashtags
   - Encurta a legenda
   - Substitui "link na bio" por CTA direto (telefone, site ou rota)
   - Remove emojis excessivos se necessario
4. Publica via GMB API

Publicacao direta sem aprovacao. Apenas o primeiro post de cada cliente novo e validado manualmente.

### Modulo 3 — Respostas a Avaliacoes (roda diariamente)

Monitorar reviews novas na ficha de cada cliente.

Classificacao automatica:
- Positiva (4-5 estrelas)
- Neutra (3 estrelas)
- Negativa (1-2 estrelas)

Regras de resposta OBRIGATORIAS:
- NUNCA usar travessoes (—)
- NUNCA usar emojis
- Tom empatico, nunca defensivo
- Respostas negativas: reconhecer, nao inventar desculpas, convidar para contato offline
- Publicacao automatica sem aprovacao

Exemplos de padrao correto:

**Positiva:**
> Que otimo ouvir isso, [Nome]! Fico muito feliz que sua experiencia tenha superado as expectativas. Te esperamos na proxima visita!

**Neutra:**
> Obrigado pelo feedback, [Nome]! Estamos trabalhando para melhorar e esperamos te receber novamente com uma experiencia ainda melhor.

**Negativa:**
> Ola [Nome], lamentamos muito pela sua experiencia. Isso nao reflete nosso padrao de atendimento. Pode nos contatar pelo [telefone/email]? Queremos resolver isso.

### Modulo 4 — Relatorio Mensal

Coletar via GMB API (Business Profile Performance API):
- Impressoes no mes
- Cliques no site
- Ligacoes recebidas
- Solicitacoes de rota
- Comparativo com mes anterior

Gerar relatorio e salvar como task no ClickUp:
- Nome da task: `Ficha otimizada | [Cliente] | [Mes Ano]`
- Responsavel: Lucas Felipe (ID: 100156957)
- Lista: Tarefas da Arttico (ID: 901306609956)
- Descricao: resumo dos 4 modulos + metricas do mes

## Cadastro de clientes

Arquivo: `~/.claude/skills/gmb-ratos/clientes.yaml`

Estrutura:
```yaml
clientes:
  - nome: Geo Engenharia
    gmb_location_id: ""
    clickup_list_id: "901306609956"
    instagram_page_id: "740905669112770"
    meta_business_id: "23863836669884532"
```

Antes de qualquer operacao, ler este arquivo para resolver nome do cliente para IDs.
Se o cliente nao estiver cadastrado, perguntar os dados e oferecer para adicionar.

## Como obter o GMB Location ID

Para cada cliente, apos aprovacao da API pelo Google:
```
GET https://mybusinessaccounts.googleapis.com/v1/accounts
```
Depois:
```
GET https://mybusiness.googleapis.com/v4/accounts/{accountId}/locations
```
O `name` retornado (ex: `accounts/123/locations/456`) e o location_id a salvar no clientes.yaml.

## Regras de seguranca

1. NUNCA publicar resposta de avaliacao com travessao ou emoji
2. NUNCA publicar post sem antes adaptar o conteudo para formato GMB
3. NUNCA hardcodar credenciais — sempre usar o .env
4. Confirmar com usuario antes de deletar qualquer post ou resposta
5. Se a GMB API retornar erro de acesso negado, informar que a aprovacao do Google ainda esta pendente

## Status da API

A Google Business Profile API requer aprovacao para gerenciar fichas de multiplos clientes.
Formulario: https://developers.google.com/my-business/content/prereqs

Enquanto aguarda aprovacao: posts e respostas podem ser gerados pelo Claude e publicados manualmente no painel do Google Meu Negocio.
