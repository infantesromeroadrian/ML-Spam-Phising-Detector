"""Model metadata entity."""

from dataclasses import dataclass
from typing import Literal

ModelType = Literal["spam_detector", "phishing_detector"]


@dataclass(frozen=True)
class ModelMetadata:
    """
    Metadata for a trained classifier model.

    Immutable value object containing information about a saved model.

    Attributes:
        name: Model identifier ('spam_detector' or 'phishing_detector')
        timestamp: Model version timestamp (format: YYYYMMDD_HHMMSS)
        accuracy: Model accuracy on test set (0.0 - 1.0)
        train_samples: Number of samples used for training
        vocabulary_size: Size of TF-IDF vocabulary
        file_size_mb: Model file size in megabytes

    Examples:
        >>> metadata = ModelMetadata(
        ...     name="spam_detector",
        ...     timestamp="20260105_194125",
        ...     accuracy=0.974,
        ...     train_samples=4457,
        ...     vocabulary_size=3000,
        ...     file_size_mb=0.135
        ... )
    """

    name: ModelType
    timestamp: str
    accuracy: float
    train_samples: int
    vocabulary_size: int
    file_size_mb: float

    def __post_init__(self) -> None:
        """Validate metadata constraints."""
        if not 0.0 <= self.accuracy <= 1.0:
            raise ValueError(f"Accuracy must be between 0 and 1, got {self.accuracy}")

        if self.train_samples <= 0:
            raise ValueError(f"Train samples must be positive, got {self.train_samples}")

        if self.vocabulary_size <= 0:
            raise ValueError(f"Vocabulary size must be positive, got {self.vocabulary_size}")

        if self.file_size_mb < 0:
            raise ValueError(f"File size cannot be negative, got {self.file_size_mb}")

    @property
    def accuracy_percent(self) -> float:
        """Get accuracy as percentage."""
        return self.accuracy * 100

    @property
    def display_name(self) -> str:
        """Get human-readable model name."""
        names = {"spam_detector": "SPAM Detector", "phishing_detector": "Phishing Detector"}
        return names.get(self.name, self.name)
