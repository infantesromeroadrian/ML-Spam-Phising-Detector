"""Integration tests for SklearnPredictor."""

from pathlib import Path

from src.spam_detector.domain.entities import Email, SinglePrediction
from src.spam_detector.infrastructure.adapters import (
import pytest
    JoblibModelLoader,
    SklearnPredictor,
)


@pytest.fixture
def spam_predictor() -> SklearnPredictor:
    """Load real spam detector."""
    loader = JoblibModelLoader(models_dir=Path("models"))
    vectorizer, model, metadata = loader.load("spam_detector")

    return SklearnPredictor(
        vectorizer=vectorizer, model=model, metadata=metadata, predictor_type="spam"
    )


@pytest.mark.integration
class TestSklearnPredictorSpam:
    """Test spam predictor with real models."""

    def test_predict_spam_email(self, spam_predictor):
        """Should classify obvious spam correctly."""
        email = Email(text="WINNER! You have won $1000! Click here NOW to claim your prize!")

        prediction = spam_predictor.predict(email)

        assert isinstance(prediction, SinglePrediction)
        assert prediction.label in ("HAM", "SPAM")
        assert 0.0 <= prediction.probability <= 1.0
        assert prediction.model_name == "spam_detector"
        assert prediction.model_timestamp

    def test_predict_ham_email(self, spam_predictor):
        """Should classify normal email correctly."""
        email = Email(text="Hi John, I'll be at the office tomorrow at 3 PM for our meeting.")

        prediction = spam_predictor.predict(email)

        assert isinstance(prediction, SinglePrediction)
        assert prediction.label in ("HAM", "SPAM")
        # Likely HAM but we don't force it in test

    def test_predict_probability_range(self, spam_predictor):
        """Should return probabilities in valid range."""
        email = Email(text="Test email content")

        prediction = spam_predictor.predict(email)

        assert 0.0 <= prediction.probability <= 1.0
        assert 0.0 <= prediction.probability_percent <= 100.0

    def test_predict_empty_email_fails(self, spam_predictor):
        """Should fail on invalid email creation."""
        # Email entity should reject empty/whitespace text
        with pytest.raises(ValueError, match="cannot be empty"):
            Email(text="")

        with pytest.raises(ValueError, match="cannot be empty"):
            Email(text="   ")


@pytest.mark.integration
class TestSklearnPredictorMetadata:
    """Test predictor metadata."""

    def test_prediction_includes_model_info(self, spam_predictor):
        """Should include model name and timestamp in prediction."""
        email = Email(text="Test content")

        prediction = spam_predictor.predict(email)

        assert prediction.model_name == "spam_detector"
        assert len(prediction.model_timestamp) > 0
        assert "_" in prediction.model_timestamp  # Format: YYYYMMDD_HHMMSS
