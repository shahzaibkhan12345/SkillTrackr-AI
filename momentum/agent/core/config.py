# agent/core/config.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # We are only using Gemini for now
    GEMINI_API_KEY: str | None = None
    SERPAPI_KEY: str | None = None

    # This tells Pydantic to ignore any extra variables in the .env file
    model_config = SettingsConfigDict(extra='ignore', env_file='.env')

# Create a single settings instance to be used across the application
settings = Settings()