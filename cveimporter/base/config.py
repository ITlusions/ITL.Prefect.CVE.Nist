from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    nvd_api_url: str
    prefect_api_url: str
    nvd_api_key: str | None = None


settings = Settings()