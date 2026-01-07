"""Unit tests for EmailClassifierService."""

from unittest.mock import Mock

import pytest

from src.spam_detector.domain.entities import Email, SinglePrediction
from src.spam_detector.domain.services import EmailClassifierService


class TestEmailClassifierService:
    """Test EmailClassifierService domain service."""

    @pytest.fixture
    def mock_spam_predictor(self):
        """Mock spam predictor."""
        predictor = Mock()
        predictor.predict.return_value = SinglePrediction(
            label="SPAM",
            probability=0.85,
            model_name="spam_detector",
            model_timestamp="20260105_194125",
        )
        return predictor

    @pytest.fixture
    def mock_phishing_predictor(self):
        """Mock phishing predictor."""
        predictor = Mock()
        predictor.predict.return_value = SinglePrediction(
            label="PHISHING",
            probability=0.92,
            model_name="phishing_detector",
            model_timestamp="20260105_195830",
        )
        return predictor

    @pytest.fixture
    def service(self, mock_spam_predictor, mock_phishing_predictor):
        """Service with mocked predictors."""
        return EmailClassifierService(
            spam_predictor=mock_spam_predictor, phishing_predictor=mock_phishing_predictor
        )

    def test_classify_calls_both_predictors(
        self, service, mock_spam_predictor, mock_phishing_predictor
    ):
        """Should call both spam and phishing predictors."""
        email = Email(text="Test email")

        result = service.classify(email)

        mock_spam_predictor.predict.assert_called_once_with(email)
        mock_phishing_predictor.predict.assert_called_once_with(email)

    def test_classify_returns_classification_result(self, service):
        """Should return ClassificationResult with both predictions."""
        email = Email(text="WINNER! Click here NOW!")

        result = service.classify(email)

        assert result.email == email
        assert result.spam_prediction.label == "SPAM"
        assert result.phishing_prediction.label == "PHISHING"
        assert result.final_verdict == "SPAM+PHISHING"

    def test_classify_measures_execution_time(self, service):
        """Should measure and include execution time."""
        email = Email(text="Test")

        result = service.classify(email)

        assert result.execution_time_ms > 0
        assert result.execution_time_ms < 1000  # Should be very fast

    def test_classify_preserves_email_reference(self, service):
        """Should preserve reference to original email."""
        email = Email(text="Test", subject="Subject", sender="sender@test.com")

        result = service.classify(email)

        assert result.email is email
        assert result.email.subject == "Subject"
        assert result.email.sender == "sender@test.com"
