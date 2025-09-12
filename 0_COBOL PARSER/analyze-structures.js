const fs = require('fs-extra');
const path = require('path');
const glob = require('glob');

// Analysis results
const analysis = {
    programs: [],
    copybooks: [],
    dependencies: {},
    calls: {},
    copyDependencies: {},
    unusedCopybooks: [],
    mainPrograms: [],
    summary: {}
};

// Function to analyze a parsed structure file
function analyzeStructure(jsonFile) {
    try {
        const data = fs.readJsonSync(jsonFile);
        
        // Skip non-COBOL files
        if (!data.sourceFile) return;
        
        const structure = data.structure;
        const sourceFile = data.sourceFile;
        const fileType = data.fileType;
        
        const fileInfo = {
            name: path.basename(sourceFile),
            path: sourceFile,
            type: fileType,
            programId: structure.programId,
            calls: structure.callStatements || [],
            copies: structure.copyStatements || [],
            performs: structure.performStatements || [],
            files: structure.fileDescriptions || [],
            divisions: structure.divisions || [],
            sections: structure.sections || [],
            paragraphs: structure.paragraphs || []
        };
        
        // Add to appropriate list
        if (fileType === 'copybook') {
            analysis.copybooks.push(fileInfo);
        } else {
            analysis.programs.push(fileInfo);
            
            // Identify main programs (those with menu-like structures)
            if (fileInfo.name.match(/^(ACAS|irs|sales|purchase|stock|general)\.cbl$/i)) {
                analysis.mainPrograms.push(fileInfo);
            }
        }
        
        // Track copy dependencies
        if (fileInfo.copies.length > 0) {
            analysis.copyDependencies[sourceFile] = fileInfo.copies;
        }
        
        // Track call dependencies
        if (fileInfo.calls.length > 0) {
            analysis.calls[sourceFile] = fileInfo.calls;
        }
        
    } catch (error) {
        // Ignore non-structure files
    }
}

// Find unused copybooks
function findUnusedCopybooks() {
    const usedCopybooks = new Set();
    
    // Collect all used copybooks
    for (const program of analysis.programs) {
        for (const copy of program.copies) {
            usedCopybooks.add(copy.toUpperCase());
        }
    }
    
    // Find copybooks that are never used
    for (const copybook of analysis.copybooks) {
        const copyName = copybook.name.replace('.cpy', '').toUpperCase();
        let isUsed = false;
        
        for (const used of usedCopybooks) {
            if (used === copyName || used.includes(copyName)) {
                isUsed = true;
                break;
            }
        }
        
        if (!isUsed) {
            analysis.unusedCopybooks.push(copybook.path);
        }
    }
}

// Generate call graph
function generateCallGraph() {
    const callGraph = {
        nodes: [],
        edges: [],
        mainPrograms: [],
        subsystems: {
            irs: { programs: [], calls: [] },
            sales: { programs: [], calls: [] },
            purchase: { programs: [], calls: [] },
            stock: { programs: [], calls: [] },
            general: { programs: [], calls: [] },
            common: { programs: [], calls: [] }
        }
    };
    
    // Add all programs as nodes
    for (const program of analysis.programs) {
        const node = {
            id: program.programId || program.name,
            label: program.name,
            type: 'program',
            path: program.path,
            subsystem: getSubsystem(program.path)
        };
        
        callGraph.nodes.push(node);
        
        // Categorize by subsystem
        const subsystem = callGraph.subsystems[node.subsystem];
        if (subsystem) {
            subsystem.programs.push(node.id);
        }
    }
    
    // Add main programs
    callGraph.mainPrograms = analysis.mainPrograms.map(p => p.name);
    
    // Add edges for calls
    for (const program of analysis.programs) {
        const callerId = program.programId || program.name;
        const subsystem = getSubsystem(program.path);
        
        for (const callee of program.calls) {
            const edge = {
                from: callerId,
                to: callee,
                type: 'calls'
            };
            
            callGraph.edges.push(edge);
            
            // Add to subsystem calls
            const sub = callGraph.subsystems[subsystem];
            if (sub) {
                sub.calls.push(edge);
            }
        }
    }
    
    return callGraph;
}

// Get subsystem from path
function getSubsystem(filePath) {
    if (filePath.includes('irs/')) return 'irs';
    if (filePath.includes('sales/')) return 'sales';
    if (filePath.includes('purchase/')) return 'purchase';
    if (filePath.includes('stock/')) return 'stock';
    if (filePath.includes('general/')) return 'general';
    return 'common';
}

// Generate system summary
function generateSummary() {
    const summary = {
        overview: {
            totalPrograms: analysis.programs.length,
            totalCopybooks: analysis.copybooks.length,
            mainPrograms: analysis.mainPrograms.length,
            unusedCopybooks: analysis.unusedCopybooks.length
        },
        subsystems: {},
        dataAccessLayer: {
            MT_modules: [],
            LD_modules: [],
            UNL_modules: [],
            RES_modules: []
        },
        fileTypes: {
            programs: {},
            copybooks: {}
        }
    };
    
    // Analyze subsystems
    const subsystems = ['irs', 'sales', 'purchase', 'stock', 'general', 'common'];
    for (const sub of subsystems) {
        const programs = analysis.programs.filter(p => getSubsystem(p.path) === sub);
        summary.subsystems[sub] = {
            programs: programs.length,
            withCalls: programs.filter(p => p.calls.length > 0).length,
            withCopies: programs.filter(p => p.copies.length > 0).length
        };
    }
    
    // Analyze DAL modules
    for (const program of analysis.programs) {
        if (program.name.endsWith('MT.cbl')) {
            summary.dataAccessLayer.MT_modules.push(program.name);
        } else if (program.name.endsWith('LD.cbl')) {
            summary.dataAccessLayer.LD_modules.push(program.name);
        } else if (program.name.endsWith('UNL.cbl')) {
            summary.dataAccessLayer.UNL_modules.push(program.name);
        } else if (program.name.endsWith('RES.cbl')) {
            summary.dataAccessLayer.RES_modules.push(program.name);
        }
    }
    
    // Count file patterns
    for (const program of analysis.programs) {
        const pattern = program.name.replace(/[0-9]+/, 'XXX');
        summary.fileTypes.programs[pattern] = (summary.fileTypes.programs[pattern] || 0) + 1;
    }
    
    return summary;
}

// Main analysis function
async function main() {
    console.log('ACAS COBOL Structure Analysis');
    console.log('=============================\n');
    
    // Find all parsed JSON files
    const jsonFiles = glob.sync('parsed-structures/*.json', {
        cwd: __dirname,
        absolute: true
    });
    
    console.log(`Found ${jsonFiles.length} parsed structure files to analyze\n`);
    
    // Analyze each file
    for (const file of jsonFiles) {
        analyzeStructure(file);
    }
    
    // Find unused copybooks
    findUnusedCopybooks();
    
    // Generate summary
    analysis.summary = generateSummary();
    
    // Generate call graph
    const callGraph = generateCallGraph();
    
    // Save analysis results
    const resultsDir = path.join(__dirname, 'analysis-results');
    await fs.ensureDir(resultsDir);
    await fs.writeJson(path.join(resultsDir, 'structure-analysis.json'), analysis, { spaces: 2 });
    await fs.writeJson(path.join(resultsDir, 'system-call-graph.json'), callGraph, { spaces: 2 });
    
    // Print detailed summary
    console.log('System Overview:');
    console.log(`- Total Programs: ${analysis.summary.overview.totalPrograms}`);
    console.log(`- Total Copybooks: ${analysis.summary.overview.totalCopybooks}`);
    console.log(`- Main Menu Programs: ${analysis.summary.overview.mainPrograms}`);
    console.log(`- Unused Copybooks: ${analysis.summary.overview.unusedCopybooks}`);
    
    console.log('\nSubsystem Breakdown:');
    for (const [sub, data] of Object.entries(analysis.summary.subsystems)) {
        console.log(`\n${sub.toUpperCase()}:`);
        console.log(`  - Programs: ${data.programs}`);
        console.log(`  - With CALL statements: ${data.withCalls}`);
        console.log(`  - With COPY statements: ${data.withCopies}`);
    }
    
    console.log('\nData Access Layer (DAL) Modules:');
    console.log(`- MT (Main Table) modules: ${analysis.summary.dataAccessLayer.MT_modules.length}`);
    console.log(`- LD (Load) modules: ${analysis.summary.dataAccessLayer.LD_modules.length}`);
    console.log(`- UNL (Unload) modules: ${analysis.summary.dataAccessLayer.UNL_modules.length}`);
    console.log(`- RES (Reserve) modules: ${analysis.summary.dataAccessLayer.RES_modules.length}`);
    
    if (analysis.unusedCopybooks.length > 0) {
        console.log('\nUnused Copybooks:');
        analysis.unusedCopybooks.forEach(cb => console.log(`  - ${cb}`));
    }
    
    // Find programs with most calls
    const programsWithCalls = analysis.programs
        .filter(p => p.calls.length > 0)
        .sort((a, b) => b.calls.length - a.calls.length)
        .slice(0, 10);
    
    if (programsWithCalls.length > 0) {
        console.log('\nTop Programs by CALL statements:');
        programsWithCalls.forEach(p => {
            console.log(`  - ${p.name}: ${p.calls.length} calls`);
        });
    }
    
    console.log('\nAnalysis complete! Results saved to:');
    console.log('- structure-analysis.json');
    console.log('- system-call-graph.json');
}

// Run analysis
main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
});