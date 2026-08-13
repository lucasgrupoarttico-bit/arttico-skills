---
name: analise-concorrentes
description: >
  Analisa concorrentes diretos e indiretos nas principais plataformas.
  Verifica presença no Meta Ads e Google Ads. Detecta criativos validados (≥2 ads com mesmo criativo)
  no Meta Ad Library por nome de página e por palavra-chave. Analisa Instagram do concorrente direto
  e retorna posts com discrepância positiva de engajamento. Busca vídeos no TikTok por palavra-chave
  e retorna os com mais curtidas, compartilhamentos e visualizações.
  Gera sugestões de criativos, funis, palavras-chave Google, títulos/descrições Meta e headlines Google.
  Use quando o usuário disser "analisa concorrentes", "pesquisa os anúncios dos concorrentes",
  "o que os concorrentes estão fazendo", "benchmarking", ou similar.
---

# /analise-concorrentes — Análise de Concorrentes

## Dependências

- **Briefing do cliente:** `clientes/[cliente]/briefing.md`
- **Script:** `.claude/skills/analise-concorrentes/scripts/analise_concorrentes.py`
- **Python + Playwright instalados**

## Setup (primeira vez)

```powershell
pip install playwright
python -m playwright install chromium
```

---

## Fluxo

### Passo 1 — Ler briefing do cliente

Ler `clientes/[cliente]/briefing.md` para entender nicho, posicionamento e diferenciais.
Se o cliente não foi informado, perguntar antes de prosseguir.

### Passo 2 — Rodar o script

Avisar o usuário:

> "O browser vai abrir em modo visível. Se aparecer CAPTCHA ou pedido de login em qualquer plataforma, resolva manualmente e pressione Enter no terminal para continuar."

```powershell
cd ".claude\skills\analise-concorrentes\scripts"; python analise_concorrentes.py
```

O script coleta de forma interativa:
1. Nome do cliente e nicho
2. Dados de cada concorrente direto (nome, Facebook, website, Instagram)
3. Palavras-chave para busca no Meta Ad Library (concorrentes indiretos)
4. Palavras-chave para busca no TikTok

### Passo 3 — Ler os dados coletados

Após o script terminar, ler `clientes/[cliente]/concorrentes/[data]/analise.json`.
Verificar também os screenshots nas subpastas para análise visual dos criativos.

### Passo 4 — Gerar o relatório

Seguir a estrutura abaixo. Salvar em `clientes/[cliente]/concorrentes/[data]/relatorio.md`.

---

## O que o script coleta em cada plataforma

### Meta Ad Library — Concorrentes Diretos

Abre `facebook.com/ads/library` buscando pelo nome/URL da página do concorrente.
- Verifica se anuncia (sim/não) e estima o volume de anúncios ativos
- Detecta **criativos validados**: anúncios com a marcação "X anúncios usam esse criativo e esse texto" onde X ≥ 2
- Para cada criativo validado: tenta extrair URL da imagem (via CDN Meta) e URL do vídeo (via interceptação de rede)
- Retorna a URL da biblioteca para acesso direto

### Meta Ad Library — Busca por Keyword (Concorrentes Indiretos)

Mesmo processo, mas usando `search_type=keyword_unordered` em vez de busca por página.
Encontra criativos validados de anunciantes do nicho que não são concorrentes diretos listados.

### Google Ads Transparency

Abre `adstransparency.google.com/?region=BR&domain=[dominio]`.
- Verifica se o concorrente anuncia (sim/não)
- Extrai os títulos (headlines) e descrições dos anúncios de texto ativos
- Usa três estratégias em sequência: web components nativos do Google → shadow DOM recursivo → seletores por classe → fallback no texto bruto da página com heurística de tamanho de linha (headlines ≤ 35 chars, descriptions 36–110 chars)
- Retorna screenshot da página e a URL para acesso direto

### Instagram — Concorrentes Diretos

Visita o perfil e extrai os URLs dos posts do grid (até 15). Para cada post, navega até ele e coleta:
- Curtidas, visualizações (reels), comentários
- Calcula a mediana de engajamento do perfil
- Retorna apenas os posts com engajamento ≥ 2× a mediana como "destaque"

**Importante:** Instagram requer login com frequência. Se pedir, o browser pausa e aguarda o usuário resolver.

### TikTok — Busca por Keyword

Abre `tiktok.com/search/video?q=[keyword]`, scrolla e extrai os cards de vídeo:
- URL de cada vídeo
- Métricas visíveis (views, likes, comentários)
- Retorna os top 10 por keyword, ordenados por engajamento

---

## Estrutura do Relatório

### 1. Presença dos Concorrentes

Tabela resumo:

| Concorrente | Meta Ads | Google Ads | URL Meta | URL Google |
|-------------|----------|------------|----------|------------|
| [Nome]      | ✅ (≈X anúncios) / ❌ | ✅ / ❌ | [link] | [link] |

### 2. Anúncios Google Ads — Títulos e Descrições

Para cada concorrente que anuncia no Google, listar os anúncios extraídos:

**[Nome do Concorrente]**
- Títulos: [headline 1] | [headline 2] | [headline 3]
- Descrição: [description 1]
- Descrição: [description 2]

Repetir para cada anúncio encontrado. Identificar padrões recorrentes (CTA, proposta de valor, urgência).

### 3. Criativos Validados — Meta (Diretos)

Para cada concorrente que anuncia, listar os criativos com ≥ 2 ads:
- Texto do criativo (copy identificada)
- Imagem: URL da imagem se extraída, ou indicar "ver screenshot em [pasta]"
- Vídeo: URL se capturada, ou indicar "não extraído"
- Quantidade de ads usando aquele criativo

### 4. Criativos Validados — Meta (Indiretos por Keyword)

Mesmo formato. Indicar qual keyword gerou cada criativo encontrado.

### 5. Instagram — Posts com Discrepância Positiva

Para cada concorrente com dados coletados:
- Mediana de engajamento do perfil
- Posts com engajamento ≥ 2× a mediana:
  - URL do post
  - Tipo (reel/post)
  - Curtidas, visualizações, comentários
  - O que pode ter gerado a discrepância (tema, formato, hook)

### 6. TikTok — Vídeos em Destaque

Lista dos vídeos com mais engajamento encontrados nas buscas por keyword:
- URL do vídeo
- Keyword que gerou o resultado
- Views, likes, comentários estimados
- O que está funcionando (tema, formato, hook)

### 7. Padrões Identificados

- Copy: argumentos e ângulos recorrentes nos criativos validados
- Formato: o que os concorrentes estão testando mais (vídeo, estático, carrossel)
- Oferta de entrada: como estão convertindo (consulta grátis, WhatsApp, formulário)
- Hook visual: o que chama atenção nos criativos de destaque

### 8. Sugestões para [Cliente]

**A. 5 Ideias de Criativos**
Formato + hook diferenciado + ângulo que os concorrentes não estão usando + CTA.

**B. 2 Estruturas de Funil**
Entrada → Meio → Conversão. Justificar por que funciona para este nicho.

**C. 3 Palavras-chave Google Ads**
Uma por intenção: comercial, informacional, cauda longa.

**D. 5 Títulos + 5 Descrições — Meta Ads**
Título até 40 chars. Texto principal recomendado até 125 chars. Sem travessões.

**E. 5 Headlines — Google Ads RSA**
Cada headline até 30 chars. Cobrir: benefício, CTA, prova, urgência, diferencial.

---

## Regras

- Nunca copiar copy dos concorrentes — identificar o padrão e propor algo diferenciado
- Sempre ler o briefing do cliente antes de gerar sugestões (Passo 1)
- Se uma plataforma falhar (CAPTCHA não resolvido, bloqueio), registrar no relatório e continuar
- Quando imagem ou vídeo não for extraído, indicar o caminho do screenshot para referência visual
- Sem travessões em qualquer copy sugerida
- Se o cliente não anunciar no Google, entregar as 3 palavras-chave e os 5 headlines como insumo estratégico
