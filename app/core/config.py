import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl
from pydantic import PostgresDsn, computed_field

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.environ.get('ENV_FILE', '.env'),
        env_ignore_empty=True,
        extra='ignore',
    )

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = 'postgres'
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @computed_field  # type: ignore[misc]
    @property
    def sqlalchemy_db_uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme='postgresql+psycopg',
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
        )

settings = Settings()