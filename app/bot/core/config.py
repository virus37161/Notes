
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    class Config:
        env_file = ".env"



    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    TOKEN: str

settings = AppSettings()


