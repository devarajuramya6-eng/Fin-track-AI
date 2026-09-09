from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application Info
    APP_NAME: str = "AI FinTech Personal Finance & Risk Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Host & Ports
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:5173"

    # CORS Origins
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
    ]

    # Database Configuration
    # Defaults to SQLite for immediate out-of-the-box local developer convenience without Docker
    DATABASE_URL: str = "sqlite+aiosqlite:///./fintech.db"
    DATABASE_SYNC_URL: str = "sqlite:///./fintech.db"

    # Security & Tokens
    SECRET_KEY: str = "dev-secret-key-super-secure-min-32-chars-long-example-solo-dev"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 120

    # Local AI & Risk Engine Configurations
    AI_ANOMALY_ZSCORE_THRESHOLD: float = 2.5
    AI_ANOMALY_IQR_MULTIPLIER: float = 1.5
    AI_RISK_CACHE_TTL_SECONDS: int = 300

    # Demo Data
    SEED_DEMO_DATA_ON_STARTUP: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
