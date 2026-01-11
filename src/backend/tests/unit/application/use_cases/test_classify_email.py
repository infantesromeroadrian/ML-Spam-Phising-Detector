"""Unit tests for ClassifyEmailUseCase."""

from unittest.mock import Mock

from src.spam_detector.application.use_cases import ClassifyEmailUseCase
from src.spam_detector.domain.entities import (
import pytest
    ClassificationResult,
    Email,
    SinglePrediction,
)


@pytest.fixture
def mock_classifier_service():
    """Mock classifier service."""
    service = Mock()

    # Mock classification result
    email = Email(text="Test email")
    spam_pred = SinglePrediction("SPAM", 0.85, "spam_detector", "20260105_194125")
    phish_pred = SinglePrediction("PHISHING", 0.92, "phishing_detector", "20260105_195830")

    result = ClassificationResult(
        email=email,
        spam_prediction=spam_pred,
        phishing_prediction=phish_pred,
        execution_time_ms=45.3,
    )

    service.classify.return_value = result
    return service


@pytest.fixture
def mock_formatter():
    """Mock output formatter."""
    formatter = Mock()
    formatter.format.return_value = "Formatted output"
    return formatter


@pytest.fixture
def use_case(mock_classifier_service, mock_formatter):
    """ClassifyEmailUseCase with mocks."""
    return ClassifyEmailUseCase(
        classifier_service=mock_classifier_service, formatter=mock_formatter
    )


class TestClassifyEmailUseCase:
    """Test ClassifyEmailUseCase."""

    def test_execute_calls_classifier(self, use_case, mock_classifier_service):
        """Should call classifier service with Email entity."""
        use_case.execute("Test email text")

        mock_classifier_service.classify.assert_called_once()
        call_args = mock_classifier_service.classify.call_args[0][0]
        assert isinstance(call_args, Email)
        assert call_args.text == "Test email text"

    def test_execute_calls_formatter(self, use_case, mock_formatter):
        """Should call formatter with result and detail level."""
        use_case.execute("Test", detail_level="detailed")

        mock_formatter.format.assert_called_once()
        args = mock_formatter.format.call_args
        assert isinstance(args[0][0], ClassificationResult)
        assert args[1]["detail_level"] == "detailed"

    def test_execute_returns_formatted_output(self, use_case):
        """Should return formatted string from formatter."""
        result = use_case.execute("Test")
        assert result == "Formatted output"

    def test_execute_with_subject_and_sender(self, use_case, mock_classifier_service):
        """Should pass subject and sender to Email entity."""
        use_case.execute(email_text="Test", subject="Test Subject", sender="test@example.com")

        call_args = mock_classifier_service.classify.call_args[0][0]
        assert call_args.subject == "Test Subject"
        assert call_args.sender == "test@example.com"

    def test_execute_with_empty_text_raises_error(self, use_case):
        """Should raise ValueError for empty email text."""
        with pytest.raises(ValueError, match="cannot be empty"):
            use_case.execute("")

    def test_execute_raw_returns_classification_result(self, use_case, mock_classifier_service):
        """Should return raw ClassificationResult without formatting."""
        result = use_case.execute_raw("Test email")

        assert isinstance(result, ClassificationResult)
        mock_classifier_service.classify.assert_called_once()

    def test_execute_raw_does_not_call_formatter(self, use_case, mock_formatter):
        """execute_raw should not call formatter."""
        use_case.execute_raw("Test")
        mock_formatter.format.assert_not_called()
