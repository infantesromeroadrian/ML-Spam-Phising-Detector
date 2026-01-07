"""Email entity - Value object inmutable."""

from dataclasses import dataclass
from datetime import datetime

from ..constants import EMAIL_PREVIEW_LENGTH


@dataclass(frozen=True)
class Email:
    """
    Email value object for classification.

    Immutable entity representing an email message with its metadata.

    Attributes:
        text: Email body content (required)
        subject: Email subject line (optional)
        sender: Email sender address (optional)
        timestamp: When email was received (optional)

    Raises:
        ValueError: If text is empty or whitespace-only

    Examples:
        >>> email = Email(text="Hello world")
        >>> email = Email(
        ...     text="Urgent! Click here",
        ...     subject="Account suspended",
        ...     sender="phishing@fake.com"
        ... )
    """

    text: str
    subject: str | None = None
    sender: str | None = None
    timestamp: datetime | None = None

    def __post_init__(self) -> None:
        """Validate email text is not empty."""
        if not self.text or not self.text.strip():
            raise ValueError("Email text cannot be empty or whitespace-only")

    @property
    def preview(self) -> str:
        """Get preview of email text (first N chars)."""
        max_len = EMAIL_PREVIEW_LENGTH
        return self.text[:max_len] + ("..." if len(self.text) > max_len else "")

    @property
    def word_count(self) -> int:
        """Count words in email text."""
        return len(self.text.split())

    @property
    def char_count(self) -> int:
        """Count characters in email text."""
        return len(self.text)
