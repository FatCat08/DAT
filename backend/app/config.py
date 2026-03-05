from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Data Assistant API"
    VERSION: str = "1.0.0"
    
    # 数据库配置
    BUSINESS_DB_PATH: str = "data/business.db"
    SESSION_DB_PATH: str = "data/sessions.db"

    # API Keys
    DASHSCOPE_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
