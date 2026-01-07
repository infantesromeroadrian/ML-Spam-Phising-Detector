/**
 * Chart creation utilities for Email Classifier
 */

// Global chart instances
window.chartInstances = {
    spam: null,
    phishing: null
};

/**
 * Create a gauge chart (simplified version)
 */
function createSimpleGaugeChart(canvasId, probability, color) {
    // Validate Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded');
        return null;
    }

    const canvas = document.getElementById(canvasId);
    if (!canvas) {
        console.error(`Canvas ${canvasId} not found`);
        return null;
    }

    // Force canvas dimensions (fix for invisible charts)
    canvas.width = 300;
    canvas.height = 200;
    canvas.style.width = '300px';
    canvas.style.height = '200px';

    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart
    const chartType = canvasId === 'spamChart' ? 'spam' : 'phishing';
    if (window.chartInstances[chartType]) {
        window.chartInstances[chartType].destroy();
    }

    // Create chart
    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [probability, 100 - probability],
                backgroundColor: [color, '#e5e7eb'],
                borderWidth: 0,
                circumference: 180,
                rotation: 270
            }]
        },
        options: {
            responsive: false,  // Disable responsive to use fixed dimensions
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            },
            cutout: '70%',
            animation: {
                animateRotate: true,
                duration: 1000
            }
        },
        plugins: [{
            id: 'centerText',
            afterDraw: function(chart) {
                const ctx = chart.ctx;
                const centerX = (chart.chartArea.left + chart.chartArea.right) / 2;
                const centerY = (chart.chartArea.top + chart.chartArea.bottom) / 2 + 20;

                ctx.save();
                ctx.font = 'bold 2rem sans-serif';
                ctx.fillStyle = color;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(`${probability.toFixed(1)}%`, centerX, centerY);
                ctx.restore();
            }
        }]
    });

    // Store instance
    window.chartInstances[chartType] = chart;
    
    console.log(`✅ Chart created: ${canvasId} = ${probability.toFixed(1)}%`);
    return chart;
}

/**
 * Update both charts with new data
 */
function updateCharts(spamProb, phishingProb) {
    // Colors based on probability
    const spamColor = spamProb > 50 ? '#f59e0b' : '#10b981';
    const phishingColor = phishingProb > 50 ? '#ef4444' : '#10b981';

    // Create charts
    createSimpleGaugeChart('spamChart', spamProb, spamColor);
    createSimpleGaugeChart('phishingChart', phishingProb, phishingColor);
}

/**
 * Destroy all charts
 */
function destroyCharts() {
    if (window.chartInstances.spam) {
        window.chartInstances.spam.destroy();
        window.chartInstances.spam = null;
    }
    if (window.chartInstances.phishing) {
        window.chartInstances.phishing.destroy();
        window.chartInstances.phishing = null;
    }
    console.log('🗑️ Charts destroyed');
}
