from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from pathlib import Path


BASE_DIR = PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class MongoSettings(BaseModel):
    """Настройки подключения к redis"""

    host: str = "127.0.0.1"
    port: int = 27017
    username: str = ""
    password: str = ""


class Settings(BaseSettings):
    """Главный класс настроек всего приложения"""

    secret_key: str = ""
    app_port: int = 8000
    app_scheme: str = "http"
    app_host: str = "127.0.0.1"
    sentry_enabled: bool = 0
    mongo: MongoSettings = MongoSettings()

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=BASE_DIR / ".env.tests",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


test_settings = Settings()
