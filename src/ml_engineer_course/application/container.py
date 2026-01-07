"""Dependency injection container."""

from typing import Literal

from ..config import Settings
from ..domain.services import EmailClassifierService
from ..infrastructure.adapters import (
    JoblibModelLoader,
    JsonFormatter,
    SklearnPredictor,
    TextFormatter,
)
from .use_cases import ClassifyEmailUseCase, ListModelsUseCase


class Container:
    """
    Dependency injection container.

    Responsible for wiring up all dependencies and creating
    properly configured instances of use cases.

    This implements the Composition Root pattern, centralizing
    all object creation and dependency management.

    Examples:
        >>> container = Container()
        >>> classify_use_case = container.get_classify_use_case()
        >>> result = classify_use_case.execute("WINNER! Click here!")
    """

    def __init__(self, settings: Settings | None = None) -> None:
        """
        Initialize container with settings.

        Args:
            settings: Application settings. If None, uses global settings.
        """
        from ..config import settings as global_settings

        self._settings = settings or global_settings
        self._model_loader: JoblibModelLoader | None = None
        self._spam_predictor: SklearnPredictor | None = None
        self._phishing_predictor: SklearnPredictor | None = None
        self._classifier_service: EmailClassifierService | None = None

    def get_model_loader(self) -> JoblibModelLoader:
        """Get or create model loader (singleton)."""
        if self._model_loader is None:
            self._model_loader = JoblibModelLoader(models_dir=self._settings.get_models_path())
        return self._model_loader

    def get_spam_predictor(self) -> SklearnPredictor:
        """Get or create spam predictor (singleton)."""
        if self._spam_predictor is None:
            loader = self.get_model_loader()
            vectorizer, model, metadata = loader.load("spam_detector")

            self._spam_predictor = SklearnPredictor(
                vectorizer=vectorizer, model=model, metadata=metadata, predictor_type="spam"
            )
        return self._spam_predictor

    def get_phishing_predictor(self) -> SklearnPredictor:
        """Get or create phishing predictor (singleton)."""
        if self._phishing_predictor is None:
            loader = self.get_model_loader()

            try:
                vectorizer, model, metadata = loader.load("phishing_detector")

                self._phishing_predictor = SklearnPredictor(
                    vectorizer=vectorizer, model=model, metadata=metadata, predictor_type="phishing"
                )
            except FileNotFoundError:
                # Fallback: use spam detector for both if phishing doesn't exist
                if self._settings.verbose:
                    print("Warning: phishing_detector not found, using spam_detector")
                self._phishing_predictor = self.get_spam_predictor()

        return self._phishing_predictor

    def get_classifier_service(self) -> EmailClassifierService:
        """Get or create classifier service (singleton)."""
        if self._classifier_service is None:
            self._classifier_service = EmailClassifierService(
                spam_predictor=self.get_spam_predictor(),
                phishing_predictor=self.get_phishing_predictor(),
            )
        return self._classifier_service

    def get_formatter(
        self, format_type: Literal["text", "json"] | None = None
    ) -> TextFormatter | JsonFormatter:
        """
        Get formatter instance.

        Args:
            format_type: "text" or "json". If None, uses setting default.

        Returns:
            Formatter instance (not cached, creates new each time)
        """
        fmt = format_type or self._settings.default_format

        if fmt == "json":
            return JsonFormatter()
        else:
            return TextFormatter()

    def get_classify_use_case(
        self, format_type: Literal["text", "json"] | None = None
    ) -> ClassifyEmailUseCase:
        """
        Get classify email use case.

        Args:
            format_type: Output format. If None, uses setting default.

        Returns:
            Configured ClassifyEmailUseCase instance
        """
        return ClassifyEmailUseCase(
            classifier_service=self.get_classifier_service(),
            formatter=self.get_formatter(format_type),
        )

    def get_list_models_use_case(self) -> ListModelsUseCase:
        """Get list models use case."""
        return ListModelsUseCase(model_loader=self.get_model_loader())

    def clear_cache(self) -> None:
        """Clear all cached instances and model cache."""
        if self._model_loader:
            self._model_loader.clear_cache()

        self._spam_predictor = None
        self._phishing_predictor = None
        self._classifier_service = None


# Global container instance (can be overridden)
container = Container()
