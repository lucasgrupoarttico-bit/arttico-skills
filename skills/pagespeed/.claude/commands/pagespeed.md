# /pagespeed pagespeed

Analisa o PageSpeed Insights do site de um cliente, cria plano de ação priorizado e
implementa as correções nos arquivos do site para atingir 90+ performance e 100 de
acessibilidade/SEO.

## REGRA CRÍTICA

Antes de qualquer análise, ler `references/pagespeed-fixes.md` para ter as soluções
prontas. Isso garante que o plano de ação seja específico e acionável.

## Dois modos de entrada

**Modo visual** (usuário envia screenshot ou PDF):
- Claude analisa a imagem com visão
- Extrai scores, Core Web Vitals e lista de oportunidades
- Não usa scripts Python

**Modo API** (usuário fornece URL):
- Claude chama o script Python para obter dados completos
- Mais preciso: inclui economias em ms para cada oportunidade

Se o usuário não especificar, SEMPRE perguntar:
> "Você quer me enviar um print do PageSpeed, ou prefere que eu consulte a API diretamente com a URL do site?"

## Instruções para execução

### PASSO 0 — Identificar cliente, modo e design

1. Ler `contas.yaml` da skill
2. Se houver mais de um cliente, perguntar qual
3. Perguntar estratégia: **mobile** (padrão e mais importante) ou **desktop**
4. Definir modo: **visual** (print/PDF) ou **API** (URL)
5. Perguntar qual design para o relatório HTML:
   > "Qual design para o relatório? **Padrão**, **Futurista** ou **Minimalista**?"

   Se o usuário não especificar, usar **Futurista** como padrão.

---

## Designs disponíveis para o relatório HTML

### PADRÃO — design Arttico (identidade da marca)
```css
:root {
  --bg: #00002c; --bg-card: #0a0a3d; --bg-card-2: #0f0f4d;
  --text: #ffffff; --text-muted: rgba(255,255,255,0.50);
  --border: rgba(255,255,255,0.07); --radius: 12px;
  --shadow: 0 4px 24px rgba(0,0,0,0.30);
  --font-title: 'Montserrat', sans-serif; --font-body: 'Inter', sans-serif;
  --green: #22c55e; --amber: #f59e0b; --red: #ef4444; --blue: #6366f1;
  --green-bg: rgba(34,197,94,0.10); --amber-bg: rgba(245,158,11,0.10);
  --red-bg: rgba(239,68,68,0.10); --blue-bg: rgba(99,102,241,0.10);
}
/* Fonts: Montserrat 400;600;800 + Inter 400;500;600 */
/* Segue o design-guide da Arttico: #00002c, cards #0a0a3d, sem bordas visíveis */
/* Estética: alto padrão, espaço negativo, Montserrat ExtraBold nos títulos */
```

### FUTURISTA — sci-fi / tech
```css
:root {
  --bg: #050508; --bg-card: #0d0d14; --bg-card-2: #12121c;
  --text: #e2e8f0; --text-muted: rgba(226,232,240,0.45);
  --border: rgba(99,255,220,0.08); --radius: 8px;
  --shadow: 0 0 20px rgba(99,255,220,0.04), 0 4px 24px rgba(0,0,0,0.6);
  --font-title: 'Space Grotesk', monospace; --font-body: 'Space Grotesk', monospace;
  --green: #00ffaa; --amber: #ffcc00; --red: #ff4466; --blue: #00ccff;
  --green-bg: rgba(0,255,170,0.07); --amber-bg: rgba(255,204,0,0.07);
  --red-bg: rgba(255,68,102,0.07); --blue-bg: rgba(0,204,255,0.07);
}
/* Fonts: Space Grotesk 400;500;700 (Google Fonts) */
/* Estética: preto profundo, glow sutil em verde/ciano, monospace, sci-fi */
/* Cards: borda 1px com cor do status em opacity baixa */
/* Score numbers: cor néon da status com text-shadow glow */
/* Section labels: prefixo "// " antes do texto */
```

### MINIMALISTA — clean / editorial
```css
:root {
  --bg: #ffffff; --bg-card: #ffffff; --bg-card-2: #fafafa;
  --text: #18181b; --text-muted: #a1a1aa;
  --border: #e4e4e7; --radius: 4px;
  --shadow: none;
  --font-title: 'DM Sans', sans-serif; --font-body: 'DM Sans', sans-serif;
  --green: #15803d; --amber: #92400e; --red: #991b1b; --blue: #1e3a8a;
  --green-bg: #f0fdf4; --amber-bg: #fffbeb; --red-bg: #fff1f2; --blue-bg: #eff6ff;
}
/* Fonts: DM Sans 400;500;700 (Google Fonts) */
/* Estética: branco total, zero sombras, bordas finas, muito espaço */
/* Cards: só borda 1px solid var(--border), sem background diferente */
/* Score numbers: cor da status, fonte menor sem ExtraBold */
/* Section labels: font-weight 400, sem uppercase, apenas linha fina acima */
/* Plano de ação: lista com linha separadora, sem card/box */
```

---

### PASSO 1A — Modo visual: ler screenshot/PDF

O usuário já enviou ou vai enviar o print. Extrair:

```
SCORES:
- Performance:    XX/100
- Acessibilidade: XX/100
- Boas Práticas:  XX/100
- SEO:            XX/100

CORE WEB VITALS:
- LCP (Largest Contentful Paint): X.Xs  [BOM/MELHORIA/RUIM]
- FID/TBT (Total Blocking Time):  XXXms [BOM/MELHORIA/RUIM]
- CLS (Cumulative Layout Shift):  0.XX  [BOM/MELHORIA/RUIM]
- FCP (First Contentful Paint):   X.Xs  [BOM/MELHORIA/RUIM]
- Speed Index:                    X.Xs
- TTI (Time to Interactive):      X.Xs

OPORTUNIDADES (do maior para menor economia):
1. [nome] — economia estimada: Xms
2. [nome] — economia estimada: Xms
...

DIAGNÓSTICOS (passa/falha):
- [nome]: FALHA
- [nome]: FALHA
...
```

### PASSO 1B — Modo API: chamar script Python

```bash
python3 ~/.claude/skills/pagespeed/scripts/pagespeed_api.py analyze \
  --url "URL_DO_CLIENTE" \
  --strategy mobile \
  --api-key "CHAVE_SE_TIVER"
```

Interpretar o JSON retornado e montar o mesmo resumo estruturado acima.

### PASSO 2 — Classificar situação atual

Para cada score, classificar:

| Score | Classificação |
|---|---|
| 90-100 | ✅ BOM |
| 50-89  | ⚠️ MELHORIA NECESSÁRIA |
| 0-49   | 🔴 CRÍTICO |

Para Core Web Vitals, usar os thresholds do Google:

| Métrica | BOM | MELHORIA | RUIM |
|---|---|---|---|
| LCP | ≤2.5s | ≤4.0s | >4.0s |
| FID/INP | ≤200ms | ≤500ms | >500ms |
| CLS | ≤0.1 | ≤0.25 | >0.25 |
| FCP | ≤1.8s | ≤3.0s | >3.0s |
| TBT | ≤200ms | ≤600ms | >600ms |

### PASSO 3 — Criar plano de ação

Ler `references/pagespeed-fixes.md` e cruzar com as oportunidades encontradas.

O plano de ação DEVE:
1. Ter no máximo 10 itens
2. Ser ordenado por impacto (maior economia de tempo primeiro)
3. Para cada item: qual é o problema, qual é a solução técnica, e quanto de impacto tem
4. Separar por categoria: CRÍTICO (bloqueia os 90+) → IMPORTANTE → OPCIONAL

**Formato do plano:**

```
═══════════════════════════════════════════════════════════
 PAGESPEED — {CLIENTE} ({ESTRATÉGIA})
 Data: {DATA}
═══════════════════════════════════════════════════════════

 SCORES ATUAIS
─────────────────────────────────────────────────────────
 Performance:    XX/100  🔴 CRÍTICO   → meta: 90+
 Acessibilidade: XX/100  ✅ BOM
 Boas Práticas:  XX/100  ⚠️ MELHORIA  → meta: 100
 SEO:            XX/100  ✅ BOM

 CORE WEB VITALS
─────────────────────────────────────────────────────────
 LCP:  X.Xs  ⚠️ MELHORIA (meta: ≤2.5s)
 TBT:  XXms  ✅ BOM
 CLS:  0.XX  ✅ BOM
 FCP:  X.Xs  🔴 CRÍTICO (meta: ≤1.8s)

 PLANO DE AÇÃO (ordenado por impacto)
─────────────────────────────────────────────────────────

 🔴 CRÍTICO — Sem isso não chega em 90+

 1. [TÍTULO] — impacto: ~XXXms
    Problema: [o que está errado]
    Solução:  [o que fazer tecnicamente]
    Arquivo:  [qual arquivo editar, se aplicável]

 2. [TÍTULO] — impacto: ~XXXms
    Problema: [o que está errado]
    Solução:  [o que fazer tecnicamente]

 ⚠️ IMPORTANTE — Grandes ganhos com esforço médio

 3. [TÍTULO] — impacto: ~XXms
    ...

 💡 OPCIONAL — Polimento final

 6. [TÍTULO]
    ...

═══════════════════════════════════════════════════════════
```

### PASSO 4 — Perguntar se implementa

Após o plano, SEMPRE perguntar:
> "Quer que eu implemente essas correções diretamente nos arquivos do site? Se sim, me diga onde os arquivos estão (ou abre a pasta do projeto)."

### PASSO 5 — Implementar correções (se autorizado)

O usuário deve fornecer:
- Caminho para os arquivos HTML/CSS/JS do site
- Ou framework usado (WordPress, Next.js, etc.)

Para cada item do plano de ação, implementar usando Edit ou Write.

**Prioridades obrigatórias para 90+ performance:**

1. **Imagens**: converter para WebP, adicionar `loading="lazy"`, definir `width` e `height`
2. **Render-blocking**: mover scripts para o final do body ou usar `defer`/`async`
3. **CSS não usado**: remover ou adiar CSS crítico via `<link media="print">`
4. **LCP**: garantir que o elemento LCP tem `fetchpriority="high"` e não é lazy
5. **Fonts**: usar `font-display: swap` e preload das fonts usadas above-the-fold
6. **Cache**: adicionar headers de cache para assets estáticos

**Para 100 de acessibilidade:**
- Todos os `<img>` devem ter `alt` descritivo
- Todos os `<input>` devem ter `<label>` associado
- Contraste de cores: verificar e corrigir
- Hierarquia de headings: h1 → h2 → h3 sem pular

**Para 100 de SEO:**
- `<title>` único e descritivo (50-60 chars)
- `<meta name="description">` (120-160 chars)
- Tags `hreflang` se site multilíngue
- Sitemap acessível
- Não bloquear indexação com noindex acidental

### PASSO 6 — Validar resultado

Após implementar, SEMPRE sugerir:
> "Recomendo rodar o PageSpeed novamente para validar as melhorias. Quer que eu rode a API agora?"

Se o usuário aceitar, rodar o script novamente e comparar os scores.

## Regras importantes

- Nunca implementar sem pedir confirmação antes
- Se o site é WordPress, WordPress.com ou SaaS (Wix, Squarespace), avisar que algumas otimizações dependem de plugin ou plano pago
- Se LCP estiver acima de 4s, priorizar isso acima de tudo — é o maior impacto
- Não inventar melhorias que não aparecem no PageSpeed — focar no que está listado
- Se o score já está 90+, confirmar e perguntar se quer focar em acessibilidade/SEO
