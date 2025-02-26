from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Configuration settings for the application."""

    # Router configuration
    API_PREFIX: str = "/api/v1"  # Base path for all endpoints
    API_TAGS: List[str] = ["Text Generation"]  # Organize routes by feature

    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["*"]  # Update with frontend domain in production
    ALLOWED_METHODS: List[str] = ["POST"]  # Only allow POST requests
    ALLOWED_HEADERS: List[str] = ["*"]

    # Model Configuration
    MODEL_NAME: str = "Qwen-2.5-0.5B-Instruct"
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH: str = os.path.join(BASE_DIR, "models/Qwen2.5-0.5B-Instruct")

    # Generation Default
    SYSTEM_PROMPT: str = "You are an AI assistant designed to provide accurate, helpful, and relevant responses. You communicate clearly and professionally while maintaining a friendly tone. If a question is ambiguous, ask for clarification. When providing answers, prioritize factual correctness and user safety. If a request is out of scope or inappropriate, politely decline while suggesting alternatives where possible."
    MAX_NEW_TOKENS: int = 512  # Default max tokens (adjust as needed)
    DO_SAMPLE: bool = True
    TOP_K: int = 50  # Default value; override as needed
    TOP_P: float = 0.9  # Default nucleus sampling probability
    TEMPERATURE: float = 0.7  # Default temperature for randomness
    MAX_CONTEXT_LENGTH: int = 32768  # Model's max context size

    # Logging Settings
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"  # Load values from a .env file (optional)
        env_file_encoding = "utf-8"

# Create a global settings instance
settings = Settings()
