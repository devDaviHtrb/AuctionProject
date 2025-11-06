from config import Config
from datetime import date
from typing import Mapping, Any
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport import Request
from googleapiclient.discovery import build
import os

REDIRECT_URI = Config.REDIRECT_URI
GOOGLE_CLIENT_ID = Config.GOOGLE_CLIENT_ID
GOOGLE_SECRETS = Config.GOOGLE_SECRECT
GOOGLE_PROJECT_ID = Config.GOOGLE_PROJECT_ID
GOOGLE_REDIRECT_URIS = Config.GOOGLE_REDIRECT_URIS.split(',')
GOOGLE_CONFIG = {
    "web":{
        "client_id":                    GOOGLE_CLIENT_ID,
        "project_id":                   GOOGLE_PROJECT_ID,
        "auth_uri":                     "https://accounts.google.com/o/oauth2/auth",
        "token_uri":                    "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url":  "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret":                GOOGLE_SECRETS,
        "redirect_uris":                GOOGLE_REDIRECT_URIS
    }
}

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def create_flow() -> Flow:
    return Flow.from_client_config(
            GOOGLE_CONFIG,
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
            redirect_uri = REDIRECT_URI,
        )

def get_id_info(credentials: Credentials, request_session: Request) -> Mapping[str, Any]:
    return id_token.verify_oauth2_token(
        credentials._id_token,
        request_session,
        GOOGLE_CLIENT_ID
    )


def get_extra_user_info(credentials: Credentials):
    service = build('people', 'v1', credentials = credentials)
    profile = service.people().get(
        resourceName='people/me',
        personFields='names,emailAddresses,birthdays,genders'
    ).execute()

    birthday = date.today()
    gender = "Indefinido"

    if 'birthdays' in profile:
        b = profile['birthdays'][0]['date']
        birthday = f"{b.get('year','0000')}-{b.get('month','00'):02}-{b.get('day','00'):02}"
    if 'genders' in profile:
        gender = profile['genders'][0]['value']

    return birthday, gender
