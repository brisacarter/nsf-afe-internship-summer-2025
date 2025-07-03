
// Navigation functions
function navigateToAnalytical() {
    window.location.href = '/analytical';
}

function navigateToInferential() {
    window.location.href = '/inferential';
}

function goHome() {
    window.location.href = '/';
}

// Analysis execution function
async function runAnalysis(analysisType) {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');
    const analysisOutput = document.getElementById('analysisOutput');
    const visualizationContainer = document.getElementById('visualizationContainer');
    const runBtn = analysisType === 'analytical' ? 
        document.getElementById('runAnalysisBtn') : 
        document.getElementById('runPredictionBtn');
    
    // Show loading state
    if (loadingSpinner) {
        loadingSpinner.classList.remove('hidden');
    }
    if (runBtn) {
        runBtn.disabled = true;
        runBtn.textContent = analysisType === 'analytical' ? 
            'Analyzing...' : 'Generating Predictions...';
    }
    if (resultsSection) {
        resultsSection.classList.add('hidden');
    }
    
    try {
        const response = await fetch('/api/run-analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ analysisType })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Display output
            if (analysisOutput) {
                analysisOutput.textContent = result.output;
            }
            
            // Display visualization if available
            if (visualizationContainer && result.hasImage) {
                const img = document.createElement('img');
                img.src = '/api/image/sales_prediction.png?' + new Date().getTime(); // Cache busting
                img.alt = 'Sales Analysis Visualization';
                img.style.maxWidth = '100%';
                img.style.height = 'auto';
                
                visualizationContainer.innerHTML = '';
                visualizationContainer.appendChild(img);
            }
            
            // Show results
            if (resultsSection) {
                resultsSection.classList.remove('hidden');
            }
            
            // Scroll to results
            if (resultsSection) {
                resultsSection.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }
            
        } else {
            if (analysisOutput) {
                analysisOutput.textContent = 'Error: ' + (result.error || 'Analysis failed');
            }
            if (resultsSection) {
                resultsSection.classList.remove('hidden');
            }
        }
        
    } catch (error) {
        console.error('Error running analysis:', error);
        if (analysisOutput) {
            analysisOutput.textContent = 'Error: Failed to connect to server';
        }
        if (resultsSection) {
            resultsSection.classList.remove('hidden');
        }
    } finally {
        // Hide loading state
        if (loadingSpinner) {
            loadingSpinner.classList.add('hidden');
        }
        if (runBtn) {
            runBtn.disabled = false;
            runBtn.textContent = analysisType === 'analytical' ? 
                'Generate Sales Analysis' : 'Generate Predictions';
        }
    }
}

// Add smooth scrolling for better UX
document.addEventListener('DOMContentLoaded', function() {
    // Add entrance animations
    const cards = document.querySelectorAll('.option-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.2}s`;
        card.style.animation = 'fadeInUp 0.6s ease forwards';
    });
    
    // Add hover effects for better interactivity
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .option-card {
        opacity: 0;
    }
`;
document.head.appendChild(style);

// Error handling for images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            this.style.display = 'none';
            const errorMsg = document.createElement('p');
            errorMsg.textContent = 'Visualization not available';
            errorMsg.style.textAlign = 'center';
            errorMsg.style.color = '#666';
            errorMsg.style.fontStyle = 'italic';
            this.parentNode.appendChild(errorMsg);
        });
    });
});
