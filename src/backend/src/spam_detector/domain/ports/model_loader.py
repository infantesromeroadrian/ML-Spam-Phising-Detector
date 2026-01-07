"""Model loader port - Interface for loading ML models."""

from typing import Any, Protocol

from ..entities import ModelMetadata


class IModelLoader(Protocol):
    """
    Port for loading machine learning models.

    This protocol defines the interface for loading trained models
    from persistent storage. Implementations can use different
    serialization formats (joblib, pickle, ONNX, etc.).

    Examples:
        >>> loader: IModelLoader = JoblibModelLoader(models_dir=Path("models"))
        >>> vectorizer, model, metadata = loader.load("spam_detector")
        >>> models = loader.list_available("spam_detector")
    """

    def load(self, model_name: str, timestamp: str | None = None) -> tuple[Any, Any, ModelMetadata]:
        """
        Load a trained model with its components.

        Args:
            model_name: Name of model ('spam_detector' or 'phishing_detector')
            timestamp: Specific version timestamp. If None, loads most recent.

        Returns:
            Tuple of (vectorizer, model, metadata)
            - vectorizer: TF-IDF vectorizer (fitted)
            - model: Trained classifier (sklearn model)
            - metadata: Model metadata with training info

        Raises:
            FileNotFoundError: If model files not found
            ValueError: If model_name is invalid
        """
        ...

    def list_available(self, model_name: str) -> list[ModelMetadata]:
        """
        List all available versions of a model.

        Args:
            model_name: Name of model to list

        Returns:
            List of ModelMetadata for all available versions,
            sorted by timestamp (newest first)

        Raises:
            ValueError: If model_name is invalid
        """
        ...
