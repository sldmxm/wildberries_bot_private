from pydantic import BaseSettings


class Settings(BaseSettings):
    telegram_token: str
    debug: bool = False
    channel_username: str


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
