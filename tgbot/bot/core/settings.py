from pydantic import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    telegram_token: str
    debug: bool = False

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
