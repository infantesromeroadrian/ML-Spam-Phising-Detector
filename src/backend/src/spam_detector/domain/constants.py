"""Domain-level constants.

Constants that are intrinsic to the business domain and should not change
based on configuration or environment.
"""

# Model names
VALID_MODEL_NAMES = frozenset({"spam_detector", "phishing_detector"})
MODEL_DISPLAY_NAMES = {
    "spam_detector": "SPAM Detector",
    "phishing_detector": "Phishing Detector",
}

# Email display
EMAIL_PREVIEW_LENGTH = 100

# Time conversion
SECONDS_TO_MILLISECONDS = 1000
MILLISECONDS_TO_SECONDS = 0.001

# Percentage conversion
PERCENTAGE_MULTIPLIER = 100

# Model file patterns
MODEL_FILE_EXTENSION = ".joblib"
MODEL_COMPONENTS = frozenset({"model", "vectorizer", "metadata"})

# Label mappings for predictions
SPAM_LABELS = {0: "HAM", 1: "SPAM"}
PHISHING_LABELS = {0: "LEGIT", 1: "PHISHING"}

# Risk level icons (for text formatters)
RISK_ICONS = {
    "LOW": "✅",
    "MEDIUM": "⚠️",
    "HIGH": "🔴",
    "CRITICAL": "🚨",
}

# Verdict styles (for text formatters)
VERDICT_STYLES = {
    "HAM": "green",
    "SPAM": "red",
    "PHISHING": "yellow",
    "SPAM+PHISHING": "bold red",
}

# Prediction icons
POSITIVE_PREDICTION_ICON = "🔴"
NEGATIVE_PREDICTION_ICON = "🟢"
