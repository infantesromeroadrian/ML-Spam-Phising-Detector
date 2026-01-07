"""
Threat Report Entities for Security Analysis

Domain entities for IOC (Indicators of Compromise) and threat intelligence.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class IOC:
    """Indicator of Compromise"""

    type: str  # "url", "keyword_urgency", "keyword_financial", "pattern", "sender"
    severity: str  # "critical", "high", "medium", "low"
    value: str
    description: str
    count: int = 1

    def __post_init__(self) -> None:
        """Validate IOC fields"""
        valid_types = {"url", "keyword_urgency", "keyword_financial", "pattern", "sender"}
        if self.type not in valid_types:
            raise ValueError(f"Invalid IOC type: {self.type}")

        valid_severities = {"critical", "high", "medium", "low"}
        if self.severity not in valid_severities:
            raise ValueError(f"Invalid severity: {self.severity}")


@dataclass(frozen=True)
class ThreatVector:
    """Identified threat vector/attack pattern"""

    name: str
    description: str
    confidence: float  # 0.0 to 1.0

    def __post_init__(self) -> None:
        """Validate confidence"""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0 and 1, got {self.confidence}")


@dataclass(frozen=True)
class TriggerWord:
    """Word/feature that triggered classification"""

    word: str
    contribution: float  # Positive = pushes towards SPAM/PHISHING, Negative = towards HAM/LEGIT
    category: str  # "spam" or "phishing"

    @property
    def is_suspicious(self) -> bool:
        """True if word pushes towards malicious classification"""
        return self.contribution > 0


@dataclass(frozen=True)
class ThreatReport:
    """Complete threat analysis report"""

    risk_score: int  # 0-100
    iocs: list[IOC] = field(default_factory=list)
    threat_vectors: list[ThreatVector] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    spam_trigger_words: list[TriggerWord] = field(default_factory=list)
    phishing_trigger_words: list[TriggerWord] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate risk score"""
        if not 0 <= self.risk_score <= 100:
            raise ValueError(f"Risk score must be between 0 and 100, got {self.risk_score}")

    @property
    def critical_iocs(self) -> list[IOC]:
        """Get only critical severity IOCs"""
        return [ioc for ioc in self.iocs if ioc.severity == "critical"]

    @property
    def high_confidence_vectors(self) -> list[ThreatVector]:
        """Get threat vectors with >70% confidence"""
        return [v for v in self.threat_vectors if v.confidence > 0.7]

    @property
    def top_suspicious_words(self) -> list[str]:
        """Get top words that triggered malicious classification"""
        all_triggers = self.spam_trigger_words + self.phishing_trigger_words
        suspicious = [tw for tw in all_triggers if tw.is_suspicious]
        suspicious.sort(key=lambda x: abs(x.contribution), reverse=True)
        return [tw.word for tw in suspicious[:10]]
