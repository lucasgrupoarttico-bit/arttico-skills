---
name: apify
description: >
  Coleta de dados via Apify para a Arttico. Quatro fontes: leads do Google Maps
  (empresas, telefone, site, avaliacoes por nicho e regiao), Instagram (posts/perfil/hashtag
  com likes e comentarios), TikTok (videos por perfil, hashtag ou busca com views/likes/shares)
  e Facebook Ad Library (anuncios ativos de concorrentes por marca ou termo). Roda os actors
  da Apify e salva o JSON na pasta do cliente. Use quando o usuario mencionar apify, scraping,
  raspar dados, coletar leads, leads do google maps, prospeccao, dados de perfil do instagram,
  videos do tiktok, anuncios de concorrente, ad library, biblioteca de anuncios, monitorar concorrente.
  Tambem dispara com /apify.
---

# /apify — Coleta de dados via Apify

Roda actors da Apify e salva o resultado em JSON na pasta do cliente, com um resumo legivel no terminal.

## Dependencias

- **Python 3** (so usa a stdlib — nao precisa instalar nada)
- **Token da Apify** em `.claude/skills/apify/.env`
- **Conta Apify com creditos** (cada run consome creditos da conta)

## Setup (primeira vez)

1. Pegar o token em https://console.apify.com/account/integrations
2. Copiar `.env.example` para `.env` e preencher `APIFY_TOKEN`:

```powershell
Copy-Item ".claude\skills\apify\.env.example" ".claude\skills\apify\.env"
```

3. Editar o `.env` e colar o token. Pronto — o `.env` ja esta no `.gitignore`.

Se o `.env` ainda nao existir quando o usuario pedir uma coleta, **pausar e pedir o token** antes de rodar.

---

## Fluxo

### Passo 1 — SEMPRE perguntar qual fonte/modo (obrigatorio)

Ao acionar a skill, **sempre apresentar o menu abaixo e esperar a escolha** antes de rodar
qualquer coisa — mesmo que a conversa ja sugira uma fonte (confirmar a escolha). Usar o
formato de pergunta com opcoes:

1. **Google Maps — Lista** (leads: empresas, telefone, site, avaliacoes do nicho)
2. **Google Maps — Auditoria de ficha** (rankeamento da ficha de um cliente dentro do nicho)
3. **Instagram** (posts de perfil ou hashtag)
4. **TikTok** (videos por perfil, hashtag ou busca)
5. **Facebook Ads Library** (anuncios ativos de concorrentes)

Depois da escolha, coletar os parametros que faltarem (nicho/regiao, perfil, termo, etc.).
Se faltar algo essencial, perguntar antes de rodar. Se for de um cliente, passar
`--cliente "Nome"` pra salvar na pasta certa.

### Passo 2 — Rodar o script

```powershell
cd ".claude\skills\apify\scripts"; python apify.py <fonte> <args>
```

**Google Maps — Lista (leads):**
```powershell
python apify.py google-maps --query "dentista em Natal RN" --max 50 --country br --cliente "Igor Flor"
```

**Google Maps — Auditoria de ficha (rankeamento do nicho):**
```powershell
python apify.py google-maps-audit --query "dentista em Natal RN" --target "Nome da Clinica" --max 50 --cliente "Igor Flor"
```
Coleta as fichas do nicho na ordem em que o Google Maps ranqueia e, para cada uma, traz:
**nome, categoria, descricao, nota, nº de avaliacoes, horario de funcionamento, horario de pico
e nº de postagens**. Mostra a **posicao** da ficha do cliente (`--target`), quantos concorrentes
estao acima e a media de nota/avaliacoes do top 5. Sem `--target`, traz so o ranking do nicho.
O JSON salvo contem **todos os campos** de cada ficha para a analise.

**Instagram (perfil ou hashtag):**
```powershell
python apify.py instagram --profile nomedoperfil --type posts --limit 30 --cliente "Prime Gourmet"
python apify.py instagram --hashtag marketingdigital --limit 30
```

**TikTok (perfil, hashtag ou busca):**
```powershell
python apify.py tiktok --profile nomedoperfil --limit 30
python apify.py tiktok --search "nutricao comportamental" --limit 30
python apify.py tiktok --hashtag emagrecimento --limit 30
```

**Facebook Ad Library (anuncios de concorrente):**
```powershell
python apify.py facebook-ads --term "nome da marca" --country BR --max 50 --cliente "Geoenge"
python apify.py facebook-ads --page-url "https://www.facebook.com/ads/library/?...page..." --max 50
```

> Avisar o usuario: cada run consome creditos da conta Apify e pode levar de 30s a alguns minutos.

### Passo 3 — Ler e analisar o JSON

O script imprime um resumo e salva o arquivo em:
- `clientes/<cliente>/apify/<fonte>-<label>-<data>.json` (com `--cliente`)
- `dados/apify/<fonte>-<label>-<data>.json` (sem cliente)

Ler o JSON salvo para a analise. Aplicar o tom de voz da Arttico (estrategico, direto, orientado a conversao)
ao interpretar e apresentar os dados. Para anuncios de concorrente, cruzar com a skill `analise-concorrentes`
quando fizer sentido.

### Passo 4 — (Auditoria Google Maps) Plano de acao a partir dos padroes

Apos a auditoria, ler o JSON completo e **comparar a ficha do cliente com os concorrentes melhor
ranqueados** nestas dimensoes, procurando os padroes do que os do topo fazem e o cliente nao:

- **Nota e nº de avaliacoes** — quanto falta pra alcancar a media do top 5
- **Descricao** — preenchida, com palavra-chave do nicho, completa vs vazia
- **Categoria** — a categoria principal/secundarias batem com a dos lideres
- **Horario de funcionamento** — completo, cobre os horarios de pico do nicho
- **Horario de pico** — quando o nicho tem mais movimento (input pra posts e atendimento)
- **Postagens** — frequencia de posts dos lideres vs do cliente

Entregar um **plano de acao priorizado** (do maior impacto pro menor) com acoes concretas:
o que mudar na ficha, quantas avaliacoes buscar, que posts publicar e em que horario, ajustes de
descricao/categoria. Conectar com a skill `gmb-ratos` para executar as otimizacoes recorrentes.
Se o cliente tiver pasta, salvar o plano em `clientes/<cliente>/`.

---

## Notas

- **Actors padrao** (sobrescreviveis no `.env`): Google Maps `compass~crawler-google-places`,
  Instagram `apify~instagram-scraper`, TikTok `clockworks~tiktok-scraper`,
  Facebook `apify~facebook-ads-scraper`.
- Se um actor mudar de input/output, ajustar em `scripts/apify.py` (cada fonte tem sua propria funcao `cmd_*`).
- Erros comuns: `401` = token errado; `404` = slug do actor errado; timeout = aumentar `--timeout` ou reduzir `--max`/`--limit`.
