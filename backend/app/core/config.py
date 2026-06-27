"""
Configuración central de AURA usando pydantic-settings
"""
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    # ─── App ──────────────────────────────────────────────────────────────────
    APP_NAME: str = "AURA"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # ─── JWT ──────────────────────────────────────────────────────────────────
    SECRET_KEY: str = "CAMBIA_ESTO_EN_PRODUCCION_usa_openssl_rand_hex_32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días

    # ─── Base de datos ────────────────────────────────────────────────────────
    # POSTGRES_* se definen primero para que el validator de DATABASE_URL los tenga
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "aura_user"
    POSTGRES_PASSWORD: str = "aura_pass"
    POSTGRES_DB: str = "aura_db"
    POSTGRES_PORT: str = "5432"
    # Railway inyecta DATABASE_URL directamente; si no, se construye desde partes
    DATABASE_URL: Optional[str] = None

    @validator("DATABASE_URL", pre=True, always=True)
    def assemble_db_url(cls, v, values):
        if v:
            return v.replace("postgres://", "postgresql://", 1)
        return (
            f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}"
            f"@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"
        )

    # ─── CORS ─────────────────────────────────────────────────────────────────
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "https://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "capacitor://localhost",
        "ionic://localhost",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
