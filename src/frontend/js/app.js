/**
 * Email Threat Intelligence Platform
 * Professional SOC-Grade Frontend Application
 */

const API_BASE = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : `${window.location.protocol}//${window.location.hostname}:8000`;

const API = {
    classify: `${API_BASE}/api/v1/classify`,
    health: `${API_BASE}/health`,
    models: `${API_BASE}/api/v1/models`,
};

// Sample threat emails for testing
const SAMPLES = {
    spam: {
        subject: "WINNER! Claim Your Prize NOW",
        sender: "prize@lottery-notification.xyz",
        body: `CONGRATULATIONS! You have WON $1,000,000 in our EXCLUSIVE lottery draw!

Click here IMMEDIATELY to claim your prize before it EXPIRES!
This is a LIMITED TIME OFFER - Act NOW or lose your winnings FOREVER!

NO PURCHASE NECESSARY! FREE MONEY! CLICK HERE!

Verify your bank account details to receive instant transfer:
Account Number: _______
Routing Number: _______
SSN: _______

URGENT! Only 24 hours remaining! Don't miss this opportunity!`
    },
    phishing: {
        subject: "URGENT: Verify Your PayPal Account",
        sender: "security@paypa1-verify.com",
        body: `Dear Valued Customer,

We have detected SUSPICIOUS ACTIVITY on your PayPal account from an unrecognized device in Nigeria.

For your security, we have TEMPORARILY SUSPENDED your account.

IMMEDIATE ACTION REQUIRED:
Click here to verify your identity: http://paypa1-secure-login.com/verify

You must complete verification within 24 HOURS or your account will be PERMANENTLY CLOSED and all funds will be FORFEIT.

Required information:
- Full Name
- Credit Card Number
- CVV Code
- Social Security Number
- Date of Birth

Failure to comply will result in legal action.

Thank you for your immediate attention to this matter.
PayPal Security Team`
    },
    combined: {
        subject: "Bank Alert: Suspicious Transaction Detected - FREE iPhone Giveaway",
        sender: "alerts@chase-secure-banking.xyz",
        body: `URGENT SECURITY ALERT + SPECIAL OFFER!

Your Chase Bank account has been LOCKED due to suspicious activity.

CLICK HERE to unlock: http://chase-verify-secure.com/unlock

⚠️ WARNING: Failure to verify within 12 hours will result in permanent account closure!

PLUS - As a valued customer, you've been selected for our EXCLUSIVE iPhone 15 Pro MAX GIVEAWAY!
Absolutely FREE! No purchase necessary!

To claim BOTH:
1. Verify your account (Username, Password, SSN, Card Number)
2. Pay only $9.99 shipping for your FREE iPhone!

ACT NOW! Limited time offer! WINNER WINNER! Click here!

This is your FINAL NOTICE! Don't miss out!`
    }
};

// DOM Elements
const $ = {
    // Form inputs
    emailSender: document.getElementById('email-sender'),
    emailSubject: document.getElementById('email-subject'),
    emailBody: document.getElementById('email-body'),
    charCount: document.getElementById('char-count'),
    analyzeBtn: document.getElementById('analyze-btn'),
    clearBtn: document.getElementById('clear-btn'),
    btnText: document.getElementById('btn-text'),
    btnSpinner: document.getElementById('btn-spinner'),
    
    // Status indicators
    backendStatus: document.getElementById('backend-status'),
    statusText: document.getElementById('status-text'),
    modelsStatus: document.getElementById('models-status'),
    modelInfo: document.getElementById('model-info'),
    
    // States
    initialState: document.getElementById('initial-state'),
    errorState: document.getElementById('error-state'),
    resultsState: document.getElementById('results-state'),
    errorMessage: document.getElementById('error-message'),
    dismissError: document.getElementById('dismiss-error'),
    
    // Results elements
    executionTime: document.getElementById('execution-time'),
    verdictCard: document.getElementById('verdict-card'),
    verdictValue: document.getElementById('verdict-value'),
    riskCard: document.getElementById('risk-card'),
    riskValue: document.getElementById('risk-value'),
    riskScoreFill: document.getElementById('risk-score-fill'),
    riskScoreText: document.getElementById('risk-score-text'),
    
    // Model predictions
    spamVersion: document.getElementById('spam-version'),
    spamLabel: document.getElementById('spam-label'),
    spamConfidence: document.getElementById('spam-confidence'),
    spamConfidenceBar: document.getElementById('spam-confidence-bar'),
    phishingVersion: document.getElementById('phishing-version'),
    phishingLabel: document.getElementById('phishing-label'),
    phishingConfidence: document.getElementById('phishing-confidence'),
    phishingConfidenceBar: document.getElementById('phishing-confidence-bar'),
    
    // Threat intelligence
    threatVectorsList: document.getElementById('threat-vectors-list'),
    iocsSubsection: document.getElementById('iocs-subsection'),
    iocsList: document.getElementById('iocs-list'),
    spamFeaturesList: document.getElementById('spam-features-list'),
    phishingFeaturesList: document.getElementById('phishing-features-list'),
    recommendationsSubsection: document.getElementById('recommendations-subsection'),
    recommendationsList: document.getElementById('recommendations-list'),
};

// API Service Layer
class ThreatIntelligenceAPI {
    static async checkHealth() {
        const response = await fetch(API.health);
        if (!response.ok) throw new Error('Backend unreachable');
        return response.json();
    }

    static async analyzeEmail(emailData) {
        const response = await fetch(API.classify, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(emailData),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }
        
        return response.json();
    }
}

// UI Controller
class DashboardUI {
    static showLoading() {
        $.analyzeBtn.disabled = true;
        $.btnText.textContent = 'Analyzing Threat...';
        $.btnSpinner.classList.remove('hidden');
        $.errorState.classList.add('hidden');
    }

    static hideLoading() {
        $.analyzeBtn.disabled = false;
        $.btnText.textContent = 'Analyze Threat';
        $.btnSpinner.classList.add('hidden');
    }

    static showError(message) {
        $.initialState.classList.add('hidden');
        $.resultsState.classList.add('hidden');
        $.errorState.classList.remove('hidden');
        $.errorMessage.textContent = message;
    }

    static updateBackendStatus(online, modelsCount = null) {
        const pulseError = $.backendStatus.querySelector('.pulse-dot');
        
        if (online) {
            pulseError.classList.add('online');
            pulseError.classList.remove('offline');
            $.statusText.textContent = 'Connected';
            $.modelsStatus.textContent = modelsCount ? `${modelsCount} Active` : 'Ready';
        } else {
            pulseError.classList.add('offline');
            pulseError.classList.remove('online');
            $.statusText.textContent = 'Disconnected';
            $.modelsStatus.textContent = 'N/A';
        }
    }

    static displayResults(data) {
        $.initialState.classList.add('hidden');
        $.errorState.classList.add('hidden');
        $.resultsState.classList.remove('hidden');

        // Execution time
        $.executionTime.textContent = `⚡ ${data.execution_time_ms.toFixed(2)} ms`;

        // Verdict
        const verdict = data.verdict || 'UNKNOWN';
        $.verdictValue.textContent = verdict;
        $.verdictValue.className = 'verdict-value ' + this.getVerdictClass(verdict);

        // Risk assessment
        const riskLevel = data.risk_level || 'UNKNOWN';
        const riskScore = data.threat_report?.risk_score || 0;
        $.riskValue.textContent = riskLevel;
        $.riskValue.className = 'risk-value ' + riskLevel.toLowerCase();
        $.riskScoreFill.style.width = `${riskScore}%`;
        $.riskScoreFill.className = 'risk-score-fill ' + riskLevel.toLowerCase();
        $.riskScoreText.textContent = `${riskScore}/100`;

        // SPAM model
        $.spamVersion.textContent = `v${data.spam_model_version}`;
        $.spamLabel.textContent = data.spam_label || 'N/A';
        $.spamLabel.className = 'prediction-label ' + (data.spam_label || '').toLowerCase();
        const spamProb = (data.spam_probability * 100).toFixed(1);
        $.spamConfidence.textContent = `${spamProb}%`;
        $.spamConfidenceBar.style.width = `${spamProb}%`;

        // Phishing model
        $.phishingVersion.textContent = `v${data.phishing_model_version}`;
        $.phishingLabel.textContent = data.phishing_label || 'N/A';
        $.phishingLabel.className = 'prediction-label ' + (data.phishing_label || '').toLowerCase();
        const phishingProb = (data.phishing_probability * 100).toFixed(1);
        $.phishingConfidence.textContent = `${phishingProb}%`;
        $.phishingConfidenceBar.style.width = `${phishingProb}%`;

        // Threat intelligence
        if (data.threat_report) {
            this.renderThreatIntelligence(data.threat_report);
        }

        // Scroll to results
        $.resultsState.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    static renderThreatIntelligence(report) {
        // Threat vectors
        if (report.threat_vectors?.length > 0) {
            $.threatVectorsList.innerHTML = report.threat_vectors.map(v => `
                <div class="threat-vector-item">
                    <div class="vector-name">${v.name}</div>
                    <div class="vector-description">${v.description}</div>
                    <div class="vector-confidence">Confidence: ${(v.confidence * 100).toFixed(1)}%</div>
                </div>
            `).join('');
        }

        // IOCs
        if (report.iocs?.length > 0) {
            $.iocsSubsection.classList.remove('hidden');
            $.iocsList.innerHTML = report.iocs.map(ioc => `
                <div class="ioc-item ${ioc.severity}">
                    <div class="ioc-header">
                        <span class="ioc-type">${ioc.type}</span>
                        <span class="ioc-severity ${ioc.severity}">${ioc.severity}</span>
                    </div>
                    <div class="ioc-value">${ioc.value}</div>
                    <div class="ioc-description">${ioc.description} (${ioc.count} occurrence${ioc.count > 1 ? 's' : ''})</div>
                </div>
            `).join('');
        } else {
            $.iocsSubsection.classList.add('hidden');
        }

        // SPAM trigger words
        if (report.spam_trigger_words?.length > 0) {
            $.spamFeaturesList.innerHTML = report.spam_trigger_words.slice(0, 10).map(w => `
                <div class="feature-item">
                    <span class="feature-word">${w.word}</span>
                    <span class="feature-score">+${w.contribution.toFixed(2)}</span>
                </div>
            `).join('');
        }

        // Phishing trigger words
        if (report.phishing_trigger_words?.length > 0) {
            $.phishingFeaturesList.innerHTML = report.phishing_trigger_words.slice(0, 10).map(w => `
                <div class="feature-item">
                    <span class="feature-word">${w.word}</span>
                    <span class="feature-score">+${w.contribution.toFixed(2)}</span>
                </div>
            `).join('');
        }

        // Recommendations
        if (report.recommendations?.length > 0) {
            $.recommendationsSubsection.classList.remove('hidden');
            $.recommendationsList.innerHTML = report.recommendations.map(rec => `
                <div class="recommendation-item">${rec}</div>
            `).join('');
        } else {
            $.recommendationsSubsection.classList.add('hidden');
        }
    }

    static getVerdictClass(verdict) {
        const map = {
            'HAM': 'safe',
            'LEGITIMATE': 'safe',
            'SPAM': 'spam',
            'PHISHING': 'phishing',
            'SPAM+PHISHING': 'critical',
        };
        return map[verdict] || '';
    }

    static clearForm() {
        $.emailSender.value = '';
        $.emailSubject.value = '';
        $.emailBody.value = '';
        $.charCount.textContent = '0 characters';
        $.errorState.classList.add('hidden');
        $.resultsState.classList.add('hidden');
        $.initialState.classList.remove('hidden');
        $.emailBody.focus();
    }

    static loadSample(type) {
        const sample = SAMPLES[type];
        if (!sample) return;
        
        $.emailSender.value = sample.sender;
        $.emailSubject.value = sample.subject;
        $.emailBody.value = sample.body;
        $.charCount.textContent = `${sample.body.length} characters`;
        $.emailBody.focus();
    }
}

// Event Handlers
async function handleAnalysis(event) {
    event.preventDefault();
    
    const emailBody = $.emailBody.value.trim();
    if (!emailBody) {
        DashboardUI.showError('Email body is required for analysis');
        return;
    }

    // Build email payload (backend expects 'email_text')
    let fullText = emailBody;
    const subject = $.emailSubject.value.trim();
    const sender = $.emailSender.value.trim();
    
    if (subject) fullText = `Subject: ${subject}\n${fullText}`;
    if (sender) fullText = `From: ${sender}\n${fullText}`;

    DashboardUI.showLoading();

    try {
        const result = await ThreatIntelligenceAPI.analyzeEmail({ 
            email_text: fullText 
        });
        DashboardUI.displayResults(result);
    } catch (error) {
        DashboardUI.showError(`Analysis failed: ${error.message}`);
    } finally {
        DashboardUI.hideLoading();
    }
}

function handleClear() {
    DashboardUI.clearForm();
}

function handleSample(event) {
    const type = event.currentTarget.dataset.type;
    DashboardUI.loadSample(type);
}

function handleDismissError() {
    $.errorState.classList.add('hidden');
    $.initialState.classList.remove('hidden');
}

function updateCharCount() {
    const length = $.emailBody.value.length;
    $.charCount.textContent = `${length} character${length !== 1 ? 's' : ''}`;
}

// Application Initialization
async function initializeApp() {
    console.log('🚀 Initializing Email Threat Intelligence Platform...');

    // Check backend health
    try {
        const health = await ThreatIntelligenceAPI.checkHealth();
        console.log('✅ Backend health check passed:', health);
        
        const modelsCount = health.models ? Object.values(health.models).filter(Boolean).length : 0;
        DashboardUI.updateBackendStatus(true, modelsCount);
        $.modelInfo.textContent = `Models: SPAM + Phishing (${modelsCount} loaded)`;
    } catch (error) {
        console.error('❌ Backend health check failed:', error);
        DashboardUI.updateBackendStatus(false);
        DashboardUI.showError('Cannot connect to backend. Ensure FastAPI server is running on port 8000.');
    }

    // Attach event listeners
    document.getElementById('analysis-form').addEventListener('submit', handleAnalysis);
    $.clearBtn.addEventListener('click', handleClear);
    $.dismissError.addEventListener('click', handleDismissError);
    $.emailBody.addEventListener('input', updateCharCount);
    
    document.querySelectorAll('.sample-btn').forEach(btn => {
        btn.addEventListener('click', handleSample);
    });

    console.log('✅ Application initialized successfully');
}

// Start application
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}
