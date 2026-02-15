from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Behavior Change Tracker"
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-opus-20240229"

    class Config:
        env_file = ".env"

settings = Settings()
