# Como Configurar — GTM Setup Automático

## 1. Instalar dependências

```bash
cd .claude/skills/gtm-setup/scripts
pip install -r requirements.txt
playwright install chromium
```

## 2. Configurar credenciais Google (uma vez só)

### 2.1 Criar projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com
2. Crie um novo projeto (ex: `arttico-automacoes`)
3. Ative a **Tag Manager API**:
   - Menu lateral → APIs e Serviços → Biblioteca
   - Busque "Tag Manager API" → Ativar

### 2.2 Criar credencial OAuth 2.0

1. APIs e Serviços → **Credenciais** → Criar credenciais → **ID do cliente OAuth 2.0**
2. Tipo: **Aplicativo de computador**
3. Baixe o arquivo JSON
4. Renomeie para `credentials.json`
5. Coloque em: `.claude/skills/gtm-setup/credentials/credentials.json`

### 2.3 Adicionar usuário de teste (se necessário)

Se o projeto estiver em modo de teste, adicione seu email em:
APIs e Serviços → Tela de permissão OAuth → Usuários de teste

## 3. Encontrar o ID da conta GTM

1. Acesse tagmanager.google.com
2. O ID da conta aparece na URL: `accounts/**1234567**/containers/...`

## 4. Primeira execução

```bash
python setup_gtm.py
```

Na primeira vez, o navegador abrirá pedindo autorização Google. Autorize e o token será salvo automaticamente para próximas execuções.

## Estrutura de arquivos

```
gtm-setup/
├── credentials/
│   ├── credentials.json    ← você coloca aqui
│   └── token.pickle        ← gerado automaticamente
├── scripts/
│   ├── setup_gtm.py        ← ponto de entrada
│   ├── auth.py
│   ├── gtm_web.py
│   ├── gtm_server.py
│   └── stape.py
└── COMO_CONFIGURAR.md
```

## Observações

- **Stape:** O script abre o Chromium visível. Se os seletores não baterem com a UI atual do Stape, o script avisa e pausa para você completar manualmente.
- **Facebook CAPI (server):** Se a tag não for criada automaticamente (template da comunidade), o script avisa com o Pixel ID para você adicionar manualmente via Galeria de Templates.
- **DNS:** Após o setup, crie o registro CNAME `stape.{domínio}` apontando para o endereço fornecido pelo Stape.
