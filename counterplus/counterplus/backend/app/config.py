from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "dev-only-secret-change-me"
    access_token_expire_minutes: int = 1440
    database_url: str = "sqlite:///./counterplus.db"

    provider_mode: str = "mock"  # "mock" or "live"
    bbps_api_base_url: str = ""
    bbps_api_key: str = ""
    bbps_api_secret: str = ""

    payment_mode: str = "mock"  # "mock" or "live"
    payment_api_key: str = ""
    payment_api_secret: str = ""
    payment_webhook_secret: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
