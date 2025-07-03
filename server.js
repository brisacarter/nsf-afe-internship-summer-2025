
const express = require('express');
const path = require('path');
const { spawn } = require('child_process');
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

// API endpoint to run Python analysis
app.post('/api/run-analysis', (req, res) => {
    const { analysisType } = req.body;
    
    let scriptToRun = 'main.py';
    if (analysisType === 'analytical') {
        scriptToRun = 'main_sales.py';
    }
    
    const python = spawn('python3', [scriptToRun]);
    
    let output = '';
    let error = '';
    
    python.stdout.on('data', (data) => {
        output += data.toString();
    });
    
    python.stderr.on('data', (data) => {
        error += data.toString();
    });
    
    python.on('close', (code) => {
        if (code === 0) {
            res.json({ 
                success: true, 
                output: output,
                hasImage: fs.existsSync('sales_prediction.png')
            });
        } else {
            res.json({ 
                success: false, 
                error: error || 'Analysis failed'
            });
        }
    });
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
