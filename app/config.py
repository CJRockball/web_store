from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
import secrets


class Settings(BaseSettings):
    app_name: str = "Kids Web Store"
    debug: bool = False
    base_url: str = "http://localhost:8000"
    secret_key: str = secrets.token_hex(32)
    cors_origins: List[str] = ["http://localhost:8000"]
    redis_url: str = "redis://localhost:6379"
    
    # Security settings
    session_expire_seconds: int = 3600
    max_cart_items: int = 50
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

