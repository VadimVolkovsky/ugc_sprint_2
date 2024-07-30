from logging import config as logging_config
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


BASE_DIR = PROJECT_ROOT = Path(__file__).resolve().parent.parent


class MongoSettings(BaseModel):
    """Настройки подключения к redis"""

    host: str = "127.0.0.1"
    port: int = 27017
    username: str = ""
    password: str = ""


class Settings(BaseSettings):
    """Главный класс настроек всего приложения"""

    # project_name: str = "movies_ugc"
    # secret_key: str = ""
    # app_port: int = 8000
    mongo: MongoSettings = MongoSettings()

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
