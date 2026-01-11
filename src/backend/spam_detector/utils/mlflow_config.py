"""MLflow configuration for model tracking."""

import mlflow

# Set tracking URI (local)
MLFLOW_TRACKING_URI = "file:./mlruns"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Set default experiment
DEFAULT_EXPERIMENT = "spam-phishing-detection"


def setup_mlflow():
    """Initialize MLflow configuration."""
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    # Create experiment if doesn't exist
    try:
        experiment_id = mlflow.create_experiment(
            DEFAULT_EXPERIMENT,
            tags={
                "project": "ML-Spam-Phising-Detector",
                "framework": "scikit-learn",
                "type": "email-classification",
            },
        )
        print(f"✅ Created experiment: {DEFAULT_EXPERIMENT} (ID: {experiment_id})")
    except Exception:
        experiment = mlflow.get_experiment_by_name(DEFAULT_EXPERIMENT)
        print(
            f"✅ Using existing experiment: {DEFAULT_EXPERIMENT} (ID: {experiment.experiment_id})"
        )

    mlflow.set_experiment(DEFAULT_EXPERIMENT)
    return DEFAULT_EXPERIMENT


if __name__ == "__main__":
    setup_mlflow()
