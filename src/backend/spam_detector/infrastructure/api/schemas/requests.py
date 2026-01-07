"""API request schemas (Pydantic models)."""

from pydantic import BaseModel, Field


class ClassifyEmailRequest(BaseModel):
    """
    Request schema for email classification endpoint.

    Attributes:
        email_text: Email body text to classify (required)
        subject: Email subject line (optional)
        sender: Email sender address (optional)

    Examples:
        >>> request = ClassifyEmailRequest(
        ...     email_text="WINNER! You have won $1000!",
        ...     subject="Urgent Prize",
        ...     sender="scam@fake.com"
        ... )
    """

    email_text: str = Field(
        ...,
        min_length=1,
        description="Email body text to classify",
        examples=["WINNER! You have won $1000! Click here NOW!"],
    )
    subject: str | None = Field(
        None, description="Email subject line", examples=["Congratulations!"]
    )
    sender: str | None = Field(None, description="Email sender address", examples=["scam@fake.com"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email_text": "URGENT! Your account has been suspended. Click here to verify.",
                    "subject": "Account Alert",
                    "sender": "phishing@fake.com",
                }
            ]
        }
    }
