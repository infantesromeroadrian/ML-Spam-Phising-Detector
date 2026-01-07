"""API response schemas (Pydantic models)."""

from typing import Literal

from pydantic import BaseModel, Field

from ....domain.entities import ClassificationResult, ModelMetadata
from ....domain.entities.threat_report import IOC, ThreatReport, ThreatVector, TriggerWord


class TriggerWordResponse(BaseModel):
    """Schema for ML Trigger Word (feature explanation)"""

    word: str = Field(..., description="Word/feature from email")
    contribution: float = Field(
        ..., description="Contribution score (+ = malicious, - = legitimate)"
    )
    category: str = Field(..., description="Category: spam or phishing")

    @classmethod
    def from_domain(cls, trigger: TriggerWord) -> "TriggerWordResponse":
        """Convert domain TriggerWord to API response"""
        return cls(word=trigger.word, contribution=trigger.contribution, category=trigger.category)


class IOCResponse(BaseModel):
    """Schema for Indicator of Compromise"""

    type: str = Field(
        ..., description="IOC type (url, keyword_urgency, keyword_financial, pattern, sender)"
    )
    severity: str = Field(..., description="Severity level (critical, high, medium, low)")
    value: str = Field(..., description="The actual IOC value")
    description: str = Field(..., description="Human-readable description")
    count: int = Field(default=1, description="Number of occurrences")

    @classmethod
    def from_domain(cls, ioc: IOC) -> "IOCResponse":
        """Convert domain IOC to API response"""
        return cls(
            type=ioc.type,
            severity=ioc.severity,
            value=ioc.value,
            description=ioc.description,
            count=ioc.count,
        )


class ThreatVectorResponse(BaseModel):
    """Schema for Threat Vector"""

    name: str = Field(..., description="Threat vector name")
    description: str = Field(..., description="Detailed description")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")

    @classmethod
    def from_domain(cls, vector: ThreatVector) -> "ThreatVectorResponse":
        """Convert domain ThreatVector to API response"""
        return cls(name=vector.name, description=vector.description, confidence=vector.confidence)


class ThreatReportResponse(BaseModel):
    """Schema for complete Threat Report"""

    risk_score: int = Field(..., ge=0, le=100, description="Overall risk score (0-100)")
    iocs: list[IOCResponse] = Field(default_factory=list, description="Indicators of Compromise")
    threat_vectors: list[ThreatVectorResponse] = Field(
        default_factory=list, description="Identified threat vectors"
    )
    recommendations: list[str] = Field(default_factory=list, description="Security recommendations")
    spam_trigger_words: list[TriggerWordResponse] = Field(
        default_factory=list, description="Words that triggered SPAM classification"
    )
    phishing_trigger_words: list[TriggerWordResponse] = Field(
        default_factory=list, description="Words that triggered PHISHING classification"
    )

    @classmethod
    def from_domain(cls, report: ThreatReport) -> "ThreatReportResponse":
        """Convert domain ThreatReport to API response"""
        return cls(
            risk_score=report.risk_score,
            iocs=[IOCResponse.from_domain(ioc) for ioc in report.iocs],
            threat_vectors=[ThreatVectorResponse.from_domain(v) for v in report.threat_vectors],
            recommendations=report.recommendations,
            spam_trigger_words=[
                TriggerWordResponse.from_domain(tw) for tw in report.spam_trigger_words
            ],
            phishing_trigger_words=[
                TriggerWordResponse.from_domain(tw) for tw in report.phishing_trigger_words
            ],
        )


class ClassificationResponse(BaseModel):
    """
    Response schema for email classification.

    Contains complete classification results from both spam and phishing detectors.

    Attributes:
        verdict: Final verdict (HAM, SPAM, PHISHING, SPAM+PHISHING)
        risk_level: Risk assessment (LOW, MEDIUM, HIGH, CRITICAL)
        is_malicious: Whether email is classified as malicious
        spam_label: Spam detector label (HAM or SPAM)
        spam_probability: Spam probability (0.0-1.0)
        spam_model_version: Spam model timestamp
        phishing_label: Phishing detector label (LEGIT or PHISHING)
        phishing_probability: Phishing probability (0.0-1.0)
        phishing_model_version: Phishing model timestamp
        execution_time_ms: Total execution time in milliseconds
    """

    verdict: Literal["HAM", "SPAM", "PHISHING", "SPAM+PHISHING"] = Field(
        ..., description="Final classification verdict"
    )
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = Field(
        ..., description="Risk level assessment"
    )
    is_malicious: bool = Field(..., description="Whether email is malicious")

    spam_label: str = Field(..., description="Spam detector label (HAM or SPAM)")
    spam_probability: float = Field(..., ge=0.0, le=1.0, description="Spam probability")
    spam_model_version: str = Field(..., description="Spam model timestamp")

    phishing_label: str = Field(..., description="Phishing detector label (LEGIT or PHISHING)")
    phishing_probability: float = Field(..., ge=0.0, le=1.0, description="Phishing probability")
    phishing_model_version: str = Field(..., description="Phishing model timestamp")

    execution_time_ms: float = Field(..., description="Execution time in milliseconds")

    threat_report: ThreatReportResponse = Field(..., description="Detailed threat analysis report")

    @classmethod
    def from_domain(
        cls, result: ClassificationResult, threat_report: ThreatReport
    ) -> "ClassificationResponse":
        """
        Convert domain entity to API response.

        Args:
            result: ClassificationResult from domain layer
            threat_report: ThreatReport from threat analyzer

        Returns:
            ClassificationResponse for API

        Examples:
            >>> from ml_engineer_course.domain.entities import Email, SinglePrediction
            >>> email = Email(text="SPAM text")
            >>> spam_pred = SinglePrediction("SPAM", 0.95, "spam_detector", "20240105")
            >>> phish_pred = SinglePrediction("PHISHING", 0.88, "phishing_detector", "20240105")
            >>> result = ClassificationResult(email, spam_pred, phish_pred, 45.3)
            >>> threat_report = ThreatReport(risk_score=95, iocs=[], threat_vectors=[], recommendations=[])
            >>> response = ClassificationResponse.from_domain(result, threat_report)
            >>> response.verdict
            'SPAM+PHISHING'
        """
        return cls(
            verdict=result.final_verdict,
            risk_level=result.risk_level,
            is_malicious=result.is_malicious,
            spam_label=result.spam_prediction.label,
            spam_probability=result.spam_prediction.probability,
            spam_model_version=result.spam_prediction.model_timestamp,
            phishing_label=result.phishing_prediction.label,
            phishing_probability=result.phishing_prediction.probability,
            phishing_model_version=result.phishing_prediction.model_timestamp,
            execution_time_ms=result.execution_time_ms,
            threat_report=ThreatReportResponse.from_domain(threat_report),
        )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "verdict": "SPAM+PHISHING",
                    "risk_level": "CRITICAL",
                    "is_malicious": True,
                    "spam_label": "SPAM",
                    "spam_probability": 0.954,
                    "spam_model_version": "20240105_143022",
                    "phishing_label": "PHISHING",
                    "phishing_probability": 0.882,
                    "phishing_model_version": "20240105_143022",
                    "execution_time_ms": 45.3,
                    "threat_report": {
                        "risk_score": 95,
                        "iocs": [
                            {
                                "type": "url",
                                "severity": "critical",
                                "value": "http://fake-bank.ru/login",
                                "description": "Suspicious URL with high-risk domain",
                                "count": 1,
                            },
                            {
                                "type": "keyword_urgency",
                                "severity": "high",
                                "value": "urgent (2x), now (3x)",
                                "description": "Urgency manipulation tactics detected",
                                "count": 5,
                            },
                        ],
                        "threat_vectors": [
                            {
                                "name": "Phishing Attack",
                                "description": "Email designed to deceive recipients",
                                "confidence": 0.882,
                            }
                        ],
                        "recommendations": [
                            "🚫 Quarantine this email immediately",
                            "🔒 Block sender domain",
                            "⚠️  Alert security team",
                        ],
                    },
                }
            ]
        }
    }


class ModelInfoResponse(BaseModel):
    """
    Response schema for model metadata information.

    Attributes:
        name: Model name
        timestamp: Model version timestamp
        accuracy: Model accuracy (0.0-1.0)
        accuracy_percent: Accuracy as percentage
        train_samples: Number of training samples
        vocabulary_size: Size of vocabulary
        file_size_mb: Model file size in megabytes
    """

    name: str = Field(..., description="Model name")
    timestamp: str = Field(..., description="Model version timestamp")
    accuracy: float = Field(..., ge=0.0, le=1.0, description="Model accuracy")
    accuracy_percent: float = Field(..., ge=0.0, le=100.0, description="Accuracy percentage")
    train_samples: int = Field(..., ge=0, description="Number of training samples")
    vocabulary_size: int = Field(..., ge=0, description="Vocabulary size")
    file_size_mb: float = Field(..., ge=0.0, description="File size in MB")

    @classmethod
    def from_domain(cls, metadata: ModelMetadata) -> "ModelInfoResponse":
        """
        Convert domain entity to API response.

        Args:
            metadata: ModelMetadata from domain layer

        Returns:
            ModelInfoResponse for API
        """
        return cls(
            name=metadata.name,
            timestamp=metadata.timestamp,
            accuracy=metadata.accuracy,
            accuracy_percent=metadata.accuracy_percent,
            train_samples=metadata.train_samples,
            vocabulary_size=metadata.vocabulary_size,
            file_size_mb=metadata.file_size_mb,
        )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "spam_detector",
                    "timestamp": "20240105_143022",
                    "accuracy": 0.963,
                    "accuracy_percent": 96.3,
                    "train_samples": 5000,
                    "vocabulary_size": 12500,
                    "file_size_mb": 2.45,
                }
            ]
        }
    }


class ModelsListResponse(BaseModel):
    """
    Response schema for list of model versions.

    Attributes:
        model_name: Name of the model type
        total_versions: Total number of versions available
        models: List of model metadata
    """

    model_name: str = Field(..., description="Model type name")
    total_versions: int = Field(..., ge=0, description="Total versions available")
    models: list[ModelInfoResponse] = Field(..., description="List of model versions")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model_name": "spam_detector",
                    "total_versions": 2,
                    "models": [
                        {
                            "name": "spam_detector",
                            "timestamp": "20240105_143022",
                            "accuracy": 0.963,
                            "accuracy_percent": 96.3,
                            "train_samples": 5000,
                            "vocabulary_size": 12500,
                            "file_size_mb": 2.45,
                        }
                    ],
                }
            ]
        }
    }
