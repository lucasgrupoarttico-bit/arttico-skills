# GitHub Deploy — Setup detalhado e troubleshooting

## Visao geral do pipeline

```
git push (main)
   -> GitHub Actions (.github/workflows/deploy.yml)
        -> npm ci
        -> npm run build           (gera dist/)
        -> FTP-Deploy-Action       (envia dist/ para server-dir via FTP)
   -> site atualizado
```

Secrets necessarios no repo (Settings > Secrets and variables > Actions):
`host_servidor`, `usuario_ftp`, `senha_ftp`.

---

## Organizacao dos projetos (workspace Arttico)

- **Repo no GitHub:** conta `lucasgrupoarttico-bit`, nome `lp-<cliente>`
  (ex.: `lp-click-cirurgia`, `lp-rafael-medeiros`, `lp-mateus-medeiros`).
- **Pasta local:** o projeto e um repo git proprio aninhado **dentro da pasta do cliente**:
  `clientes/<cliente>/lp-<cliente>/`. A pasta `clientes/` e ignorada pelo `.gitignore` do
  Arttico (projetos de cliente tem repo proprio) — por isso o repo aninhado nao conflita.
- **Monorepo (uma subpasta por pagina):** dentro do repo da LP, cada pagina fica na sua
  subpasta com projeto completo; na raiz so `.github/` e `.gitignore`.

```
clientes/<cliente>/
├── briefing.md, copy/, marca/, google.ads/, meta.ads/, relatorios/ ...
└── lp-<cliente>/                     (repo git proprio: lp-<cliente>.git)
    ├── .github/workflows/deploy.yml  (paths-filter + 1 job por pagina)
    ├── .gitignore
    └── <pagina>/                     (ex.: vesicula/  -> Vite: src/, public/, package.json...)
```

**Casos reais:**
- `lp-rafael-medeiros` -> paginas `lp/` e `intensivo/`
- `lp-mateus-medeiros` -> paginas `lp/` e `tqb/`
- `lp-click-cirurgia`  -> pagina `vesicula/` (futuro `hernia/`)

### Mover um projeto solto para a pasta do cliente
Se o projeto estiver fora (ex.: em Downloads), mover a pasta inteira (com o `.git`) para
`clientes/<cliente>/lp-<cliente>/`. Como `clientes/` e ignorada, nao afeta o repo Arttico.
O remote e o historico do repo da LP continuam intactos — muda so o caminho local.

### Adicionar uma nova pagina a um repo existente (monorepo)
1. Criar a subpasta com o projeto (ex.: `hernia/`).
2. No `deploy.yml`: adicionar um filtro em `changes` (`hernia: - 'hernia/**'`) e um job
   `deploy-hernia` espelhando o existente (trocar caminhos e `server-dir`).
3. Commit + push: o paths-filter so deploya a pagina que mudou.
Usar `templates/deploy-monorepo.yml` como base.

---

## Descobrir o owner do GitHub e o nome exato do repo

Se `git push` retornar **"Repository not found"**, normalmente e nome errado ou conta errada.

1. Descobrir o owner por outro repo ja vinculado:
   ```bash
   git -C <outro-projeto> remote -v
   ```

2. Listar os repos do usuario autenticado (sem expor o token):
   ```bash
   TOKEN=$(printf "protocol=https\nhost=github.com\n\n" | git credential fill 2>/dev/null \
           | grep "^password=" | cut -d= -f2)
   curl -s -H "Authorization: Bearer $TOKEN" \
        "https://api.github.com/user/repos?per_page=100&affiliation=owner,organization_member" \
        | python -c "import sys,json;[print(r['full_name']) for r in json.load(sys.stdin)]"
   ```

3. Corrigir o remote:
   ```bash
   git remote set-url origin https://github.com/<owner>/<repo>.git
   git push -u origin main
   ```

---

## Definir o `server-dir` com seguranca

A `FTP-Deploy-Action` faz **mirror**: envia o build e **apaga no servidor** o que nao existe
no build. Errar a pasta pode apagar o site. Sempre perguntar ao usuario:

> "O usuario FTP entra na raiz do site (ex.: public_html) ou ja entra dentro da pasta da pagina?"

| Resposta | server-dir |
|---|---|
| Entra na raiz do site | `./<subpasta-da-pagina>/` (ex.: `./cirurgiadevesicula/`) |
| Entra direto na pasta da pagina | `./` |
| Caminho custom | o caminho exato informado (ex.: `/public_html/lp/`) |

Manter no `exclude` os arquivos do servidor que nao vem do build (ex.: `**/.htaccess`),
senao eles somem no primeiro deploy.

Em caso de duvida, descobrir a estrutura conectando no FTP e listando:
```bash
curl -s --user "$USUARIO:$SENHA" "ftp://$HOST/" --list-only
```

### Regra do `public_html` (home da conta FTP)

O destino sempre tem que cair **dentro do `public_html`** (a pasta web). Se vai ou nao o
prefixo `/public_html/` depende de onde a **conta FTP abre** — isso e definido na hospedagem
(cPanel: campo "Directory" ao criar o usuario FTP), nao no codigo:

| Onde o FTP abre (home) | server-dir | Exemplo |
|---|---|---|
| **Dentro do `public_html`** (recomendado) | caminho relativo simples, SEM prefixo | `./cirurgiadevesicula/`, `/lp/` |
| **Acima, na raiz da conta** | precisa do prefixo `/public_html/` | `/public_html/lp/`, `/public_html/tqb/` |

**Padronizacao recomendada:** criar todas as contas FTP com a home **no `public_html`**
(como Clínica Exemplo, Cliente Exemplo A e Cliente Exemplo B). Assim o `server-dir` fica sempre
relativo simples e nunca precisa de `/public_html/`. NUNCA adicionar `/public_html/` num
server-dir cuja conta ja abre dentro do `public_html` — isso vira `public_html/public_html/...`
e quebra o deploy.

> ⚠️ **ARMADILHA CRITICA — o deploy errado NAO falha, ele "tem sucesso".** Se a conta abre
> dentro do `public_html` e voce poe `server-dir: /public_html/tqb/`, a action cria a pasta
> aninhada `public_html/public_html/tqb/` e sobe os arquivos la. O run fica **verde**, o log
> mostra "Uploading ... files" normalmente, mas o site real (`dominio.com/tqb/`) **nunca muda**.
> O lixo aninhado ate fica acessivel em `dominio.com/public_html/tqb/`. Por isso: **NUNCA
> confie so no check verde — valide sempre no site live** (ver "Validar deploy de verdade").

Casos reais (referencia):
- `lp-click-cirurgia` -> FTP abre no `public_html` -> `./cirurgiadevesicula/`
- `lp-rafael-medeiros` -> FTP abre no `public_html` -> `/lp/` e `/intensivo/`
- `lp-mateus-medeiros` -> FTP abre no `public_html` -> `tqb/` e `lp/`
  (ja teve o bug do `/public_html/tqb/` duplicado, corrigido em jun/2026 para `server-dir` relativo)

---

## Lockfile e `npm ci`

O workflow usa `npm ci`, que exige `package.json` e `package-lock.json` sincronizados.
Sempre que mexer em dependencias:
```bash
npm install            # atualiza o package-lock.json
git add package-lock.json package.json
git commit -m "deps"
```
Sintoma de lockfile dessincronizado no Action: erro
`npm ci can only install packages when your package.json and package-lock.json are in sync`.

---

## Troubleshooting do run

| Sintoma | Causa provavel | Acao |
|---|---|---|
| `npm ci` falha | lockfile dessincronizado | `npm install` + commit do lock |
| Build falha | erro de codigo/TS | rodar `npm run build` local e corrigir |
| FTP: `530 Login incorrect` | secret errado | revisar `host_servidor`/`usuario_ftp`/`senha_ftp` |
| FTP: timeout/`ECONNREFUSED` | host/porta ou firewall | confirmar host; testar FTPS (`protocol: ftps`) |
| Deploy OK (verde) mas site nao muda | `server-dir` com `/public_html/` numa conta que ja abre no public_html -> subiu pra `public_html/public_html/...` | tornar o `server-dir` relativo (`tqb/`); checar se o conteudo novo aparece em `dominio.com/public_html/<pagina>/` confirma o diagnostico |
| Arquivos do servidor sumiram | faltou `exclude` | re-subir os arquivos e adicionar ao `exclude` |

Ver logs completos sempre pela URL do run (campo `html_url`), ou:
```bash
python scripts/check_deploy.py --watch
```

### Validar deploy de verdade (nao confiar so no check verde)

O run verde so prova que a action rodou, NAO que o site mudou (ver "ARMADILHA CRITICA" acima).
Depois de todo deploy, validar no site live. Para SPA (Vite/React), o `index.html` so referencia
o bundle com hash novo — entao a prova e o hash novo estar no ar:

```bash
export MSYS_NO_PATHCONV=1   # Git Bash converte /public_html em path do Windows; isso desativa
# 1. index.html foi reescrito? (Last-Modified tem que ser de agora)
curl -s -I "https://<dominio>/<pagina>/" | grep -i last-modified
# 2. o build novo realmente subiu? (pega o hash referenciado e confirma 200)
HASH=$(curl -s "https://<dominio>/<pagina>/" | grep -o 'index-[A-Za-z0-9_-]*\.js' | head -1)
curl -s -o /dev/null -w "%{http_code}\n" "https://<dominio>/<pagina>/assets/$HASH"
```

Se o `Last-Modified` continuar antigo ou o asset novo der 404, o deploy caiu na pasta errada
(quase sempre o `/public_html/` duplicado). Para confirmar, teste `https://<dominio>/public_html/<pagina>/`:
se o conteudo NOVO aparecer la, e exatamente esse bug — corrija o `server-dir` para relativo.

> Limpeza opcional: a pasta aninhada `public_html/public_html/<pagina>/` fica orfa no servidor
> apos a correcao. Nao quebra nada, mas da pra remover via FTP/cPanel.

---

## Variacoes uteis do workflow

- **FTPS (FTP sobre TLS):** adicionar `protocol: ftps` nos `with:` da action.
- **Saida diferente de dist:** ajustar `local-dir` (ex.: `./build/`, `./public/`).
- **Sem build (HTML puro):** remover os steps de Node/`npm` e deixar so o checkout + deploy,
  com `local-dir: ./`.
- **Build com pnpm/yarn:** trocar `npm ci`/`npm run build` pelos comandos equivalentes.
