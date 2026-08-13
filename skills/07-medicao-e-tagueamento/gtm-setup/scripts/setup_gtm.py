"""
GTM Setup Automático — Grupo Arttico

Uso:
    python setup_gtm.py

Pré-requisito: seguir COMO_CONFIGURAR.md antes da primeira execução.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from auth import get_gtm_service
from gtm_web import setup_web_container
from gtm_server import setup_server_container
from stape import configure_stape


def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default or ""


def ask_bool(prompt):
    r = input(f"{prompt} [s/n]: ").strip().lower()
    return r in ("s", "sim", "y", "yes")


def collect_inputs():
    print("\n=== GTM Setup Automático — Grupo Arttico ===\n")

    config = {}

    config["client_name"] = ask("Nome do cliente (ex: Clínica Exemplo)")
    config["domain"] = ask("Domínio do cliente (ex: clinicaexemplo.com.br)")

    print()
    print("─" * 55)
    print("  PRÓXIMO PASSO: Criar a conta GTM do cliente")
    print("─" * 55)
    print("  1. Acesse: https://tagmanager.google.com")
    print("  2. Clique em 'Criar conta'")
    print(f"  3. Nome da conta: {config['client_name']}")
    print(f"  4. País: Brasil")
    print(f"  5. Compartilhar dados: a seu critério")
    print("  6. Clique em 'Criar' e aceite os termos")
    print("  7. Feche o popup que abrir (não precisa criar contêiner)")
    print("  8. O ID da conta aparece na URL:")
    print("     tagmanager.google.com/...#/accounts/XXXXXXX/...")
    print("─" * 55)
    input("  Pressione Enter quando a conta estiver criada...")
    print()

    config["gtm_account_id"] = ask("Cole o ID da conta GTM (só números, ex: 1234567)")
    config["ga4_id"] = ask("GA4 Measurement ID (ex: G-XXXXXXXXXX)")

    print()
    config["use_meta"] = ask_bool("Cliente usa Meta Ads?")
    if config["use_meta"]:
        config["meta_pixel_id"] = ask("Meta Pixel ID")
        config["meta_capi_token"] = ask("Meta CAPI Token (Access Token do pixel)")

    config["use_google"] = ask_bool("Cliente usa Google Ads?")

    print()
    config["conv_whatsapp"] = ask_bool("Conversão: click_whatsapp?")
    if config["conv_whatsapp"]:
        config["whatsapp_number"] = ask("Numero WhatsApp sem + (ex: 5584999999999)")

    config["conv_lead"] = ask_bool("Conversão: Lead (form)?")

    print()
    pages_input = ask("Paginas separadas por virgula (ex: lp,home,avcb)")
    config["pages"] = [{"slug": s.strip()} for s in pages_input.split(",") if s.strip()]

    print()
    clarity_id = ask("Microsoft Clarity Project ID (Enter para pular)", default="")
    config["clarity_id"] = clarity_id if clarity_id else None

    config["stape_domain"] = f"stape.{config['domain']}"

    return config


def confirm(config):
    print("\n--- Resumo do Setup ---")
    print(f"  Cliente:        {config['client_name']}")
    print(f"  Domínio:        {config['domain']}")
    print(f"  GA4 ID:         {config['ga4_id']}")
    print(f"  Meta Pixel:     {config.get('meta_pixel_id', '—')}")
    print(f"  Paginas:        {', '.join(p['slug'] for p in config['pages'])}")
    print(f"  Conv. WhatsApp: {'Sim' if config['conv_whatsapp'] else 'Nao'}")
    print(f"  Conv. Lead:     {'Sim' if config['conv_lead'] else 'Nao'}")
    print(f"  Clarity:        {config.get('clarity_id') or '—'}")
    print(f"  Stape domain:   {config['stape_domain']}")
    print()
    ok = input("Confirmar e executar? [s/n]: ").strip().lower()
    return ok in ("s", "sim", "y")


def main():
    config = collect_inputs()

    if not confirm(config):
        print("Cancelado.")
        return

    print("\n[1/4] Autenticando com Google...")
    svc = get_gtm_service()

    print("[2/4] Criando contêiner WEB...")
    web = setup_web_container(svc, config)
    print(f"      OK — {web['publicId']}")

    print("[3/4] Criando contêiner SERVER...")
    server = setup_server_container(svc, config)
    print(f"      OK — {server['publicId']}")

    print("[4/4] Stape — configure manualmente:")
    print(f"      GTM Server ID: {server['publicId']}")
    print(f"      Dominio:       {config['stape_domain']}")

    print("\n=== Concluido ===")
    print(f"  Contêiner WEB:    {web['publicId']}")
    print(f"  Contêiner SERVER: {server['publicId']}")
    print()
    print("Proximos passos:")
    print(f"  1. Acesse app.stape.io e crie container com GTM ID: {server['publicId']}")
    print(f"  2. Configure dominio: {config['stape_domain']}")
    print(f"  3. DNS: CNAME stape.{config['domain']} -> sad.stape.io")
    print("  4. Verifique as tags no GTM Preview")
    print("  5. Publique apos validacao")


if __name__ == "__main__":
    main()
