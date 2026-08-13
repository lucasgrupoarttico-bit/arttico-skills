---
name: github-deploy
description: Configura e executa deploy automatico de sites estaticos via FTP usando GitHub Actions. Cria o repositorio, gera o workflow, orienta os secrets FTP, faz o primeiro deploy e monitora os runs. A cada git push na branch main o site builda e publica sozinho. Use quando o usuario mencionar deploy ftp, publicar site, github actions, automatizar deploy, subir landing page, CI/CD, conectar repositorio ao servidor, deploy automatico, hospedagem. Tambem dispara com /github-deploy.
---

# GitHub Deploy

Automatiza a publicacao de sites estaticos (landing pages, sites Vite/React/Vue/Astro, HTML puro)
no servidor do cliente via **FTP**, disparado por **GitHub Actions** a cada `git push`.

**Fluxo final:** o usuario edita -> `git commit` -> `git push` na `main` -> o GitHub Action
builda o projeto e envia a pasta de saida (ex.: `dist/`) por FTP -> site atualizado.

---

## PRIMEIRO PASSO — sempre, ao invocar esta skill (obrigatorio)

Antes de qualquer coisa, **sempre rodar o setup inicial** perguntando ao usuario:

> "E um **cliente novo** (projeto ainda nao existe aqui no Claude) ou **ja possui projeto**
> aqui no Claude?"

- **Cliente novo** -> seguir **Setup (primeira vez)**: localizar/criar o projeto da LP, mover
  para `clientes/<cliente>/lp-<cliente>/`, criar repo, workflow, secrets, primeiro deploy.
- **Ja possui projeto aqui** -> identificar o projeto existente (`clientes/<cliente>/lp-<cliente>/`)
  e seguir **Deploy recorrente** ou **Publicar uma pagina nova**, conforme o pedido.

Nao pular essa pergunta nem assumir o modo — perguntar sempre, mesmo que o contexto pareca obvio.

---

## Quando usar cada modo

| Situacao | Va para |
|---|---|
| Projeto novo, ainda sem deploy automatico | **Setup (primeira vez)** |
| Repo + Action ja existem, so quero publicar mudancas | **Deploy recorrente** |
| Deploy falhou / quero ver status | **Monitorar deploy** |

Ler `references/setup.md` para o passo a passo detalhado e troubleshooting.

---

## Organizacao e estrutura

### Onde o projeto fica no workspace
Cada projeto de LP e um **repo git proprio aninhado dentro da pasta do cliente**, em
`clientes/<cliente>/lp-<cliente>/` (ex.: `clientes/click-cirurgia/lp-click-cirurgia/`).
A pasta `clientes/` e ignorada pelo `.gitignore` do workspace Arttico justamente porque
esses projetos tem repo proprio — entao nao ha conflito de repos aninhados.

### Estrutura interna: monorepo (uma subpasta por pagina)
O repo da LP e um **monorepo**: cada pagina fica na sua propria subpasta, com seu build e
seu deploy. Ex.: `lp-click-cirurgia/vesicula/`, e no futuro `lp-click-cirurgia/hernia/`.
Na raiz do repo ficam so `.github/` e `.gitignore`.

```
lp-<cliente>/
├── .github/workflows/deploy.yml   (paths-filter + 1 job por pagina)
├── .gitignore
├── <pagina-1>/    (ex.: vesicula/  -> projeto Vite completo: src/, public/, package.json...)
└── <pagina-2>/    (ex.: hernia/)
```

O workflow usa **`dorny/paths-filter`** (cada pagina so e deployada quando os arquivos da SUA
subpasta mudam) + **`working-directory: ./<pagina>`** nos steps de build. Assim, mexer numa
pagina nao re-deploya as outras.

- **Uma pagina so:** pode usar `templates/deploy.yml` (workflow simples).
- **Duas ou mais paginas (monorepo):** usar `templates/deploy-monorepo.yml` (com paths-filter).

Para **adicionar uma nova pagina** a um repo existente: criar a subpasta com o projeto, e no
workflow adicionar um filtro em `changes` + um job `deploy-<pagina>` espelhando o existente.

---

## Setup (primeira vez)

Objetivo: transformar um projeto local em um repo com deploy FTP automatico.

### 1. Conferir o build do projeto
Descobrir o comando de build e a **pasta de saida**:
- Vite/React/Vue: `npm run build` -> `dist/`
- Astro: `npm run build` -> `dist/`
- Next export / HTML puro: ajustar conforme o caso

Se o `package.json` foi editado (deps adicionadas/removidas), **regenerar o lockfile** com
`npm install` e commitar o `package-lock.json` — o workflow usa `npm ci`, que e estrito e
falha se `package.json` e `package-lock.json` estiverem dessincronizados.

### 2. Inicializar git e commitar (se ainda nao for repo)
```bash
git init -b main
# garantir .gitignore com: node_modules/, dist/, .env*  (!.env.example)
git add -A
git commit -m "Setup inicial"
```
**Conferir antes de commitar** que nada sensivel entrou: `.env`, `node_modules/`, chaves.
`.env.example` (so placeholders) pode ser versionado.

### 3. Criar o repositorio no GitHub
- Se o `gh` CLI estiver disponivel: `gh repo create <nome> --private --source=. --remote=origin`
- Senao: pedir ao usuario para criar um repo **vazio** (sem README/gitignore/license) e informar a URL.

Para descobrir o usuario/owner do GitHub do cliente, checar o remote de outro repo:
`git -C <outro-projeto> remote -v`. Padrao de nome de repo de LP do usuario: `lp-<cliente>`.

### 4. Vincular e enviar
```bash
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin main
```
Se der "Repository not found", confirmar o nome exato listando os repos do usuario
(ver `references/setup.md` — usa `git credential fill` + API do GitHub).

### 5. Cadastrar os secrets FTP no repo
O usuario adiciona em **GitHub > repo > Settings > Secrets and variables > Actions**:

| Secret | Conteudo |
|---|---|
| `host_servidor` | host/IP do FTP (ex.: `ftp.cliente.com.br`) |
| `usuario_ftp` | usuario do FTP |
| `senha_ftp` | senha do FTP |

(Os nomes dos secrets sao convencao do usuario. Se mudar, ajustar no workflow.)

### 6. Adicionar o workflow
Copiar `templates/deploy.yml` para `.github/workflows/deploy.yml` do projeto e ajustar:
- `node-version` se necessario
- comando de build, se nao for `npm run build`
- `local-dir` = pasta de saida do build (ex.: `./dist/`)
- **`server-dir`** = pasta de destino no servidor FTP (ver REGRA DE SEGURANCA abaixo)

### 7. Confirmar o `server-dir` ANTES do primeiro deploy (critico)
Ver **Regras de seguranca**. So depois de confirmado, `git push` para disparar o deploy.

### 8. Monitorar
Rodar `scripts/check_deploy.py` para acompanhar o run ate concluir (ver Monitorar deploy).

---

## Deploy recorrente (dia a dia)

Repo + Action ja configurados. Para publicar uma mudanca:

```bash
git add -A
git commit -m "<descricao da mudanca>"
git push
```

O push dispara o Action automaticamente. Depois, monitorar (proxima secao).
Lembrar: se mexeu no `package.json`, rodar `npm install` e commitar o lockfile junto.

---

## Publicar uma pagina nova em subpasta (ex.: /catarata)

Caso de uso: subir uma LP nova numa **subpasta** do dominio, tipo
`clickcirurgia.com.br/catarata/`, reaproveitando o mesmo FTP/repo. Funciona **so com FTP**
porque a subpasta fica dentro do `public_html` (raiz web), entao o servidor ja serve
automaticamente — nao precisa de cPanel nem DNS. A `FTP-Deploy-Action` **cria a pasta no
servidor sozinha** no primeiro deploy.

> Diferenca importante:
> - **Subpasta** `dominio.com/catarata/` -> so FTP (este passo a passo). ✅
> - **Subdominio** `catarata.dominio.com/` -> precisa criar antes no cPanel (Subdomains) + DNS;
>   depois publica igual, apontando o `server-dir` pro document root do subdominio.

### Passo a passo

1. **Preparar o projeto da pagina.** Ter o projeto (Vite/React/HTML) que builda para `dist/`.
   Se for novo, criar normalmente (ou copiar uma pagina existente como base).

2. **Colocar como subpasta no repo da LP (monorepo).** Mover/criar o projeto em
   `lp-<cliente>/<pagina>/` (ex.: `lp-click-cirurgia/catarata/`). Na raiz do repo so ficam
   `.github/` e `.gitignore`.

3. **Adicionar o job no workflow.** Em `.github/workflows/deploy.yml`:
   - um filtro novo em `changes`:
     ```yaml
     catarata:
       - 'catarata/**'
     ```
   - um job `deploy-catarata` espelhando os existentes, trocando os caminhos:
     ```yaml
     deploy-catarata:
       needs: changes
       if: needs.changes.outputs.catarata == 'true'
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with:
             node-version: 20
             cache: npm
             cache-dependency-path: catarata/package-lock.json
         - run: npm ci
           working-directory: ./catarata
         - run: npm run build
           working-directory: ./catarata
         - uses: SamKirkland/FTP-Deploy-Action@v4.3.5
           with:
             server: ${{ secrets.host_servidor }}
             username: ${{ secrets.usuario_ftp }}
             password: ${{ secrets.senha_ftp }}
             port: 21
             protocol: ftp
             local-dir: ./catarata/dist/
             server-dir: ./catarata/        # FTP abre no public_html -> cria public_html/catarata/
             timeout: 120000
             dangerous-clean-slate: false
             exclude: |
               **/.htaccess
     ```

4. **Conferir o `server-dir`.** Se o FTP abre **dentro** do `public_html` -> `./catarata/`.
   Se abre **acima** -> `/public_html/catarata/`. (Ver Regra do public_html em `references/setup.md`.)

5. **Commit + push.** O `paths-filter` detecta a `catarata/` e dispara so esse job.
   A pasta no servidor e criada automaticamente.

6. **Monitorar e validar.**
   ```bash
   python scripts/check_deploy.py --watch
   curl -s "https://<dominio>/catarata/" | head -c 300
   ```
   No ar em `https://<dominio>/catarata/`.

---

## Monitorar deploy

```bash
python scripts/check_deploy.py            # status do run mais recente
python scripts/check_deploy.py --watch    # fica acompanhando ate concluir
```

O script descobre owner/repo pelo `git remote`, pega o token via Git Credential Manager
e consulta a API de Actions do GitHub. Em caso de falha, mostra a URL do run para ver os logs.

**O run verde NAO prova que o site mudou** — so prova que a action rodou. Um `server-dir`
errado (ex.: `/public_html/tqb/` numa conta FTP que ja abre dentro do `public_html`) sobe pra
uma pasta aninhada errada e o run fica verde do mesmo jeito. SEMPRE validar no site live:
```bash
export MSYS_NO_PATHCONV=1
curl -s -I "<URL_DO_SITE>" | grep -i last-modified   # Last-Modified tem que ser de agora
curl -s "<URL_DO_SITE>" | head -c 500                # confere se o conteudo novo subiu
```
Para SPA, confirmar que o bundle com hash novo esta no ar (ver "Validar deploy de verdade" em
`references/setup.md`). Se o site nao mudou, quase sempre e o `server-dir` com `/public_html/`
duplicado — ver a "ARMADILHA CRITICA" em `references/setup.md`.

---

## Regras de seguranca

1. **Confirmar o `server-dir` antes do primeiro deploy.** A FTP-Deploy-Action **sincroniza e
   APAGA** arquivos do servidor que nao existem no build. Se a pasta apontar para a raiz errada,
   pode danificar o site. Perguntar ao usuario: *"O FTP entra na raiz do site ou direto na pasta
   da pagina?"*
   - Entra na raiz (public_html) -> `server-dir: <subpasta-da-pagina>/` (relativo, SEM `/public_html/`)
   - Entra direto na pasta -> `server-dir: ./`
   - **NUNCA** por `/public_html/...` se a conta ja abre no public_html: vira
     `public_html/public_html/...`, o run fica VERDE mas o site nao muda (bug silencioso).
2. **Preservar arquivos do servidor** que nao vem do build: manter `**/.htaccess` (e similares)
   no `exclude` do workflow.
3. **Nunca commitar segredos.** `.env*` no `.gitignore`. Secrets FTP so como GitHub Secrets,
   nunca no codigo nem no workflow em texto.
4. **Nunca expor o token** ao usar `git credential fill` — capturar em variavel, nunca imprimir.
5. **Lockfile em dia.** Se `package.json` mudou, `npm install` + commit do `package-lock.json`
   antes do push, senao o `npm ci` do Action falha.
6. **Confirmar antes de publicar em producao** quando a mudanca for grande ou o site estiver no ar.

---

## Arquivos da skill

| Arquivo | Uso |
|---|---|
| `templates/deploy.yml` | Workflow simples — projeto com **uma** pagina (build na raiz) |
| `templates/deploy-monorepo.yml` | Workflow **monorepo** — uma subpasta por pagina (paths-filter + working-directory) |
| `scripts/check_deploy.py` | Verifica status do run mais recente do Action |
| `references/setup.md` | Passo a passo detalhado, descoberta de owner/repo, troubleshooting |
