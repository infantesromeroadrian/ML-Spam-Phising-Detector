"""List available models use case."""

from ...domain.entities import ModelMetadata, ModelType
from ...domain.ports import IModelLoader


class ListModelsUseCase:
    """
    Use case: List available model versions.

    Provides information about available trained models,
    including their metadata (accuracy, version, etc.).

    Attributes:
        _model_loader: Loader for accessing model metadata

    Examples:
        >>> use_case = ListModelsUseCase(loader)
        >>> models = use_case.execute("spam_detector")
        >>> for model in models:
        ...     print(f"{model.timestamp}: {model.accuracy_percent:.2f}%")
    """

    def __init__(self, model_loader: IModelLoader) -> None:
        """
        Initialize use case with model loader.

        Args:
            model_loader: Loader implementation for model access
        """
        self._model_loader = model_loader

    def execute(self, model_name: ModelType) -> list[ModelMetadata]:
        """
        List all available versions of a model.

        Args:
            model_name: Name of model to list ('spam_detector' or 'phishing_detector')

        Returns:
            List of ModelMetadata, sorted by timestamp (newest first)

        Raises:
            ValueError: If model_name is invalid
        """
        return self._model_loader.list_available(model_name)

    def get_latest(self, model_name: ModelType) -> ModelMetadata | None:
        """
        Get metadata for latest version of a model.

        Args:
            model_name: Name of model

        Returns:
            ModelMetadata for latest version, or None if no models exist
        """
        models = self.execute(model_name)
        return models[0] if models else None

    def format_summary(self, model_name: ModelType) -> str:
        """
        Get formatted summary of available models.

        Args:
            model_name: Name of model

        Returns:
            Human-readable summary string
        """
        models = self.execute(model_name)

        if not models:
            return f"No models found for '{model_name}'"

        lines = [f"Available models for '{model_name}':", f"Total versions: {len(models)}", ""]

        for i, model in enumerate(models, 1):
            latest_mark = " (latest)" if i == 1 else ""
            lines.append(
                f"{i}. {model.timestamp}{latest_mark}"
                f" - Accuracy: {model.accuracy_percent:.2f}%"
                f" - Size: {model.file_size_mb:.2f}MB"
            )

        return "\n".join(lines)
