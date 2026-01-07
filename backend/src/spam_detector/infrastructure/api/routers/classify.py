"""Classification endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Request, status

from ....application import Container
from ....domain.services.feature_explainer import FeatureExplainer
from ....domain.services.threat_analyzer import ThreatAnalyzer
from ..schemas import ClassificationResponse, ClassifyEmailRequest

router = APIRouter()

# Initialize services (stateless, can be singletons)
threat_analyzer = ThreatAnalyzer()
feature_explainer = FeatureExplainer()


def get_container(request: Request) -> Container:
    """
    Dependency to get container instance from app state.

    Args:
        request: FastAPI request object

    Returns:
        Container instance from app state
    """
    return request.app.state.container


@router.post(
    "/classify",
    response_model=ClassificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Classify email",
    description="""
    Classify an email as HAM, SPAM, PHISHING, or SPAM+PHISHING.

    Uses dual classification with both spam and phishing detectors
    to provide comprehensive email threat assessment.
    """,
    response_description="Classification result with detailed predictions",
)
def classify_email(
    request: ClassifyEmailRequest, container: Container = Depends(get_container)
) -> ClassificationResponse:
    """
    Classify an email as SPAM/PHISHING.

    Args:
        request: Email classification request with text and optional metadata
        container: DI container (injected)

    Returns:
        ClassificationResponse with complete classification results

    Raises:
        HTTPException 400: Invalid email text or validation error
        HTTPException 503: Model not loaded or unavailable
    """
    try:
        # Get use case from container
        use_case = container.get_classify_use_case()

        # Build full email text (subject + sender + body)
        full_text = request.email_text
        if request.subject:
            full_text = f"Subject: {request.subject}\n{full_text}"
        if request.sender:
            full_text = f"From: {request.sender}\n{full_text}"

        # Execute classification (use execute_raw to get domain entity)
        result = use_case.execute_raw(email_text=full_text)

        # Get model loader from container
        model_loader = container.get_model_loader()

        # Load SPAM model and vectorizer
        spam_vectorizer, spam_model, _ = model_loader.load("spam_detector")

        # Load PHISHING model and vectorizer
        phishing_vectorizer, phishing_model, _ = model_loader.load("phishing_detector")

        # Perform threat analysis (with feature explanation)
        threat_report = threat_analyzer.analyze(
            email=result.email,
            spam_prediction=result.spam_prediction,
            phishing_prediction=result.phishing_prediction,
            spam_model=spam_model,
            spam_vectorizer=spam_vectorizer,
            phishing_model=phishing_model,
            phishing_vectorizer=phishing_vectorizer,
            feature_explainer=feature_explainer,
        )

        # Convert domain entity → API response (with threat report)
        return ClassificationResponse.from_domain(result, threat_report)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Model not loaded: {e}"
        ) from e
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e
