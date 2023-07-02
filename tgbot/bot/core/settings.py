from pydantic import BaseSettings


class Settings(BaseSettings):
    telegram_token: str
    debug: bool = False
    channel_username: str
    log_filename: str = 'bot.log'
    log_level: str = 'INFO'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
