"""Unit tests for Email entity."""

from datetime import datetime

from src.spam_detector.domain.entities import Email
import pytest
class TestEmailCreation:
    """Test Email entity creation."""

    def test_create_email_with_text_only(self):
        """Should create email with just text."""
        email = Email(text="Hello world")
        assert email.text == "Hello world"
        assert email.subject is None
        assert email.sender is None
        assert email.timestamp is None

    def test_create_email_with_all_fields(self):
        """Should create email with all metadata."""
        ts = datetime(2026, 1, 5, 19, 41, 25)
        email = Email(
            text="Urgent message",
            subject="Account suspended",
            sender="phishing@fake.com",
            timestamp=ts,
        )
        assert email.text == "Urgent message"
        assert email.subject == "Account suspended"
        assert email.sender == "phishing@fake.com"
        assert email.timestamp == ts

    def test_email_is_immutable(self):
        """Should not allow modification after creation."""
        email = Email(text="Original")
        with pytest.raises(AttributeError):
            email.text = "Modified"  # type: ignore


class TestEmailValidation:
    """Test Email validation."""

    def test_empty_text_raises_error(self):
        """Should raise ValueError for empty text."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Email(text="")

    def test_whitespace_only_text_raises_error(self):
        """Should raise ValueError for whitespace-only text."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Email(text="   \n\t  ")


class TestEmailProperties:
    """Test Email computed properties."""

    def test_preview_short_text(self):
        """Should return full text if under 100 chars."""
        email = Email(text="Short message")
        assert email.preview == "Short message"

    def test_preview_long_text(self):
        """Should truncate text over 100 chars with ellipsis."""
        long_text = "A" * 150
        email = Email(text=long_text)
        assert len(email.preview) == 103  # 100 + "..."
        assert email.preview.endswith("...")
        assert email.preview.startswith("A" * 100)

    def test_word_count(self):
        """Should count words correctly."""
        email = Email(text="This is a test message")
        assert email.word_count == 5

    def test_char_count(self):
        """Should count characters correctly."""
        email = Email(text="Hello")
        assert email.char_count == 5
