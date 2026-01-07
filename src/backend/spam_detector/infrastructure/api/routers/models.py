"""Models management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Path, Request, status

from ....application import Container
from ....domain.entities import ModelType
from ..schemas import ModelInfoResponse, ModelsListResponse

router = APIRouter()


def get_container(request: Request) -> Container:
    """
    Dependency to get container instance from app state.

    Args:
        request: FastAPI request object

    Returns:
        Container instance from app state
    """
    return request.app.state.container


@router.get(
    "/models/{model_name}",
    response_model=ModelsListResponse,
    status_code=status.HTTP_200_OK,
    summary="List model versions",
    description="Get list of all available versions for a specific model type.",
    response_description="List of model versions with metadata",
)
def list_models(
    model_name: ModelType = Path(
        ..., description="Model type (spam_detector or phishing_detector)"
    ),
    container: Container = Depends(get_container),
) -> ModelsListResponse:
    """
    List all available versions of a model.

    Args:
        model_name: Type of model to list
        container: DI container (injected)

    Returns:
        ModelsListResponse with all versions

    Raises:
        HTTPException 400: Invalid model name
    """
    try:
        use_case = container.get_list_models_use_case()
        models = use_case.execute(model_name)

        return ModelsListResponse(
            model_name=model_name,
            total_versions=len(models),
            models=[ModelInfoResponse.from_domain(m) for m in models],
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.get(
    "/models/{model_name}/latest",
    response_model=ModelInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get latest model",
    description="Get metadata for the latest version of a specific model type.",
    response_description="Latest model metadata",
)
def get_latest_model(
    model_name: ModelType = Path(
        ..., description="Model type (spam_detector or phishing_detector)"
    ),
    container: Container = Depends(get_container),
) -> ModelInfoResponse:
    """
    Get info about latest model version.

    Args:
        model_name: Type of model
        container: DI container (injected)

    Returns:
        ModelInfoResponse for latest version

    Raises:
        HTTPException 404: No models found
    """
    try:
        use_case = container.get_list_models_use_case()
        latest = use_case.get_latest(model_name)

        if not latest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No models found for '{model_name}'",
            )

        return ModelInfoResponse.from_domain(latest)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e
