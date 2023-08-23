from pydantic_settings import BaseSettings
import os

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DEBUG: bool = os.getenv("DEBUG", False)
    DATABASE_URL: str
    API_PREFIX: str = "/api"
    SECRET_KEY: str

    class Config:
        env_file = ".env"

        # Tells pydantic to load the environment variables from the .env file
        # before validating the settings
        load_dotenv = True


settings = Settings()
