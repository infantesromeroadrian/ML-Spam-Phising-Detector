"""Classify email use case."""

from ...domain.entities import ClassificationResult, Email
from ...domain.ports import DetailLevel, IOutputFormatter
from ...domain.services import EmailClassifierService


class ClassifyEmailUseCase:
    """
    Use case: Classify an email as spam/phishing.

    Orchestrates the complete email classification workflow:
    1. Create Email entity from text
    2. Classify with EmailClassifierService
    3. Format output with IOutputFormatter

    This is the main entry point for email classification.

    Attributes:
        _classifier_service: Domain service for classification
        _formatter: Output formatter implementation

    Examples:
        >>> use_case = ClassifyEmailUseCase(service, formatter)
        >>> output = use_case.execute("WINNER! Click here!")
        >>> print(output)
        🚨 SPAM+PHISHING (92.7% confidence)
    """

    def __init__(
        self, classifier_service: EmailClassifierService, formatter: IOutputFormatter
    ) -> None:
        """
        Initialize use case with dependencies.

        Args:
            classifier_service: Service for email classification
            formatter: Formatter for output rendering
        """
        self._classifier_service = classifier_service
        self._formatter = formatter

    def execute(
        self,
        email_text: str,
        subject: str | None = None,
        sender: str | None = None,
        detail_level: DetailLevel = "simple",
    ) -> str:
        """
        Execute email classification workflow.

        Args:
            email_text: Email body text to classify
            subject: Optional email subject
            sender: Optional sender email address
            detail_level: Output detail level (simple/detailed/debug)

        Returns:
            Formatted classification result as string

        Raises:
            ValueError: If email_text is empty or invalid
        """
        # Create email entity
        email = Email(text=email_text, subject=subject, sender=sender)

        # Classify
        result = self._classifier_service.classify(email)

        # Format output
        return self._formatter.format(result, detail_level=detail_level)

    def execute_raw(
        self, email_text: str, subject: str | None = None, sender: str | None = None
    ) -> ClassificationResult:
        """
        Execute classification without formatting.

        Useful when caller wants direct access to ClassificationResult
        for further processing.

        Args:
            email_text: Email body text to classify
            subject: Optional email subject
            sender: Optional sender email address

        Returns:
            Raw ClassificationResult entity

        Raises:
            ValueError: If email_text is empty or invalid
        """
        email = Email(text=email_text, subject=subject, sender=sender)

        return self._classifier_service.classify(email)
