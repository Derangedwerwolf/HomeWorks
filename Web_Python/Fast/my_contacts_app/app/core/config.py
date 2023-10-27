import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


# database_url = os.environ.get("SQLALCHEMY_DATABASE_URL")


class Settings(BaseSettings):
    DEBUG: bool = os.getenv("DEBUG", False)
    DATABASE_URL: str
    API_PREFIX: str = "/api"
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
