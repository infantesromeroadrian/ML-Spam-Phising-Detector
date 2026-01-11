"""Integration tests for DI Container."""

from pathlib import Path

import pytest

from spam_detector.application import Container
from spam_detector.application.use_cases import (
    ClassifyEmailUseCase,
    ListModelsUseCase,
)


class TestContainer:
    """Test DI Container integration."""

    def test_container_initialization(self, tmp_path: Path):
        """Test container can be initialized."""
        # Create dummy model files
        models_dir = tmp_path / "models"
        models_dir.mkdir()

        # Create minimal model files
        for model_type in ["spam_detector", "phishing_detector"]:
            for suffix in ["model", "vectorizer", "metadata"]:
                file_path = models_dir / f"{model_type}_{suffix}_latest.joblib"
                file_path.write_text("dummy")

        # Initialize container
        container = Container(models_dir=models_dir)

        assert container is not None
        assert container._models_dir == models_dir

    def test_container_provides_use_cases(self, tmp_path: Path):
        """Test container provides use cases."""
        # Create dummy model files
        models_dir = tmp_path / "models"
        models_dir.mkdir()

        for model_type in ["spam_detector", "phishing_detector"]:
            for suffix in ["model", "vectorizer", "metadata"]:
                file_path = models_dir / f"{model_type}_{suffix}_latest.joblib"
                file_path.write_text("dummy")

        container = Container(models_dir=models_dir)

        # Test ClassifyEmailUseCase
        classify_use_case = container.classify_email_use_case()
        assert isinstance(classify_use_case, ClassifyEmailUseCase)

        # Test ListModelsUseCase
        list_models_use_case = container.list_models_use_case()
        assert isinstance(list_models_use_case, ListModelsUseCase)
