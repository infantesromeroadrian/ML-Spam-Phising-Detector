"""Domain ports - Protocols defining interfaces."""

from .model_loader import IModelLoader
from .output_formatter import DetailLevel, IOutputFormatter
from .predictor import IPredictor

__all__ = [
    "IModelLoader",
    "IPredictor",
    "IOutputFormatter",
    "DetailLevel",
]
