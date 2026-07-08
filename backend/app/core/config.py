from pydantic_settings import BaseSettings, SettingsConfigDict


from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(alias="APP_NAME")
    app_version: str = Field(alias="APP_VERSION")
    debug: bool = Field(alias="DEBUG")
    api_prefix: str = Field(alias="API_PREFIX")
    upload_dir: str = Field(alias="UPLOAD_DIR")
    groq_api_key: str = Field(alias="groq_api_key")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
    )



settings = Settings()