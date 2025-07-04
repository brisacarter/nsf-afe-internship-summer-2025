
const express = require('express');
const path = require('path');
const { spawn, exec } = require('child_process');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(express.static(path.join(__dirname, 'public')));
app.use('/css', express.static(path.join(__dirname, 'static/css')));
app.use('/js', express.static(path.join(__dirname, 'static/js')));
app.use('/images', express.static(path.join(__dirname, 'static/images')));
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
            pythonScript = 'src/python/main_sales.py';
            imageName = 'sales_analysis.png';
        } else if (analysisType === 'inferential') {
            pythonScript = 'src/python/main.py';
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
            const imagePath = path.join(__dirname, 'src/assets', imageName);
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
        const { analysisType, yearRange } = req.body;

        console.log(`Running specific analysis: ${analysisType} with year range: ${yearRange}`);

        const { spawn } = require('child_process');
        const pythonProcess = spawn('python3', ['src/python/main_analytics.py', analysisType, yearRange || '25']);

        let output = '';
        let errorOutput = '';

        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                // Determine the image name based on analysis type
                let imageName = 'all_analysis_summary.png';
                if (analysisType === 'genre') imageName = 'genre_analysis.png';
                else if (analysisType === 'platform') imageName = 'platform_analysis.png';
                else if (analysisType === 'publisher') imageName = 'publisher_analysis.png';

                // Check if image was created
                const imagePath = path.join(__dirname, 'src/assets', imageName);
                const hasImage = fs.existsSync(imagePath);
                
                res.json({
                    success: true,
                    output: output,
                    hasImage: hasImage,
                    imageName: imageName
                });
            } else {
                res.json({
                    success: false,
                    error: errorOutput || 'Analysis failed'
                });
            }
        });
    } catch (error) {
        console.error('Error running specific analysis:', error);
        res.json({
            success: false,
            error: error.message
        });
    }
});

// API endpoint for running inferential analysis
app.post('/api/run-inferential', async (req, res) => {
    try {
        const { yearRange } = req.body;
        console.log(`Running inferential analysis with year range: ${yearRange}`);

        const { spawn } = require('child_process');
        const pythonProcess = spawn('python3', ['src/python/main.py', yearRange || '25']);

        let output = '';
        let errorOutput = '';

        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                // Check if image was created
                const imagePath = path.join(__dirname, 'src/assets/sales_prediction.png');
                const hasImage = fs.existsSync(imagePath);
                
                res.json({
                    success: true,
                    output: output,
                    hasImage: hasImage,
                    imageName: 'sales_prediction.png'
                });
            } else {
                res.json({
                    success: false,
                    error: errorOutput || 'Prediction analysis failed'
                });
            }
        });
    } catch (error) {
        console.error('Error running inferential analysis:', error);
        res.json({
            success: false,
            error: error.message
        });
    }
});

// Serve generated images
app.get('/api/image/:filename', (req, res) => {
    const filename = req.params.filename;
    const imagePath = path.join(__dirname, 'src/assets', filename);

    if (fs.existsSync(imagePath)) {
        res.sendFile(imagePath);
    } else {
        res.status(404).send('Image not found');
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on http://0.0.0.0:${PORT}`);
});
