from pydantic import BaseSettings


class Settings(BaseSettings):
    telegram_token: str
    debug: bool = False
    channel_username: str
    webhook_url: str = None
    webhook_port: int = 8443
    webhook_local_link: str = '0.0.0.0'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
