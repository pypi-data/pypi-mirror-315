from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_TITLE: str = "BBia External"
    PROJECT_DESCRIPTION: str = "Assistente virtual da BBoom"
    PROJECT_VERSION: str = "0.1.0"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    SECRET_KEY: str = Field(validation_alias="SECRET_KEY")
    VERIFIY_TOKEN: str = Field(validation_alias="VERIFIY_TOKEN")

    DEBUG: bool = True
    HF_HUB_DISABLE_SYMLINKS_WARNING: bool = True

    RATE_LIMIT: int = 20
    RATE_LIMIT_TIME: int = 60

    GROQ_API_KEY: str = Field(validation_alias="GROQ_API_KEY")
    PINECONE_API_KEY: str = Field(validation_alias="PINECONE_API_KEY")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
