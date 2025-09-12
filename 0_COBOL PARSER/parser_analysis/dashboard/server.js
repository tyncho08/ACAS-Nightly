const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files
app.use('/static', express.static(path.join(__dirname, 'static')));
app.use('/data', express.static(path.join(__dirname, 'data')));

// Serve main dashboard
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// API endpoint for metrics data
app.get('/api/metrics', (req, res) => {
    res.sendFile(path.join(__dirname, 'data', 'metrics.json'));
});

// Start server
app.listen(PORT, () => {
    console.log(`Dashboard server running at http://localhost:${PORT}`);
    console.log('Press Ctrl+C to stop');
});