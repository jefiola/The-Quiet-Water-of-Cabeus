from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Mission Lore Archive"
    app_env: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///./app.db"
    max_unlocks_per_session: int = 250

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
