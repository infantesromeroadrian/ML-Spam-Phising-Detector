"""Prediction result entities."""

from dataclasses import dataclass
from typing import Literal

from .email import Email

# Risk level thresholds (business rules)
RISK_THRESHOLD_LOW_CONFIDENCE = 0.8  # HAM with >80% confidence = LOW risk
RISK_THRESHOLD_HIGH_CONFIDENCE = 0.7  # Single threat >70% confidence = HIGH risk

VerdictType = Literal["HAM", "SPAM", "PHISHING", "SPAM+PHISHING"]
LabelType = Literal["HAM", "SPAM", "LEGIT", "PHISHING"]


@dataclass(frozen=True)
class SinglePrediction:
    """
    Result of a single model prediction.

    Attributes:
        label: Classification label
        probability: Confidence probability (0.0 - 1.0)
        model_name: Name of model that made prediction
        model_timestamp: Timestamp of model version used
    """

    label: LabelType
    probability: float
    model_name: str
    model_timestamp: str

    def __post_init__(self) -> None:
        """Validate probability range."""
        if not 0.0 <= self.probability <= 1.0:
            raise ValueError(f"Probability must be between 0 and 1, got {self.probability}")

    @property
    def probability_percent(self) -> float:
        """Get probability as percentage."""
        return self.probability * 100

    @property
    def is_positive(self) -> bool:
        """Check if prediction is positive (SPAM/PHISHING)."""
        return self.label in ("SPAM", "PHISHING")


@dataclass(frozen=True)
class ClassificationResult:
    """
    Complete dual classification result.

    Result from classifying an email with both spam and phishing detectors.

    Attributes:
        email: Original email that was classified
        spam_prediction: Result from spam detector
        phishing_prediction: Result from phishing detector
        execution_time_ms: Total execution time in milliseconds

    Examples:
        >>> result = ClassificationResult(
        ...     email=Email(text="WINNER! Click here"),
        ...     spam_prediction=SinglePrediction("SPAM", 0.85, "spam_detector", "..."),
        ...     phishing_prediction=SinglePrediction("PHISHING", 0.92, "phishing_detector", "..."),
        ...     execution_time_ms=45.3
        ... )
        >>> result.final_verdict
        'SPAM+PHISHING'
        >>> result.max_confidence
        0.92
    """

    email: Email
    spam_prediction: SinglePrediction
    phishing_prediction: SinglePrediction
    execution_time_ms: float

    @property
    def final_verdict(self) -> VerdictType:
        """
        Determine final verdict based on both predictions.

        Returns:
            "HAM": Both negative
            "SPAM": Only spam positive
            "PHISHING": Only phishing positive
            "SPAM+PHISHING": Both positive
        """
        spam_positive = self.spam_prediction.is_positive
        phishing_positive = self.phishing_prediction.is_positive

        if spam_positive and phishing_positive:
            return "SPAM+PHISHING"
        elif spam_positive:
            return "SPAM"
        elif phishing_positive:
            return "PHISHING"
        else:
            return "HAM"

    @property
    def max_confidence(self) -> float:
        """Get highest confidence from both predictions."""
        return max(self.spam_prediction.probability, self.phishing_prediction.probability)

    @property
    def is_malicious(self) -> bool:
        """Check if email is classified as malicious (spam or phishing)."""
        return self.final_verdict != "HAM"

    @property
    def risk_level(self) -> Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        """
        Assess risk level based on confidence and verdict.

        Returns:
            "LOW": HAM with high confidence
            "MEDIUM": HAM with low confidence or single threat low confidence
            "HIGH": Single threat high confidence
            "CRITICAL": Both threats detected
        """
        if self.final_verdict == "SPAM+PHISHING":
            return "CRITICAL"

        if self.final_verdict == "HAM":
            return "LOW" if self.max_confidence > RISK_THRESHOLD_LOW_CONFIDENCE else "MEDIUM"

        # Single threat (SPAM or PHISHING)
        return "HIGH" if self.max_confidence > RISK_THRESHOLD_HIGH_CONFIDENCE else "MEDIUM"

    @property
    def models_used(self) -> dict[str, str]:
        """Get dictionary of models used with their timestamps."""
        return {
            "spam": self.spam_prediction.model_timestamp,
            "phishing": self.phishing_prediction.model_timestamp,
        }
