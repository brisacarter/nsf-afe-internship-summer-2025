const express = require('express');
const path = require('path');
const { spawn, exec } = require('child_process');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/analytical', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'analytical.html'));
});

app.get('/inferential', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'inferential.html'));
});

// API endpoint to run analysis
app.post('/api/run-analysis', async (req, res) => {
    try {
        const { analysisType } = req.body;
        let pythonScript;
        let imageName;

        if (analysisType === 'analytical') {
            pythonScript = 'main_sales.py';
            imageName = 'sales_analysis.png';
        } else if (analysisType === 'inferential') {
            pythonScript = 'main.py';
            imageName = 'sales_prediction.png';
        } else {
            return res.json({ success: false, error: 'Invalid analysis type' });
        }

        // Execute Python script
        const result = await new Promise((resolve, reject) => {
            exec(`python ${pythonScript}`, (error, stdout, stderr) => {
                if (error) {
                    console.error('Python execution error:', error);
                    resolve({ success: false, error: error.message, output: stderr });
                } else {
                    resolve({ success: true, output: stdout });
                }
            });
        });

        if (result.success) {
            // Check if image was created
            const imagePath = path.join(__dirname, imageName);
            const hasImage = fs.existsSync(imagePath);

            res.json({
                success: true,
                output: result.output,
                hasImage: hasImage,
                imageName: imageName
            });
        } else {
            res.json(result);
        }
    } catch (error) {
        console.error('Server error:', error);
        res.json({ success: false, error: 'Server error occurred' });
    }
});

// API endpoint for specific analysis types
app.post('/api/run-specific-analysis', async (req, res) => {
    try {
        const { analysisType } = req.body;

        const analysisMap = {
            'genre': { script: 'main_analytics.py', arg: 'genre', image: 'genre_analysis.png' },
            'regional': { script: 'main_analytics.py', arg: 'regional', image: 'regional_analysis.png' },
            'platform': { script: 'main_analytics.py', arg: 'platform', image: 'platform_analysis.png' },
            'publisher': { script: 'main_analytics.py', arg: 'publisher', image: 'publisher_analysis.png' },
            'historical': { script: 'main_analytics.py', arg: 'historical', image: 'historical_analysis.png' },
            'all': { script: 'main_analytics.py', arg: 'all', image: 'all_analysis_summary.png' }
        };

        const analysis = analysisMap[analysisType];
        if (!analysis) {
            return res.json({ success: false, error: 'Invalid analysis type' });
        }

        // Execute Python script with argument
        const command = `python ${analysis.script} ${analysis.arg}`;
        const result = await new Promise((resolve, reject) => {
            exec(command, (error, stdout, stderr) => {
                if (error) {
                    console.error('Python execution error:', error);
                    resolve({ success: false, error: error.message, output: stderr });
                } else {
                    resolve({ success: true, output: stdout });
                }
            });
        });

        if (result.success) {
            // Check if image was created
            const imagePath = path.join(__dirname, analysis.image);
            const hasImage = fs.existsSync(imagePath);

            res.json({
                success: true,
                output: result.output,
                hasImage: hasImage,
                imageName: analysis.image
            });
        } else {
            res.json(result);
        }
    } catch (error) {
        console.error('Server error:', error);
        res.json({ success: false, error: 'Server error occurred' });
    }
});

// Serve generated images
app.get('/api/image/:filename', (req, res) => {
    const filename = req.params.filename;
    const imagePath = path.join(__dirname, filename);

    if (fs.existsSync(imagePath)) {
        res.sendFile(imagePath);
    } else {
        res.status(404).send('Image not found');
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on http://0.0.0.0:${PORT}`);
});