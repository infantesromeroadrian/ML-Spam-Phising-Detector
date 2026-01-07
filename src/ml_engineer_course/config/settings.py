"""Application settings using Pydantic."""

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration settings.

    Settings can be configured via:
    - Environment variables (prefixed with EMAIL_CLASSIFIER_)
    - .env file
    - Direct instantiation

    Examples:
        >>> settings = Settings()
        >>> settings.models_dir
        PosixPath('models')

        >>> # Via env vars:
        >>> # EMAIL_CLASSIFIER_MODELS_DIR=/custom/path
        >>> # EMAIL_CLASSIFIER_DEFAULT_FORMAT=json
    """

    model_config = SettingsConfigDict(
        env_prefix="EMAIL_CLASSIFIER_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Model settings
    models_dir: Path = Field(
        default=Path("models"), description="Directory containing trained models"
    )

    cache_models: bool = Field(default=True, description="Cache loaded models in memory")

    # Output settings
    default_format: Literal["text", "json"] = Field(
        default="text", description="Default output format"
    )

    default_detail_level: Literal["simple", "detailed", "debug"] = Field(
        default="simple", description="Default detail level for output"
    )

    # Classification settings
    min_confidence_threshold: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Minimum confidence threshold for warnings"
    )

    # Risk level thresholds
    confidence_threshold_low: float = Field(
        default=0.8, ge=0.0, le=1.0, description="Threshold for LOW risk (HAM with high confidence)"
    )
    confidence_threshold_high: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Threshold for HIGH risk (single threat)"
    )

    # Model fallback behavior
    allow_model_fallback: bool = Field(
        default=True, description="Allow fallback to spam detector if phishing detector not found"
    )
    strict_mode: bool = Field(
        default=False, description="Raise error if any model is missing (no fallback)"
    )

    # Performance settings
    enable_performance_metrics: bool = Field(
        default=True, description="Include execution time in results"
    )

    # Verbose output
    verbose: bool = Field(default=False, description="Enable verbose logging")

    # API settings
    api_host: str = Field(default="0.0.0.0", description="API host address")
    api_port: int = Field(default=8000, ge=1, le=65535, description="API port")
    api_reload: bool = Field(default=False, description="Enable hot reload (dev only)")
    api_workers: int = Field(default=1, ge=1, description="Number of uvicorn workers")
    api_cors_origins: list[str] = Field(
        default=["*"], description="CORS allowed origins (use ['*'] for all)"
    )
    api_version: str = Field(default="v1", description="API version prefix")
    api_prefix: str = Field(default="/api", description="API base prefix")
    docs_path: str = Field(default="/docs", description="Swagger UI path")
    redoc_path: str = Field(default="/redoc", description="ReDoc path")
    static_path: str = Field(default="/static", description="Static files path")

    # File settings
    file_encoding: str = Field(default="utf-8", description="Default file encoding")
    json_indent: int = Field(default=2, ge=0, description="JSON output indent spaces")
    json_ensure_ascii: bool = Field(default=False, description="Ensure ASCII in JSON output")

    def get_models_path(self) -> Path:
        """Get absolute path to models directory."""
        return self.models_dir.resolve()

    @property
    def api_base_path(self) -> str:
        """Get full API base path with version."""
        return f"{self.api_prefix}/{self.api_version}"


# Global settings instance (can be overridden)
settings = Settings()
