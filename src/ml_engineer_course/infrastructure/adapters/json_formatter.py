"""JSON output formatter."""

import json
from typing import Any

from ...domain.entities import ClassificationResult
from ...domain.ports import DetailLevel


class JsonFormatter:
    """
    Format classification results as JSON.

    Implements IOutputFormatter port for JSON output.
    Useful for API responses and programmatic consumption.

    Examples:
        >>> formatter = JsonFormatter()
        >>> output = formatter.format(result, detail_level="simple")
        >>> print(output)
        {"verdict": "SPAM+PHISHING", "confidence": 0.92, ...}
    """

    def format(self, result: ClassificationResult, detail_level: DetailLevel = "simple") -> str:
        """
        Format classification result as JSON string.

        Args:
            result: Classification result to format
            detail_level: Amount of detail to include
                - "simple": Just verdict and confidence
                - "detailed": Include both predictions, models used
                - "debug": Include all metadata, execution time, etc.

        Returns:
            JSON string (pretty-printed with indent=2)
        """
        if detail_level == "simple":
            data = self._format_simple(result)
        elif detail_level == "detailed":
            data = self._format_detailed(result)
        else:  # debug
            data = self._format_debug(result)

        return json.dumps(data, indent=2, ensure_ascii=False)

    # === Private methods ===

    def _format_simple(self, result: ClassificationResult) -> dict[str, Any]:
        """Format simple output."""
        return {
            "verdict": result.final_verdict,
            "confidence": round(result.max_confidence, 4),
            "is_malicious": result.is_malicious,
            "risk_level": result.risk_level,
        }

    def _format_detailed(self, result: ClassificationResult) -> dict[str, Any]:
        """Format detailed output."""
        return {
            "verdict": result.final_verdict,
            "risk_level": result.risk_level,
            "is_malicious": result.is_malicious,
            "spam": {
                "label": result.spam_prediction.label,
                "probability": round(result.spam_prediction.probability, 4),
                "model": result.spam_prediction.model_name,
                "version": result.spam_prediction.model_timestamp,
            },
            "phishing": {
                "label": result.phishing_prediction.label,
                "probability": round(result.phishing_prediction.probability, 4),
                "model": result.phishing_prediction.model_name,
                "version": result.phishing_prediction.model_timestamp,
            },
            "email_preview": result.email.preview,
            "execution_time_ms": round(result.execution_time_ms, 2),
        }

    def _format_debug(self, result: ClassificationResult) -> dict[str, Any]:
        """Format debug output with all details."""
        return {
            "verdict": result.final_verdict,
            "risk_level": result.risk_level,
            "is_malicious": result.is_malicious,
            "confidence": {
                "max": round(result.max_confidence, 4),
                "spam": round(result.spam_prediction.probability, 4),
                "phishing": round(result.phishing_prediction.probability, 4),
            },
            "predictions": {
                "spam": {
                    "label": result.spam_prediction.label,
                    "probability": round(result.spam_prediction.probability, 4),
                    "probability_percent": round(result.spam_prediction.probability_percent, 2),
                    "is_positive": result.spam_prediction.is_positive,
                    "model_name": result.spam_prediction.model_name,
                    "model_timestamp": result.spam_prediction.model_timestamp,
                },
                "phishing": {
                    "label": result.phishing_prediction.label,
                    "probability": round(result.phishing_prediction.probability, 4),
                    "probability_percent": round(result.phishing_prediction.probability_percent, 2),
                    "is_positive": result.phishing_prediction.is_positive,
                    "model_name": result.phishing_prediction.model_name,
                    "model_timestamp": result.phishing_prediction.model_timestamp,
                },
            },
            "email": {
                "preview": result.email.preview,
                "word_count": result.email.word_count,
                "char_count": result.email.char_count,
                "subject": result.email.subject,
                "sender": result.email.sender,
            },
            "execution_time_ms": round(result.execution_time_ms, 2),
            "models_used": result.models_used,
        }
