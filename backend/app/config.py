from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Data Assistant API"
    VERSION: str = "1.0.0"
    
    # 数据库配置
    BUSINESS_DB_PATH: str = "data/business.db"
    SESSION_DB_PATH: str = "data/sessions.db"

    # API Keys
    DASHSCOPE_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env")

from functools import lru_cache

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
