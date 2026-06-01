from pydantic_settings import BaseSettings


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


settings = Settings()
