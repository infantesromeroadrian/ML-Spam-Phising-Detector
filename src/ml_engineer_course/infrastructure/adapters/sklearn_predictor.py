"""Sklearn predictor - Makes predictions using sklearn models."""

from typing import Any, Literal

from ...domain.entities import Email, LabelType, ModelMetadata, SinglePrediction

PredictorType = Literal["spam", "phishing"]


class SklearnPredictor:
    """
    Email classifier using sklearn models.

    Implements IPredictor port for making predictions with
    scikit-learn models (Logistic Regression + TF-IDF vectorizer).

    Attributes:
        _vectorizer: Fitted TF-IDF vectorizer
        _model: Trained sklearn classifier
        _metadata: Model metadata
        _predictor_type: Type of prediction ("spam" or "phishing")

    Examples:
        >>> predictor = SklearnPredictor(
        ...     vectorizer=vec,
        ...     model=clf,
        ...     metadata=meta,
        ...     predictor_type="spam"
        ... )
        >>> email = Email(text="WINNER! Click here!")
        >>> prediction = predictor.predict(email)
        >>> prediction.label
        'SPAM'
        >>> prediction.probability
        0.85
    """

    def __init__(
        self, vectorizer: Any, model: Any, metadata: ModelMetadata, predictor_type: PredictorType
    ) -> None:
        """
        Initialize predictor with sklearn components.

        Args:
            vectorizer: Fitted TF-IDF vectorizer
            model: Trained sklearn classifier
            metadata: Model metadata
            predictor_type: "spam" or "phishing"
        """
        self._vectorizer = vectorizer
        self._model = model
        self._metadata = metadata
        self._predictor_type = predictor_type

    def predict(self, email: Email) -> SinglePrediction:
        """
        Predict classification for an email.

        Args:
            email: Email entity to classify

        Returns:
            SinglePrediction with label, probability, and model info

        Raises:
            ValueError: If email text cannot be vectorized
        """
        try:
            # Vectorize email text
            text_vectorized = self._vectorizer.transform([email.text])

            # Get prediction and probabilities
            prediction = self._model.predict(text_vectorized)[0]
            probabilities = self._model.predict_proba(text_vectorized)[0]

            # Convert prediction to label
            label = self._convert_to_label(prediction)

            # Get probability for predicted class
            probability = probabilities[prediction]

            return SinglePrediction(
                label=label,
                probability=float(probability),
                model_name=self._metadata.name,
                model_timestamp=self._metadata.timestamp,
            )

        except Exception as e:
            raise ValueError(f"Failed to vectorize or predict email: {e}") from e

    # === Private methods ===

    def _convert_to_label(self, prediction: int) -> LabelType:
        """
        Convert numeric prediction to label.

        Args:
            prediction: 0 or 1 from model

        Returns:
            Label string based on predictor type
        """
        if self._predictor_type == "spam":
            # 0 = HAM, 1 = SPAM
            return "SPAM" if prediction == 1 else "HAM"
        else:  # phishing
            # 0 = LEGIT, 1 = PHISHING
            return "PHISHING" if prediction == 1 else "LEGIT"
