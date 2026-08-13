---
name: yt-research
description: >
  Pesquisa vídeos no YouTube sobre um tema, alimenta o NotebookLM com os vídeos como fontes
  e retorna insights estruturados de mercado (dores, hooks, objeções, oportunidades de copy).
  Use quando o usuário pedir: "pesquisa no youtube sobre X", "busca vídeos de X", "pesquisa de mercado X",
  "o que o youtube fala sobre X", "analisa concorrentes de X no youtube".
---

# /yt-research — Pesquisa YouTube + NotebookLM

## Dependências

- `yt-dlp` — instalado em `C:\Users\Lucas Felipe\AppData\Local\Python\pythoncore-3.14-64\Scripts`
- `notebooklm` — instalado em `C:\Users\Lucas Felipe\AppData\Local\Python\pythoncore-3.14-64\Scripts`
- Script de busca: `~/.claude/skills/yt-search/scripts/search.py`

Incluir em todo comando Bash:
```
export PATH="$PATH:/c/Users/Lucas Felipe/AppData/Local/Python/pythoncore-3.14-64/Scripts"
```

---

## Parâmetros

- **query** — tema de busca (obrigatório)
- `--count N` — quantidade de vídeos (padrão: 5)
- `--months N` — filtro de data em meses (padrão: 6)
- `--no-date-filter` — sem filtro de data

---

## Fluxo

### 1. Buscar vídeos no YouTube

```bash
export PATH="$PATH:/c/Users/Lucas Felipe/AppData/Local/Python/pythoncore-3.14-64/Scripts" && python "/c/Users/Lucas Felipe/.claude/skills/yt-search/scripts/search.py" <query> --count <N>
```

Apresentar resultados ao usuário. Extrair todas as URLs no formato `https://youtube.com/watch?v=...`.

### 2. Criar notebook no NotebookLM

```bash
export PATH="$PATH:/c/Users/Lucas Felipe/AppData/Local/Python/pythoncore-3.14-64/Scripts" && notebooklm create "Pesquisa: <query>"
```

Capturar o `notebook_id` retornado no output. Em seguida:

```bash
export PATH="$PATH:/c/Users/Lucas Felipe/AppData/Local/Python/pythoncore-3.14-64/Scripts" && notebooklm use <notebook_id>
```

### 3. Adicionar vídeos como fontes

Para cada URL extraída no passo 1:

```bash
export PATH="$PATH:/c/Users/Lucas Felipe/AppData/Local/Python/pythoncore-3.14-64/Scripts" && notebooklm source add "<youtube_url>"
```

### 4. Perguntas estruturadas de pesquisa

```bash
export PATH="$PATH:/c/Users/Lucas Felipe/AppData/Local/Python/pythoncore-3.14-64/Scripts" && notebooklm ask "Quais são as principais dores e frustrações do público nesse nicho?"
```

```bash
export PATH="$PATH:/c/Users/Lucas Felipe/AppData/Local/Python/pythoncore-3.14-64/Scripts" && notebooklm ask "Quais hooks e ganchos de atenção são mais recorrentes nesses vídeos?"
```

```bash
export PATH="$PATH:/c/Users/Lucas Felipe/AppData/Local/Python/pythoncore-3.14-64/Scripts" && notebooklm ask "Quais objeções ao produto ou serviço aparecem com mais frequência?"
```

```bash
export PATH="$PATH:/c/Users/Lucas Felipe/AppData/Local/Python/pythoncore-3.14-64/Scripts" && notebooklm ask "Quais ângulos de copy e oportunidades de conteúdo você identifica a partir desses vídeos?"
```

### 5. Retornar ao usuário

Apresentar os insights organizados por categoria. Ao final, perguntar o que o usuário quer fazer com os insights:
- Gerar criativos
- Montar roteiro
- Estruturar oferta
- Análise de concorrente

---

## Skills de suporte

### `/yt-search` — Busca no YouTube

Script: `~/.claude/skills/yt-search/scripts/search.py`

```
/yt-search <query> [--count N] [--months N] [--no-date-filter]
```

| Flag | Padrão | Descrição |
|------|--------|-----------|
| `--count N` | 20 | Quantidade de vídeos |
| `--months N` | 6 | Filtrar últimos N meses |
| `--no-date-filter` | — | Sem filtro de data |

Retorna por vídeo: título, canal, inscritos, views, duração, data, link.

---

### `notebooklm` — NotebookLM CLI

Autenticado como `lucas.grupoarttico@gmail.com`.
Session salva em: `C:\Users\Lucas Felipe\.notebooklm\profiles\default\storage_state.json`

**Notebooks:**
```bash
notebooklm create "Nome"
notebooklm use <notebook_id>
```

**Fontes:**
```bash
notebooklm source add "<url_ou_arquivo>"
```

**Chat:**
```bash
notebooklm ask "pergunta"
notebooklm ask --prompt-file ./pergunta.txt
```

**Gerar conteúdo:**
```bash
notebooklm generate audio "instrução" --wait
notebooklm generate video --style whiteboard --wait
notebooklm generate cinematic-video "instrução" --wait
notebooklm generate quiz --difficulty hard
notebooklm generate flashcards --quantity more
notebooklm generate slide-deck
notebooklm generate infographic --orientation portrait
notebooklm generate mind-map
notebooklm generate data-table "instrução"
```

**Download:**
```bash
notebooklm download audio ./podcast.mp3
notebooklm download video ./video.mp4
notebooklm download cinematic-video ./doc.mp4
notebooklm download quiz --format markdown ./quiz.md
notebooklm download flashcards --format json ./cards.json
notebooklm download slide-deck ./slides.pdf
notebooklm download infographic ./infografico.png
notebooklm download mind-map ./mapa.json
notebooklm download data-table ./tabela.csv
```
