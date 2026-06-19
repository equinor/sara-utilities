from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SARA_UTILITIES_")

    SOURCE_STORAGE_ACCOUNT: str = Field(default="")
    SOURCE_STORAGE_CONNECTION_STRING: str = Field(default="")
    DESTINATION_STORAGE_ACCOUNT: str = Field(default="")
    DESTINATION_STORAGE_CONNECTION_STRING: str = Field(default="")
    OTEL_SERVICE_NAME: str = Field(default="sara-utilities")
    OTEL_EXPORTER_OTLP_ENDPOINT: str = Field(default="http://localhost:4318")


settings = Settings()
