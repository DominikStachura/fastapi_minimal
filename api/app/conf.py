from typing import Any

from pydantic import PostgresDsn, model_validator, RedisDsn, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    Values will by taken form env vars by field name. If you want to populate using different environment variable name
    use Field(default=..., alias="YOUR_ENV_VAR_NAME")
    """
    ENVIRONMENT: str = Field(default="local")

    # postgres
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_DB: str = Field(default="postgres")
    POSTGRES_HOST: str = Field(default="0.0.0.0")
    POSTGRES_PORT: int | str = Field(default=5432)
    POSTGRES_URI: PostgresDsn | str = ""

    REDIS_URL: RedisDsn | str = Field(default="redis://redis")

    ORIGINS: list[str] = Field(default=["http://127.0.0.1:3000", "https://127.0.0.1:3000"])

    class Config:
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            # will be deprecated in pydantic v3.0
            # all variables that should be parsed to list
            if field_name in ["ORIGINS"]:
                return [x for x in raw_val.split(",")]
            return cls.json_loads(raw_val)  # type: ignore

    @model_validator(mode="after")
    def assemble_db_connection(self):
        self.POSTGRES_URI = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            path=self.POSTGRES_DB,
            port=int(self.POSTGRES_PORT),
        )


settings = Settings()
