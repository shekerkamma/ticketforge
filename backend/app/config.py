import re
from urllib.parse import urlparse

from pydantic_settings import BaseSettings


def normalize_origin(origin: str) -> str | None:
    parsed = urlparse(origin.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    if parsed.path not in {"", "/"} or parsed.params or parsed.query or parsed.fragment:
        return None
    return f"{parsed.scheme}://{parsed.netloc}"


class Settings(BaseSettings):
    model_config = {"env_prefix": "", "env_file": ".env", "extra": "ignore"}

    # Database
    database_url: str = "postgresql+asyncpg://ticketforge:ticketforge@localhost:5432/ticketforge"

    # GitHub OAuth
    github_client_id: str = ""
    github_client_secret: str = ""
    github_webhook_secret: str = ""

    # Claude API
    anthropic_api_key: str = ""

    # Stripe
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_id_team: str = ""

    # App
    app_url: str = "http://localhost:3000"
    app_urls: str = ""
    app_url_regex: str = ""
    api_url: str = "http://localhost:8000"
    jwt_secret: str = "change-me-in-production"
    jwt_expiry_hours: int = 24
    local_dev_github_id: int = 0
    local_dev_github_login: str = "local-dev"
    local_dev_email: str = "local-dev@example.com"
    local_dev_team_name: str = "Local Dev Team"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # Sentry
    sentry_dsn: str = ""

    # Encryption
    encryption_key: str = ""

    def allowed_app_origins(self) -> list[str]:
        origins: list[str] = []
        raw_origins = [self.app_url]
        if self.app_urls:
            raw_origins.extend(part.strip() for part in self.app_urls.split(","))

        for origin in raw_origins:
            normalized = normalize_origin(origin)
            if normalized and normalized not in origins:
                origins.append(normalized)

        return origins

    def is_allowed_app_origin(self, candidate: str) -> bool:
        normalized = normalize_origin(candidate)
        if normalized is None:
            return False
        if normalized in self.allowed_app_origins():
            return True
        if self.app_url_regex:
            return re.fullmatch(self.app_url_regex, normalized) is not None
        return False


settings = Settings()
