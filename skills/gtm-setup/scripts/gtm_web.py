"""
Cria e configura o contêiner WEB no GTM.
Ordem obrigatória: variáveis → triggers → tags → publicar.
"""


def _p(key, value, ptype="template"):
    return {"type": ptype, "key": key, "value": value}


def _filter(ftype, arg0, arg1):
    return {
        "type": ftype,
        "parameter": [
            {"type": "template", "key": "arg0", "value": arg0},
            {"type": "template", "key": "arg1", "value": arg1},
        ],
    }


def _safe_create(fn, body):
    try:
        return fn(parent_=None, body=body)
    except Exception:
        pass


def _create_variables(svc, wpath, config):
    def create(body):
        try:
            return svc.accounts().containers().workspaces().variables().create(
                parent=wpath, body=body
            ).execute()
        except Exception as e:
            if "duplicate name" not in str(e).lower():
                raise

    create({"name": "GA4 | ID", "type": "c", "parameter": [_p("value", config["ga4_id"])]})

    if config.get("use_meta"):
        create({"name": "FB | Pixel", "type": "c", "parameter": [_p("value", config["meta_pixel_id"])]})
        create({"name": "event_id", "type": "cvt_M63B8", "parameter": []})


def _create_triggers(svc, wpath, config):
    def create(body):
        try:
            return svc.accounts().containers().workspaces().triggers().create(
                parent=wpath, body=body
            ).execute()
        except Exception as e:
            if "duplicate name" not in str(e).lower():
                raise
            return None

    triggers = {}
    pages = config.get("pages", [])
    wpp_num = config.get("whatsapp_number", "")
    domain = config.get("domain", "")

    for page in pages:
        slug = page["slug"]
        path_filter_type = "equals" if slug == "/" else "contains"

        # PageView trigger por página
        triggers[f"pageview_{slug}"] = create({
            "name": f"PageView_{slug}",
            "type": "domReady",
            "filter": [_filter(path_filter_type, "{{Page Path}}", slug)],
        })

        # WhatsApp trigger por página
        if config.get("conv_whatsapp"):
            triggers[f"whatsapp_{slug}"] = create({
                "name": f"click_whatsapp_{slug}",
                "type": "linkClick",
                "filter": [
                    _filter(path_filter_type, "{{Page Path}}", slug),
                    _filter("contains", "{{Click URL}}", f"https://wa.me/{wpp_num}"),
                ],
                "waitForTags": {"type": "boolean", "value": "false"},
                "checkValidation": {"type": "boolean", "value": "false"},
            })

        # Lead trigger por página
        if config.get("conv_lead"):
            triggers[f"lead_{slug}"] = create({
                "name": f"Lead_{slug}",
                "type": "formSubmission",
                "filter": [
                    _filter(path_filter_type, "{{Page Path}}", slug),
                    _filter("contains", "{{Form URL}}", f"{domain}/{slug}"),
                ],
                "waitForTags": {"type": "boolean", "value": "false"},
                "checkValidation": {"type": "boolean", "value": "false"},
            })

    return triggers


def _create_tags(svc, wpath, config, triggers):
    def create(body):
        try:
            return svc.accounts().containers().workspaces().tags().create(
                parent=wpath, body=body
            ).execute()
        except Exception as e:
            if "duplicate name" not in str(e).lower():
                raise

    pages = config.get("pages", [])

    # 0 | Tag do Google — usa trigger built-in Initialization (2147479573)
    create({
        "name": "0 | Tag do Google",
        "type": "googtag",
        "parameter": [
            _p("tagId", "{{GA4 | ID}}"),
            {
                "type": "list",
                "key": "configSettingsTable",
                "list": [
                    {
                        "type": "map",
                        "map": [
                            _p("parameter", "send_page_view"),
                            _p("parameterValue", "true"),
                        ],
                    },
                    {
                        "type": "map",
                        "map": [
                            _p("parameter", "server_container_url"),
                            _p("parameterValue", f"https://{config['stape_domain']}"),
                        ],
                    },
                ],
            },
        ],
        "firingTriggerId": ["2147479573"],
        "tagFiringOption": "oncePerEvent",
    })

    # Microsoft Clarity
    if config.get("clarity_id"):
        all_pv_ids = [triggers[f"pageview_{p['slug']}"]["triggerId"] for p in pages]
        create({
            "name": "Microsoft Clarity",
            "type": "cvt_MQDKZ",
            "parameter": [_p("projectId", config["clarity_id"])],
            "firingTriggerId": all_pv_ids,
        })

    for page in pages:
        slug = page["slug"]
        pv_id = triggers[f"pageview_{slug}"]["triggerId"]

        # 01 | GA4 - PageView
        create({
            "name": f"01 | GA4 - page_view_{slug}",
            "type": "gaawe",
            "parameter": [
                _p("measurementIdOverride", "{{GA4 | ID}}"),
                _p("eventName", f"PageView_{slug}"),
                _p("sendEcommerceData", "false", "boolean"),
            ],
            "firingTriggerId": [pv_id],
        })

        # 01 | FB - PageView
        if config.get("use_meta"):
            create({
                "name": f"01 | FB - PageView_{slug}",
                "type": "cvt_5RM3Q",
                "parameter": [
                    _p("pixelId", "{{FB | Pixel}}"),
                    _p("eventId", "{{event_id}}"),
                    _p("eventName", "custom"),
                    _p("customEventName", f"PageView_{slug}"),
                    _p("disablePushState", "false", "boolean"),
                    _p("disableAutoConfig", "false", "boolean"),
                    _p("enhancedEcommerce", "false", "boolean"),
                    _p("dpoLDU", "false", "boolean"),
                    _p("consent", "true", "boolean"),
                    _p("advancedMatching", "false", "boolean"),
                    _p("objectPropertiesFromVariable", "false", "boolean"),
                ],
                "firingTriggerId": [pv_id],
            })

        # 02 | click_whatsapp
        if config.get("conv_whatsapp"):
            wpp_id = triggers[f"whatsapp_{slug}"]["triggerId"]

            create({
                "name": f"02 | GA4 - click_whatsapp_{slug}",
                "type": "gaawe",
                "parameter": [
                    _p("measurementIdOverride", "{{GA4 | ID}}"),
                    _p("eventName", f"click_whatsapp_{slug}"),
                    _p("sendEcommerceData", "false", "boolean"),
                ],
                "firingTriggerId": [wpp_id],
            })

            if config.get("use_meta"):
                create({
                    "name": f"02 | FB - click_whatsapp_{slug}",
                    "type": "cvt_5RM3Q",
                    "parameter": [
                        _p("pixelId", "{{FB | Pixel}}"),
                        _p("eventId", "{{event_id}}"),
                        _p("eventName", "custom"),
                        _p("customEventName", f"click_whatsapp_{slug}"),
                        _p("disablePushState", "false", "boolean"),
                        _p("disableAutoConfig", "false", "boolean"),
                        _p("enhancedEcommerce", "false", "boolean"),
                        _p("dpoLDU", "false", "boolean"),
                        _p("consent", "true", "boolean"),
                        _p("advancedMatching", "false", "boolean"),
                        _p("objectPropertiesFromVariable", "false", "boolean"),
                    ],
                    "firingTriggerId": [wpp_id],
                })

        # 02 | Lead
        if config.get("conv_lead"):
            lead_id = triggers[f"lead_{slug}"]["triggerId"]

            create({
                "name": f"02 | GA4 - Lead_{slug}",
                "type": "gaawe",
                "parameter": [
                    _p("measurementIdOverride", "{{GA4 | ID}}"),
                    _p("eventName", f"Lead_{slug}"),
                    _p("sendEcommerceData", "false", "boolean"),
                ],
                "firingTriggerId": [lead_id],
            })

            if config.get("use_meta"):
                create({
                    "name": f"02 | FB - Lead_{slug}",
                    "type": "cvt_5RM3Q",
                    "parameter": [
                        _p("pixelId", "{{FB | Pixel}}"),
                        _p("eventId", "{{event_id}}"),
                        _p("eventName", "custom"),
                        _p("customEventName", f"Lead_{slug}"),
                        _p("disablePushState", "false", "boolean"),
                        _p("disableAutoConfig", "false", "boolean"),
                        _p("enhancedEcommerce", "false", "boolean"),
                        _p("dpoLDU", "false", "boolean"),
                        _p("consent", "true", "boolean"),
                        _p("advancedMatching", "false", "boolean"),
                        _p("objectPropertiesFromVariable", "false", "boolean"),
                    ],
                    "firingTriggerId": [lead_id],
                })


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


def setup_web_container(svc, config):
    account_id = config["gtm_account_id"]

    container = _get_or_create_container(
        svc, account_id, f"[WEB] {config['client_name']}", "web"
    )

    existing_workspaces = svc.accounts().containers().workspaces().list(
        parent=container["path"]
    ).execute().get("workspace", [])
    workspace = next((w for w in existing_workspaces if w["name"] == "Arttico Setup"), None)
    if not workspace:
        workspace = svc.accounts().containers().workspaces().create(
            parent=container["path"],
            body={"name": "Arttico Setup", "description": f"Setup automatico — {config['domain']}"},
        ).execute()

    wpath = workspace["path"]

    _create_variables(svc, wpath, config)
    triggers = _create_triggers(svc, wpath, config)
    _create_tags(svc, wpath, config, triggers)

    version = svc.accounts().containers().workspaces().create_version(
        path=wpath,
        body={"name": "v1 — Arttico Setup", "notes": f"Setup automatico para {config['domain']}"},
    ).execute()

    svc.accounts().containers().versions().publish(
        path=version["containerVersion"]["path"]
    ).execute()

    return container
