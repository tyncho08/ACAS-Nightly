const fs = require('fs-extra');
const path = require('path');
const glob = require('glob');
const sqlite3 = require('sqlite3').verbose();

// Paths
const PARSED_DIR = path.join(__dirname, '../../parsed-structures');
const DATA_DIR = path.join(__dirname, '../dashboard/data');
const DB_PATH = path.join(DATA_DIR, 'metrics.db');

// Ensure directories exist
fs.ensureDirSync(DATA_DIR);

async function analyzeMetrics() {
    console.log('Analyzing COBOL Metrics...\n');
    
    // Initialize SQLite database
    const db = await initializeDatabase();
    
    // Load all parsed JSON files
    const jsonFiles = glob.sync('*.json', { cwd: PARSED_DIR });
    
    console.log(`Processing ${jsonFiles.length} files...`);
    
    // Process each file and collect metrics
    const metrics = [];
    
    for (const file of jsonFiles) {
        const data = await fs.readJson(path.join(PARSED_DIR, file));
        const metric = calculateMetrics(data);
        metrics.push(metric);
        
        // Insert into database
        await insertMetric(db, metric);
    }
    
    // Calculate aggregate metrics
    const aggregates = calculateAggregates(metrics);
    
    // Save metrics to JSON for dashboard
    await fs.writeJson(path.join(DATA_DIR, 'metrics.json'), {
        timestamp: new Date().toISOString(),
        totalFiles: metrics.length,
        metrics: metrics,
        aggregates: aggregates
    }, { spaces: 2 });
    
    // Generate summary report
    await generateMetricsReport(aggregates, metrics);
    
    // Close database
    db.close();
    
    console.log(`\n✓ Metrics analysis complete`);
    console.log(`✓ Database created: ${DB_PATH}`);
    console.log(`✓ Metrics saved: ${DATA_DIR}/metrics.json`);
}

function calculateMetrics(programData) {
    const structure = programData.structure;
    const name = path.basename(programData.sourceFile);
    const subsystem = getSubsystem(programData.sourceFile);
    
    // Calculate complexity metrics
    const complexity = {
        cyclomatic: calculateCyclomaticComplexity(structure),
        halstead: calculateHalsteadMetrics(structure),
        maintainability: 0
    };
    
    // Calculate maintainability index (simplified)
    complexity.maintainability = Math.max(0, 
        171 - 5.2 * Math.log(complexity.halstead.volume) 
        - 0.23 * complexity.cyclomatic 
        - 16.2 * Math.log(programData.stats?.lines || 1)
    ) * 100 / 171;
    
    return {
        file: name,
        path: programData.sourceFile,
        subsystem: subsystem,
        fileType: programData.fileType,
        lines: programData.stats?.lines || 0,
        size: programData.stats?.size || 0,
        divisions: structure.divisions.length,
        sections: structure.sections.length,
        paragraphs: structure.paragraphs.length,
        dataItems: structure.dataItems?.length || 0,
        workingStorage: structure.workingStorage?.length || 0,
        fileOperations: structure.fileDescriptions.length,
        callStatements: structure.callStatements.length,
        copyStatements: structure.copyStatements.length,
        performStatements: structure.performStatements.length,
        complexity: complexity,
        dependencies: {
            calls: structure.callStatements,
            copies: structure.copyStatements,
            performs: structure.performStatements
        }
    };
}

function calculateCyclomaticComplexity(structure) {
    // Simplified calculation based on decision points
    let complexity = 1; // Base complexity
    
    // Add complexity for each section and paragraph (potential branch points)
    complexity += structure.sections.length;
    complexity += structure.paragraphs.length;
    
    // Add complexity for PERFORM statements (loops/branches)
    complexity += structure.performStatements.length;
    
    // Add complexity for file operations (I/O branches)
    complexity += structure.fileDescriptions.length;
    
    return complexity;
}

function calculateHalsteadMetrics(structure) {
    // Simplified Halstead metrics
    const operators = new Set();
    const operands = new Set();
    
    // Count unique operators (verbs, keywords)
    operators.add('DIVISION');
    operators.add('SECTION');
    operators.add('PERFORM');
    operators.add('CALL');
    operators.add('COPY');
    
    // Count unique operands (identifiers, literals)
    structure.paragraphs.forEach(p => operands.add(p));
    structure.dataItems?.forEach(d => operands.add(d));
    structure.callStatements.forEach(c => operands.add(c));
    structure.copyStatements.forEach(c => operands.add(c));
    
    const n1 = operators.size; // Unique operators
    const n2 = operands.size;  // Unique operands
    const N1 = structure.sections.length + structure.paragraphs.length + 
               structure.performStatements.length + structure.callStatements.length;
    const N2 = structure.dataItems?.length || 0 + structure.workingStorage?.length || 0;
    
    const vocabulary = n1 + n2;
    const length = N1 + N2;
    const volume = length * Math.log2(vocabulary || 1);
    const difficulty = (n1 / 2) * (N2 / (n2 || 1));
    const effort = volume * difficulty;
    
    return {
        vocabulary,
        length,
        volume: Math.round(volume),
        difficulty: Math.round(difficulty * 100) / 100,
        effort: Math.round(effort)
    };
}

function calculateAggregates(metrics) {
    const agg = {
        bySubsystem: {},
        byFileType: {},
        overall: {
            totalPrograms: metrics.filter(m => m.fileType === 'program').length,
            totalCopybooks: metrics.filter(m => m.fileType === 'copybook').length,
            totalLines: metrics.reduce((sum, m) => sum + m.lines, 0),
            totalSize: metrics.reduce((sum, m) => sum + m.size, 0),
            avgComplexity: 0,
            avgMaintainability: 0,
            mostComplex: [],
            leastMaintainable: [],
            largestPrograms: [],
            mostDependencies: []
        }
    };
    
    // Calculate by subsystem
    const subsystems = ['irs', 'sales', 'purchase', 'stock', 'general', 'common'];
    for (const subsys of subsystems) {
        const subsysMetrics = metrics.filter(m => m.subsystem === subsys);
        if (subsysMetrics.length > 0) {
            agg.bySubsystem[subsys] = {
                programs: subsysMetrics.filter(m => m.fileType === 'program').length,
                copybooks: subsysMetrics.filter(m => m.fileType === 'copybook').length,
                totalLines: subsysMetrics.reduce((sum, m) => sum + m.lines, 0),
                avgComplexity: average(subsysMetrics.map(m => m.complexity.cyclomatic)),
                avgMaintainability: average(subsysMetrics.map(m => m.complexity.maintainability))
            };
        }
    }
    
    // Calculate overall averages
    agg.overall.avgComplexity = average(metrics.map(m => m.complexity.cyclomatic));
    agg.overall.avgMaintainability = average(metrics.map(m => m.complexity.maintainability));
    
    // Find outliers
    const programs = metrics.filter(m => m.fileType === 'program');
    
    agg.overall.mostComplex = programs
        .sort((a, b) => b.complexity.cyclomatic - a.complexity.cyclomatic)
        .slice(0, 10)
        .map(m => ({ file: m.file, complexity: m.complexity.cyclomatic }));
    
    agg.overall.leastMaintainable = programs
        .sort((a, b) => a.complexity.maintainability - b.complexity.maintainability)
        .slice(0, 10)
        .map(m => ({ file: m.file, maintainability: Math.round(m.complexity.maintainability) }));
    
    agg.overall.largestPrograms = programs
        .sort((a, b) => b.lines - a.lines)
        .slice(0, 10)
        .map(m => ({ file: m.file, lines: m.lines }));
    
    agg.overall.mostDependencies = programs
        .sort((a, b) => (b.callStatements + b.copyStatements) - (a.callStatements + a.copyStatements))
        .slice(0, 10)
        .map(m => ({ file: m.file, dependencies: m.callStatements + m.copyStatements }));
    
    return agg;
}

function average(numbers) {
    if (numbers.length === 0) return 0;
    return Math.round(numbers.reduce((a, b) => a + b, 0) / numbers.length * 100) / 100;
}

async function initializeDatabase() {
    return new Promise((resolve, reject) => {
        const db = new sqlite3.Database(DB_PATH);
        
        db.serialize(() => {
            // Create metrics table
            db.run(`CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file TEXT NOT NULL,
                path TEXT NOT NULL,
                subsystem TEXT,
                fileType TEXT,
                lines INTEGER,
                size INTEGER,
                divisions INTEGER,
                sections INTEGER,
                paragraphs INTEGER,
                dataItems INTEGER,
                workingStorage INTEGER,
                fileOperations INTEGER,
                callStatements INTEGER,
                copyStatements INTEGER,
                performStatements INTEGER,
                cyclomaticComplexity INTEGER,
                halsteadVolume INTEGER,
                maintainability REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )`);
            
            // Create dependencies table
            db.run(`CREATE TABLE IF NOT EXISTS dependencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sourceFile TEXT NOT NULL,
                targetFile TEXT NOT NULL,
                dependencyType TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )`);
            
            // Clear existing data
            db.run('DELETE FROM metrics');
            db.run('DELETE FROM dependencies');
            
            resolve(db);
        });
    });
}

function insertMetric(db, metric) {
    return new Promise((resolve, reject) => {
        const stmt = db.prepare(`INSERT INTO metrics 
            (file, path, subsystem, fileType, lines, size, divisions, sections, 
             paragraphs, dataItems, workingStorage, fileOperations, callStatements, 
             copyStatements, performStatements, cyclomaticComplexity, halsteadVolume, 
             maintainability) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`);
        
        stmt.run(
            metric.file,
            metric.path,
            metric.subsystem,
            metric.fileType,
            metric.lines,
            metric.size,
            metric.divisions,
            metric.sections,
            metric.paragraphs,
            metric.dataItems,
            metric.workingStorage,
            metric.fileOperations,
            metric.callStatements,
            metric.copyStatements,
            metric.performStatements,
            metric.complexity.cyclomatic,
            metric.complexity.halstead.volume,
            metric.complexity.maintainability
        );
        
        stmt.finalize();
        
        // Insert dependencies
        const depStmt = db.prepare(`INSERT INTO dependencies 
            (sourceFile, targetFile, dependencyType) VALUES (?, ?, ?)`);
        
        metric.dependencies.calls.forEach(target => {
            depStmt.run(metric.file, target, 'CALL');
        });
        
        metric.dependencies.copies.forEach(target => {
            depStmt.run(metric.file, target, 'COPY');
        });
        
        depStmt.finalize();
        
        resolve();
    });
}

async function generateMetricsReport(aggregates, metrics) {
    let report = '# COBOL Metrics Analysis Report\n\n';
    report += `Generated: ${new Date().toISOString()}\n\n`;
    
    report += '## Overall Statistics\n\n';
    report += `- **Total Programs:** ${aggregates.overall.totalPrograms}\n`;
    report += `- **Total Copybooks:** ${aggregates.overall.totalCopybooks}\n`;
    report += `- **Total Lines of Code:** ${aggregates.overall.totalLines.toLocaleString()}\n`;
    report += `- **Total Size:** ${(aggregates.overall.totalSize / 1024 / 1024).toFixed(2)} MB\n`;
    report += `- **Average Complexity:** ${aggregates.overall.avgComplexity}\n`;
    report += `- **Average Maintainability:** ${aggregates.overall.avgMaintainability.toFixed(1)}%\n\n`;
    
    report += '## Subsystem Metrics\n\n';
    report += '| Subsystem | Programs | Lines | Avg Complexity | Avg Maintainability |\n';
    report += '|-----------|----------|-------|----------------|--------------------|\n';
    
    for (const [subsys, data] of Object.entries(aggregates.bySubsystem)) {
        report += `| ${subsys.toUpperCase()} | ${data.programs} | ${data.totalLines.toLocaleString()} | ${data.avgComplexity} | ${data.avgMaintainability.toFixed(1)}% |\n`;
    }
    
    report += '\n## Top 10 Most Complex Programs\n\n';
    aggregates.overall.mostComplex.forEach((prog, idx) => {
        report += `${idx + 1}. **${prog.file}** - Complexity: ${prog.complexity}\n`;
    });
    
    report += '\n## Top 10 Least Maintainable Programs\n\n';
    aggregates.overall.leastMaintainable.forEach((prog, idx) => {
        report += `${idx + 1}. **${prog.file}** - Maintainability: ${prog.maintainability}%\n`;
    });
    
    report += '\n## Top 10 Largest Programs\n\n';
    aggregates.overall.largestPrograms.forEach((prog, idx) => {
        report += `${idx + 1}. **${prog.file}** - Lines: ${prog.lines.toLocaleString()}\n`;
    });
    
    await fs.writeFile(path.join(DATA_DIR, 'metrics-report.md'), report);
}

function getSubsystem(filePath) {
    if (filePath.includes('irs/')) return 'irs';
    if (filePath.includes('sales/')) return 'sales';
    if (filePath.includes('purchase/')) return 'purchase';
    if (filePath.includes('stock/')) return 'stock';
    if (filePath.includes('general/')) return 'general';
    return 'common';
}

// Run if called directly
if (require.main === module) {
    analyzeMetrics().catch(console.error);
}

module.exports = { analyzeMetrics };