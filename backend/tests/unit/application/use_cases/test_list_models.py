"""Unit tests for ListModelsUseCase."""

from unittest.mock import Mock

import pytest

from src.spam_detector.application.use_cases import ListModelsUseCase
from src.spam_detector.domain.entities import ModelMetadata


@pytest.fixture
def mock_model_loader():
    """Mock model loader."""
    loader = Mock()

    # Mock available models
    models = [
        ModelMetadata(
            name="spam_detector",
            timestamp="20260105_194125",
            accuracy=0.974,
            train_samples=4457,
            vocabulary_size=3000,
            file_size_mb=0.135,
        ),
        ModelMetadata(
            name="spam_detector",
            timestamp="20260104_120000",
            accuracy=0.968,
            train_samples=4000,
            vocabulary_size=2500,
            file_size_mb=0.120,
        ),
    ]

    loader.list_available.return_value = models
    return loader


@pytest.fixture
def use_case(mock_model_loader):
    """ListModelsUseCase with mock loader."""
    return ListModelsUseCase(model_loader=mock_model_loader)


class TestListModelsUseCase:
    """Test ListModelsUseCase."""

    def test_execute_calls_loader(self, use_case, mock_model_loader):
        """Should call loader.list_available."""
        use_case.execute("spam_detector")

        mock_model_loader.list_available.assert_called_once_with("spam_detector")

    def test_execute_returns_model_list(self, use_case):
        """Should return list of ModelMetadata."""
        models = use_case.execute("spam_detector")

        assert isinstance(models, list)
        assert len(models) == 2
        assert all(isinstance(m, ModelMetadata) for m in models)

    def test_get_latest_returns_first_model(self, use_case):
        """Should return first model (newest)."""
        latest = use_case.get_latest("spam_detector")

        assert latest is not None
        assert latest.timestamp == "20260105_194125"

    def test_get_latest_with_empty_list_returns_none(self, mock_model_loader):
        """Should return None if no models available."""
        mock_model_loader.list_available.return_value = []
        use_case = ListModelsUseCase(mock_model_loader)

        latest = use_case.get_latest("spam_detector")

        assert latest is None

    def test_format_summary_with_models(self, use_case):
        """Should format summary string for available models."""
        summary = use_case.format_summary("spam_detector")

        assert "spam_detector" in summary
        assert "Total versions: 2" in summary
        assert "20260105_194125" in summary
        assert "(latest)" in summary
        assert "97.40%" in summary

    def test_format_summary_with_no_models(self, mock_model_loader):
        """Should handle case with no models."""
        mock_model_loader.list_available.return_value = []
        use_case = ListModelsUseCase(mock_model_loader)

        summary = use_case.format_summary("spam_detector")

        assert "No models found" in summary
