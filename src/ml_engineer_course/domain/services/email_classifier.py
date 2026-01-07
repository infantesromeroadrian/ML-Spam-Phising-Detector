"""Email classifier service - Domain service orchestrating classification."""

import time

from ..entities import ClassificationResult, Email
from ..ports import IPredictor


class EmailClassifierService:
    """
    Domain service for dual email classification.

    Orchestrates spam and phishing detection on emails,
    combining predictions from both classifiers.

    This is a pure domain service with no infrastructure dependencies.
    It coordinates the classification workflow using injected predictors.

    Attributes:
        _spam_predictor: Predictor for spam detection
        _phishing_predictor: Predictor for phishing detection

    Examples:
        >>> service = EmailClassifierService(
        ...     spam_predictor=spam_pred,
        ...     phishing_predictor=phishing_pred
        ... )
        >>> email = Email(text="WINNER! Click here NOW!")
        >>> result = service.classify(email)
        >>> result.final_verdict
        'SPAM+PHISHING'
    """

    def __init__(self, spam_predictor: IPredictor, phishing_predictor: IPredictor) -> None:
        """
        Initialize classifier service with predictors.

        Args:
            spam_predictor: Predictor implementing spam detection
            phishing_predictor: Predictor implementing phishing detection
        """
        self._spam_predictor = spam_predictor
        self._phishing_predictor = phishing_predictor

    def classify(self, email: Email) -> ClassificationResult:
        """
        Classify email with both spam and phishing detectors.

        Args:
            email: Email entity to classify

        Returns:
            ClassificationResult with dual predictions and metadata

        Raises:
            ValueError: If email is invalid or cannot be processed
        """
        start_time = time.perf_counter()

        # Run both predictions
        spam_prediction = self._spam_predictor.predict(email)
        phishing_prediction = self._phishing_predictor.predict(email)

        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) * 1000

        return ClassificationResult(
            email=email,
            spam_prediction=spam_prediction,
            phishing_prediction=phishing_prediction,
            execution_time_ms=execution_time_ms,
        )
