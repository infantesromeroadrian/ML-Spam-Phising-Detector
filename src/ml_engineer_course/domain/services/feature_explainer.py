"""
Feature Explainer Service

Explains ML predictions by showing which features (words) contributed most
to the classification decision.
"""

import re

import numpy as np


class FeatureExplainer:
    """
    Explains classification decisions by analyzing feature importance.

    For Logistic Regression models, uses coefficients to determine
    which words most strongly influenced the prediction.
    """

    def explain_prediction(
        self, text: str, vectorizer, model, top_n: int = 10
    ) -> list[tuple[str, float]]:
        """
        Get top contributing features for a specific text.

        Args:
            text: The text that was classified
            vectorizer: Fitted TfidfVectorizer
            model: Fitted LogisticRegression model
            top_n: Number of top features to return

        Returns:
            List of (feature_name, contribution_score) tuples, sorted by absolute contribution
        """
        # Get feature names from vectorizer
        try:
            feature_names = vectorizer.get_feature_names_out()
        except AttributeError:
            # Fallback for older sklearn versions
            feature_names = vectorizer.get_feature_names()

        # Transform the text to get TF-IDF values
        text_vector = vectorizer.transform([text])

        # Get model coefficients (feature importance)
        # For binary classification, coef_ shape is (1, n_features)
        coefficients = model.coef_[0]

        # Get indices of non-zero features in this text
        # (only words that appear in this specific email)
        text_features = text_vector.toarray()[0]
        non_zero_indices = np.where(text_features > 0)[0]

        # Calculate contribution for each feature
        # Contribution = TF-IDF value * coefficient
        contributions = []
        for idx in non_zero_indices:
            feature_name = feature_names[idx]
            tfidf_value = text_features[idx]
            coefficient = coefficients[idx]
            contribution = tfidf_value * coefficient

            contributions.append((feature_name, contribution))

        # Sort by absolute contribution (strongest influence, positive or negative)
        contributions.sort(key=lambda x: abs(x[1]), reverse=True)

        return contributions[:top_n]

    def get_top_spam_indicators(
        self, vectorizer, model, top_n: int = 20
    ) -> list[tuple[str, float]]:
        """
        Get top words that generally indicate SPAM (global feature importance).

        Args:
            vectorizer: Fitted TfidfVectorizer
            model: Fitted LogisticRegression model
            top_n: Number of top features to return

        Returns:
            List of (word, coefficient) tuples for top SPAM indicators
        """
        try:
            feature_names = vectorizer.get_feature_names_out()
        except AttributeError:
            feature_names = vectorizer.get_feature_names()

        coefficients = model.coef_[0]

        # Get indices sorted by coefficient (highest = strongest SPAM indicator)
        top_indices = np.argsort(coefficients)[::-1][:top_n]

        return [(feature_names[idx], coefficients[idx]) for idx in top_indices]

    def get_top_ham_indicators(self, vectorizer, model, top_n: int = 20) -> list[tuple[str, float]]:
        """
        Get top words that generally indicate HAM/LEGIT (global feature importance).

        Args:
            vectorizer: Fitted TfidfVectorizer
            model: Fitted LogisticRegression model
            top_n: Number of top features to return

        Returns:
            List of (word, coefficient) tuples for top HAM indicators
        """
        try:
            feature_names = vectorizer.get_feature_names_out()
        except AttributeError:
            feature_names = vectorizer.get_feature_names()

        coefficients = model.coef_[0]

        # Get indices sorted by coefficient (lowest = strongest HAM indicator)
        bottom_indices = np.argsort(coefficients)[:top_n]

        return [(feature_names[idx], coefficients[idx]) for idx in bottom_indices]

    def format_explanation(
        self, contributions: list[tuple[str, float]], threshold: float = 0.01
    ) -> dict[str, list[str]]:
        """
        Format feature contributions into human-readable explanation.

        Args:
            contributions: List of (feature, contribution) tuples
            threshold: Minimum absolute contribution to include

        Returns:
            Dict with 'positive' and 'negative' lists of features
        """
        positive = []  # Features pushing towards SPAM/PHISHING
        negative = []  # Features pushing towards HAM/LEGIT

        for feature, contribution in contributions:
            if abs(contribution) < threshold:
                continue

            if contribution > 0:
                positive.append(f"{feature} (+{contribution:.3f})")
            else:
                negative.append(f"{feature} ({contribution:.3f})")

        return {
            "positive": positive,  # Suspicious indicators
            "negative": negative,  # Legitimate indicators
        }

    def extract_triggered_words(
        self, text: str, contributions: list[tuple[str, float]], min_contribution: float = 0.05
    ) -> list[str]:
        """
        Extract actual words from text that triggered the classification.

        Args:
            text: Original email text
            contributions: Feature contributions from explain_prediction()
            min_contribution: Minimum contribution to consider

        Returns:
            List of words found in text that strongly contributed
        """
        triggered = []
        text_lower = text.lower()

        for feature, contribution in contributions:
            if abs(contribution) >= min_contribution:
                # Check if feature appears in text (simple word boundary check)
                if re.search(r"\b" + re.escape(feature) + r"\b", text_lower):
                    triggered.append(feature)

        return triggered[:10]  # Limit to top 10 actual words
