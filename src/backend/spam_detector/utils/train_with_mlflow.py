"""
Training script wrapper for MLflow tracking.

Usage:
    python -m spam_detector.utils.train_with_mlflow --model spam
    python -m spam_detector.utils.train_with_mlflow --model phishing
"""

import argparse
from datetime import datetime

import mlflow
import mlflow.sklearn

from .mlflow_config import setup_mlflow


def train_and_log(model_type: str, data_path: str):
    """
    Train model and log everything to MLflow.

    Args:
        model_type: "spam" or "phishing"
        data_path: Path to training data CSV
    """
    setup_mlflow()

    with mlflow.start_run(
        run_name=f"{model_type}_detector_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    ):
        # Log parameters
        mlflow.log_param("model_type", model_type)
        mlflow.log_param("algorithm", "LogisticRegression")
        mlflow.log_param("max_features_tfidf", 5000)
        mlflow.log_param("ngram_range", "(1, 2)")
        mlflow.log_param("data_path", data_path)

        # TODO: Load your data and train
        # For now, placeholder
        print(f"🎯 Training {model_type} detector...")
        print("⚠️  Replace this with actual training code from your notebooks")

        # Example metrics (replace with real ones)
        accuracy = 0.95 if model_type == "spam" else 0.92
        precision = 0.948 if model_type == "spam" else 0.915
        recall = 0.931 if model_type == "spam" else 0.903
        f1 = 0.939 if model_type == "spam" else 0.909

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        # Log tags
        mlflow.set_tag("stage", "development")
        mlflow.set_tag("team", "ml-team")

        # TODO: Log actual model artifacts
        # mlflow.sklearn.log_model(model, "model")
        # mlflow.sklearn.log_model(vectorizer, "vectorizer")

        print(f"✅ Run logged to MLflow")
        print(f"   Run ID: {mlflow.active_run().info.run_id}")
        print(f"   Accuracy: {accuracy:.3f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["spam", "phishing"], required=True)
    parser.add_argument("--data", default="data/email.csv")
    args = parser.parse_args()

    train_and_log(args.model, args.data)
