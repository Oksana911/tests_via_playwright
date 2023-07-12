from typing import Any, Optional
from pathlib import Path, PosixPath
from pydantic import BaseModel, Field, PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings


class TestUser(BaseModel):
    username: str
    password: str


class Settings(BaseSettings):
    base_dir: PosixPath = Path().absolute()
    base_url: str = Field(env='BASE_URL')
    username: str = Field(env='USERNAME')
    password: str = Field(env='PASSWORD')
    db_host: str = Field(env='DB_HOST')
    db_port: str = Field(env='DB_PORT')
    db_user: str = Field(env='DB_USER')
    db_password: str = Field(env='DB_PASSWORD')
    db_name: str = Field(env='DB_NAME')

    sqlalchemy_database_uri: Optional[PostgresDsn] = None

    @field_validator('sqlalchemy_database_uri', mode='before')
    def assemble_db_connection(cls, v: Optional[str], values: Any) -> PostgresDsn:
        if isinstance(v, str):
            return v
        scheme = 'postgresql',
        db_user = values.data['db_user'],
        db_password = values.data['db_password'],
        host = values.data['db_host'],
        port = values.data['db_port'],
        path = f"{values.data['db_name'] or ''}"
        url = f'{scheme[0]}://{db_user[0]}:{db_password[0]}@{host[0]}:{port[0]}/{path}'   # TODO проверить PostgresDsn.build

        return PostgresDsn(url)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @property
    def user(self) -> TestUser:
        return TestUser(username=self.username, password=self.password)


settings = Settings()
