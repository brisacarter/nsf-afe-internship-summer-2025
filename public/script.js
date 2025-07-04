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

function goToAbout() {
    window.location.href = '/about.html';
}

function goHome() {
    window.location.href = '/';
}

// Specific analysis execution function
async function runSpecificAnalysis(specificType) {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');
    const analysisOutput = document.getElementById('analysisOutput');
    const visualizationContainer = document.getElementById('visualizationContainer');

    // Get the clicked button
    const buttonMap = {
        'genre': 'salesByGenreBtn',
        'platform': 'platformPerformanceBtn',
        'publisher': 'publisherRankingsBtn',
        'all': 'runAllAnalysisBtn'
    };

    const runBtn = document.getElementById(buttonMap[specificType]);

    // Update active button state
    setActiveButton(runBtn);

    // Show loading state
    if (loadingSpinner) {
        loadingSpinner.classList.remove('hidden');
    }
    if (runBtn) {
        runBtn.disabled = true;
        runBtn.textContent = 'Analyzing...';
    }
    if (resultsSection) {
        resultsSection.classList.add('hidden');
    }

    try {
        // Get selected year range if available
        const selectedYearRange = document.querySelector('input[name="yearRange"]:checked');
        const yearRange = selectedYearRange ? selectedYearRange.value : '5';

        const response = await fetch('/api/run-specific-analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ analysisType: specificType, yearRange: yearRange })
        });

        const result = await response.json();

        if (result.success) {
            // Display output
            if (analysisOutput) {
                analysisOutput.textContent = result.output;
            }

            // Display visualization if available
            if (visualizationContainer && result.hasImage) {
                // For 'all' analysis, show HTML summary instead of image
                if (specificType === 'all') {
                    const summaryContainer = document.getElementById('analysisSummaryContainer');
                    if (summaryContainer) {
                        visualizationContainer.innerHTML = '';
                        summaryContainer.classList.remove('hidden');
                    }
                } else {
                    const img = document.createElement('img');
                    const imageName = result.imageName || 'sales_analysis.png';
                    img.src = `/api/image/${imageName}?` + new Date().getTime(); // Cache busting
                    img.alt = 'Sales Analysis Visualization';
                    img.style.maxWidth = '100%';
                    img.style.height = 'auto';

                    visualizationContainer.innerHTML = '';
                    visualizationContainer.appendChild(img);

                    // Hide summary container for other analysis types
                    const summaryContainer = document.getElementById('analysisSummaryContainer');
                    if (summaryContainer) {
                        summaryContainer.classList.add('hidden');
                    }
                }
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
            const originalTexts = {
                'genre': 'Sales by Genre',
                'platform': 'Platform Performance',
                'publisher': 'Publisher Rankings',
                'all': 'Generate All Analysis'
            };
            runBtn.textContent = originalTexts[specificType];
        }
    }
}

// Analysis execution function
async function runAnalysis(analysisType) {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');
    const analysisOutput = document.getElementById('analysisOutput');
    const visualizationContainer = document.getElementById('visualizationContainer');
    const runBtn = document.getElementById(analysisType === 'analytical' ? 'runAnalyticalBtn' : 'runInferentialBtn');

    // Get selected year range if available
    const selectedYearRange = document.querySelector('input[name="yearRange"]:checked');
    const yearRange = selectedYearRange ? selectedYearRange.value : '5';

    // Show loading state
    if (loadingSpinner) {
        loadingSpinner.classList.remove('hidden');
    }
    if (runBtn) {
        runBtn.disabled = true;
        runBtn.textContent = 'Analyzing...';
    }
    if (resultsSection) {
        resultsSection.classList.add('hidden');
    }

    try {
        const response = await fetch(`/api/run-${analysisType}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ yearRange: yearRange })
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
                const imageName = result.imageName || 'sales_prediction.png';
                img.src = `/api/image/${imageName}?` + new Date().getTime(); // Cache busting
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

// Function to set active button
function setActiveButton(activeBtn) {
    // Remove active class from all analysis buttons
    const allAnalysisButtons = document.querySelectorAll('.btn-analytical');
    allAnalysisButtons.forEach(btn => {
        btn.classList.remove('btn-active');
    });

    // Add active class to clicked button
    if (activeBtn) {
        activeBtn.classList.add('btn-active');
    }
}

// Add smooth scrolling for better UX
document.addEventListener('DOMContentLoaded', function() {
    // Set default active button to Sales by Genre
    const defaultActiveBtn = document.getElementById('salesByGenreBtn');
    if (defaultActiveBtn) {
        setActiveButton(defaultActiveBtn);
    }

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
            if (!this.classList.contains('btn-active')) {
                this.style.transform = 'translateY(-2px) scale(1.05)';
            }
        });

        button.addEventListener('mouseleave', function() {
            if (!this.classList.contains('btn-active')) {
                this.style.transform = 'translateY(0) scale(1)';
            }
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

// Navigation functions
function navigateToAbout() {
    window.location.href = 'about.html';
}

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