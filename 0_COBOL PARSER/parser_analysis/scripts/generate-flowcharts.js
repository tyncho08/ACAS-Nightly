const fs = require('fs-extra');
const path = require('path');
const glob = require('glob');

// Paths
const PARSED_DIR = path.join(__dirname, '../../parsed-structures');
const OUTPUT_DIR = path.join(__dirname, '../visualizations/flowcharts');

// Ensure output directory exists
fs.ensureDirSync(OUTPUT_DIR);

async function generateFlowcharts() {
    console.log('Generating COBOL Procedure Flowcharts...\n');
    
    // Load all parsed JSON files
    const jsonFiles = glob.sync('*.json', { cwd: PARSED_DIR });
    
    // Process main programs (not copybooks)
    const programs = [];
    for (const file of jsonFiles) {
        const data = await fs.readJson(path.join(PARSED_DIR, file));
        if (data.fileType === 'program' && data.structure.paragraphs.length > 0) {
            programs.push(data);
        }
    }
    
    console.log(`Found ${programs.length} programs with procedures to visualize.`);
    
    // Generate flowchart for each program
    for (const program of programs.slice(0, 10)) { // Limit to first 10 for demo
        await generateProgramFlowchart(program);
    }
    
    // Generate index HTML
    await generateFlowchartIndex(programs.slice(0, 10));
    
    console.log(`\n✓ Flowcharts generated in: ${OUTPUT_DIR}`);
}

async function generateProgramFlowchart(programData) {
    const programName = path.basename(programData.sourceFile, path.extname(programData.sourceFile));
    const structure = programData.structure;
    
    // Build Mermaid flowchart
    let mermaid = 'graph TD\n';
    mermaid += '    Start([Start])\n';
    
    // Add divisions
    if (structure.divisions.length > 0) {
        mermaid += '    Start --> Divisions\n';
        mermaid += `    Divisions[/"${structure.divisions.length} Divisions"\\]\n`;
    }
    
    // Add sections as subgraphs
    const sectionMap = new Map();
    structure.sections.forEach((section, idx) => {
        const sectionId = `Section${idx}`;
        sectionMap.set(section, sectionId);
        mermaid += `    ${sectionId}["${section}"]\n`;
    });
    
    // Add paragraphs
    const paragraphMap = new Map();
    structure.paragraphs.forEach((para, idx) => {
        const paraId = `Para${idx}`;
        paragraphMap.set(para, paraId);
        mermaid += `    ${paraId}("${para}")\n`;
    });
    
    // Add PERFORM relationships
    if (structure.performStatements.length > 0) {
        mermaid += '    %% PERFORM relationships\n';
        structure.performStatements.forEach((perform, idx) => {
            const targetPara = paragraphMap.get(perform);
            if (targetPara) {
                mermaid += `    Para0 -.->|PERFORM| ${targetPara}\n`;
            }
        });
    }
    
    // Add CALL relationships
    if (structure.callStatements.length > 0) {
        mermaid += '    %% External CALL relationships\n';
        structure.callStatements.forEach((call, idx) => {
            const callId = `Call${idx}`;
            mermaid += `    ${callId}[["${call}"]]\n`;
            if (paragraphMap.size > 0) {
                mermaid += `    Para0 ==>|CALL| ${callId}\n`;
            }
        });
    }
    
    // Add file operations
    if (structure.fileDescriptions.length > 0) {
        mermaid += '    %% File operations\n';
        structure.fileDescriptions.forEach((file, idx) => {
            const fileId = `File${idx}`;
            mermaid += `    ${fileId}[("${file}")]\n`;
        });
    }
    
    mermaid += '    End([End])\n';
    
    // Generate HTML with Mermaid
    const htmlContent = `<!DOCTYPE html>
<html>
<head>
    <title>Flowchart: ${programName}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        .info {
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .mermaid {
            text-align: center;
            background-color: #fafafa;
            padding: 20px;
            border-radius: 5px;
        }
        .legend {
            margin-top: 20px;
            padding: 15px;
            background-color: #f0f0f0;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Flowchart: ${programName}</h1>
        
        <div class="info">
            <strong>Source:</strong> ${programData.sourceFile}<br>
            <strong>Divisions:</strong> ${structure.divisions.length}<br>
            <strong>Sections:</strong> ${structure.sections.length}<br>
            <strong>Paragraphs:</strong> ${structure.paragraphs.length}<br>
            <strong>PERFORM statements:</strong> ${structure.performStatements.length}<br>
            <strong>CALL statements:</strong> ${structure.callStatements.length}<br>
            <strong>File operations:</strong> ${structure.fileDescriptions.length}
        </div>
        
        <div class="mermaid">
${mermaid}
        </div>
        
        <div class="legend">
            <h3>Legend</h3>
            <ul>
                <li><strong>Rounded rectangles:</strong> Start/End points</li>
                <li><strong>Rectangles:</strong> Sections and divisions</li>
                <li><strong>Rounded rectangles with parentheses:</strong> Paragraphs</li>
                <li><strong>Double-bordered rectangles:</strong> External CALL targets</li>
                <li><strong>Cylinders:</strong> File operations</li>
                <li><strong>Dashed arrows:</strong> PERFORM relationships</li>
                <li><strong>Thick arrows:</strong> CALL relationships</li>
            </ul>
        </div>
    </div>
    
    <script>
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }
        });
    </script>
</body>
</html>`;
    
    const filename = `${programName}-flowchart.html`;
    await fs.writeFile(path.join(OUTPUT_DIR, filename), htmlContent);
    console.log(`  - Generated: ${filename}`);
}

async function generateFlowchartIndex(programs) {
    const indexHtml = `<!DOCTYPE html>
<html>
<head>
    <title>COBOL Flowchart Index</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        .program-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .program-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            background-color: #fafafa;
            transition: transform 0.2s;
        }
        .program-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .program-card h3 {
            margin-top: 0;
            color: #4CAF50;
        }
        .program-card a {
            display: inline-block;
            margin-top: 10px;
            padding: 8px 15px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 3px;
        }
        .program-card a:hover {
            background-color: #45a049;
        }
        .stats {
            font-size: 0.9em;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>COBOL Program Flowcharts</h1>
        <p>Generated flowcharts for COBOL programs showing procedure flow, PERFORM statements, and external CALL relationships.</p>
        
        <div class="program-grid">
            ${programs.map(program => {
                const name = path.basename(program.sourceFile, path.extname(program.sourceFile));
                const structure = program.structure;
                return `
                <div class="program-card">
                    <h3>${name}</h3>
                    <div class="stats">
                        <strong>Source:</strong> ${program.sourceFile}<br>
                        <strong>Procedures:</strong> ${structure.paragraphs.length}<br>
                        <strong>PERFORM:</strong> ${structure.performStatements.length}<br>
                        <strong>CALL:</strong> ${structure.callStatements.length}
                    </div>
                    <a href="${name}-flowchart.html">View Flowchart</a>
                </div>`;
            }).join('')}
        </div>
    </div>
</body>
</html>`;
    
    await fs.writeFile(path.join(OUTPUT_DIR, 'index.html'), indexHtml);
}

// Run if called directly
if (require.main === module) {
    generateFlowcharts().catch(console.error);
}

module.exports = { generateFlowcharts };