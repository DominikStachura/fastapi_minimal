from typing import Any

from pydantic import BaseSettings, PostgresDsn, root_validator, RedisDsn, Field


class Settings(BaseSettings):
    """
    Application settings
    """
    ENVIRONMENT: str = Field(default="local", env="ENVIRONMENT")

    # postgres
    POSTGRES_USER: str = Field(default="postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="postgres", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(default="postgres", env="POSTGRES_DB")
    POSTGRES_HOST: str = Field(default="0.0.0.0", env="POSTGRES_HOST")
    POSTGRES_PORT: int | str = Field(default=5432, env="POSTGRES_PORT")
    POSTGRES_URI: PostgresDsn | str = ""

    REDIS_URL: RedisDsn | str = Field(default="redis://redis", env="REDIS_URL")

    ORIGINS: list[str] = Field(default=["http://127.0.0.1:3000", "https://127.0.0.1:3000"], env="ORIGINS")

    class Config:
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            # all variables that should be parsed to list
            if field_name in ["ORIGINS"]:
                return [x for x in raw_val.split(",")]
            return cls.json_loads(raw_val)  # type: ignore

    @root_validator
    def assemble_db_connection(cls, values):
        values["POSTGRES_URI"] = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB')}",
            port=str(values.get("POSTGRES_PORT")),
        )
        return values


settings = Settings()
