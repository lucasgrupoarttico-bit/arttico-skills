"""
Automatiza a configuração do Stape via Playwright.

Fluxo:
  1. Login em app.stape.io
  2. Criar novo contêiner com o ID do SERVER do GTM
  3. Configurar domínio do servidor: stape.{domínio do cliente}
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

STAPE_URL = "https://app.stape.io"


async def _login(page, email, password):
    await page.goto(f"{STAPE_URL}/login", wait_until="networkidle")
    await page.fill('input[type="email"], input[name="email"]', email)
    await page.fill('input[type="password"], input[name="password"]', password)
    await page.click('button[type="submit"]')
    await page.wait_for_url(f"{STAPE_URL}/**", timeout=15000)


async def _create_container(page, client_name, gtm_server_id, stape_domain):
    # Aguarda o dashboard carregar
    await page.wait_for_load_state("networkidle")

    # Tenta localizar o botão de criar contêiner (o texto pode variar por idioma/versão)
    create_btn = page.locator(
        'button:has-text("Create container"), '
        'button:has-text("New container"), '
        'a:has-text("Create container")'
    ).first
    await create_btn.click(timeout=10000)

    # Preenche nome do contêiner
    name_input = page.locator(
        'input[placeholder*="name"], input[placeholder*="Name"], input[name="name"]'
    ).first
    await name_input.fill(client_name)

    # Preenche o GTM container ID (ex: GTM-XXXXXXX)
    gtm_input = page.locator(
        'input[placeholder*="GTM"], input[placeholder*="container id"], input[name*="gtm"]'
    ).first
    await gtm_input.fill(gtm_server_id)

    # Confirma criação
    submit_btn = page.locator(
        'button[type="submit"]:has-text("Create"), '
        'button:has-text("Create"), '
        'button:has-text("Save")'
    ).first
    await submit_btn.click()
    await page.wait_for_load_state("networkidle")

    # Configura o domínio do servidor
    domain_input = page.locator(
        'input[placeholder*="domain"], input[placeholder*="Domain"], input[name*="domain"]'
    ).first

    try:
        await domain_input.wait_for(timeout=8000)
        await domain_input.fill(stape_domain)

        save_btn = page.locator(
            'button:has-text("Save"), button:has-text("Confirm"), button[type="submit"]'
        ).first
        await save_btn.click()
        await page.wait_for_load_state("networkidle")
    except PlaywrightTimeout:
        print(
            "\n  [aviso] Campo de domínio não encontrado automaticamente.\n"
            f"  -> Configure manualmente o domínio '{stape_domain}' no painel Stape."
        )


async def _run(config, gtm_server_id):
    async with async_playwright() as p:
        # headless=False para o usuário acompanhar e intervir se necessário
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            print("  Fazendo login no Stape...")
            await _login(page, config["stape_email"], config["stape_password"])

            print("  Criando contêiner e configurando domínio...")
            await _create_container(
                page,
                client_name=config["client_name"],
                gtm_server_id=gtm_server_id,
                stape_domain=config["stape_domain"],
            )
        except Exception as e:
            print(f"\n  [erro Stape] {e}")
            print(
                f"  -> Finalize manualmente:\n"
                f"     GTM Server ID: {gtm_server_id}\n"
                f"     Domínio:       {config['stape_domain']}"
            )
            input("\n  Pressione Enter após concluir no Stape...")
        finally:
            await browser.close()


def configure_stape(config, gtm_server_id):
    asyncio.run(_run(config, gtm_server_id))
