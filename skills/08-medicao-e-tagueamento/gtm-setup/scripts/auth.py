import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
    "https://www.googleapis.com/auth/tagmanager.publish",
    "https://www.googleapis.com/auth/tagmanager.readonly",
]

CREDS_DIR = Path(__file__).parent.parent / "credentials"
TOKEN_FILE = CREDS_DIR / "token.pickle"
CREDENTIALS_FILE = CREDS_DIR / "credentials.json"


def get_gtm_service():
    CREDS_DIR.mkdir(exist_ok=True)
    creds = None

    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"\nArquivo credentials.json não encontrado em:\n  {CREDS_DIR}\n\n"
                    "Siga os passos em COMO_CONFIGURAR.md para criar as credenciais."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("tagmanager", "v2", credentials=creds)
