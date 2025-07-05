const express = require('express');
const path = require('path');
const { spawn, exec } = require('child_process');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 5000;

// Define base paths for the new structure
const publicPath = path.join(__dirname, '../../../public');
const pythonPath = path.join(__dirname, '../../python');
const analysisImagesPath = path.join(__dirname, '../../../public/analysis');

// Middleware
app.use(express.static(publicPath));
app.use(express.json({ limit: '10mb' }));
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
    if (req.method === 'OPTIONS') {
        res.sendStatus(200);
    } else {
        next();
    }
});

// Routes - serve from public folder
app.get('/', (req, res) => {
    res.sendFile(path.join(publicPath, 'index.html'));
});

app.get('/analytical', (req, res) => {
    res.sendFile(path.join(publicPath, 'analytical.html'));
});

app.get('/inferential', (req, res) => {
    res.sendFile(path.join(publicPath, 'inferential.html'));
});

app.get('/about', (req, res) => {
    res.sendFile(path.join(publicPath, 'about.html'));
});

// API endpoint to run analysis
app.post('/api/run-analysis', async (req, res) => {
    try {
        const { analysisType } = req.body;
        let pythonScript;
        let imageName;

        if (analysisType === 'analytical') {
            pythonScript = path.join(pythonPath, 'main_sales.py');
            imageName = 'sales_analysis.png';
        } else if (analysisType === 'inferential') {
            pythonScript = path.join(pythonPath, 'main.py');
            imageName = 'sales_prediction.png';
        } else {
            return res.json({ success: false, error: 'Invalid analysis type' });
        }

        // Execute Python script from the python directory
        const result = await new Promise((resolve, reject) => {
            exec(`python "${pythonScript}"`, { cwd: pythonPath }, (error, stdout, stderr) => {
                if (error) {
                    console.error('Python execution error:', error);
                    resolve({ success: false, error: error.message, output: stderr });
                } else {
                    resolve({ success: true, output: stdout });
                }
            });
        });

        if (result.success) {
            // Check if image was created in the analysis folder
            const imagePath = path.join(analysisImagesPath, imageName);
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
        if (!req.body) {
            return res.status(400).json({ success: false, error: 'Request body is required' });
        }

        const { analysisType, yearRange } = req.body;

        if (!analysisType) {
            return res.status(400).json({ success: false, error: 'Analysis type is required' });
        }

        console.log(`Running specific analysis: ${analysisType} with year range: ${yearRange}`);

        const pythonScript = path.join(pythonPath, 'main_analytics.py');
        const pythonProcess = spawn('python', [pythonScript, analysisType, yearRange || '5'], { cwd: pythonPath });

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

                // Check if image was created in the analysis folder
                const imagePath = path.join(analysisImagesPath, imageName);
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
        if (!req.body) {
            return res.status(400).json({ success: false, error: 'Request body is required' });
        }

        const { yearRange } = req.body;
        console.log(`Running inferential analysis with year range: ${yearRange}`);

        const pythonScript = path.join(pythonPath, 'main.py');
        const pythonProcess = spawn('python', [pythonScript, yearRange || '5'], { cwd: pythonPath });

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
                // Check if image was created in the analysis folder
                const imagePath = path.join(analysisImagesPath, 'sales_prediction.png');
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

// Serve generated images from the analysis folder
app.get('/api/image/:filename', (req, res) => {
    const filename = req.params.filename;
    const imagePath = path.join(analysisImagesPath, filename);

    if (fs.existsSync(imagePath)) {
        res.sendFile(imagePath);
    } else {
        res.status(404).send('Image not found');
    }
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on http://0.0.0.0:${PORT}`);
    console.log(`Server accessible at: http://localhost:${PORT}`);
    console.log(`Public path: ${publicPath}`);
    console.log(`Python path: ${pythonPath}`);
    console.log(`Analysis images path: ${analysisImagesPath}`);
    
    // Log if files exist
    console.log(`Index.html exists: ${require('fs').existsSync(path.join(publicPath, 'index.html'))}`);
});