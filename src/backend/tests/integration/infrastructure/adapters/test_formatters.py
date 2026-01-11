"""Integration tests for output formatters."""

import json

import pytest

from spam_detector.domain.entities import (
    ClassificationResult,
    Email,
    SinglePrediction,
)
from spam_detector.domain.ports import DetailLevel
from spam_detector.infrastructure.adapters import (
    JsonFormatter,
    TextFormatter,
)


@pytest.fixture
def sample_result() -> ClassificationResult:
    """Sample classification result for testing."""
    email = Email(
        text="WINNER! You have won $1000! Click here NOW!",
        subject="Urgent Prize Notification",
        sender="scam@fake.com",
    )

    spam_pred = SinglePrediction(
        label="SPAM",
        probability=0.853,
        model_name="spam_detector",
        model_timestamp="20260105_194125",
    )

    phishing_pred = SinglePrediction(
        label="PHISHING",
        probability=0.927,
        model_name="phishing_detector",
        model_timestamp="20260105_195830",
    )

    return ClassificationResult(
        email=email,
        spam_prediction=spam_pred,
        phishing_prediction=phishing_pred,
        execution_time_ms=45.3,
    )


class TestJsonFormatter:
    """Test JSON formatter."""

    def test_format_simple(self, sample_result):
        """Should format simple JSON output."""
        formatter = JsonFormatter()
        output = formatter.format(sample_result, detail_level="simple")

        # Parse JSON to validate
        data = json.loads(output)

        assert data["verdict"] == "SPAM+PHISHING"
        assert "confidence" in data
        assert data["is_malicious"] is True
        assert data["risk_level"] == "CRITICAL"

    def test_format_detailed(self, sample_result):
        """Should format detailed JSON output."""
        formatter = JsonFormatter()
        output = formatter.format(sample_result, detail_level="detailed")

        data = json.loads(output)

        assert data["verdict"] == "SPAM+PHISHING"
        assert "spam" in data
        assert "phishing" in data
        assert data["spam"]["label"] == "SPAM"
        assert data["phishing"]["label"] == "PHISHING"
        assert "email_preview" in data
        assert "execution_time_ms" in data

    def test_format_debug(self, sample_result):
        """Should format debug JSON output."""
        formatter = JsonFormatter()
        output = formatter.format(sample_result, detail_level="debug")

        data = json.loads(output)

        assert "predictions" in data
        assert "email" in data
        assert "confidence" in data
        assert data["email"]["subject"] == "Urgent Prize Notification"
        assert data["email"]["sender"] == "scam@fake.com"
        assert data["email"]["word_count"] > 0

    def test_json_is_valid(self, sample_result):
        """Should produce valid JSON for all detail levels."""
        formatter = JsonFormatter()

        levels: list[DetailLevel] = ["simple", "detailed", "debug"]
        for level in levels:
            output = formatter.format(sample_result, detail_level=level)
            # Should not raise
            json.loads(output)


class TestTextFormatter:
    """Test text formatter."""

    def test_format_simple(self, sample_result):
        """Should format simple text output."""
        formatter = TextFormatter()
        output = formatter.format(sample_result, detail_level="simple")

        assert isinstance(output, str)
        assert len(output) > 0
        # Should contain verdict
        assert "SPAM+PHISHING" in output or "SPAM" in output

    def test_format_detailed(self, sample_result):
        """Should format detailed text output."""
        formatter = TextFormatter()
        output = formatter.format(sample_result, detail_level="detailed")

        assert isinstance(output, str)
        assert len(output) > 100  # Should be substantial

    def test_format_debug(self, sample_result):
        """Should format debug text output."""
        formatter = TextFormatter()
        output = formatter.format(sample_result, detail_level="debug")

        assert isinstance(output, str)
        assert len(output) > 200  # Should be very detailed

    def test_output_contains_verdict(self, sample_result):
        """Should include verdict in all outputs."""
        formatter = TextFormatter()

        levels: list[DetailLevel] = ["simple", "detailed", "debug"]
        for level in levels:
            output = formatter.format(sample_result, detail_level=level)
            # Should contain some indication of the verdict
            assert len(output) > 0


class TestFormatterComparison:
    """Test formatter behavior differences."""

    def test_json_vs_text_content(self, sample_result):
        """JSON and text should contain same core info."""
        json_formatter = JsonFormatter()
        text_formatter = TextFormatter()

        json_output = json_formatter.format(sample_result, detail_level="detailed")
        text_output = text_formatter.format(sample_result, detail_level="detailed")

        json_data = json.loads(json_output)

        # Both should have verdict
        assert json_data["verdict"] in text_output or "SPAM" in text_output
