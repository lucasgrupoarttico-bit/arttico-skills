# PageSpeed Fixes — Referência de Correções

Base de conhecimento para o plano de ação do `/pagespeed pagespeed`.
Carregar este arquivo antes de gerar qualquer plano de ação.

---

## 🔴 Críticos — Maior impacto em Performance

### 1. Imagens sem dimensões (Cumulative Layout Shift)
**Oportunidade PageSpeed:** "Image elements do not have explicit width and height"
**Impacto:** CLS alto (layout shift), penaliza Core Web Vitals
**Fix:**
```html
<!-- ❌ Errado -->
<img src="banner.jpg" alt="Banner">

<!-- ✅ Correto -->
<img src="banner.jpg" alt="Banner" width="1200" height="600">
```
Para imagens responsivas com CSS `width: 100%`, definir `aspect-ratio` no CSS:
```css
img { aspect-ratio: 2 / 1; width: 100%; height: auto; }
```

---

### 2. Imagens não otimizadas / sem formato moderno
**Oportunidade PageSpeed:** "Serve images in next-gen formats" / "Properly size images"
**Impacto:** 200ms–2s de economia
**Fix:**
```html
<!-- ✅ WebP com fallback -->
<picture>
  <source srcset="imagem.webp" type="image/webp">
  <img src="imagem.jpg" alt="Descrição" width="800" height="400">
</picture>
```
Conversão em lote (linha de comando):
```bash
# Instalar: brew install imagemagick (Mac) ou apt install imagemagick (Linux)
find . -name "*.jpg" -exec convert {} -quality 85 {}.webp \;
find . -name "*.png" -exec convert {} -quality 85 {}.webp \;
```

---

### 3. Imagens acima do fold sem preload / LCP sem prioridade
**Oportunidade PageSpeed:** "Largest Contentful Paint element" com tempo alto
**Impacto:** LCP alto — maior impacto no score de performance
**Fix:**
```html
<!-- No <head>: preload da imagem LCP -->
<link rel="preload" as="image" href="imagem-principal.webp" fetchpriority="high">

<!-- Na tag img: NÃO usar lazy loading no LCP -->
<img src="imagem-principal.webp" alt="..." fetchpriority="high" loading="eager">

<!-- Imagens abaixo do fold: usar lazy -->
<img src="imagem-secundaria.webp" alt="..." loading="lazy">
```

---

### 4. Render-blocking resources (CSS e JS bloqueando renderização)
**Oportunidade PageSpeed:** "Eliminate render-blocking resources"
**Impacto:** 300ms–1s de economia
**Fix para JavaScript:**
```html
<!-- ❌ Errado — bloqueia renderização -->
<script src="app.js"></script>

<!-- ✅ Defer — executa após HTML, mantém ordem -->
<script src="app.js" defer></script>

<!-- ✅ Async — executa assim que carrega, sem ordem garantida -->
<script src="analytics.js" async></script>
```
**Fix para CSS não crítico:**
```html
<!-- Técnica: carregar CSS como print, depois trocar para all -->
<link rel="stylesheet" href="nao-critico.css" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="nao-critico.css"></noscript>
```

---

### 5. CSS não utilizado (Unused CSS)
**Oportunidade PageSpeed:** "Reduce unused CSS"
**Impacto:** 100ms–500ms de economia
**Fix:**
- Usar PurgeCSS para remover classes não utilizadas:
```bash
npm install -D purgecss
npx purgecss --css styles.css --content index.html --output styles.purged.css
```
- Para WordPress: plugin Asset CleanUp ou WP Rocket
- Para Tailwind: configurar `purge` no `tailwind.config.js`
```js
module.exports = {
  content: ['./src/**/*.{html,js}'],
  // purge automático no build
}
```

---

### 6. JavaScript não utilizado (Unused JavaScript)
**Oportunidade PageSpeed:** "Reduce unused JavaScript"
**Impacto:** 200ms–1s de economia
**Fix:**
- Verificar quais scripts são desnecessários (ex: jQuery se não usar)
- Code splitting se usar bundler:
```js
// Lazy load de componente React
const Component = React.lazy(() => import('./Component'));
```
- Para WordPress: desativar scripts de plugins inativos via functions.php

---

### 7. Fontes sem font-display swap
**Oportunidade PageSpeed:** "Ensure text remains visible during webfont load"
**Impacto:** FOIT (Flash of Invisible Text), penaliza LCP e CLS
**Fix:**
```css
@font-face {
  font-family: 'MinhaFonte';
  src: url('fonte.woff2') format('woff2');
  font-display: swap; /* ← Isso aqui */
}
```
Para Google Fonts, adicionar `&display=swap` na URL:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
```

---

### 8. Ausência de compressão (Gzip/Brotli)
**Oportunidade PageSpeed:** "Enable text compression"
**Impacto:** 50-80% de redução no tamanho dos arquivos transferidos
**Fix no .htaccess (Apache):**
```apache
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/css
  AddOutputFilterByType DEFLATE application/javascript application/json
  AddOutputFilterByType DEFLATE image/svg+xml
</IfModule>
```
**Fix no nginx.conf:**
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml;
gzip_min_length 1000;
```

---

### 9. Cache de assets estáticos
**Oportunidade PageSpeed:** "Serve static assets with an efficient cache policy"
**Impacto:** Acelera carregamentos subsequentes significativamente
**Fix no .htaccess:**
```apache
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
</IfModule>
```

---

## ⚠️ Importantes — Acessibilidade (meta: 100)

### 10. Imagens sem atributo alt
**Audit:** "Image elements do not have [alt] attributes"
**Fix:**
```html
<!-- ❌ Errado -->
<img src="foto.jpg">

<!-- ✅ Imagem com conteúdo -->
<img src="foto.jpg" alt="Lucas atendendo cliente no escritório">

<!-- ✅ Imagem decorativa (ignorada por leitores de tela) -->
<img src="decoracao.png" alt="" role="presentation">
```

### 11. Inputs sem label
**Audit:** "Form elements do not have associated labels"
**Fix:**
```html
<!-- ❌ Errado -->
<input type="email" placeholder="Seu email">

<!-- ✅ Label visível -->
<label for="email">Seu email</label>
<input type="email" id="email" placeholder="email@exemplo.com">

<!-- ✅ Label visualmente oculto (se design não permite label visível) -->
<label for="email" class="sr-only">Seu email</label>
<input type="email" id="email" placeholder="Seu email">
```
CSS para `.sr-only`:
```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  white-space: nowrap;
}
```

### 12. Contraste de cores insuficiente
**Audit:** "Background and foreground colors do not have a sufficient contrast ratio"
**Ratios mínimos:** Texto normal ≥ 4.5:1 | Texto grande (18px+) ≥ 3:1
**Ferramentas para checar:** https://webaim.org/resources/contrastchecker/
**Fix:** Escurecer cor do texto ou clarear o fundo até atingir o ratio mínimo.

### 13. Hierarquia de headings quebrada
**Audit:** "Heading elements are not in a sequentially-descending order"
**Fix:** Garantir que a ordem seja sempre h1 → h2 → h3 sem pular níveis.
Só deve haver UM h1 por página.

### 14. Links sem texto descritivo
**Audit:** "Links do not have a discernible name"
**Fix:**
```html
<!-- ❌ Errado -->
<a href="/contato"><img src="icone.png"></a>

<!-- ✅ Correto -->
<a href="/contato" aria-label="Ir para página de contato">
  <img src="icone.png" alt="Contato">
</a>
```

---

## 💡 SEO (meta: 100)

### 15. Meta description ausente ou muito longa
**Fix:**
```html
<meta name="description" content="Descrição clara do conteúdo da página em 120-160 caracteres. Inclui palavra-chave principal.">
```

### 16. Title tag ausente, duplicada ou muito longa
**Fix:**
```html
<title>Página Específica | Nome do Site</title>
<!-- Máximo: 60 caracteres -->
```

### 17. Links sem texto / anchor text genérico
**Audit:** "Links are not crawlable"
**Fix:** Substituir "clique aqui" por texto descritivo.

### 18. Robots.txt bloqueando indexação acidentalmente
**Verificar:** `https://seusite.com/robots.txt`
Nunca deve ter `Disallow: /` em produção.

### 19. Viewport meta tag ausente
**Fix:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

---

## Estimativas de ganho por fix

| Fix | Ganho médio no score |
|---|---|
| Otimizar imagem LCP + fetchpriority | +10 a +25 pontos |
| Converter imagens para WebP | +5 a +15 pontos |
| Remover render-blocking JS | +5 a +15 pontos |
| Ativar compressão Gzip/Brotli | +3 a +10 pontos |
| font-display: swap | +2 a +8 pontos |
| Cache de assets | +2 a +5 pontos |
| Remover CSS não utilizado | +3 a +10 pontos |

**Regra de ouro:** Corrigir o LCP sempre primeiro — é o maior peso no score de performance.
