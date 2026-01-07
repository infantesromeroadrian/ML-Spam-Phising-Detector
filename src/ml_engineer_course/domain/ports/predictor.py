"""Predictor port - Interface for making predictions."""

from typing import Protocol

from ..entities import Email, SinglePrediction


class IPredictor(Protocol):
    """
    Port for email classification prediction.

    This protocol defines the interface for making predictions
    on email content. Implementations wrap specific ML frameworks
    (sklearn, PyTorch, TensorFlow, etc.).

    Examples:
        >>> predictor: IPredictor = SklearnPredictor(
        ...     vectorizer=vec,
        ...     model=clf,
        ...     metadata=meta,
        ...     model_type="spam"
        ... )
        >>> prediction = predictor.predict(Email(text="Win $1000!"))
        >>> prediction.label
        'SPAM'
        >>> prediction.probability
        0.85
    """

    def predict(self, email: Email) -> SinglePrediction:
        """
        Predict classification for an email.

        Args:
            email: Email entity to classify

        Returns:
            SinglePrediction with label, probability, and model info

        Raises:
            ValueError: If email text cannot be vectorized
        """
        ...
