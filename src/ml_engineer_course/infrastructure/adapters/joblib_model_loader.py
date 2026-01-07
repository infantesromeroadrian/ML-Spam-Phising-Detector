"""Joblib model loader - Loads models from .joblib files."""

from pathlib import Path
from typing import Any

import joblib

from ...domain.entities import ModelMetadata


class JoblibModelLoader:
    """
    Load ML models from joblib files with caching.

    Implements IModelLoader port for loading models serialized
    with joblib. Supports model versioning via timestamps and
    caches loaded models in memory for performance.

    Attributes:
        _models_dir: Directory containing model files
        _cache: In-memory cache of loaded models

    Examples:
        >>> loader = JoblibModelLoader(models_dir=Path("models"))
        >>> vec, model, meta = loader.load("spam_detector")
        >>> models = loader.list_available("spam_detector")
    """

    def __init__(self, models_dir: Path) -> None:
        """
        Initialize loader with models directory.

        Args:
            models_dir: Path to directory containing .joblib model files

        Raises:
            ValueError: If models_dir doesn't exist
        """
        if not models_dir.exists():
            raise ValueError(f"Models directory does not exist: {models_dir}")

        self._models_dir = models_dir
        self._cache: dict[str, tuple[Any, Any, ModelMetadata]] = {}

    def load(self, model_name: str, timestamp: str | None = None) -> tuple[Any, Any, ModelMetadata]:
        """
        Load a trained model with its components.

        Args:
            model_name: Name of model ('spam_detector' or 'phishing_detector')
            timestamp: Specific version timestamp. If None, loads most recent.

        Returns:
            Tuple of (vectorizer, model, metadata)

        Raises:
            FileNotFoundError: If model files not found
            ValueError: If model_name is invalid
        """
        self._validate_model_name(model_name)

        # Check cache first
        cache_key = f"{model_name}_{timestamp or 'latest'}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Determine timestamp
        if timestamp is None:
            timestamp = self._get_latest_timestamp(model_name)

        # Load components
        vectorizer = self._load_component(model_name, "vectorizer", timestamp)
        model = self._load_component(model_name, "model", timestamp)
        metadata_dict = self._load_component(model_name, "metadata", timestamp)

        # Build metadata entity
        metadata = self._build_metadata(model_name, metadata_dict)

        # Cache and return
        result = (vectorizer, model, metadata)
        self._cache[cache_key] = result
        return result

    def list_available(self, model_name: str) -> list[ModelMetadata]:
        """
        List all available versions of a model.

        Args:
            model_name: Name of model to list

        Returns:
            List of ModelMetadata for all versions, newest first

        Raises:
            ValueError: If model_name is invalid
        """
        self._validate_model_name(model_name)

        # Find all model files
        pattern = f"{model_name}_model_*.joblib"
        model_files = sorted(
            self._models_dir.glob(pattern),
            reverse=True,  # Newest first
        )

        if not model_files:
            return []

        # Load metadata for each version
        metadatas: list[ModelMetadata] = []
        for model_file in model_files:
            timestamp = self._extract_timestamp(model_file)
            try:
                metadata_dict = self._load_component(model_name, "metadata", timestamp)
                metadata = self._build_metadata(model_name, metadata_dict)
                metadatas.append(metadata)
            except FileNotFoundError:
                continue  # Skip if metadata missing

        return metadatas

    def clear_cache(self) -> None:
        """Clear the in-memory model cache."""
        self._cache.clear()

    # === Private methods ===

    def _validate_model_name(self, model_name: str) -> None:
        """Validate model name is supported."""
        valid_names = {"spam_detector", "phishing_detector"}
        if model_name not in valid_names:
            raise ValueError(f"Invalid model_name '{model_name}'. Must be one of: {valid_names}")

    def _get_latest_timestamp(self, model_name: str) -> str:
        """Get timestamp of most recent model version."""
        model_files = sorted(self._models_dir.glob(f"{model_name}_model_*.joblib"), reverse=True)

        if not model_files:
            raise FileNotFoundError(f"No models found for '{model_name}' in {self._models_dir}")

        return self._extract_timestamp(model_files[0])

    def _extract_timestamp(self, model_path: Path) -> str:
        """Extract timestamp from model filename."""
        # Example: spam_detector_model_20260105_194125.joblib
        # Extract: 20260105_194125
        parts = model_path.stem.split("_")
        return "_".join(parts[-2:])

    def _load_component(self, model_name: str, component: str, timestamp: str) -> Any:
        """Load a specific model component from disk."""
        filename = f"{model_name}_{component}_{timestamp}.joblib"
        filepath = self._models_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Component file not found: {filepath}")

        return joblib.load(filepath)

    def _build_metadata(self, model_name: str, metadata_dict: dict) -> ModelMetadata:
        """Build ModelMetadata entity from loaded dict."""
        # Get file size
        model_file = self._models_dir / (f"{model_name}_model_{metadata_dict['timestamp']}.joblib")
        file_size_mb = model_file.stat().st_size / (1024 * 1024)

        return ModelMetadata(
            name=model_name,  # type: ignore
            timestamp=metadata_dict["timestamp"],
            accuracy=metadata_dict["accuracy"],
            train_samples=metadata_dict["train_samples"],
            vocabulary_size=metadata_dict["vocabulary_size"],
            file_size_mb=file_size_mb,
        )
