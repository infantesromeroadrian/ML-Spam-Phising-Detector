"""Unit tests for Prediction entities."""

import pytest

from src.spam_detector.domain.entities import (
    ClassificationResult,
    Email,
    SinglePrediction,
)


class TestSinglePrediction:
    """Test SinglePrediction entity."""

    def test_create_spam_prediction(self):
        """Should create spam prediction."""
        pred = SinglePrediction(
            label="SPAM",
            probability=0.85,
            model_name="spam_detector",
            model_timestamp="20260105_194125",
        )
        assert pred.label == "SPAM"
        assert pred.probability == 0.85
        assert pred.is_positive is True

    def test_create_ham_prediction(self):
        """Should create ham prediction."""
        pred = SinglePrediction(
            label="HAM",
            probability=0.92,
            model_name="spam_detector",
            model_timestamp="20260105_194125",
        )
        assert pred.label == "HAM"
        assert pred.is_positive is False

    def test_probability_percent(self):
        """Should convert probability to percentage."""
        pred = SinglePrediction(
            label="SPAM",
            probability=0.853,
            model_name="spam_detector",
            model_timestamp="20260105_194125",
        )
        assert pred.probability_percent == 85.3

    def test_invalid_probability_raises_error(self):
        """Should raise ValueError for probability > 1."""
        with pytest.raises(ValueError, match="between 0 and 1"):
            SinglePrediction(
                label="SPAM",
                probability=1.5,
                model_name="spam_detector",
                model_timestamp="20260105_194125",
            )


class TestClassificationResult:
    """Test ClassificationResult entity."""

    @pytest.fixture
    def sample_email(self):
        """Sample email for testing."""
        return Email(text="WINNER! Click here NOW!")

    @pytest.fixture
    def ham_spam_result(self, sample_email):
        """Result with HAM spam, HAM phishing."""
        return ClassificationResult(
            email=sample_email,
            spam_prediction=SinglePrediction("HAM", 0.92, "spam_detector", "20260105_194125"),
            phishing_prediction=SinglePrediction(
                "LEGIT", 0.88, "phishing_detector", "20260105_195830"
            ),
            execution_time_ms=45.3,
        )

    @pytest.fixture
    def spam_result(self, sample_email):
        """Result with SPAM, LEGIT phishing."""
        return ClassificationResult(
            email=sample_email,
            spam_prediction=SinglePrediction("SPAM", 0.85, "spam_detector", "20260105_194125"),
            phishing_prediction=SinglePrediction(
                "LEGIT", 0.65, "phishing_detector", "20260105_195830"
            ),
            execution_time_ms=42.1,
        )

    @pytest.fixture
    def phishing_result(self, sample_email):
        """Result with HAM spam, PHISHING."""
        return ClassificationResult(
            email=sample_email,
            spam_prediction=SinglePrediction("HAM", 0.75, "spam_detector", "20260105_194125"),
            phishing_prediction=SinglePrediction(
                "PHISHING", 0.92, "phishing_detector", "20260105_195830"
            ),
            execution_time_ms=38.7,
        )

    @pytest.fixture
    def both_malicious_result(self, sample_email):
        """Result with SPAM + PHISHING."""
        return ClassificationResult(
            email=sample_email,
            spam_prediction=SinglePrediction("SPAM", 0.85, "spam_detector", "20260105_194125"),
            phishing_prediction=SinglePrediction(
                "PHISHING", 0.92, "phishing_detector", "20260105_195830"
            ),
            execution_time_ms=51.2,
        )

    def test_final_verdict_ham(self, ham_spam_result):
        """Should return HAM when both negative."""
        assert ham_spam_result.final_verdict == "HAM"

    def test_final_verdict_spam(self, spam_result):
        """Should return SPAM when only spam positive."""
        assert spam_result.final_verdict == "SPAM"

    def test_final_verdict_phishing(self, phishing_result):
        """Should return PHISHING when only phishing positive."""
        assert phishing_result.final_verdict == "PHISHING"

    def test_final_verdict_both(self, both_malicious_result):
        """Should return SPAM+PHISHING when both positive."""
        assert both_malicious_result.final_verdict == "SPAM+PHISHING"

    def test_max_confidence(self, spam_result):
        """Should return highest probability."""
        assert spam_result.max_confidence == 0.85

    def test_is_malicious_ham(self, ham_spam_result):
        """Should return False for HAM."""
        assert ham_spam_result.is_malicious is False

    def test_is_malicious_spam(self, spam_result):
        """Should return True for SPAM."""
        assert spam_result.is_malicious is True

    def test_risk_level_critical(self, both_malicious_result):
        """Should return CRITICAL for both threats."""
        assert both_malicious_result.risk_level == "CRITICAL"

    def test_risk_level_low(self, ham_spam_result):
        """Should return LOW for HAM with high confidence."""
        assert ham_spam_result.risk_level == "LOW"

    def test_risk_level_high(self, phishing_result):
        """Should return HIGH for single threat high confidence."""
        assert phishing_result.risk_level == "HIGH"

    def test_models_used(self, spam_result):
        """Should return dict with model timestamps."""
        models = spam_result.models_used
        assert models["spam"] == "20260105_194125"
        assert models["phishing"] == "20260105_195830"
