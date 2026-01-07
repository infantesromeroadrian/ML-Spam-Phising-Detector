# ML Models - Version Control

This directory contains versioned ML models tracked with **Git LFS** and **MLflow**.

## 📦 Model Versioning Strategy

### Git LFS (Production Models)
- Production-ready models are versioned with Git LFS
- Tagged releases (v1.0.0, v1.1.0, etc.)
- Stored in GitHub with LFS

### MLflow (Experiment Tracking)
- All training runs tracked in `mlruns/`
- Compare experiments: `mlflow ui`
- Best models promoted to production

## 🚀 Current Production Models

### v1.0.0 (Latest)

**SPAM Detector:**
- Algorithm: Logistic Regression
- Features: TF-IDF (5000 max features)
- Training: 5,000+ emails
- Accuracy: 95.2%
- Date: 2026-01-05

**PHISHING Detector:**
- Algorithm: Logistic Regression
- Features: TF-IDF + URL patterns
- Training: 3,500+ emails
- Accuracy: 92.1%
- Date: 2026-01-05

## 📊 View Experiment Tracking

```bash
# Start MLflow UI
mlflow ui

# Open browser
http://localhost:5000
```

## 🔄 Workflow

### 1. Train New Model (with MLflow tracking)

```bash
# Run training script (tracks to MLflow)
python -m ml_engineer_course.utils.train_with_mlflow --model spam
```

### 2. Compare in MLflow UI

```bash
mlflow ui
# Compare metrics, choose best model
```

### 3. Promote to Production

```bash
# Copy best model from mlruns/ to models/
cp mlruns/<experiment_id>/<run_id>/artifacts/model/model.joblib models/spam_detector_model_v1.1.0.joblib

# Update latest symlinks
ln -sf spam_detector_model_v1.1.0.joblib models/spam_detector_latest.joblib

# Commit with Git LFS
git add models/spam_detector_*.joblib
git commit -m "feat(models): release spam detector v1.1.0 - improved accuracy to 96%"
git tag -a v1.1.0 -m "Release v1.1.0"
git push --tags
```

## 📥 Download Models (Users)

Models are tracked with Git LFS, so clone will download them automatically:

```bash
git clone https://github.com/infantesromeroadrian/ML-Spam-Phising-Detector.git
cd ML-Spam-Phising-Detector

# Models are already downloaded via LFS
ls models/*.joblib
```

## 🔢 Model Naming Convention

```
{model_type}_{component}_{version}.joblib

Examples:
- spam_detector_model_v1.0.0.joblib
- spam_detector_vectorizer_v1.0.0.joblib
- spam_detector_metadata_v1.0.0.joblib
- phishing_detector_model_v1.0.0.joblib
```

## 📋 Version History

| Version | Date | Changes | Metrics |
|---------|------|---------|---------|
| v1.0.0 | 2026-01-05 | Initial release | SPAM: 95.2% acc, PHISHING: 92.1% acc |

