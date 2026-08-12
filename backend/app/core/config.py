from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = Field(
        default="AI Document Super",
        alias="APP_NAME",
    )

    app_version: str = Field(
        default="1.0.0",
        alias="APP_VERSION",
    )

    debug: bool = Field(
        default=False,
        alias="DEBUG",
    )

    api_prefix: str = Field(
        default="/api",
        alias="API_PREFIX",
    )

    upload_dir: str = Field(
        default="data/uploads",
        alias="UPLOAD_DIR",
    )

    groq_api_key: str = Field(
        alias="GROQ_API_KEY",
    )

    vector_db_dir: str = Field(
        default="data/vector_db",
        alias="VECTOR_DB_DIR",
    )

    database_path: str = Field(
        default="data/documents.db",
        alias="DATABASE_PATH",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
    )


settings = Settings()