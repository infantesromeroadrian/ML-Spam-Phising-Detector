"""Domain entities - Value objects and aggregates."""

from .classifier_metadata import ModelMetadata, ModelType
from .email import Email
from .prediction import (
    ClassificationResult,
    LabelType,
    SinglePrediction,
    VerdictType,
)

__all__ = [
    # Email
    "Email",
    # Predictions
    "SinglePrediction",
    "ClassificationResult",
    "LabelType",
    "VerdictType",
    # Model Metadata
    "ModelMetadata",
    "ModelType",
]
