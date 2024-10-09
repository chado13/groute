from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # gptapi_key: str
    # tour_api_key: str
    # kakao_map_api_key: str
    tour_api_service_key: str
    origins: str
    weather_api_key: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Settings()  # type: ignore
