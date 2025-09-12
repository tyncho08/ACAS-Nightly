const fs = require('fs-extra');
const path = require('path');

// Paths
const DATA_DIR = path.join(__dirname, '../dashboard/data');
const DASHBOARD_DIR = path.join(__dirname, '../dashboard');
const STATIC_DIR = path.join(DASHBOARD_DIR, 'static');

// Ensure directories exist
fs.ensureDirSync(DASHBOARD_DIR);
fs.ensureDirSync(STATIC_DIR);

async function buildDashboard() {
    console.log('Building COBOL Metrics Dashboard...\n');
    
    // Load metrics data
    const metricsData = await fs.readJson(path.join(DATA_DIR, 'metrics.json'));
    
    // Generate dashboard HTML
    const dashboardHTML = generateDashboardHTML(metricsData);
    await fs.writeFile(path.join(DASHBOARD_DIR, 'index.html'), dashboardHTML);
    
    // Generate dashboard JavaScript
    const dashboardJS = generateDashboardJS(metricsData);
    await fs.writeFile(path.join(STATIC_DIR, 'dashboard.js'), dashboardJS);
    
    // Generate dashboard CSS
    const dashboardCSS = generateDashboardCSS();
    await fs.writeFile(path.join(STATIC_DIR, 'dashboard.css'), dashboardCSS);
    
    // Create a simple Express server
    const serverJS = generateServer();
    await fs.writeFile(path.join(DASHBOARD_DIR, 'server.js'), serverJS);
    
    console.log(`✓ Dashboard built: ${DASHBOARD_DIR}/index.html`);
    console.log(`✓ To view the dashboard, run: cd parser_analysis && npm run start-dashboard`);
}

function generateDashboardHTML(metricsData) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACAS COBOL Metrics Dashboard</title>
    <link rel="stylesheet" href="static/dashboard.css">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
</head>
<body>
    <div class="dashboard-container">
        <header>
            <h1>ACAS COBOL Metrics Dashboard</h1>
            <div class="timestamp">Last Updated: ${metricsData.timestamp}</div>
        </header>
        
        <div class="metrics-grid">
            <!-- Overview Cards -->
            <div class="metric-card overview-card">
                <h3>Total Programs</h3>
                <div class="metric-value">${metricsData.aggregates.overall.totalPrograms}</div>
            </div>
            
            <div class="metric-card overview-card">
                <h3>Total Copybooks</h3>
                <div class="metric-value">${metricsData.aggregates.overall.totalCopybooks}</div>
            </div>
            
            <div class="metric-card overview-card">
                <h3>Lines of Code</h3>
                <div class="metric-value">${metricsData.aggregates.overall.totalLines.toLocaleString()}</div>
            </div>
            
            <div class="metric-card overview-card">
                <h3>Avg Complexity</h3>
                <div class="metric-value">${(metricsData.aggregates.overall.avgComplexity || 0).toFixed(1)}</div>
            </div>
            
            <div class="metric-card overview-card">
                <h3>Avg Maintainability</h3>
                <div class="metric-value">${(metricsData.aggregates.overall.avgMaintainability || 0).toFixed(1)}%</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <!-- Subsystem Distribution -->
            <div class="chart-container">
                <h3>Programs by Subsystem</h3>
                <div id="subsystem-chart"></div>
            </div>
            
            <!-- Complexity Distribution -->
            <div class="chart-container">
                <h3>Complexity Distribution</h3>
                <div id="complexity-chart"></div>
            </div>
            
            <!-- Maintainability Heatmap -->
            <div class="chart-container full-width">
                <h3>Maintainability by Subsystem</h3>
                <div id="maintainability-heatmap"></div>
            </div>
            
            <!-- Top Complex Programs -->
            <div class="chart-container">
                <h3>Most Complex Programs</h3>
                <div id="complex-programs-chart"></div>
            </div>
            
            <!-- File Size Distribution -->
            <div class="chart-container">
                <h3>Program Size Distribution</h3>
                <div id="size-distribution-chart"></div>
            </div>
            
            <!-- Dependencies Network -->
            <div class="chart-container full-width">
                <h3>Dependencies Overview</h3>
                <div id="dependencies-chart"></div>
            </div>
        </div>
        
        <!-- Detailed Tables -->
        <div class="tables-section">
            <h2>Detailed Metrics</h2>
            
            <div class="table-tabs">
                <button class="tab-button active" onclick="showTab('programs')">Programs</button>
                <button class="tab-button" onclick="showTab('complexity')">Complexity Analysis</button>
                <button class="tab-button" onclick="showTab('dependencies')">Dependencies</button>
            </div>
            
            <div id="programs-tab" class="tab-content active">
                <input type="text" id="program-search" placeholder="Search programs..." onkeyup="filterPrograms()">
                <div id="programs-table"></div>
            </div>
            
            <div id="complexity-tab" class="tab-content">
                <div id="complexity-table"></div>
            </div>
            
            <div id="dependencies-tab" class="tab-content">
                <div id="dependencies-table"></div>
            </div>
        </div>
        
        <!-- Quick Links -->
        <div class="quick-links">
            <h3>Quick Links</h3>
            <a href="../docs/index.html">📚 Documentation</a>
            <a href="../visualizations/call-graph.html">🔗 Call Graph</a>
            <a href="../visualizations/flowcharts/index.html">📊 Flowcharts</a>
            <a href="data/metrics-report.md">📈 Metrics Report</a>
        </div>
    </div>
    
    <script>
        const metricsData = ${JSON.stringify(metricsData)};
    </script>
    <script src="static/dashboard.js"></script>
</body>
</html>`;
}

function generateDashboardJS(metricsData) {
    return `// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Subsystem Distribution Pie Chart
    const subsystemData = Object.entries(metricsData.aggregates.bySubsystem).map(([key, value]) => ({
        name: key.toUpperCase(),
        value: value.programs
    }));
    
    Plotly.newPlot('subsystem-chart', [{
        values: subsystemData.map(d => d.value),
        labels: subsystemData.map(d => d.name),
        type: 'pie',
        marker: {
            colors: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#dda15e', '#c9ada7']
        }
    }], {
        height: 300,
        margin: { t: 30, b: 30, l: 30, r: 30 }
    });
    
    // Complexity Distribution Histogram
    const complexityValues = metricsData.metrics
        .filter(m => m.fileType === 'program')
        .map(m => m.complexity.cyclomatic);
    
    Plotly.newPlot('complexity-chart', [{
        x: complexityValues,
        type: 'histogram',
        nbinsx: 20,
        marker: { color: '#3498db' }
    }], {
        height: 300,
        xaxis: { title: 'Cyclomatic Complexity' },
        yaxis: { title: 'Number of Programs' },
        margin: { t: 30, b: 50, l: 50, r: 30 }
    });
    
    // Maintainability Heatmap
    const subsystems = Object.keys(metricsData.aggregates.bySubsystem);
    const maintainabilityData = [];
    
    subsystems.forEach(subsys => {
        const programs = metricsData.metrics.filter(m => 
            m.subsystem === subsys && m.fileType === 'program'
        );
        
        const maintainabilityBins = [0, 20, 40, 60, 80, 100];
        const counts = new Array(maintainabilityBins.length - 1).fill(0);
        
        programs.forEach(p => {
            const maint = p.complexity.maintainability;
            for (let i = 0; i < maintainabilityBins.length - 1; i++) {
                if (maint >= maintainabilityBins[i] && maint < maintainabilityBins[i + 1]) {
                    counts[i]++;
                    break;
                }
            }
        });
        
        maintainabilityData.push(counts);
    });
    
    Plotly.newPlot('maintainability-heatmap', [{
        z: maintainabilityData,
        x: ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'],
        y: subsystems.map(s => s.toUpperCase()),
        type: 'heatmap',
        colorscale: 'RdYlGn'
    }], {
        height: 250,
        xaxis: { title: 'Maintainability Range' },
        margin: { t: 30, b: 50, l: 80, r: 30 }
    });
    
    // Most Complex Programs Bar Chart
    const complexPrograms = metricsData.aggregates.overall.mostComplex.slice(0, 10);
    
    Plotly.newPlot('complex-programs-chart', [{
        x: complexPrograms.map(p => p.complexity),
        y: complexPrograms.map(p => p.file),
        type: 'bar',
        orientation: 'h',
        marker: { color: '#e74c3c' }
    }], {
        height: 300,
        xaxis: { title: 'Complexity' },
        margin: { t: 30, b: 50, l: 150, r: 30 }
    });
    
    // Size Distribution Box Plot
    const sizeBySubsystem = {};
    subsystems.forEach(subsys => {
        sizeBySubsystem[subsys] = metricsData.metrics
            .filter(m => m.subsystem === subsys && m.fileType === 'program')
            .map(m => m.lines);
    });
    
    const sizeTraces = Object.entries(sizeBySubsystem).map(([subsys, sizes]) => ({
        y: sizes,
        type: 'box',
        name: subsys.toUpperCase()
    }));
    
    Plotly.newPlot('size-distribution-chart', sizeTraces, {
        height: 300,
        yaxis: { title: 'Lines of Code' },
        margin: { t: 30, b: 50, l: 50, r: 30 }
    });
    
    // Dependencies Summary
    const dependencyTypes = {
        'CALL Dependencies': metricsData.metrics.reduce((sum, m) => sum + m.callStatements, 0),
        'COPY Dependencies': metricsData.metrics.reduce((sum, m) => sum + m.copyStatements, 0),
        'PERFORM Statements': metricsData.metrics.reduce((sum, m) => sum + m.performStatements, 0)
    };
    
    Plotly.newPlot('dependencies-chart', [{
        x: Object.keys(dependencyTypes),
        y: Object.values(dependencyTypes),
        type: 'bar',
        marker: { color: ['#3498db', '#2ecc71', '#f39c12'] }
    }], {
        height: 250,
        yaxis: { title: 'Count' },
        margin: { t: 30, b: 50, l: 50, r: 30 }
    });
    
    // Generate Programs Table
    generateProgramsTable();
    generateComplexityTable();
    generateDependenciesTable();
});

function generateProgramsTable() {
    const programs = metricsData.metrics.filter(m => m.fileType === 'program');
    
    let html = '<table class="data-table">';
    html += '<thead><tr>';
    html += '<th>Program</th><th>Subsystem</th><th>Lines</th><th>Complexity</th><th>Maintainability</th>';
    html += '</tr></thead><tbody>';
    
    programs.forEach(prog => {
        const maintClass = prog.complexity.maintainability < 40 ? 'low' : 
                          prog.complexity.maintainability < 70 ? 'medium' : 'high';
        html += '<tr>';
        html += '<td>' + prog.file + '</td>';
        html += '<td>' + prog.subsystem.toUpperCase() + '</td>';
        html += '<td>' + prog.lines.toLocaleString() + '</td>';
        html += '<td>' + prog.complexity.cyclomatic + '</td>';
        html += '<td class="maint-' + maintClass + '">' + prog.complexity.maintainability.toFixed(1) + '%</td>';
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    document.getElementById('programs-table').innerHTML = html;
}

function generateComplexityTable() {
    const programs = metricsData.metrics
        .filter(m => m.fileType === 'program')
        .sort((a, b) => b.complexity.cyclomatic - a.complexity.cyclomatic)
        .slice(0, 20);
    
    let html = '<table class="data-table">';
    html += '<thead><tr>';
    html += '<th>Rank</th><th>Program</th><th>Cyclomatic</th><th>Halstead Volume</th><th>Effort</th>';
    html += '</tr></thead><tbody>';
    
    programs.forEach((prog, idx) => {
        html += '<tr>';
        html += '<td>' + (idx + 1) + '</td>';
        html += '<td>' + prog.file + '</td>';
        html += '<td>' + prog.complexity.cyclomatic + '</td>';
        html += '<td>' + prog.complexity.halstead.volume.toLocaleString() + '</td>';
        html += '<td>' + prog.complexity.halstead.effort.toLocaleString() + '</td>';
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    document.getElementById('complexity-table').innerHTML = html;
}

function generateDependenciesTable() {
    const programs = metricsData.metrics.filter(m => 
        m.fileType === 'program' && (m.callStatements > 0 || m.copyStatements > 0)
    );
    
    let html = '<table class="data-table">';
    html += '<thead><tr>';
    html += '<th>Program</th><th>CALL Dependencies</th><th>COPY Dependencies</th><th>Details</th>';
    html += '</tr></thead><tbody>';
    
    programs.forEach(prog => {
        html += '<tr>';
        html += '<td>' + prog.file + '</td>';
        html += '<td>' + prog.callStatements + '</td>';
        html += '<td>' + prog.copyStatements + '</td>';
        html += '<td>';
        if (prog.dependencies.calls.length > 0) {
            html += '<strong>Calls:</strong> ' + prog.dependencies.calls.join(', ') + '<br>';
        }
        if (prog.dependencies.copies.length > 0) {
            html += '<strong>Copies:</strong> ' + prog.dependencies.copies.join(', ');
        }
        html += '</td>';
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    document.getElementById('dependencies-table').innerHTML = html;
}

function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

function filterPrograms() {
    const searchTerm = document.getElementById('program-search').value.toLowerCase();
    const rows = document.querySelectorAll('#programs-table tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}`;
}

function generateDashboardCSS() {
    return `/* Dashboard Styles */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: #f0f2f5;
    color: #333;
    line-height: 1.6;
}

.dashboard-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

header {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

h1 {
    color: #2c3e50;
    font-size: 28px;
}

.timestamp {
    color: #7f8c8d;
    font-size: 14px;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
}

.metric-card h3 {
    color: #7f8c8d;
    font-size: 14px;
    font-weight: normal;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #2c3e50;
}

.charts-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin-bottom: 30px;
}

.chart-container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chart-container h3 {
    color: #2c3e50;
    margin-bottom: 15px;
    font-size: 18px;
}

.chart-container.full-width {
    grid-column: span 2;
}

.tables-section {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.tables-section h2 {
    color: #2c3e50;
    margin-bottom: 20px;
}

.table-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.tab-button {
    padding: 10px 20px;
    background-color: #ecf0f1;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
}

.tab-button.active {
    background-color: #3498db;
    color: white;
}

.tab-button:hover {
    background-color: #bdc3c7;
}

.tab-button.active:hover {
    background-color: #2980b9;
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

#program-search {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table thead {
    background-color: #34495e;
    color: white;
}

.data-table th,
.data-table td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ecf0f1;
}

.data-table tbody tr:hover {
    background-color: #f8f9fa;
}

.maint-low { color: #e74c3c; }
.maint-medium { color: #f39c12; }
.maint-high { color: #27ae60; }

.quick-links {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.quick-links h3 {
    color: #2c3e50;
    margin-bottom: 15px;
}

.quick-links a {
    display: inline-block;
    margin-right: 20px;
    color: #3498db;
    text-decoration: none;
    padding: 8px 0;
}

.quick-links a:hover {
    text-decoration: underline;
}

@media (max-width: 768px) {
    .charts-grid {
        grid-template-columns: 1fr;
    }
    
    .chart-container.full-width {
        grid-column: span 1;
    }
    
    .metrics-grid {
        grid-template-columns: 1fr;
    }
}`;
}

function generateServer() {
    return `const express = require('express');
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
    console.log(\`Dashboard server running at http://localhost:\${PORT}\`);
    console.log('Press Ctrl+C to stop');
});`;
}

// Run if called directly
if (require.main === module) {
    buildDashboard().catch(console.error);
}

module.exports = { buildDashboard };