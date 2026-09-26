from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    database_url: str
    upstash_redis_url: str
    upstash_redis_token: str
    hf_token: str
    hf_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    groq_api_key: str
    groq_model: str = "openai/gpt-oss-120b"
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")

settings = Settings()
