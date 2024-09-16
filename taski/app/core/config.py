from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Настройки проекта."""
    app_title: str
    database_url: str
    superuser_email: Optional[EmailStr] = None
    superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
