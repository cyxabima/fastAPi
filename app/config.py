from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_name: str
    database_host: str
    database_port: str
    database_user: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")


# settings = Settings()
# print(settings.dict())
