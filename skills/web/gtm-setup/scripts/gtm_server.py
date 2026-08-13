"""
Cria e configura o contêiner SERVER no GTM.

Tipos usados:
  - Cliente GA4:   gaaw_c
  - Tag GA4:       sgtmgaaw
  - Tag Meta CAPI: cvt_5TP8W (template Stape — pre-instalado em containers SERVER do Stape)
"""


def _p(key, value, ptype="template"):
    return {"type": ptype, "key": key, "value": value}


def _create_variables(svc, wpath, config):
    def create(body):
        return svc.accounts().containers().workspaces().variables().create(
            parent=wpath, body=body
        ).execute()

    create({"name": "GA4 | ID", "type": "c", "parameter": [_p("value", config["ga4_id"])]})

    if config.get("use_meta"):
        create({"name": "FB | Pixel", "type": "c", "parameter": [_p("value", config["meta_pixel_id"])]})
        create({"name": "FB | Token", "type": "c", "parameter": [_p("value", config["meta_capi_token"])]})


def _create_ga4_client(svc, wpath):
    try:
        svc.accounts().containers().workspaces().clients().create(
            parent=wpath,
            body={
                "name": "GA4 Client",
                "type": "gaaw_c",
                "parameter": [
                    _p("activationPagePath", "/"),
                    _p("serverSideTaggingEnabled", "true", "boolean"),
                ],
                "priority": 0,
            },
        ).execute()
    except Exception as e:
        print(f"  [aviso] GA4 Client: {e}")
        print("  -> Adicione o GA4 Client manualmente no contêiner SERVER.")


def _get_or_create_container(svc, account_id, name, usage_context):
    try:
        return svc.accounts().containers().create(
            parent=f"accounts/{account_id}",
            body={"name": name, "usageContext": [usage_context]},
        ).execute()
    except Exception as e:
        if "duplicate name" not in str(e).lower():
            raise
    containers = svc.accounts().containers().list(
        parent=f"accounts/{account_id}"
    ).execute().get("container", [])
    for c in containers:
        if c["name"] == name:
            return c
    raise RuntimeError(f"Contêiner '{name}' já existe mas não foi encontrado na listagem.")


def setup_server_container(svc, config):
    account_id = config["gtm_account_id"]

    container = _get_or_create_container(
        svc, account_id, f"[STAPE] {config['client_name']}", "server"
    )

    existing_workspaces = svc.accounts().containers().workspaces().list(
        parent=container["path"]
    ).execute().get("workspace", [])
    workspace = next((w for w in existing_workspaces if w["name"] == "Arttico Setup"), None)
    if not workspace:
        workspace = svc.accounts().containers().workspaces().create(
            parent=container["path"],
            body={"name": "Arttico Setup"},
        ).execute()

    wpath = workspace["path"]

    _create_variables(svc, wpath, config)
    _create_ga4_client(svc, wpath)

    pages = config.get("pages", [])

    # GA4 | Todos os Eventos — trigger always (ID built-in: 2147479553)
    try:
        svc.accounts().containers().workspaces().tags().create(
            parent=wpath,
            body={
                "name": "GA4 | Todos os Eventos",
                "type": "sgtmgaaw",
                "parameter": [
                    _p("measurementId", "{{GA4 | ID}}"),
                    _p("redactVisitorIp", "false", "boolean"),
                    _p("epToIncludeDropdown", "all"),
                    _p("upToIncludeDropdown", "all"),
                ],
                "firingTriggerId": ["2147479553"],
            },
        ).execute()
    except Exception as e:
        print(f"  [aviso] GA4 server tag: {e}")
        print("  -> Adicione manualmente: GA4 | Todos os Eventos (tipo: sgtmgaaw).")

    # Tags Meta CAPI por página
    if config.get("use_meta"):
        for page in pages:
            slug = page["slug"]

            # Trigger customEvent por página
            def create_trigger(name):
                return svc.accounts().containers().workspaces().triggers().create(
                    parent=wpath,
                    body={"name": name, "type": "customEvent", "customEventFilter": [{
                        "type": "equals",
                        "parameter": [
                            {"type": "template", "key": "arg0", "value": "{{_event}}"},
                            {"type": "template", "key": "arg1", "value": name},
                        ],
                    }]},
                ).execute()

            def capi_tag(tag_name, event_name, trigger_id):
                try:
                    svc.accounts().containers().workspaces().tags().create(
                        parent=wpath,
                        body={
                            "name": tag_name,
                            "type": "cvt_5TP8W",
                            "parameter": [
                                _p("pixelId", "{{FB | Pixel}}"),
                                _p("accessToken", "{{FB | Token}}"),
                                _p("eventNameCustom", event_name),
                                _p("inheritEventName", "override"),
                                _p("eventName", "custom"),
                                _p("actionSource", "website"),
                                _p("logType", "debug"),
                                _p("adStorageConsent", "optional"),
                                _p("generateFbp", "true", "boolean"),
                                _p("overrideCookieDomain", "false", "boolean"),
                                _p("useAppSecretProof", "false", "boolean"),
                                _p("useHttpOnlyCookie", "false", "boolean"),
                                _p("useOptimisticScenario", "false", "boolean"),
                                _p("bigQueryLogType", "no"),
                                _p("enableMultipixelSetup", "false", "boolean"),
                                _p("enableEventEnhancement", "true", "boolean"),
                            ],
                            "firingTriggerId": [trigger_id],
                        },
                    ).execute()
                except Exception as e:
                    print(f"  [aviso] {tag_name}: {e}")
                    print(f"  -> Adicione manualmente a tag CAPI para {event_name}.")

            pv_trigger = create_trigger(f"PageView_{slug}")
            capi_tag(f"01 | FB - PageView_{slug}", f"PageView_{slug}", pv_trigger["triggerId"])

            if config.get("conv_whatsapp"):
                wpp_trigger = create_trigger(f"click_whatsapp_{slug}")
                capi_tag(f"02 | FB - click_whatsapp_{slug}", f"click_whatsapp_{slug}", wpp_trigger["triggerId"])

            if config.get("conv_lead"):
                lead_trigger = create_trigger(f"Lead_{slug}")
                capi_tag(f"02 | FB - Lead_{slug}", f"Lead_{slug}", lead_trigger["triggerId"])

    version = svc.accounts().containers().workspaces().create_version(
        path=wpath,
        body={"name": "v1 — Arttico Setup"},
    ).execute()

    svc.accounts().containers().versions().publish(
        path=version["containerVersion"]["path"]
    ).execute()

    return container
