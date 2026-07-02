# apify

Coleta de dados via [Apify](https://apify.com) pra Arttico. Sem dependencias — so Python stdlib.

## Fontes

| Fonte | Comando | Pra que serve |
|-------|---------|---------------|
| Google Maps | `google-maps` | Leads: empresas, telefone, site, nota e nº de avaliacoes por nicho/regiao |
| Instagram | `instagram` | Posts de perfil ou hashtag, com likes/comentarios/legenda |
| TikTok | `tiktok` | Videos por perfil, hashtag ou busca, com views/likes/shares |
| Facebook Ad Library | `facebook-ads` | Anuncios ativos de concorrentes por marca/termo |

## Setup

```powershell
Copy-Item .env.example .env
# edite o .env e cole o APIFY_TOKEN (https://console.apify.com/account/integrations)
```

## Exemplos

```powershell
cd scripts
python apify.py google-maps  --query "clinica de estetica em Recife" --max 60 --cliente "Clínica Exemplo"
python apify.py instagram    --profile concorrente --type posts --limit 40
python apify.py tiktok       --search "limpa fossa" --limit 30
python apify.py facebook-ads --term "Marca Exemplo" --country BR --max 50
```

## Saida

JSON salvo em `clientes/<cliente>/apify/` (com `--cliente`) ou `dados/apify/`.
Cada comando tambem imprime um resumo legivel no terminal.

## Estrutura

```
apify/
├── SKILL.md            # fluxo pro Claude
├── README.md           # este arquivo
├── .env.example        # modelo de config (copiar pra .env)
├── .gitignore          # ignora .env e __pycache__
└── scripts/
    ├── apify.py        # CLI com os 4 subcomandos
    └── lib/__init__.py # .env loader + cliente HTTP da Apify + helpers
```

## Trocar de actor

Cada fonte usa um actor padrao do Apify Store. Pra trocar, defina no `.env`:

```
APIFY_ACTOR_INSTAGRAM=outro-owner~outro-actor
```

Se o novo actor tiver input/output diferente, ajuste a funcao `cmd_*` correspondente em `scripts/apify.py`.
