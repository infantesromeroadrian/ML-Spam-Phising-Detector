"""Unit tests for ModelMetadata entity."""

from src.spam_detector.domain.entities import ModelMetadata
import pytest
class TestModelMetadataCreation:
    """Test ModelMetadata creation."""

    def test_create_spam_detector_metadata(self):
        """Should create metadata for spam detector."""
        meta = ModelMetadata(
            name="spam_detector",
            timestamp="20260105_194125",
            accuracy=0.974,
            train_samples=4457,
            vocabulary_size=3000,
            file_size_mb=0.135,
        )
        assert meta.name == "spam_detector"
        assert meta.timestamp == "20260105_194125"
        assert meta.accuracy == 0.974
        assert meta.train_samples == 4457

    def test_create_phishing_detector_metadata(self):
        """Should create metadata for phishing detector."""
        meta = ModelMetadata(
            name="phishing_detector",
            timestamp="20260105_195830",
            accuracy=0.981,
            train_samples=65989,
            vocabulary_size=5000,
            file_size_mb=0.245,
        )
        assert meta.name == "phishing_detector"

    def test_metadata_is_immutable(self):
        """Should not allow modification after creation."""
        meta = ModelMetadata(
            name="spam_detector",
            timestamp="20260105_194125",
            accuracy=0.974,
            train_samples=4457,
            vocabulary_size=3000,
            file_size_mb=0.135,
        )
        with pytest.raises(AttributeError):
            meta.accuracy = 0.99  # type: ignore


class TestModelMetadataValidation:
    """Test ModelMetadata validation."""

    def test_accuracy_above_one_raises_error(self):
        """Should raise ValueError for accuracy > 1."""
        with pytest.raises(ValueError, match="between 0 and 1"):
            ModelMetadata(
                name="spam_detector",
                timestamp="20260105_194125",
                accuracy=1.5,
                train_samples=4457,
                vocabulary_size=3000,
                file_size_mb=0.135,
            )

    def test_accuracy_below_zero_raises_error(self):
        """Should raise ValueError for accuracy < 0."""
        with pytest.raises(ValueError, match="between 0 and 1"):
            ModelMetadata(
                name="spam_detector",
                timestamp="20260105_194125",
                accuracy=-0.1,
                train_samples=4457,
                vocabulary_size=3000,
                file_size_mb=0.135,
            )

    def test_negative_train_samples_raises_error(self):
        """Should raise ValueError for negative samples."""
        with pytest.raises(ValueError, match="must be positive"):
            ModelMetadata(
                name="spam_detector",
                timestamp="20260105_194125",
                accuracy=0.974,
                train_samples=-100,
                vocabulary_size=3000,
                file_size_mb=0.135,
            )

    def test_zero_vocabulary_raises_error(self):
        """Should raise ValueError for zero vocabulary."""
        with pytest.raises(ValueError, match="must be positive"):
            ModelMetadata(
                name="spam_detector",
                timestamp="20260105_194125",
                accuracy=0.974,
                train_samples=4457,
                vocabulary_size=0,
                file_size_mb=0.135,
            )


class TestModelMetadataProperties:
    """Test ModelMetadata computed properties."""

    def test_accuracy_percent(self):
        """Should convert accuracy to percentage."""
        meta = ModelMetadata(
            name="spam_detector",
            timestamp="20260105_194125",
            accuracy=0.974,
            train_samples=4457,
            vocabulary_size=3000,
            file_size_mb=0.135,
        )
        assert abs(meta.accuracy_percent - 97.4) < 0.001

    def test_display_name_spam(self):
        """Should return human-readable name for spam detector."""
        meta = ModelMetadata(
            name="spam_detector",
            timestamp="20260105_194125",
            accuracy=0.974,
            train_samples=4457,
            vocabulary_size=3000,
            file_size_mb=0.135,
        )
        assert meta.display_name == "SPAM Detector"

    def test_display_name_phishing(self):
        """Should return human-readable name for phishing detector."""
        meta = ModelMetadata(
            name="phishing_detector",
            timestamp="20260105_195830",
            accuracy=0.981,
            train_samples=65989,
            vocabulary_size=5000,
            file_size_mb=0.245,
        )
        assert meta.display_name == "Phishing Detector"
