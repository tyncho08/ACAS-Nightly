const fs = require('fs-extra');
const path = require('path');
const glob = require('glob');

// Paths
const PARSED_DIR = path.join(__dirname, '../../parsed-structures');
const ANALYSIS_DIR = path.join(__dirname, '../../analysis-results');
const OUTPUT_DIR = path.join(__dirname, '../docs');

// Ensure output directory exists
fs.ensureDirSync(OUTPUT_DIR);

async function generateDocumentation() {
    console.log('Generating COBOL System Documentation...\n');
    
    // Load all parsed JSON files
    const jsonFiles = glob.sync('*.json', { cwd: PARSED_DIR });
    
    // Organize data
    const programs = [];
    const copybooks = [];
    const subsystems = {
        irs: { programs: [], copybooks: [], description: 'Internal Revenue System' },
        sales: { programs: [], copybooks: [], description: 'Sales Ledger' },
        purchase: { programs: [], copybooks: [], description: 'Purchase Ledger' },
        stock: { programs: [], copybooks: [], description: 'Stock Control' },
        general: { programs: [], copybooks: [], description: 'General Ledger' },
        common: { programs: [], copybooks: [], description: 'Common/Shared Modules' }
    };
    
    // Process each file
    for (const file of jsonFiles) {
        const data = await fs.readJson(path.join(PARSED_DIR, file));
        const subsystem = getSubsystem(data.sourceFile);
        
        if (data.fileType === 'copybook') {
            copybooks.push(data);
            subsystems[subsystem].copybooks.push(data);
        } else {
            programs.push(data);
            subsystems[subsystem].programs.push(data);
        }
    }
    
    // Generate main documentation
    let markdown = '# ACAS COBOL System Documentation\n\n';
    markdown += `Generated on: ${new Date().toISOString()}\n\n`;
    
    // Table of Contents
    markdown += '## Table of Contents\n\n';
    markdown += '1. [System Overview](#system-overview)\n';
    markdown += '2. [Architecture](#architecture)\n';
    markdown += '3. [Subsystems](#subsystems)\n';
    markdown += '4. [Data Access Layer](#data-access-layer)\n';
    markdown += '5. [Programs Index](#programs-index)\n';
    markdown += '6. [Copybooks Index](#copybooks-index)\n';
    markdown += '7. [Dependencies](#dependencies)\n';
    markdown += '8. [Visualizations](#visualizations)\n\n';
    
    // System Overview
    markdown += '## System Overview\n\n';
    markdown += 'ACAS (Applewood Computers Accounting System) is a comprehensive accounting and business management system written in COBOL.\n\n';
    
    markdown += '### Statistics\n\n';
    markdown += `- **Total Programs:** ${programs.length}\n`;
    markdown += `- **Total Copybooks:** ${copybooks.length}\n`;
    markdown += `- **Total Files:** ${programs.length + copybooks.length}\n\n`;
    
    // Architecture
    markdown += '## Architecture\n\n';
    markdown += '### Subsystem Distribution\n\n';
    markdown += '| Subsystem | Programs | Copybooks | Description |\n';
    markdown += '|-----------|----------|-----------|-------------|\n';
    
    for (const [key, data] of Object.entries(subsystems)) {
        markdown += `| ${key.toUpperCase()} | ${data.programs.length} | ${data.copybooks.length} | ${data.description} |\n`;
    }
    
    // Subsystems detail
    markdown += '\n## Subsystems\n\n';
    
    for (const [key, data] of Object.entries(subsystems)) {
        if (data.programs.length === 0 && data.copybooks.length === 0) continue;
        
        markdown += `### ${key.toUpperCase()} - ${data.description}\n\n`;
        
        if (data.programs.length > 0) {
            markdown += '#### Programs\n\n';
            markdown += '| Program | Divisions | Sections | Paragraphs | CALLs | COPYs |\n';
            markdown += '|---------|-----------|----------|------------|-------|-------|\n';
            
            for (const prog of data.programs.sort((a, b) => a.sourceFile.localeCompare(b.sourceFile))) {
                const name = path.basename(prog.sourceFile);
                const s = prog.structure;
                markdown += `| ${name} | ${s.divisions.length} | ${s.sections.length} | ${s.paragraphs.length} | ${s.callStatements.length} | ${s.copyStatements.length} |\n`;
            }
            markdown += '\n';
        }
        
        if (data.copybooks.length > 0) {
            markdown += '#### Copybooks\n\n';
            for (const copy of data.copybooks) {
                markdown += `- **${path.basename(copy.sourceFile)}**\n`;
            }
            markdown += '\n';
        }
    }
    
    // Data Access Layer
    markdown += '## Data Access Layer\n\n';
    markdown += 'The system uses a consistent DAL pattern with specialized modules:\n\n';
    
    const dalTypes = {
        MT: { name: 'Main Table', pattern: 'MT.cbl', programs: [] },
        LD: { name: 'Load', pattern: 'LD.cbl', programs: [] },
        UNL: { name: 'Unload', pattern: 'UNL.cbl', programs: [] },
        RES: { name: 'Reserve', pattern: 'RES.cbl', programs: [] }
    };
    
    for (const prog of programs) {
        const name = path.basename(prog.sourceFile);
        for (const [key, type] of Object.entries(dalTypes)) {
            if (name.endsWith(type.pattern)) {
                type.programs.push(name);
            }
        }
    }
    
    for (const [key, type] of Object.entries(dalTypes)) {
        markdown += `### ${type.name} Modules (${key})\n\n`;
        markdown += `Total: ${type.programs.length} modules\n\n`;
        if (type.programs.length > 0) {
            markdown += '```\n';
            type.programs.sort().forEach(p => markdown += `${p}\n`);
            markdown += '```\n\n';
        }
    }
    
    // Programs Index
    markdown += '## Programs Index\n\n';
    markdown += generateProgramsIndex(programs);
    
    // Copybooks Index
    markdown += '## Copybooks Index\n\n';
    markdown += generateCopybooksIndex(copybooks);
    
    // Dependencies
    markdown += '## Dependencies\n\n';
    markdown += '### Call Dependencies\n\n';
    markdown += generateCallDependencies(programs);
    
    markdown += '### Copy Dependencies\n\n';
    markdown += generateCopyDependencies(programs);
    
    // Visualizations
    markdown += '## Visualizations\n\n';
    markdown += '- [Call Graph](../visualizations/call-graph.html) - Interactive network graph of program dependencies\n';
    markdown += '- [Flowcharts](../visualizations/flowcharts/index.html) - Procedure flow diagrams for programs\n';
    markdown += '- [Dashboard](../dashboard/index.html) - Interactive metrics dashboard\n';
    
    // Save main documentation
    await fs.writeFile(path.join(OUTPUT_DIR, 'COBOL-Documentation.md'), markdown);
    
    // Generate HTML version
    const htmlContent = generateHTMLDoc(markdown);
    await fs.writeFile(path.join(OUTPUT_DIR, 'index.html'), htmlContent);
    
    // Generate subsystem-specific docs
    for (const [key, data] of Object.entries(subsystems)) {
        if (data.programs.length > 0) {
            await generateSubsystemDoc(key, data);
        }
    }
    
    console.log(`✓ Documentation generated: ${OUTPUT_DIR}/COBOL-Documentation.md`);
    console.log(`✓ HTML documentation: ${OUTPUT_DIR}/index.html`);
    console.log(`✓ Subsystem docs generated`);
}

function generateProgramsIndex(programs) {
    let index = 'Complete alphabetical listing of all programs:\n\n';
    
    const sorted = programs.sort((a, b) => 
        path.basename(a.sourceFile).localeCompare(path.basename(b.sourceFile))
    );
    
    index += '| Program | Path | Program ID | Size (lines) |\n';
    index += '|---------|------|------------|-------------|\n';
    
    for (const prog of sorted) {
        const name = path.basename(prog.sourceFile);
        const programId = prog.structure.programId || '-';
        const lines = prog.stats?.lines || '-';
        index += `| ${name} | ${prog.sourceFile} | ${programId} | ${lines} |\n`;
    }
    
    return index + '\n';
}

function generateCopybooksIndex(copybooks) {
    if (copybooks.length === 0) {
        return 'No copybooks found in the system.\n\n';
    }
    
    let index = 'Complete listing of all copybooks:\n\n';
    
    index += '| Copybook | Path | Size (lines) |\n';
    index += '|----------|------|-------------|\n';
    
    for (const copy of copybooks.sort((a, b) => a.sourceFile.localeCompare(b.sourceFile))) {
        const name = path.basename(copy.sourceFile);
        const lines = copy.stats?.lines || '-';
        index += `| ${name} | ${copy.sourceFile} | ${lines} |\n`;
    }
    
    return index + '\n';
}

function generateCallDependencies(programs) {
    let deps = '';
    const callMap = new Map();
    
    for (const prog of programs) {
        if (prog.structure.callStatements.length > 0) {
            const caller = path.basename(prog.sourceFile);
            callMap.set(caller, prog.structure.callStatements);
        }
    }
    
    if (callMap.size === 0) {
        return 'No CALL dependencies found.\n\n';
    }
    
    deps += `Found ${callMap.size} programs with CALL statements:\n\n`;
    
    for (const [caller, callees] of callMap) {
        deps += `**${caller}** calls:\n`;
        callees.forEach(callee => deps += `  - ${callee}\n`);
        deps += '\n';
    }
    
    return deps;
}

function generateCopyDependencies(programs) {
    let deps = '';
    const copyMap = new Map();
    
    for (const prog of programs) {
        if (prog.structure.copyStatements.length > 0) {
            const program = path.basename(prog.sourceFile);
            copyMap.set(program, prog.structure.copyStatements);
        }
    }
    
    if (copyMap.size === 0) {
        return 'No COPY dependencies found.\n\n';
    }
    
    deps += `Found ${copyMap.size} programs with COPY statements:\n\n`;
    
    for (const [program, copies] of copyMap) {
        deps += `**${program}** copies:\n`;
        copies.forEach(copy => deps += `  - ${copy}\n`);
        deps += '\n';
    }
    
    return deps;
}

async function generateSubsystemDoc(subsystem, data) {
    let markdown = `# ${subsystem.toUpperCase()} - ${data.description}\n\n`;
    markdown += `Generated on: ${new Date().toISOString()}\n\n`;
    
    markdown += '## Overview\n\n';
    markdown += `- **Programs:** ${data.programs.length}\n`;
    markdown += `- **Copybooks:** ${data.copybooks.length}\n\n`;
    
    if (data.programs.length > 0) {
        markdown += '## Programs\n\n';
        
        for (const prog of data.programs.sort((a, b) => a.sourceFile.localeCompare(b.sourceFile))) {
            const name = path.basename(prog.sourceFile);
            const s = prog.structure;
            
            markdown += `### ${name}\n\n`;
            markdown += `- **Path:** ${prog.sourceFile}\n`;
            markdown += `- **Program ID:** ${s.programId || 'Not specified'}\n`;
            markdown += `- **Divisions:** ${s.divisions.length}\n`;
            markdown += `- **Sections:** ${s.sections.length}\n`;
            markdown += `- **Paragraphs:** ${s.paragraphs.length}\n`;
            
            if (s.callStatements.length > 0) {
                markdown += `- **CALL statements:** ${s.callStatements.join(', ')}\n`;
            }
            
            if (s.copyStatements.length > 0) {
                markdown += `- **COPY statements:** ${s.copyStatements.join(', ')}\n`;
            }
            
            markdown += '\n';
        }
    }
    
    await fs.writeFile(path.join(OUTPUT_DIR, `${subsystem}-documentation.md`), markdown);
}

function generateHTMLDoc(markdown) {
    // Simple markdown to HTML conversion
    const html = markdown
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^#### (.*$)/gim, '<h4>$1</h4>')
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/\*([^*]+)\*/g, '<em>$1</em>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
        .replace(/^- (.*$)/gim, '<li>$1</li>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/```([^`]*)```/g, '<pre><code>$1</code></pre>')
        .replace(/\|([^|]+)\|/g, '<td>$1</td>')
        .replace(/<td>-+<\/td>/g, '');
    
    return `<!DOCTYPE html>
<html>
<head>
    <title>ACAS COBOL System Documentation</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2, h3, h4 {
            color: #2c3e50;
        }
        h1 {
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            border-bottom: 1px solid #ecf0f1;
            padding-bottom: 5px;
            margin-top: 30px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .toc {
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }
        .toc h2 {
            margin-top: 0;
            border: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <p>${html}</p>
    </div>
</body>
</html>`;
}

function getSubsystem(filePath) {
    if (filePath.includes('irs/')) return 'irs';
    if (filePath.includes('sales/')) return 'sales';
    if (filePath.includes('purchase/')) return 'purchase';
    if (filePath.includes('stock/')) return 'stock';
    if (filePath.includes('general/')) return 'general';
    if (filePath.includes('copybooks/')) return 'common';
    return 'common';
}

// Run if called directly
if (require.main === module) {
    generateDocumentation().catch(console.error);
}

module.exports = { generateDocumentation };