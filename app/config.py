from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_password: str = "Fuckyou1"
    database_name: str = "fastapi"
    database_username: str = "postgres"
    secret_key: str = "OI3U4OIU3OIU4"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"    #TODO -- i think there are some issues reading in the .env

settings = Settings()

print(settings.access_token_expire_minutes)


   