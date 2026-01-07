/**
 * SOC Dashboard - Email Threat Analyzer
 * Frontend logic for Security Operations Center interface
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const form = document.getElementById('classifyForm');
const emailTextArea = document.getElementById('emailText');
const subjectInput = document.getElementById('subject');
const senderInput = document.getElementById('sender');
const charCountSpan = document.getElementById('charCount');

const inputSection = document.getElementById('inputSection');
const resultsSection = document.getElementById('resultsSection');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

const scanAnotherBtn = document.getElementById('scanAnotherBtn');
const dismissErrorBtn = document.getElementById('dismissErrorBtn');

// Result elements
const threatBanner = document.getElementById('threatBanner');
const threatIcon = document.getElementById('threatIcon');
const riskLevelText = document.getElementById('riskLevelText');
const verdictText = document.getElementById('verdictText');
const confidenceValue = document.getElementById('confidenceValue');
const riskScoreText = document.getElementById('riskScoreText');
const riskMeterFill = document.getElementById('riskMeterFill');

const spamCard = document.getElementById('spamCard');
const spamPercentage = document.getElementById('spamPercentage');
const spamSeverity = document.getElementById('spamSeverity');
const spamModel = document.getElementById('spamModel');

const phishingCard = document.getElementById('phishingCard');
const phishingPercentage = document.getElementById('phishingPercentage');
const phishingSeverity = document.getElementById('phishingSeverity');
const phishingModel = document.getElementById('phishingModel');

const iocList = document.getElementById('iocList');
const threatVectorsList = document.getElementById('threatVectorsList');
const recommendationsList = document.getElementById('recommendationsList');
const spamTriggerWords = document.getElementById('spamTriggerWords');
const phishingTriggerWords = document.getElementById('phishingTriggerWords');
const execTime = document.getElementById('execTime');

// ============================================
// Event Listeners
// ============================================

// Character counter
emailTextArea.addEventListener('input', () => {
    charCountSpan.textContent = emailTextArea.value.length;
});

// Form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    await classifyEmail();
});

// Scan another button
scanAnotherBtn.addEventListener('click', resetForm);

// Dismiss error button
dismissErrorBtn.addEventListener('click', () => {
    errorDiv.style.display = 'none';
    inputSection.style.display = 'block';
});

// ============================================
// API Functions
// ============================================

async function classifyEmail() {
    const emailText = emailTextArea.value.trim();
    
    if (!emailText) {
        showError('Email content is required');
        return;
    }
    
    // Show loading
    inputSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorDiv.style.display = 'none';
    loadingDiv.style.display = 'block';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/classify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email_text: emailText,
                subject: subjectInput.value.trim() || null,
                sender: senderInput.value.trim() || null,
            }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Classification failed');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Classification error:', error);
        showError(error.message || 'Failed to classify email. Please try again.');
    } finally {
        loadingDiv.style.display = 'none';
    }
}

// ============================================
// Display Functions
// ============================================

function displayResults(data) {
    console.log('Classification result:', data);
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.classList.add('fade-in');
    
    // Update threat banner
    updateThreatBanner(data);
    
    // Update detection matrix
    updateDetectionMatrix(data);
    
    // Update IOCs
    updateIOCs(data.threat_report.iocs);
    
    // Update trigger words (ML explanation)
    updateTriggerWords(data.threat_report.spam_trigger_words, data.threat_report.phishing_trigger_words);
    
    // Update threat vectors
    updateThreatVectors(data.threat_report.threat_vectors);
    
    // Update recommendations
    updateRecommendations(data.threat_report.recommendations);
    
    // Update execution time
    execTime.textContent = data.execution_time_ms.toFixed(2);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function updateThreatBanner(data) {
    const riskLevel = data.risk_level;
    const verdict = data.verdict;
    const riskScore = data.threat_report.risk_score;
    
    // Determine highest probability for confidence
    const maxProb = Math.max(data.spam_probability, data.phishing_probability);
    const confidence = (maxProb * 100).toFixed(1);
    
    // Update threat level styling
    threatBanner.className = 'threat-banner';
    threatBanner.classList.add(riskLevel.toLowerCase());
    
    // Update icon based on risk
    const icons = {
        'CRITICAL': '🚨',
        'HIGH': '⚠️',
        'MEDIUM': '🟡',
        'LOW': '✅'
    };
    threatIcon.textContent = icons[riskLevel] || '⚠️';
    
    // Update text
    riskLevelText.textContent = riskLevel;
    riskLevelText.style.color = getRiskColor(riskLevel);
    
    verdictText.textContent = `${verdict} DETECTED`;
    confidenceValue.textContent = `${confidence}%`;
    confidenceValue.style.color = getRiskColor(riskLevel);
    
    // Update risk score
    riskScoreText.textContent = `${riskScore}/100`;
    riskMeterFill.style.width = `${riskScore}%`;
    
    // Animate the meter fill
    setTimeout(() => {
        riskMeterFill.style.transition = 'width 1.5s ease-out';
    }, 100);
}

function updateDetectionMatrix(data) {
    // SPAM card
    const spamProb = (data.spam_probability * 100).toFixed(1);
    const spamRisk = getCardRisk(data.spam_probability);
    
    spamCard.className = 'detection-card';
    spamCard.classList.add(spamRisk.toLowerCase());
    spamPercentage.textContent = `${spamProb}%`;
    spamPercentage.style.color = getRiskColor(spamRisk);
    spamSeverity.textContent = data.spam_label;
    spamSeverity.className = 'detection-label';
    spamSeverity.classList.add(spamRisk.toLowerCase());
    spamModel.textContent = `Model: v${data.spam_model_version}`;
    
    // PHISHING card
    const phishProb = (data.phishing_probability * 100).toFixed(1);
    const phishRisk = getCardRisk(data.phishing_probability);
    
    phishingCard.className = 'detection-card';
    phishingCard.classList.add(phishRisk.toLowerCase());
    phishingPercentage.textContent = `${phishProb}%`;
    phishingPercentage.style.color = getRiskColor(phishRisk);
    phishingSeverity.textContent = data.phishing_label;
    phishingSeverity.className = 'detection-label';
    phishingSeverity.classList.add(phishRisk.toLowerCase());
    phishingModel.textContent = `Model: v${data.phishing_model_version}`;
}

function updateIOCs(iocs) {
    if (!iocs || iocs.length === 0) {
        iocList.innerHTML = '<p style="text-align: center; color: var(--text-muted); padding: var(--spacing-lg);">No IOCs detected - Email appears clean</p>';
        return;
    }
    
    const iocIcons = {
        'url': '🔗',
        'keyword_urgency': '⏰',
        'keyword_financial': '💳',
        'pattern': '🔍',
        'sender': '📧'
    };
    
    const html = iocs.map(ioc => `
        <div class="ioc-item ${ioc.severity}">
            <div class="ioc-icon">${getSeverityIcon(ioc.severity)}</div>
            <div class="ioc-content">
                <div class="ioc-description">${ioc.description}</div>
                <div class="ioc-value">${ioc.value}</div>
                ${ioc.count > 1 ? `<div class="ioc-count">Detected ${ioc.count} time(s)</div>` : ''}
            </div>
        </div>
    `).join('');
    
    iocList.innerHTML = html;
}

function updateTriggerWords(spamWords, phishingWords) {
    // Update SPAM trigger words
    if (!spamWords || spamWords.length === 0) {
        spamTriggerWords.innerHTML = '<span style="color: var(--text-muted); font-size: 0.875rem;">No suspicious words detected</span>';
    } else {
        const spamHtml = spamWords
            .filter(tw => tw.contribution > 0)  // Only suspicious words (positive contribution)
            .slice(0, 10)  // Top 10
            .map(tw => `
                <span style="
                    display: inline-block;
                    padding: var(--spacing-xs) var(--spacing-sm);
                    background: rgba(255, 99, 72, 0.2);
                    border: 1px solid var(--high);
                    border-radius: var(--radius-sm);
                    font-family: var(--font-mono);
                    font-size: 0.75rem;
                    color: var(--high);
                    font-weight: 600;
                ">
                    ${tw.word} <span style="color: var(--text-muted);">(+${tw.contribution.toFixed(3)})</span>
                </span>
            `).join('');
        
        spamTriggerWords.innerHTML = spamHtml || '<span style="color: var(--text-muted); font-size: 0.875rem;">No suspicious words detected</span>';
    }
    
    // Update PHISHING trigger words
    if (!phishingWords || phishingWords.length === 0) {
        phishingTriggerWords.innerHTML = '<span style="color: var(--text-muted); font-size: 0.875rem;">No suspicious words detected</span>';
    } else {
        const phishingHtml = phishingWords
            .filter(tw => tw.contribution > 0)  // Only suspicious words
            .slice(0, 10)  // Top 10
            .map(tw => `
                <span style="
                    display: inline-block;
                    padding: var(--spacing-xs) var(--spacing-sm);
                    background: rgba(255, 71, 87, 0.2);
                    border: 1px solid var(--critical);
                    border-radius: var(--radius-sm);
                    font-family: var(--font-mono);
                    font-size: 0.75rem;
                    color: var(--critical);
                    font-weight: 600;
                ">
                    ${tw.word} <span style="color: var(--text-muted);">(+${tw.contribution.toFixed(3)})</span>
                </span>
            `).join('');
        
        phishingTriggerWords.innerHTML = phishingHtml || '<span style="color: var(--text-muted); font-size: 0.875rem;">No suspicious words detected</span>';
    }
}

function updateThreatVectors(vectors) {
    if (!vectors || vectors.length === 0) {
        threatVectorsList.innerHTML = '<p style="text-align: center; color: var(--text-muted); padding: var(--spacing-lg);">No threat vectors identified</p>';
        return;
    }
    
    const html = vectors.map(vector => `
        <div class="threat-vector-item">
            <div class="threat-vector-content">
                <div class="threat-vector-name">${vector.name}</div>
                <div class="threat-vector-description">${vector.description}</div>
            </div>
            <div class="threat-vector-confidence">${(vector.confidence * 100).toFixed(1)}%</div>
        </div>
    `).join('');
    
    threatVectorsList.innerHTML = html;
}

function updateRecommendations(recommendations) {
    if (!recommendations || recommendations.length === 0) {
        recommendationsList.innerHTML = '<p style="text-align: center; color: var(--text-muted); padding: var(--spacing-lg);">No specific recommendations</p>';
        return;
    }
    
    const html = recommendations.map(rec => `
        <div class="recommendation-item">
            <div class="recommendation-text">${rec}</div>
        </div>
    `).join('');
    
    recommendationsList.innerHTML = html;
}

// ============================================
// Utility Functions
// ============================================

function getRiskColor(risk) {
    const colors = {
        'CRITICAL': 'var(--critical)',
        'HIGH': 'var(--high)',
        'MEDIUM': 'var(--medium)',
        'LOW': 'var(--low)'
    };
    return colors[risk] || 'var(--text-primary)';
}

function getCardRisk(probability) {
    if (probability >= 0.7) return 'CRITICAL';
    if (probability >= 0.5) return 'HIGH';
    if (probability >= 0.3) return 'MEDIUM';
    return 'LOW';
}

function getSeverityIcon(severity) {
    const icons = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢'
    };
    return icons[severity] || '⚪';
}

function showError(message) {
    errorText.textContent = message;
    errorDiv.style.display = 'block';
    inputSection.style.display = 'none';
    resultsSection.style.display = 'none';
}

function resetForm() {
    form.reset();
    charCountSpan.textContent = '0';
    inputSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorDiv.style.display = 'none';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================
// Health Check on Load
// ============================================

async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ API is healthy');
        } else {
            console.warn('⚠️ API health check failed');
        }
    } catch (error) {
        console.error('❌ API is not reachable:', error);
    }
}

// Initialize
console.log('🛡️  SOC Dashboard Ready');
console.log('API URL:', API_BASE_URL);
checkAPIHealth();
