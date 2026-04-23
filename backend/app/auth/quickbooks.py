import secrets
from urllib.parse import urlencode

from pydantic_settings import BaseSettings, SettingsConfigDict


class QuickBooksSettings(BaseSettings):
    qb_client_id: str = ""
    qb_client_secret: str = ""
    qb_redirect_uri: str = "http://localhost:8000/api/qb/callback"
    qb_environment: str = "sandbox"
    frontend_url: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def create_oauth_state() -> str:
    return secrets.token_urlsafe(32)


def get_quickbooks_authorize_base(environment: str) -> str:
    if environment.lower() == "production":
        return "https://appcenter.intuit.com/connect/oauth2"
    return "https://appcenter.intuit.com/connect/oauth2"


def build_quickbooks_connect_url(settings: QuickBooksSettings, state: str) -> str:
    params = {
        "client_id": settings.qb_client_id,
        "response_type": "code",
        "scope": "com.intuit.quickbooks.accounting",
        "redirect_uri": settings.qb_redirect_uri,
        "state": state,
    }
    base_url = get_quickbooks_authorize_base(settings.qb_environment)
    return f"{base_url}?{urlencode(params)}"
