// Dashboard JavaScript
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
}