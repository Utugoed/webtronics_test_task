from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_URL: str = "postgresql://webtronics:qwerty123@localhost:5432/webtronics"


settings = Settings()