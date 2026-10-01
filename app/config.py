from pydantic_settings import BaseSettings


class Settings(BaseSettings): 
    #provide all the environment variables that we want set 
    database_hostname: str 
    database_port: str 
    database_password: str 
    database_name: str 
    database_username: str 
    secret_key: str 
    algorithm: str 
    access_token_expire_minutes: int

    class Config:
        env_file = ".env" #tell pydantics to run the env file


settings = Settings()
