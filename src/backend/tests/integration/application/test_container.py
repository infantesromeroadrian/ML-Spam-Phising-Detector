"""Integration tests for DI Container."""

from pathlib import Path

import pytest

from src.spam_detector.application import Container
from src.spam_detector.application.use_cases import (
    ClassifyEmailUseCase,
    ListModelsUseCase,
)
from src.spam_detector.config import Settings
from src.spam_detector.domain.services import EmailClassifierService
from src.spam_detector.infrastructure.adapters import (
    JoblibModelLoader,
    JsonFormatter,
    SklearnPredictor,
    TextFormatter,
)


@pytest.fixture
def container():
    """Container with test settings."""
    settings = Settings(models_dir=Path("models"))
    return Container(settings=settings)


@pytest.mark.integration
class TestContainer:
    """Test dependency injection container."""

    def test_get_model_loader(self, container):
        """Should create and cache model loader."""
        loader1 = container.get_model_loader()
        loader2 = container.get_model_loader()

        assert isinstance(loader1, JoblibModelLoader)
        assert loader1 is loader2  # Same instance (singleton)

    def test_get_spam_predictor(self, container):
        """Should create and cache spam predictor."""
        pred1 = container.get_spam_predictor()
        pred2 = container.get_spam_predictor()

        assert isinstance(pred1, SklearnPredictor)
        assert pred1 is pred2  # Same instance

    def test_get_phishing_predictor(self, container):
        """Should create phishing predictor or fallback to spam."""
        predictor = container.get_phishing_predictor()

        assert isinstance(predictor, SklearnPredictor)
        # May be same as spam predictor if phishing doesn't exist

    def test_get_classifier_service(self, container):
        """Should create and cache classifier service."""
        service1 = container.get_classifier_service()
        service2 = container.get_classifier_service()

        assert isinstance(service1, EmailClassifierService)
        assert service1 is service2  # Same instance

    def test_get_formatter_text(self, container):
        """Should create text formatter."""
        formatter = container.get_formatter(format_type="text")

        assert isinstance(formatter, TextFormatter)

    def test_get_formatter_json(self, container):
        """Should create JSON formatter."""
        formatter = container.get_formatter(format_type="json")

        assert isinstance(formatter, JsonFormatter)

    def test_get_formatter_default(self, container):
        """Should use default format from settings."""
        formatter = container.get_formatter()

        # Default is 'text'
        assert isinstance(formatter, TextFormatter)

    def test_get_classify_use_case(self, container):
        """Should create classify use case with all dependencies."""
        use_case = container.get_classify_use_case()

        assert isinstance(use_case, ClassifyEmailUseCase)

    def test_get_list_models_use_case(self, container):
        """Should create list models use case."""
        use_case = container.get_list_models_use_case()

        assert isinstance(use_case, ListModelsUseCase)

    def test_clear_cache(self, container):
        """Should clear all cached instances."""
        # Load some instances
        container.get_spam_predictor()
        container.get_classifier_service()

        # Clear
        container.clear_cache()

        # Should be None
        assert container._spam_predictor is None
        assert container._classifier_service is None


@pytest.mark.integration
class TestContainerEndToEnd:
    """Test complete workflow through container."""

    def test_classify_email_workflow(self, container):
        """Should execute complete classification workflow."""
        use_case = container.get_classify_use_case(format_type="text")

        result = use_case.execute(email_text="WINNER! You have won $1000!", detail_level="simple")

        assert isinstance(result, str)
        assert len(result) > 0

    def test_list_models_workflow(self, container):
        """Should execute list models workflow."""
        use_case = container.get_list_models_use_case()

        models = use_case.execute("spam_detector")

        assert isinstance(models, list)

    def test_json_output_workflow(self, container):
        """Should produce valid JSON output."""
        import json

        use_case = container.get_classify_use_case(format_type="json")

        result = use_case.execute(email_text="Test email", detail_level="simple")

        # Should be valid JSON
        data = json.loads(result)
        assert "verdict" in data
