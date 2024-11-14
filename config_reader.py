from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr
    api_weather_token: SecretStr
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    print('1')
    class Config:
        env_prefix = ""


config = Settings()
