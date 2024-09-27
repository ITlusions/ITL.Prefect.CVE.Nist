from pydantic-settings import BaseSettings, Field

class Settings(BaseSettings):
    nvd_api_url: str = Field(..., env="NVD_API_URL")
    prefect_api_url: str = Field(..., env="PREFECT_API_URL")
    
    class Config:
        env_file = ".env"

# Instantiate the settings
settings = Settings()