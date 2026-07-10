// Extrai um frame de capa (poster) de vídeos mp4/H.264 usando o Chrome/Edge do SISTEMA,
// que tem os codecs proprietários (o Chromium do Playwright não decodifica H.264).
// Salva thumb_<nome>.jpg na pasta de saída, para usar como arte clicável no deck do plano.
//
// Uso:
//   node extract-video-thumbs.js <marcaDir> <outDir> [video1.mp4 video2.mp4 ...]
//   - Sem lista de vídeos: processa todos os .mp4 de <marcaDir>.
//   - <outDir> normalmente é clientes/<cliente>/plano-acao/assets
//
// Requisitos: Playwright instalado no projeto e Google Chrome (ou Edge) instalado no Windows.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');

(async () => {
  const marcaDir = process.argv[2];
  const outDir = process.argv[3];
  if (!marcaDir || !outDir) {
    console.error('Uso: node extract-video-thumbs.js <marcaDir> <outDir> [video1.mp4 ...]');
    process.exit(1);
  }
  let videos = process.argv.slice(4);
  if (videos.length === 0) {
    videos = fs.readdirSync(marcaDir).filter((f) => /\.mp4$/i.test(f));
  }
  fs.mkdirSync(outDir, { recursive: true });

  // Página-sonda DENTRO da pasta marca -> vídeos ficam same-origin (file://) na mesma pasta.
  const probe = path.join(marcaDir, '_probe.html');
  fs.writeFileSync(probe, '<!doctype html><meta charset="utf-8"><body>');

  const args = ['--allow-file-access-from-files', '--disable-web-security'];
  let browser;
  for (const ch of ['chrome', 'msedge']) {
    try { browser = await chromium.launch({ channel: ch, args }); console.error('Browser: ' + ch); break; }
    catch (e) { console.error('Falhou canal ' + ch); }
  }
  if (!browser) { console.error('Nenhum Chrome/Edge disponivel no sistema'); process.exit(2); }

  const page = await browser.newPage();
  await page.goto(pathToFileURL(path.resolve(probe)).href);

  for (const v of videos) {
    const r = await page.evaluate(async (name) => new Promise((res) => {
      const vid = document.createElement('video');
      vid.muted = true; vid.preload = 'auto'; vid.src = name;
      let done = false; const fin = (x) => { if (!done) { done = true; res(x); } };
      vid.addEventListener('error', () => fin({ ok: false, err: 'load ' + (vid.error && vid.error.code) }));
      vid.addEventListener('loadeddata', () => {
        const t = Math.min(1.0, (vid.duration || 2) * 0.25);
        vid.currentTime = isFinite(t) ? t : 0.2;
      });
      vid.addEventListener('seeked', () => {
        try {
          const c = document.createElement('canvas');
          c.width = vid.videoWidth; c.height = vid.videoHeight;
          if (!c.width || !c.height) return fin({ ok: false, err: 'no-dimensions' });
          c.getContext('2d').drawImage(vid, 0, 0, c.width, c.height);
          fin({ ok: true, data: c.toDataURL('image/jpeg', 0.82), w: c.width, h: c.height });
        } catch (e) { fin({ ok: false, err: String(e) }); }
      });
      setTimeout(() => fin({ ok: false, err: 'timeout' }), 20000);
    }), v);

    if (r.ok) {
      const out = path.join(outDir, 'thumb_' + v.replace(/\.mp4$/i, '') + '.jpg');
      fs.writeFileSync(out, Buffer.from(r.data.replace(/^data:image\/jpeg;base64,/, ''), 'base64'));
      console.log('OK    ' + v + '  (' + r.w + 'x' + r.h + ')');
    } else {
      console.log('FALHA ' + v + '  -> ' + r.err);
    }
  }

  fs.unlinkSync(probe);
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
