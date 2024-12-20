import os
from pydantic_settings import BaseSettings, SettingsConfigDict


PROFILE = os.environ.get("PROFILE", "local")


class Settings(BaseSettings):
    git_repo: str
    branch: str

    index_name: str
    elasticsearch_urls: list[str]

    model_config = SettingsConfigDict(env_file=f"./config/.env", env_file_encoding="utf-8")


config = Settings()
