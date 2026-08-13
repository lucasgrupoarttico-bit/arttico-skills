"""
Análise de Concorrentes v2 — Arttico

Fase 1 — Concorrentes diretos:
  - Meta Ad Library: verifica presença, detecta criativos validados (≥2 ads), extrai imagem/vídeo
  - Google Ads Transparency: verifica presença, retorna URL
  - Instagram: visita cada post, mede engajamento, retorna URLs com discrepância positiva

Fase 2 — Busca por keyword no Meta Ad Library:
  - Encontra criativos validados de concorrentes indiretos

Fase 3 — Busca por keyword no TikTok:
  - Retorna URLs dos vídeos com mais engajamento
"""

import asyncio
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout


# ─── Helpers ──────────────────────────────────────────────────────────────────

def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        val = input(f"{prompt}{suffix}: ").strip()
    except EOFError:
        return default
    return val if val else default


def ask_bool(prompt: str, default: bool = False) -> bool:
    hint = "S/n" if default else "s/N"
    try:
        val = input(f"{prompt} [{hint}]: ").strip().lower()
    except EOFError:
        return default
    if not val:
        return default
    return val in ("s", "sim", "y", "yes")


def sep(title: str = ""):
    line = "─" * 58
    if title:
        print(f"\n{line}\n  {title}\n{line}")
    else:
        print(f"\n{line}")


async def safe_shot(page, path: Path) -> str | None:
    try:
        await page.screenshot(path=str(path), full_page=False)
        return str(path)
    except Exception:
        return None


async def scroll_load(page, scrolls: int = 5, delay: int = 1800):
    for _ in range(scrolls):
        await page.evaluate("window.scrollBy(0, window.innerHeight * 0.85)")
        await page.wait_for_timeout(delay)


def slugify(text: str) -> str:
    """Remove acentos e caracteres especiais para nomes de pasta."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^\w]", "_", ascii_text.lower()).strip("_")


def parse_count(text: str) -> int:
    """Converte '1.2K', '500', '1M' para inteiro."""
    if not text:
        return 0
    text = str(text).strip().replace(",", ".").upper()
    try:
        if text.endswith("M"):
            return int(float(text[:-1]) * 1_000_000)
        if text.endswith("K"):
            return int(float(text[:-1]) * 1_000)
        digits = re.sub(r"[^\d]", "", text)
        return int(digits) if digits else 0
    except (ValueError, TypeError):
        return 0


# ─── Interceptor de Vídeos ────────────────────────────────────────────────────

class VideoInterceptor:
    """Captura URLs de vídeo nas respostas de rede do Playwright."""

    def __init__(self):
        self.urls: list[str] = []

    def _handler(self, response):
        url = response.url
        ct = response.headers.get("content-type", "")
        if "video/mp4" in ct or ".mp4" in url or "video.f" in url:
            if url not in self.urls:
                self.urls.append(url)

    def attach(self, page):
        page.on("response", self._handler)

    def detach(self, page):
        try:
            page.remove_listener("response", self._handler)
        except Exception:
            pass

    def get(self) -> list[str]:
        return list(self.urls)

    def reset(self):
        self.urls.clear()


# ─── JS: detecta criativos validados no Meta Ad Library ──────────────────────

_META_VALIDATED_JS = """
() => {
    const results = [];
    const seen = new Set();
    // Padrão: "X anúncios usam esse criativo e esse texto" (≥ 2)
    const pat = /(\\d+)\\s+anúncios?\\s+usam\\s+esse/i;

    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);

    while (walker.nextNode()) {
        if (results.length >= 20) break;
        const raw = walker.currentNode.textContent || '';
        const m = pat.exec(raw);
        if (!m) continue;
        const count = parseInt(m[1]);
        if (count < 2) continue;

        // Sobe na árvore até achar o container do card
        let el = walker.currentNode.parentElement;
        for (let i = 0; i < 10 && el; i++) {
            const r = el.getBoundingClientRect();
            if (r.height > 150 && r.width > 200) break;
            el = el.parentElement;
        }
        if (!el) continue;

        const snippet = (el.innerText || raw).slice(0, 60);
        if (seen.has(snippet)) continue;
        seen.add(snippet);

        const imgs = Array.from(el.querySelectorAll('img'))
            .map(i => i.src)
            .filter(s => s && s.startsWith('http') && !s.startsWith('data:'));

        const videos = Array.from(el.querySelectorAll('video'))
            .map(v => v.src || v.currentSrc || (v.querySelector('source') || {}).src || '')
            .filter(Boolean);

        results.push({
            count,
            texto: (el.innerText || raw).trim().slice(0, 700),
            imagens: imgs.slice(0, 3),
            videos: videos.slice(0, 2),
        });
    }
    return results;
}
"""


# ─── Meta Ad Library ──────────────────────────────────────────────────────────

async def check_meta_competitor(page, fb_identifier: str, comp_dir: Path, iv: VideoInterceptor) -> dict:
    """Verifica se o concorrente anuncia no Meta e retorna criativos validados."""
    print(f"  📱 Meta → '{fb_identifier}'")

    # Normaliza: extrai o slug caso seja uma URL completa
    slug = fb_identifier.rstrip("/").split("/")[-1] if "facebook.com" in fb_identifier else fb_identifier
    url = (
        "https://www.facebook.com/ads/library/"
        f"?active_status=active&ad_type=all&country=BR"
        f"&q={slug}&search_type=page"
    )

    result = {
        "anuncia": False,
        "url": url,
        "total_anuncios_estimado": 0,
        "criativos_validados": [],
        "videos_interceptados": [],
        "screenshot": None,
    }

    iv.reset()
    iv.attach(page)

    try:
        await page.goto(url, timeout=45000, wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)

        body = await page.inner_text("body")
        if any(w in body.lower() for w in ("faça login", "log in", "fazer login")):
            print("    ⚠️  Pediu login. Resolva no browser e pressione Enter.")
            try:
                input("    → Enter para continuar: ")
            except EOFError:
                await page.wait_for_timeout(8000)
            await page.wait_for_timeout(3000)
            body = await page.inner_text("body")

        sem_anuncios = any(p in body for p in (
            "Nenhum anúncio", "No ads", "não encontramos", "nenhum resultado"
        ))
        if sem_anuncios:
            print("    ❌ Não anuncia no Meta")
            result["screenshot"] = await safe_shot(page, comp_dir / "meta_sem_anuncios.png")
            return result

        result["anuncia"] = True
        await scroll_load(page, scrolls=7, delay=2000)
        result["screenshot"] = await safe_shot(page, comp_dir / "meta_library.png")

        # Estima total de anúncios ativos
        m = re.search(r"([\d.]+)\s+anúncio", body)
        if m:
            result["total_anuncios_estimado"] = parse_count(m.group(1))

        # Detecta criativos validados (≥ 2 ads com mesmo criativo)
        validated = await page.evaluate(_META_VALIDATED_JS)
        result["criativos_validados"] = validated or []

        # Vídeos interceptados durante a navegação
        result["videos_interceptados"] = iv.get()

        qtd = len(result["criativos_validados"])
        print(f"    ✅ Anuncia | ≈{result['total_anuncios_estimado']} anúncios | {qtd} validados")

    except PlaywrightTimeout:
        print("    ⚠️  Timeout")
    except Exception as e:
        print(f"    ⚠️  Erro: {e}")
    finally:
        iv.detach(page)

    return result


async def search_meta_keywords(page, keywords: list[str], out_dir: Path, iv: VideoInterceptor) -> list[dict]:
    """Busca criativos validados por palavra-chave no Meta Ad Library (concorrentes indiretos)."""
    all_validated: list[dict] = []
    kw_dir = out_dir / "_meta_keywords"
    kw_dir.mkdir(exist_ok=True)

    for kw in keywords:
        print(f"  📱 Meta keyword → '{kw}'")
        url = (
            "https://www.facebook.com/ads/library/"
            f"?active_status=active&ad_type=all&country=BR"
            f"&q={kw}&search_type=keyword_unordered"
        )

        iv.reset()
        iv.attach(page)

        try:
            await page.goto(url, timeout=45000, wait_until="domcontentloaded")
            await page.wait_for_timeout(4000)
            await scroll_load(page, scrolls=7, delay=2000)

            await safe_shot(page, kw_dir / f"{kw[:25].replace(' ', '_')}.png")

            validated = await page.evaluate(_META_VALIDATED_JS)
            videos = iv.get()

            if validated:
                for v in validated:
                    v["keyword"] = kw
                    if not v.get("videos") and videos:
                        v["videos"] = videos[:1]
                all_validated.extend(validated)

            print(f"    ✅ {len(validated or [])} criativo(s) validado(s)")

        except Exception as e:
            print(f"    ⚠️  Erro: {e}")
        finally:
            iv.detach(page)

    # Remove duplicatas pelo snippet de texto
    seen: set[str] = set()
    unique: list[dict] = []
    for item in all_validated:
        key = item.get("texto", "")[:60]
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique


# ─── Google Ads Transparency ──────────────────────────────────────────────────

# JS com múltiplas estratégias de extração para o Google Ads Transparency Center.
# Google usa web components e shadow DOM — tentamos várias abordagens em sequência.
_GOOGLE_ADS_JS = """
() => {
    const results = [];
    const seen = new Set();

    function textOf(el) {
        let t = (el.innerText || el.textContent || '').trim();
        if (el.shadowRoot) t += ' ' + (el.shadowRoot.innerText || el.shadowRoot.textContent || '').trim();
        return t;
    }

    function addCard(text, source) {
        const key = text.slice(0, 50);
        if (seen.has(key) || text.length < 15) return;
        seen.add(key);

        // Tenta estruturar: linhas curtas = headlines, médias = descrições
        const lines = text.split('\\n').map(l => l.trim()).filter(l => l.length > 3);
        const headlines    = lines.filter(l => l.length >= 5  && l.length <= 35);
        const descriptions = lines.filter(l => l.length >= 36 && l.length <= 110);

        results.push({
            source,
            raw: text.slice(0, 700),
            headlines:    headlines.slice(0, 5),
            descriptions: descriptions.slice(0, 4),
        });
    }

    // Estratégia 1 — elementos customizados (web components do Google)
    const customTags = [
        'creative-preview', 'text-ad-preview', 'ad-preview',
        'google-text-ad',   'ad-preview-card', 'creative-card',
    ];
    let found = false;
    for (const tag of customTags) {
        const els = document.querySelectorAll(tag);
        if (els.length > 0) {
            els.forEach((el, i) => { if (i < 20) addCard(textOf(el), 'custom:' + tag); });
            found = true;
            break;
        }
    }

    // Estratégia 2 — shadow DOM recursivo
    if (!found) {
        function searchShadow(root, depth) {
            if (depth > 6 || results.length >= 20) return;
            root.querySelectorAll('*').forEach(el => {
                if (el.shadowRoot) {
                    const t = textOf(el);
                    if (t.length > 30) addCard(t, 'shadow');
                    searchShadow(el.shadowRoot, depth + 1);
                }
            });
        }
        searchShadow(document.body, 0);
        if (results.length > 0) found = true;
    }

    // Estratégia 3 — seletores por classe (Google muda nomes com frequência)
    if (!found) {
        const patterns = [
            'creative', 'Creative', 'AdCard', 'ad-card',
            'AdPreview', 'ad-preview', 'TextAd', 'text-ad',
        ];
        for (const p of patterns) {
            const els = document.querySelectorAll('[class*="' + p + '"]');
            if (els.length >= 2) {
                els.forEach((el, i) => { if (i < 20) addCard(textOf(el), 'class:' + p); });
                if (results.length >= 2) { found = true; break; }
            }
        }
    }

    // Estratégia 4 — texto bruto da página (fallback)
    if (!found || results.length === 0) {
        const main = document.querySelector('main, [role="main"]') || document.body;
        addCard((main.innerText || '').slice(0, 5000), 'raw_page');
    }

    return results.slice(0, 20);
}
"""


def _parse_google_ads_from_raw(raw_text: str) -> list[dict]:
    """
    Heurística de fallback: analisa o texto bruto da página e tenta identificar
    grupos de headline + description no padrão de texto de anúncio do Google.
    """
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    ads: list[dict] = []
    current: dict = {"headlines": [], "descriptions": []}

    for line in lines:
        length = len(line)
        if 5 <= length <= 35:
            current["headlines"].append(line)
        elif 36 <= length <= 110:
            current["descriptions"].append(line)
        else:
            # Linha longa ou muito curta = possível separador de bloco
            if current["headlines"] or current["descriptions"]:
                if current["headlines"] or current["descriptions"]:
                    ads.append({
                        "headlines":    current["headlines"][:5],
                        "descriptions": current["descriptions"][:4],
                    })
                current = {"headlines": [], "descriptions": []}

    if current["headlines"] or current["descriptions"]:
        ads.append(current)

    return ads[:15]


async def check_google_competitor(page, domain: str, comp_dir: Path) -> dict:
    """Verifica presença no Google Ads e extrai títulos e descrições dos anúncios."""
    print(f"  🔍 Google Transparency → '{domain}'")

    domain = (
        domain.replace("https://", "").replace("http://", "")
              .replace("www.", "").split("/")[0].strip()
    )
    url = f"https://adstransparency.google.com/?region=BR&domain={domain}"
    result = {
        "anuncia": False,
        "url": url,
        "anuncios": [],          # lista estruturada com headlines + descriptions
        "screenshot": None,
    }

    try:
        await page.goto(url, timeout=45000, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
        await scroll_load(page, scrolls=5, delay=2000)

        result["screenshot"] = await safe_shot(page, comp_dir / "google_transparency.png")
        body = await page.inner_text("body")

        sem_anuncios = any(p in body for p in (
            "nenhum resultado", "No results", "não há anúncios", "has no ads"
        ))
        if sem_anuncios:
            print("    ❌ Não anuncia no Google")
            return result

        result["anuncia"] = True

        # Tentativa 1: extração via JS com múltiplas estratégias
        raw_cards = await page.evaluate(_GOOGLE_ADS_JS) or []

        structured: list[dict] = []
        for card in raw_cards:
            if card.get("source") == "raw_page":
                # Se só temos o texto bruto, usa heurística de parsing
                parsed = _parse_google_ads_from_raw(card.get("raw", ""))
                structured.extend(parsed)
            else:
                headlines    = card.get("headlines", [])
                descriptions = card.get("descriptions", [])
                if headlines or descriptions:
                    structured.append({
                        "headlines":    headlines[:5],
                        "descriptions": descriptions[:4],
                    })

        # Deduplica por primeira headline
        seen_h: set[str] = set()
        unique: list[dict] = []
        for ad in structured:
            key = (ad.get("headlines") or [""])[0][:30]
            if key and key not in seen_h:
                seen_h.add(key)
                unique.append(ad)

        # Fallback: se JS não retornou nada estruturado, usa heurística no texto da página
        if not unique:
            unique = _parse_google_ads_from_raw(body)

        result["anuncios"] = unique
        qtd = len(unique)
        print(f"    ✅ Anuncia | {qtd} anúncio(s) extraído(s)")

    except PlaywrightTimeout:
        print("    ⚠️  Timeout")
    except Exception as e:
        print(f"    ⚠️  Erro: {e}")

    return result


# ─── Instagram ────────────────────────────────────────────────────────────────

async def analyze_instagram(page, username: str, comp_dir: Path) -> dict:
    """Analisa perfil Instagram e retorna posts com discrepância positiva de engajamento."""
    print(f"  📸 Instagram → @{username}")

    username = username.lstrip("@").strip()
    profile_url = f"https://www.instagram.com/{username}/"
    result = {
        "username": username,
        "profile_url": profile_url,
        "screenshot": None,
        "posts_destaque": [],
        "mediana_engajamento": 0,
    }

    try:
        await page.goto(profile_url, timeout=45000, wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)

        body = await page.inner_text("body")
        if any(w in body.lower() for w in ("faça login", "log in", "criar conta")):
            print("    ⚠️  Pediu login. Resolva no browser e pressione Enter.")
            try:
                input("    → Enter para continuar: ")
            except EOFError:
                await page.wait_for_timeout(8000)
            await page.wait_for_timeout(3000)

        result["screenshot"] = await safe_shot(page, comp_dir / "instagram_profile.png")

        # Coleta URLs dos posts do grid (até 15)
        post_urls: list[str] = await page.evaluate("""
            () => {
                const links = document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]');
                return [...new Set(Array.from(links).map(a => a.href))].slice(0, 15);
            }
        """) or []

        if not post_urls:
            print("    ⚠️  Posts não visíveis sem login")
            return result

        print(f"    → Coletando métricas de {len(post_urls)} post(s)...")

        posts: list[dict] = []
        for i, post_url in enumerate(post_urls):
            try:
                await page.goto(post_url, timeout=30000, wait_until="domcontentloaded")
                await page.wait_for_timeout(2500)

                m = await page.evaluate("""
                    () => {
                        const body = document.body.innerText || '';
                        const likeM   = body.match(/([\\d.,]+[KkMm]?)\\s*curtida/i)
                                     || body.match(/([\\d.,]+[KkMm]?)\\s*like/i);
                        const viewM   = body.match(/([\\d.,]+[KkMm]?)\\s*visualizaç/i)
                                     || body.match(/([\\d.,]+[KkMm]?)\\s*view/i)
                                     || body.match(/([\\d.,]+[KkMm]?)\\s*reproduç/i);
                        const commM   = body.match(/([\\d.,]+[KkMm]?)\\s*comentário/i)
                                     || body.match(/([\\d.,]+[KkMm]?)\\s*comment/i);
                        return {
                            likes_raw:    likeM   ? likeM[1]   : '',
                            views_raw:    viewM   ? viewM[1]   : '',
                            comments_raw: commM   ? commM[1]   : '',
                            is_reel: window.location.href.includes('/reel/'),
                        };
                    }
                """) or {}

                likes    = parse_count(m.get("likes_raw", ""))
                views    = parse_count(m.get("views_raw", ""))
                comments = parse_count(m.get("comments_raw", ""))
                engagement = likes + views + (comments * 3)

                posts.append({
                    "url": post_url,
                    "tipo": "reel" if m.get("is_reel") else "post",
                    "likes": likes,
                    "views": views,
                    "comments": comments,
                    "engagement": engagement,
                })
                print(f"      [{i+1}/{len(post_urls)}] likes={likes} views={views} comments={comments}")

            except Exception:
                posts.append({"url": post_url, "engagement": 0})

        # Calcula mediana e detecta discrepância (≥ 2× mediana)
        valid = [p for p in posts if p["engagement"] > 0]
        if valid:
            engs = sorted(p["engagement"] for p in valid)
            median = engs[len(engs) // 2]
            threshold = max(median * 2, 1)
            result["posts_destaque"] = [p for p in valid if p["engagement"] >= threshold]
            result["mediana_engajamento"] = median

        print(f"    ✅ {len(posts)} posts | {len(result['posts_destaque'])} com discrepância positiva")

    except PlaywrightTimeout:
        print("    ⚠️  Timeout")
    except Exception as e:
        print(f"    ⚠️  Erro: {e}")

    return result


# ─── TikTok Keyword Search ────────────────────────────────────────────────────

async def search_tiktok_keywords(page, keywords: list[str], out_dir: Path) -> list[dict]:
    """Busca vídeos no TikTok por keyword e retorna os com maior engajamento."""
    all_videos: list[dict] = []
    tt_dir = out_dir / "_tiktok"
    tt_dir.mkdir(exist_ok=True)

    for kw in keywords:
        print(f"  🎵 TikTok keyword → '{kw}'")
        url = f"https://www.tiktok.com/search/video?q={kw}"

        try:
            await page.goto(url, timeout=45000, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)
            await scroll_load(page, scrolls=4, delay=2000)

            await safe_shot(page, tt_dir / f"{kw[:25].replace(' ', '_')}.png")

            videos: list[dict] = await page.evaluate("""
                () => {
                    const seen = new Set();
                    const results = [];

                    // TikTok muda seletores com frequência — tentamos múltiplos
                    const selectors = [
                        '[data-e2e="search_video-item"]',
                        '[class*="DivItemContainer"]',
                        '[class*="video-feed-item"]',
                    ];

                    let cards = [];
                    for (const sel of selectors) {
                        const found = document.querySelectorAll(sel);
                        if (found.length > 0) { cards = [...found]; break; }
                    }

                    // Fallback: encontra links de vídeo diretamente
                    if (cards.length === 0) {
                        document.querySelectorAll('a[href*="/video/"]').forEach(a => {
                            if (results.length >= 20 || seen.has(a.href)) return;
                            seen.add(a.href);
                            const parent = a.closest('[class]') || a;
                            results.push({ url: a.href, texto: (parent.innerText || '').slice(0, 300), nums_raw: [] });
                        });
                        return results;
                    }

                    cards.slice(0, 25).forEach(card => {
                        const link = card.querySelector('a[href*="/video/"]');
                        const href = link?.href || '';
                        if (!href || seen.has(href)) return;
                        seen.add(href);

                        const texto = card.innerText || '';
                        // Números do card: tipicamente views, likes, comentários
                        const nums = (texto.match(/[\\d.,]+[KkMm]?/g) || []);

                        results.push({
                            url: href,
                            texto: texto.slice(0, 400),
                            nums_raw: nums.slice(0, 6),
                        });
                    });
                    return results;
                }
            """) or []

            parsed: list[dict] = []
            for v in videos:
                nums = sorted([parse_count(n) for n in v.get("nums_raw", [])], reverse=True)
                parsed.append({
                    "url": v["url"],
                    "titulo": v.get("texto", "")[:150],
                    "keyword": kw,
                    "views":       nums[0] if len(nums) > 0 else 0,
                    "likes":       nums[1] if len(nums) > 1 else 0,
                    "comentarios": nums[2] if len(nums) > 2 else 0,
                    "engagement":  sum(nums[:3]),
                })

            parsed.sort(key=lambda x: x["engagement"], reverse=True)
            all_videos.extend(parsed[:10])
            print(f"    ✅ {len(parsed)} vídeo(s) coletados")

        except Exception as e:
            print(f"    ⚠️  Erro: {e}")

    all_videos.sort(key=lambda x: x["engagement"], reverse=True)
    return all_videos[:20]


# ─── Coleta de Input ──────────────────────────────────────────────────────────

def collect_input():
    sep("ANÁLISE DE CONCORRENTES — ARTTICO")

    cliente = ask("\nCliente")
    nicho = ask("Nicho/segmento (ex: clínica estética, advocacia trabalhista)")

    # Concorrentes diretos
    competitors: list[dict] = []
    sep("Concorrentes Diretos")
    print("Enter em branco pula o campo. Nome em branco encerra a lista.\n")

    while True:
        n = len(competitors) + 1
        print(f"  Concorrente {n}:")
        nome = ask("  Nome")
        if not nome:
            if not competitors:
                print("  Informe ao menos um concorrente.")
                continue
            break
        facebook  = ask("  Facebook (nome da página ou URL)")
        website   = ask("  Website/domínio (Google Transparency)")
        instagram = ask("  Instagram (@username)")
        competitors.append({"nome": nome, "facebook": facebook, "website": website, "instagram": instagram})
        if not ask_bool("\n  Adicionar outro concorrente?", default=False):
            break
        print()

    # Keywords Meta
    sep("Palavras-chave — Meta Ad Library (concorrentes indiretos)")
    print("Ex: 'implante capilar', 'clínica estética Natal'")
    print("(Enter em branco termina a lista)\n")
    meta_keywords: list[str] = []
    while True:
        try:
            kw = input(f"  Keyword {len(meta_keywords)+1}: ").strip()
        except EOFError:
            break
        if not kw:
            break
        meta_keywords.append(kw)

    # Keywords TikTok
    sep("Palavras-chave — TikTok")
    print("(Enter em branco termina a lista)\n")
    tiktok_keywords: list[str] = []
    while True:
        try:
            kw = input(f"  Keyword {len(tiktok_keywords)+1}: ").strip()
        except EOFError:
            break
        if not kw:
            break
        tiktok_keywords.append(kw)

    return cliente, nicho, competitors, meta_keywords, tiktok_keywords


# ─── Orquestrador ─────────────────────────────────────────────────────────────

async def run(cliente, nicho, competitors, meta_keywords, tiktok_keywords):
    date_str = datetime.now().strftime("%Y-%m-%d")
    project_root = Path(__file__).resolve().parent.parent.parent.parent.parent

    client_slug = slugify(cliente).replace("_", "-")
    output_dir = project_root / "clientes" / client_slug / "concorrentes" / date_str
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        rel = output_dir.relative_to(project_root)
    except ValueError:
        rel = output_dir

    print(f"\n📁 Salvando em: {rel}")

    all_data: dict = {
        "cliente": cliente,
        "nicho": nicho,
        "data": date_str,
        "concorrentes_diretos": [],
        "meta_keywords": [],
        "tiktok": [],
    }

    iv = VideoInterceptor()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        page = await ctx.new_page()

        # ── Fase 1: Concorrentes diretos ──────────────────────────────────────
        for comp in competitors:
            sep(f"Concorrente: {comp['nome']}")
            slug = slugify(comp["nome"])
            comp_dir = output_dir / slug
            comp_dir.mkdir(exist_ok=True)

            comp_result: dict = {"nome": comp["nome"], "meta": {}, "google": {}, "instagram": {}}

            if comp.get("facebook"):
                comp_result["meta"] = await check_meta_competitor(page, comp["facebook"], comp_dir, iv)

            if comp.get("website"):
                comp_result["google"] = await check_google_competitor(page, comp["website"], comp_dir)

            if comp.get("instagram"):
                comp_result["instagram"] = await analyze_instagram(page, comp["instagram"], comp_dir)

            all_data["concorrentes_diretos"].append(comp_result)

        # ── Fase 2: Meta keyword search ───────────────────────────────────────
        if meta_keywords:
            sep("Meta Ad Library — Busca por Keyword")
            all_data["meta_keywords"] = await search_meta_keywords(page, meta_keywords, output_dir, iv)

        # ── Fase 3: TikTok keyword search ─────────────────────────────────────
        if tiktok_keywords:
            sep("TikTok — Busca por Keyword")
            all_data["tiktok"] = await search_tiktok_keywords(page, tiktok_keywords, output_dir)

        await browser.close()

    # Salva JSON
    json_path = output_dir / "analise.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    sep("COLETA CONCLUÍDA")
    print(f"  📁 {rel}")
    print(f"  📄 analise.json")
    print()

    # Imprime para o Claude ler
    print("=" * 60)
    print("DADOS COLETADOS — LEITURA DO CLAUDE")
    print("=" * 60)
    output_str = json.dumps(all_data, ensure_ascii=False, indent=2)
    if len(output_str) > 12000:
        print(output_str[:12000])
        print(f"\n... [truncado — ler o arquivo completo em {json_path}]")
    else:
        print(output_str)


if __name__ == "__main__":
    cliente, nicho, competitors, meta_keywords, tiktok_keywords = collect_input()
    asyncio.run(run(cliente, nicho, competitors, meta_keywords, tiktok_keywords))
