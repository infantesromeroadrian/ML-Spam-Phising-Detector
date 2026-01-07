"""
Threat Analysis Service

Analyzes emails for security threats, extracts IOCs, and identifies attack vectors.
"""

import re

from ..entities.email import Email
from ..entities.prediction import SinglePrediction
from ..entities.threat_report import IOC, ThreatReport, ThreatVector, TriggerWord

# Security keyword patterns
URGENCY_KEYWORDS = {
    "urgent",
    "immediately",
    "now",
    "asap",
    "hurry",
    "quick",
    "fast",
    "expire",
    "expiring",
    "deadline",
    "limited time",
    "act now",
    "don't wait",
}

FINANCIAL_KEYWORDS = {
    "password",
    "credit card",
    "bank",
    "account",
    "pin",
    "ssn",
    "social security",
    "verify",
    "confirm",
    "update payment",
    "billing",
    "invoice",
    "refund",
    "prize",
    "winner",
    "lottery",
}

SUSPICIOUS_PATTERNS = {
    r"\$+[\d,]+": "Money amounts",
    r"!{3,}": "Excessive exclamation marks",
    r"[A-Z]{10,}": "Excessive capitalization",
    r"click\s+here": "Generic link text (case insensitive)",
    r"http://[^\s]+": "Non-HTTPS URL",
}

# High-risk TLDs
RISKY_TLDS = {".ru", ".cn", ".tk", ".ml", ".ga", ".cf", ".gq"}


class ThreatAnalyzer:
    """
    Analyzes emails for security threats.

    Pure domain service - no infrastructure dependencies.
    """

    def analyze(
        self,
        email: Email,
        spam_prediction: SinglePrediction,
        phishing_prediction: SinglePrediction,
        spam_model=None,
        spam_vectorizer=None,
        phishing_model=None,
        phishing_vectorizer=None,
        feature_explainer=None,
    ) -> ThreatReport:
        """
        Perform comprehensive threat analysis.

        Args:
            email: The email to analyze
            spam_prediction: SPAM classification result
            phishing_prediction: PHISHING classification result
            spam_model: Trained SPAM model (optional, for feature explanation)
            spam_vectorizer: SPAM vectorizer (optional, for feature explanation)
            phishing_model: Trained PHISHING model (optional, for feature explanation)
            phishing_vectorizer: PHISHING vectorizer (optional, for feature explanation)
            feature_explainer: FeatureExplainer instance (optional)

        Returns:
            Complete threat report with IOCs and recommendations
        """
        iocs: list[IOC] = []
        threat_vectors: list[ThreatVector] = []
        recommendations: list[str] = []
        spam_trigger_words: list[TriggerWord] = []
        phishing_trigger_words: list[TriggerWord] = []

        # Calculate risk score (0-100)
        risk_score = self._calculate_risk_score(
            spam_prediction.probability, phishing_prediction.probability
        )

        # Extract IOCs
        iocs.extend(self._extract_urls(email.text))
        iocs.extend(self._detect_urgency_keywords(email.text))
        iocs.extend(self._detect_financial_keywords(email.text))
        iocs.extend(self._detect_suspicious_patterns(email.text))

        if email.sender:
            iocs.extend(self._analyze_sender(email.sender))

        # Identify threat vectors
        threat_vectors = self._identify_threat_vectors(spam_prediction, phishing_prediction, iocs)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            risk_score, spam_prediction, phishing_prediction, iocs
        )

        # Extract trigger words (ML feature explanation)
        if feature_explainer and spam_model and spam_vectorizer:
            spam_trigger_words = self._extract_trigger_words(
                email.text, spam_model, spam_vectorizer, feature_explainer, "spam"
            )

        if feature_explainer and phishing_model and phishing_vectorizer:
            phishing_trigger_words = self._extract_trigger_words(
                email.text, phishing_model, phishing_vectorizer, feature_explainer, "phishing"
            )

        return ThreatReport(
            risk_score=risk_score,
            iocs=iocs,
            threat_vectors=threat_vectors,
            recommendations=recommendations,
            spam_trigger_words=spam_trigger_words,
            phishing_trigger_words=phishing_trigger_words,
        )

    def _calculate_risk_score(self, spam_prob: float, phishing_prob: float) -> int:
        """
        Calculate overall risk score (0-100).

        Phishing is weighted higher as it's more dangerous.
        """
        # Phishing weight: 0.7, Spam weight: 0.3
        weighted_risk = (phishing_prob * 0.7) + (spam_prob * 0.3)
        return int(weighted_risk * 100)

    def _extract_urls(self, text: str) -> list[IOC]:
        """Extract URLs and assess their risk"""
        iocs = []

        # Find all URLs
        url_pattern = r'https?://[^\s<>"\']+'
        urls = re.findall(url_pattern, text, re.IGNORECASE)

        for url in urls:
            # Check if non-HTTPS
            is_http = url.startswith("http://")

            # Check for risky TLD
            has_risky_tld = any(url.lower().endswith(tld) for tld in RISKY_TLDS)

            # Determine severity
            if has_risky_tld:
                severity = "critical"
                description = "Suspicious URL with high-risk domain"
            elif is_http:
                severity = "high"
                description = "Insecure HTTP URL detected"
            else:
                severity = "medium"
                description = "URL detected in email"

            iocs.append(IOC(type="url", severity=severity, value=url, description=description))

        return iocs

    def _detect_urgency_keywords(self, text: str) -> list[IOC]:
        """Detect urgency manipulation tactics"""
        text_lower = text.lower()
        found_keywords = []

        for keyword in URGENCY_KEYWORDS:
            count = text_lower.count(keyword)
            if count > 0:
                found_keywords.append((keyword, count))

        if not found_keywords:
            return []

        total_count = sum(count for _, count in found_keywords)
        keywords_str = ", ".join(f"{kw} ({cnt}x)" for kw, cnt in found_keywords[:5])

        # More urgency keywords = higher severity
        if total_count >= 5:
            severity = "critical"
        elif total_count >= 3:
            severity = "high"
        else:
            severity = "medium"

        return [
            IOC(
                type="keyword_urgency",
                severity=severity,
                value=keywords_str,
                description="Urgency manipulation tactics detected",
                count=total_count,
            )
        ]

    def _detect_financial_keywords(self, text: str) -> list[IOC]:
        """Detect financial/credential harvesting attempts"""
        text_lower = text.lower()
        found_keywords = []

        for keyword in FINANCIAL_KEYWORDS:
            if keyword in text_lower:
                count = text_lower.count(keyword)
                found_keywords.append((keyword, count))

        if not found_keywords:
            return []

        keywords_str = ", ".join(kw for kw, _ in found_keywords[:5])

        # Financial keywords in suspicious email = critical
        return [
            IOC(
                type="keyword_financial",
                severity="critical",
                value=keywords_str,
                description="Financial credential request detected",
                count=len(found_keywords),
            )
        ]

    def _detect_suspicious_patterns(self, text: str) -> list[IOC]:
        """Detect suspicious text patterns"""
        iocs = []

        for pattern, description in SUSPICIOUS_PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                iocs.append(
                    IOC(
                        type="pattern",
                        severity="medium",
                        value=", ".join(matches[:3]),  # First 3 matches
                        description=description,
                        count=len(matches),
                    )
                )

        return iocs

    def _analyze_sender(self, sender: str) -> list[IOC]:
        """Analyze sender email/domain"""
        iocs = []

        # Extract domain from email
        if "@" in sender:
            domain = sender.split("@")[1].lower()

            # Check for risky TLD
            has_risky_tld = any(domain.endswith(tld) for tld in RISKY_TLDS)

            if has_risky_tld:
                iocs.append(
                    IOC(
                        type="sender",
                        severity="high",
                        value=domain,
                        description="Sender domain has high-risk TLD",
                    )
                )

        return iocs

    def _identify_threat_vectors(
        self,
        spam_prediction: SinglePrediction,
        phishing_prediction: SinglePrediction,
        iocs: list[IOC],
    ) -> list[ThreatVector]:
        """Identify attack vectors based on predictions and IOCs"""
        vectors = []

        # Social engineering (urgency keywords)
        urgency_iocs = [ioc for ioc in iocs if ioc.type == "keyword_urgency"]
        if urgency_iocs:
            vectors.append(
                ThreatVector(
                    name="Social Engineering",
                    description="Uses urgency tactics to manipulate victims",
                    confidence=min(urgency_iocs[0].count / 10.0, 1.0),
                )
            )

        # Credential harvesting (financial keywords + URLs)
        financial_iocs = [ioc for ioc in iocs if ioc.type == "keyword_financial"]
        url_iocs = [ioc for ioc in iocs if ioc.type == "url"]

        if financial_iocs and url_iocs:
            vectors.append(
                ThreatVector(
                    name="Credential Harvesting",
                    description="Attempts to steal login credentials or financial information",
                    confidence=phishing_prediction.probability,
                )
            )

        # Phishing attack
        if phishing_prediction.probability > 0.7:
            vectors.append(
                ThreatVector(
                    name="Phishing Attack",
                    description="Email designed to deceive recipients into revealing sensitive data",
                    confidence=phishing_prediction.probability,
                )
            )

        # Spam campaign
        if spam_prediction.probability > 0.7:
            vectors.append(
                ThreatVector(
                    name="Spam Campaign",
                    description="Unsolicited bulk email, potentially part of larger campaign",
                    confidence=spam_prediction.probability,
                )
            )

        return vectors

    def _generate_recommendations(
        self,
        risk_score: int,
        spam_prediction: SinglePrediction,
        phishing_prediction: SinglePrediction,
        iocs: list[IOC],
    ) -> list[str]:
        """Generate security recommendations"""
        recommendations = []

        # Critical recommendations
        if risk_score >= 70:
            recommendations.append("🚫 Quarantine this email immediately")
            recommendations.append("🔒 Block sender domain")

        if phishing_prediction.probability > 0.7:
            recommendations.append("⚠️  Alert security team about potential phishing")
            recommendations.append("📊 Add to threat intelligence database")

        # URL-specific recommendations
        url_iocs = [ioc for ioc in iocs if ioc.type == "url"]
        if url_iocs:
            recommendations.append("🔗 Do NOT click any links in this email")
            if any(ioc.severity in ["critical", "high"] for ioc in url_iocs):
                recommendations.append("🛡️  Add URLs to blocklist")

        # Sender recommendations
        sender_iocs = [ioc for ioc in iocs if ioc.type == "sender"]
        if sender_iocs:
            recommendations.append("📧 Mark sender as malicious")

        # If safe
        if risk_score < 30:
            recommendations.append("✅ Email appears legitimate, safe to process")

        return recommendations

    def _extract_trigger_words(
        self,
        text: str,
        model,
        vectorizer,
        feature_explainer,
        category: str,
    ) -> list[TriggerWord]:
        """
        Extract words that triggered the classification decision.

        Args:
            text: Email text
            model: Trained model
            vectorizer: Fitted vectorizer
            feature_explainer: FeatureExplainer instance
            category: "spam" or "phishing"

        Returns:
            List of TriggerWord entities
        """
        try:
            # Get feature contributions
            contributions = feature_explainer.explain_prediction(
                text=text, vectorizer=vectorizer, model=model, top_n=10
            )

            # Convert to TriggerWord entities
            trigger_words = []
            for word, contribution in contributions:
                trigger_words.append(
                    TriggerWord(word=word, contribution=float(contribution), category=category)
                )

            return trigger_words

        except Exception as e:
            # If feature explanation fails, return empty list (graceful degradation)
            print(f"Warning: Feature explanation failed for {category}: {e}")
            return []
