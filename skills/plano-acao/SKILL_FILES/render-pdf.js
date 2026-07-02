// Renderiza um deck da Arttico em PDF, uma página por slide, mantendo o fundo escuro
// e congelando as animações no estado final.
//   - Deck do Plano de Ação (16:9):      node render-pdf.js <html> <pdf>
//   - Deck de Criativos (folha vertical): node render-pdf.js <html> <pdf> 1080 1528
// Os dois últimos argumentos (largura/altura em px) são opcionais; padrão 1280x720.
const { chromium } = require('playwright');
const path = require('path');
const { pathToFileURL } = require('url');

(async () => {
  const htmlPath = process.argv[2];
  const pdfPath = process.argv[3];
  const W = parseInt(process.argv[4], 10) || 1280;
  const H = parseInt(process.argv[5], 10) || 720;
  if (!htmlPath || !pdfPath) {
    console.error('Uso: node render-pdf.js <html> <pdf> [largura] [altura]');
    process.exit(1);
  }

  const url = pathToFileURL(path.resolve(htmlPath)).href;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.goto(url, { waitUntil: 'networkidle' });

  // Congela o estado final das animações de entrada (senão slides ao fim da página
  // podem renderizar ainda em opacity:0).
  await page.addStyleTag({ content: '*,*::before,*::after{animation:none !important;opacity:1 !important;transform:none !important;}' });
  await page.waitForTimeout(300);

  await page.pdf({
    path: pdfPath, width: W + 'px', height: H + 'px',
    printBackground: true, margin: { top: '0', bottom: '0', left: '0', right: '0' },
  });

  await browser.close();
  console.log('PDF gerado: ' + pdfPath);
})().catch((err) => { console.error(err); process.exit(1); });
