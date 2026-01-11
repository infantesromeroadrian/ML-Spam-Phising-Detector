"""Integration tests for JoblibModelLoader."""

from pathlib import Path

from spam_detector.domain.entities import ModelMetadata
from spam_detector.infrastructure.adapters import JoblibModelLoader
import pytest

@pytest.fixture
def models_dir() -> Path:
    """Path to actual models directory."""
    return Path("models")


@pytest.fixture
def loader(models_dir: Path) -> JoblibModelLoader:
    """JoblibModelLoader instance."""
    return JoblibModelLoader(models_dir=models_dir)


class TestJoblibModelLoaderInit:
    """Test loader initialization."""

    def test_init_with_valid_directory(self, models_dir):
        """Should initialize with existing directory."""
        loader = JoblibModelLoader(models_dir=models_dir)
        assert loader._models_dir == models_dir
        assert loader._cache == {}

    def test_init_with_invalid_directory_raises_error(self):
        """Should raise ValueError for non-existent directory."""
        with pytest.raises(ValueError, match="does not exist"):
            JoblibModelLoader(models_dir=Path("/nonexistent/path"))


@pytest.mark.integration
class TestJoblibModelLoaderLoad:
    """Test loading models from disk."""

    def test_load_spam_detector_latest(self, loader):
        """Should load latest spam detector model."""
        vectorizer, model, metadata = loader.load("spam_detector")

        # Check components loaded
        assert vectorizer is not None
        assert model is not None
        assert isinstance(metadata, ModelMetadata)

        # Check metadata
        assert metadata.name == "spam_detector"
        assert metadata.timestamp
        assert 0.0 <= metadata.accuracy <= 1.0
        assert metadata.train_samples > 0
        assert metadata.vocabulary_size > 0

    def test_load_specific_timestamp(self, loader):
        """Should load model with specific timestamp."""
        # Get available models first
        models = loader.list_available("spam_detector")
        if not models:
            pytest.skip("No spam models available")

        # Load specific version
        timestamp = models[0].timestamp
        vectorizer, model, metadata = loader.load("spam_detector", timestamp=timestamp)

        assert metadata.timestamp == timestamp

    def test_load_caches_model(self, loader):
        """Should cache loaded model for reuse."""
        # First load
        vec1, model1, meta1 = loader.load("spam_detector")

        # Second load (should come from cache)
        vec2, model2, meta2 = loader.load("spam_detector")

        # Should be same objects (cached)
        assert vec1 is vec2
        assert model1 is model2
        assert meta1 is meta2

    def test_load_invalid_model_name_raises_error(self, loader):
        """Should raise ValueError for invalid model name."""
        with pytest.raises(ValueError, match="Invalid model_name"):
            loader.load("invalid_model")

    def test_load_nonexistent_timestamp_raises_error(self, loader):
        """Should raise FileNotFoundError for missing timestamp."""
        with pytest.raises(FileNotFoundError):
            loader.load("spam_detector", timestamp="99999999_999999")


@pytest.mark.integration
class TestJoblibModelLoaderListAvailable:
    """Test listing available models."""

    def test_list_spam_detector_models(self, loader):
        """Should list available spam detector models."""
        models = loader.list_available("spam_detector")

        assert isinstance(models, list)
        if models:  # If any models exist
            assert all(isinstance(m, ModelMetadata) for m in models)
            assert all(m.name == "spam_detector" for m in models)

            # Check sorted newest first
            if len(models) > 1:
                timestamps = [m.timestamp for m in models]
                assert timestamps == sorted(timestamps, reverse=True)

    def test_list_phishing_detector_models(self, loader):
        """Should list available phishing detector models."""
        models = loader.list_available("phishing_detector")

        assert isinstance(models, list)
        # May be empty if no phishing models trained yet

    def test_list_invalid_model_name_raises_error(self, loader):
        """Should raise ValueError for invalid model name."""
        with pytest.raises(ValueError, match="Invalid model_name"):
            loader.list_available("invalid_model")


@pytest.mark.integration
class TestJoblibModelLoaderCache:
    """Test cache functionality."""

    def test_clear_cache(self, loader):
        """Should clear cached models."""
        # Load model (caches it)
        loader.load("spam_detector")
        assert len(loader._cache) > 0

        # Clear cache
        loader.clear_cache()
        assert len(loader._cache) == 0
