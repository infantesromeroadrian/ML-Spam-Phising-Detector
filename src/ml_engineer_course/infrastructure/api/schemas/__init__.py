"""API request/response schemas."""

from .requests import ClassifyEmailRequest
from .responses import ClassificationResponse, ModelInfoResponse, ModelsListResponse

__all__ = [
    "ClassifyEmailRequest",
    "ClassificationResponse",
    "ModelInfoResponse",
    "ModelsListResponse",
]
