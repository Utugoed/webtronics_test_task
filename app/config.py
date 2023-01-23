from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "webtronics"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_HOST: str = "postgres_db"
    POSTGRES_PORT: int = 5432

    REDIS_HOST: str = "redis_db"
    REDIS_PORT: int = 6379

    SECRET_AUTH_KEY: str = "8aba20e02ac80fa4add1fd01b5891021f79138ffefe15744d0188f5426ae3506"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 130

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()