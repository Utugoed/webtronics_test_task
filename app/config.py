from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "webtronics"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_HOST: str = "postgres_db"
    POSTGRES_PORT: int = 5432

    REDIS_HOST: str = "redis_db"
    REDIS_PORT: int = 6379

    SECRET_AUTH_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 130

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()