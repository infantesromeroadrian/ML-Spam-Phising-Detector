"""Integration tests for FastAPI endpoints."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from ml_engineer_course.application import Container
from ml_engineer_course.config import settings
from ml_engineer_course.infrastructure.api.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create FastAPI test client with initialized container."""
    # Initialize container and attach to app state
    container = Container(settings)
    app.state.container = container

    # Create test client with app
    with TestClient(app) as test_client:
        yield test_client


class TestHealthEndpoints:
    """Test health and info endpoints."""

    def test_root_endpoint(self, client: TestClient) -> None:
        """Test root endpoint returns HTML landing page."""
        response = client.get("/")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Email Classifier" in response.text
        assert "Launch App" in response.text

    def test_health_endpoint(self, client: TestClient) -> None:
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestClassifyEndpoint:
    """Test email classification endpoint."""

    def test_classify_spam(self, client: TestClient) -> None:
        """Test classification of obvious spam email."""
        payload = {
            "email_text": "WINNER! You have won $1000! Click here NOW to claim!",
            "subject": "Urgent Prize Notification",
            "sender": "scam@fake.com",
        }

        response = client.post("/api/v1/classify", json=payload)

        assert response.status_code == 200
        data = response.json()

        # Check structure
        assert "verdict" in data
        assert "risk_level" in data
        assert "is_malicious" in data
        assert "spam_label" in data
        assert "spam_probability" in data
        assert "spam_model_version" in data
        assert "phishing_label" in data
        assert "phishing_probability" in data
        assert "phishing_model_version" in data
        assert "execution_time_ms" in data

        # Check types
        assert isinstance(data["is_malicious"], bool)
        assert isinstance(data["spam_probability"], float)
        assert isinstance(data["phishing_probability"], float)
        assert isinstance(data["execution_time_ms"], float)

        # Check ranges
        assert 0.0 <= data["spam_probability"] <= 1.0
        assert 0.0 <= data["phishing_probability"] <= 1.0
        assert data["execution_time_ms"] >= 0.0

    def test_classify_ham(self, client: TestClient) -> None:
        """Test classification of legitimate email."""
        payload = {
            "email_text": "Hello John, hope you're doing well. Let's catch up next week.",
            "subject": "Catching up",
            "sender": "friend@example.com",
        }

        response = client.post("/api/v1/classify", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert data["verdict"] == "HAM"
        assert data["is_malicious"] is False
        assert data["risk_level"] in ["LOW", "MEDIUM"]

    def test_classify_minimal_payload(self, client: TestClient) -> None:
        """Test classification with only email_text (no subject/sender)."""
        payload = {"email_text": "This is a simple test email."}

        response = client.post("/api/v1/classify", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "verdict" in data

    def test_classify_empty_text_fails(self, client: TestClient) -> None:
        """Test that empty email text returns validation error."""
        payload = {"email_text": ""}

        response = client.post("/api/v1/classify", json=payload)

        assert response.status_code == 422  # Validation error

    def test_classify_missing_email_text_fails(self, client: TestClient) -> None:
        """Test that missing email_text returns validation error."""
        payload = {"subject": "Test"}

        response = client.post("/api/v1/classify", json=payload)

        assert response.status_code == 422  # Validation error


class TestModelsEndpoints:
    """Test model management endpoints."""

    def test_list_spam_models(self, client: TestClient) -> None:
        """Test listing spam detector models."""
        response = client.get("/api/v1/models/spam_detector")

        assert response.status_code == 200
        data = response.json()

        assert "model_name" in data
        assert data["model_name"] == "spam_detector"
        assert "total_versions" in data
        assert "models" in data
        assert isinstance(data["models"], list)
        assert data["total_versions"] == len(data["models"])

        # Check model metadata structure if models exist
        if data["models"]:
            model = data["models"][0]
            assert "name" in model
            assert "timestamp" in model
            assert "accuracy" in model
            assert "accuracy_percent" in model
            assert "train_samples" in model
            assert "vocabulary_size" in model
            assert "file_size_mb" in model

    def test_list_phishing_models(self, client: TestClient) -> None:
        """Test listing phishing detector models."""
        response = client.get("/api/v1/models/phishing_detector")

        assert response.status_code == 200
        data = response.json()

        assert data["model_name"] == "phishing_detector"
        assert "total_versions" in data
        assert "models" in data

    def test_get_latest_spam_model(self, client: TestClient) -> None:
        """Test getting latest spam detector model."""
        response = client.get("/api/v1/models/spam_detector/latest")

        assert response.status_code == 200
        data = response.json()

        assert "name" in data
        assert data["name"] == "spam_detector"
        assert "timestamp" in data
        assert "accuracy" in data
        assert 0.0 <= data["accuracy"] <= 1.0

    def test_get_latest_phishing_model(self, client: TestClient) -> None:
        """Test getting latest phishing detector model."""
        response = client.get("/api/v1/models/phishing_detector/latest")

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == "phishing_detector"

    def test_invalid_model_name_fails(self, client: TestClient) -> None:
        """Test that invalid model name returns error."""
        response = client.get("/api/v1/models/invalid_model")

        assert response.status_code == 422  # Validation error


class TestOpenAPISchema:
    """Test OpenAPI documentation."""

    def test_openapi_schema_available(self, client: TestClient) -> None:
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        data = response.json()

        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "Email Classifier API"
        assert data["info"]["version"] == "1.0.0"
        assert "paths" in data

    def test_swagger_docs_available(self, client: TestClient) -> None:
        """Test that Swagger UI is available."""
        response = client.get("/docs")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_redoc_available(self, client: TestClient) -> None:
        """Test that ReDoc is available."""
        response = client.get("/redoc")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
