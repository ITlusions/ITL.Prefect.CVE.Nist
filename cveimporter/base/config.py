from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    nvd_api_url: str = Field(..., env="NVD_API_URL")
    prefect_api_url: str = Field(..., env="PREFECT_API_URL")
    nvd_api_key: str = Field(None, env="NVD_API_KEY")

    class Config:
        env_file = ".env"

# Instantiate the settings
settings = Settings()
