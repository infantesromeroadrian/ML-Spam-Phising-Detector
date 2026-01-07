"""Output formatter port - Interface for formatting results."""

from typing import Literal, Protocol

from ..entities import ClassificationResult

DetailLevel = Literal["simple", "detailed", "debug"]


class IOutputFormatter(Protocol):
    """
    Port for formatting classification results.

    This protocol defines the interface for converting
    ClassificationResult into output strings. Implementations
    can format as text, JSON, HTML, etc.

    Examples:
        >>> formatter: IOutputFormatter = TextFormatter()
        >>> output = formatter.format(result, detail_level="simple")
        >>> print(output)
        ⚠️ SPAM + PHISHING (92.7% confidence)

        >>> formatter: IOutputFormatter = JsonFormatter()
        >>> output = formatter.format(result, detail_level="detailed")
        >>> print(output)
        {"verdict": "SPAM+PHISHING", ...}
    """

    def format(self, result: ClassificationResult, detail_level: DetailLevel = "simple") -> str:
        """
        Format classification result as string.

        Args:
            result: Classification result to format
            detail_level: Amount of detail to include
                - "simple": Just verdict and confidence
                - "detailed": Include both predictions, models used
                - "debug": Include all metadata, execution time, etc.

        Returns:
            Formatted string ready for output
        """
        ...
