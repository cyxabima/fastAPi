from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    database_name: str
    database_host: str
    database_port: str
    database_user: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Manually load the .env file
load_dotenv()


# Now create settings
settings = Settings()
