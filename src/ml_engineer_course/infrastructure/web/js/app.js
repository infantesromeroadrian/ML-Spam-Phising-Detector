/**
 * Email Classifier Frontend
 * Connects to FastAPI backend for email classification
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const form = document.getElementById('classifyForm');
const emailTextArea = document.getElementById('emailText');
const subjectInput = document.getElementById('subject');
const senderInput = document.getElementById('sender');
const submitBtn = document.getElementById('submitBtn');
const charCountSpan = document.getElementById('charCount');

const resultsCard = document.getElementById('resultsCard');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

const analyzeAnotherBtn = document.getElementById('analyzeAnotherBtn');
const dismissErrorBtn = document.getElementById('dismissErrorBtn');

// Result elements
const verdictBadge = document.getElementById('verdictBadge');
const verdictIcon = document.getElementById('verdictIcon');
const verdictText = document.getElementById('verdictText');
const riskBadge = document.getElementById('riskBadge');
const riskText = document.getElementById('riskText');

const spamFill = document.getElementById('spamFill');
const spamProb = document.getElementById('spamProb');
const spamLabel = document.getElementById('spamLabel');
const spamModel = document.getElementById('spamModel');

const phishingFill = document.getElementById('phishingFill');
const phishingProb = document.getElementById('phishingProb');
const phishingLabel = document.getElementById('phishingLabel');
const phishingModel = document.getElementById('phishingModel');

const execTime = document.getElementById('execTime');

// ============================================
// Chart Functions (now in charts.js)
// ============================================
// Chart creation and management is now handled by charts.js
// Functions available: updateCharts(spamProb, phishingProb), destroyCharts()

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

// Analyze another email
analyzeAnotherBtn.addEventListener('click', () => {
    resetForm();
});

// Dismiss error
dismissErrorBtn.addEventListener('click', () => {
    hideError();
});

// ============================================
// Main Functions
// ============================================

/**
 * Classify email by calling the API
 */
async function classifyEmail() {
    // Get form data
    const emailText = emailTextArea.value.trim();
    const subject = subjectInput.value.trim();
    const sender = senderInput.value.trim();

    // Validation
    if (!emailText) {
        showError('Please enter email content');
        return;
    }

    // Prepare request payload
    const payload = {
        email_text: emailText,
    };

    if (subject) payload.subject = subject;
    if (sender) payload.sender = sender;

    // Show loading, hide form and results
    showLoading();

    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/api/v1/classify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        // Check response
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Classification failed');
        }

        // Parse result
        const result = await response.json();

        // Display results
        displayResults(result);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to connect to API. Make sure the backend is running.');
    } finally {
        hideLoading();
    }
}

/**
 * Display classification results
 */
function displayResults(data) {
    // Verdict
    const verdict = data.verdict;
    const riskLevel = data.risk_level;

    // Set verdict badge
    verdictText.textContent = verdict;
    verdictBadge.className = 'verdict-badge';
    
    if (verdict === 'HAM') {
        verdictBadge.classList.add('ham');
        verdictIcon.textContent = '✅';
    } else if (verdict === 'SPAM') {
        verdictBadge.classList.add('spam');
        verdictIcon.textContent = '🗑️';
    } else if (verdict === 'PHISHING') {
        verdictBadge.classList.add('phishing');
        verdictIcon.textContent = '🎣';
    } else if (verdict === 'SPAM+PHISHING') {
        verdictBadge.classList.add('critical');
        verdictIcon.textContent = '🚨';
    }

    // Set risk badge
    riskText.textContent = riskLevel;
    riskBadge.className = 'risk-badge';
    riskBadge.classList.add(riskLevel.toLowerCase());

    // Calculate probabilities
    const spamProbability = data.spam_probability * 100;
    const phishingProbability = data.phishing_probability * 100;

    // Update charts using the new simplified function from charts.js
    updateCharts(spamProbability, phishingProbability);
    
    // Update labels
    spamLabel.textContent = data.spam_label;
    spamModel.textContent = data.spam_model_version;
    phishingLabel.textContent = data.phishing_label;
    phishingModel.textContent = data.phishing_model_version;
    
    // Update old progress bars (hidden but keep for fallback)
    spamFill.style.width = spamProbability + '%';
    spamProb.textContent = spamProbability.toFixed(1) + '%';
    phishingFill.style.width = phishingProbability + '%';
    phishingProb.textContent = phishingProbability.toFixed(1) + '%';

    // Execution time
    execTime.textContent = data.execution_time_ms.toFixed(2);

    // Show results
    resultsCard.style.display = 'block';
    
    // Scroll to results
    setTimeout(() => {
        resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

/**
 * Reset form to initial state
 */
function resetForm() {
    form.reset();
    charCountSpan.textContent = '0';
    resultsCard.style.display = 'none';
    
    // Destroy charts using the new function from charts.js
    destroyCharts();
    
    // Reset progress bars (fallback)
    spamFill.style.width = '0%';
    phishingFill.style.width = '0%';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================
// UI Helper Functions
// ============================================

/**
 * Show loading spinner
 */
function showLoading() {
    loadingDiv.style.display = 'block';
    submitBtn.disabled = true;
    resultsCard.style.display = 'none';
    errorDiv.style.display = 'none';
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    loadingDiv.style.display = 'none';
    submitBtn.disabled = false;
}

/**
 * Show error message
 */
function showError(message) {
    errorText.textContent = message;
    errorDiv.style.display = 'block';
    loadingDiv.style.display = 'none';
    resultsCard.style.display = 'none';
    
    // Scroll to error
    setTimeout(() => {
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
}

/**
 * Hide error message
 */
function hideError() {
    errorDiv.style.display = 'none';
}

// ============================================
// Example Email Templates (Optional)
// ============================================

/**
 * Load example spam email
 */
function loadSpamExample() {
    emailTextArea.value = "WINNER! Congratulations! You have won $1,000,000 in our lottery! Click here NOW to claim your prize! This is a limited time offer. ACT FAST!";
    subjectInput.value = "🎉 YOU WON! Claim Your Prize NOW!";
    senderInput.value = "lottery@winner-claim.com";
    charCountSpan.textContent = emailTextArea.value.length;
}

/**
 * Load example phishing email
 */
function loadPhishingExample() {
    emailTextArea.value = "URGENT: Your account has been suspended due to suspicious activity. Click here immediately to verify your identity and restore access. Failure to do so within 24 hours will result in permanent account closure.";
    subjectInput.value = "Account Security Alert - Action Required";
    senderInput.value = "security@paypa1-verify.com";
    charCountSpan.textContent = emailTextArea.value.length;
}

/**
 * Load example legitimate email
 */
function loadHamExample() {
    emailTextArea.value = "Hi there, just wanted to follow up on our meeting last week. Can we schedule a time next Tuesday to discuss the project timeline? Let me know what works best for you.";
    subjectInput.value = "Follow-up: Project Meeting";
    senderInput.value = "colleague@company.com";
    charCountSpan.textContent = emailTextArea.value.length;
}

// ============================================
// Initialization
// ============================================

/**
 * Check if API is available
 */
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ API is healthy');
        } else {
            console.warn('⚠️ API health check failed');
        }
    } catch (error) {
        console.error('❌ Cannot connect to API:', error.message);
        console.log('Make sure the backend is running: email-classifier-api');
    }
}

// Check API on page load
checkAPIHealth();

// Log ready message
console.log('📧 Email Classifier Frontend Ready');
console.log('API URL:', API_BASE_URL);
