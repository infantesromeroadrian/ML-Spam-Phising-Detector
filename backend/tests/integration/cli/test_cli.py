"""Integration tests for CLI."""

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from src.spam_detector.infrastructure.cli import app

runner = CliRunner()


@pytest.mark.integration
class TestCLIPredict:
    """Test predict command."""

    def test_predict_with_text_argument(self):
        """Should classify email from text argument."""
        result = runner.invoke(app, ["predict", "WINNER! Click here!"])

        assert result.exit_code == 0
        assert len(result.stdout) > 0

    def test_predict_ham_email(self):
        """Should classify normal email as HAM."""
        result = runner.invoke(app, ["predict", "Hi John, let's meet tomorrow at 3 PM."])

        assert result.exit_code == 0
        assert "HAM" in result.stdout or "✅" in result.stdout

    def test_predict_spam_email(self):
        """Should classify spam email."""
        result = runner.invoke(app, ["predict", "WINNER! You have won $1000!"])

        assert result.exit_code == 0
        # Should detect as spam or phishing
        output = result.stdout.upper()
        assert "SPAM" in output or "PHISHING" in output

    def test_predict_json_output(self):
        """Should produce JSON output."""
        result = runner.invoke(app, ["predict", "Test email", "--format", "json"])

        assert result.exit_code == 0

        # Should be valid JSON
        data = json.loads(result.stdout)
        assert "verdict" in data
        assert "confidence" in data

    def test_predict_detailed_output(self):
        """Should produce detailed output."""
        result = runner.invoke(app, ["predict", "Test", "--detail", "detailed"])

        assert result.exit_code == 0
        # Detailed output should be longer
        assert len(result.stdout) > 50

    def test_predict_with_file(self, tmp_path: Path):
        """Should read email from file."""
        email_file = tmp_path / "test_email.txt"
        email_file.write_text("URGENT! Click here NOW!")

        result = runner.invoke(app, ["predict", "--file", str(email_file)])

        assert result.exit_code == 0
        assert len(result.stdout) > 0

    def test_predict_with_subject_and_sender(self):
        """Should accept subject and sender options."""
        result = runner.invoke(
            app,
            ["predict", "Test email", "--subject", "Test Subject", "--sender", "test@example.com"],
        )

        assert result.exit_code == 0

    def test_predict_no_input_fails(self):
        """Should fail when no input provided."""
        result = runner.invoke(app, ["predict"])

        assert result.exit_code == 1
        assert "No email text" in result.stdout

    def test_predict_invalid_format_fails(self):
        """Should fail with invalid format."""
        result = runner.invoke(app, ["predict", "Test", "--format", "invalid"])

        assert result.exit_code == 1
        assert "Invalid format" in result.stdout

    def test_predict_invalid_detail_fails(self):
        """Should fail with invalid detail level."""
        result = runner.invoke(app, ["predict", "Test", "--detail", "invalid"])

        assert result.exit_code == 1
        assert "Invalid detail level" in result.stdout


@pytest.mark.integration
class TestCLIModels:
    """Test models commands."""

    def test_models_list_spam(self):
        """Should list spam detector models."""
        result = runner.invoke(app, ["models", "list", "spam_detector"])

        assert result.exit_code == 0
        # Should show table or message
        assert len(result.stdout) > 0

    def test_models_list_default(self):
        """Should list spam detector by default."""
        result = runner.invoke(app, ["models", "list"])

        assert result.exit_code == 0
        assert "spam_detector" in result.stdout

    def test_models_list_invalid_name_fails(self):
        """Should fail with invalid model name."""
        result = runner.invoke(app, ["models", "list", "invalid_model"])

        assert result.exit_code == 1
        assert "Invalid model name" in result.stdout

    def test_models_info_spam(self):
        """Should show info for spam detector."""
        result = runner.invoke(app, ["models", "info", "spam_detector"])

        assert result.exit_code == 0
        assert "Accuracy" in result.stdout or "accuracy" in result.stdout.lower()

    def test_models_info_default(self):
        """Should show info for spam detector by default."""
        result = runner.invoke(app, ["models", "info"])

        assert result.exit_code == 0


@pytest.mark.integration
class TestCLIOptions:
    """Test global CLI options."""

    def test_help_option(self):
        """Should show help."""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "email-classifier" in result.stdout.lower()
        assert "predict" in result.stdout
        assert "models" in result.stdout

    def test_predict_help(self):
        """Should show predict help."""
        result = runner.invoke(app, ["predict", "--help"])

        assert result.exit_code == 0
        assert "Examples:" in result.stdout

    def test_models_help(self):
        """Should show models help."""
        result = runner.invoke(app, ["models", "--help"])

        assert result.exit_code == 0

    def test_custom_models_dir(self, tmp_path: Path):
        """Should accept custom models directory."""
        # This will fail since models don't exist, but should accept the option
        result = runner.invoke(app, ["--models-dir", str(tmp_path), "predict", "Test"])

        # Will fail trying to load models, but that's expected
        # Just verify option was accepted (no "Unrecognized option" error)
        assert "Unrecognized option" not in result.stdout
