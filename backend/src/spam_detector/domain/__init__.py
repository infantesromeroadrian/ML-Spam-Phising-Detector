"""Domain layer - Core business logic without external dependencies."""

from . import constants
from .entities import (
    ClassificationResult,
    Email,
    LabelType,
    ModelMetadata,
    ModelType,
    SinglePrediction,
    VerdictType,
)
from .ports import DetailLevel, IModelLoader, IOutputFormatter, IPredictor
from .services import EmailClassifierService

__all__ = [
    # Entities
    "Email",
    "SinglePrediction",
    "ClassificationResult",
    "ModelMetadata",
    # Types
    "LabelType",
    "VerdictType",
    "ModelType",
    "DetailLevel",
    # Ports
    "IModelLoader",
    "IPredictor",
    "IOutputFormatter",
    # Services
    "EmailClassifierService",
    # Constants
    "constants",
]
