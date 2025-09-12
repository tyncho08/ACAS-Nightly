const fs = require('fs-extra');
const path = require('path');
const CobolParser = require('cobol-parsers');

// Test file - let's use a simple COBOL file
const TEST_FILE = path.join(__dirname, '..', 'common', 'ACAS.cbl');

// Function to extract basic COBOL structure
function extractStructure(content) {
    const lines = content.split('\n');
    const structure = {
        programId: null,
        divisions: [],
        sections: [],
        paragraphs: [],
        copyStatements: [],
        callStatements: [],
        fileDescriptions: []
    };
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim().toUpperCase();
        
        // Extract PROGRAM-ID
        if (line.includes('PROGRAM-ID')) {
            const nextLine = i + 1 < lines.length ? lines[i + 1].trim() : '';
            const match = nextLine.match(/^\s*([A-Z0-9-]+)/);
            if (match) {
                structure.programId = match[1];
            }
        }
        
        // Extract divisions
        if (line.match(/^\s*(IDENTIFICATION|ENVIRONMENT|DATA|PROCEDURE)\s+DIVISION/)) {
            structure.divisions.push(line.trim());
        }
        
        // Extract sections
        if (line.match(/^\s*[A-Z0-9-]+\s+SECTION\s*\.?$/)) {
            structure.sections.push(line.trim());
        }
        
        // Extract paragraphs (simple heuristic)
        if (line.match(/^[A-Z0-9-]+\s*\.$/) && !line.includes('DIVISION') && !line.includes('SECTION')) {
            structure.paragraphs.push(line.replace('.', '').trim());
        }
        
        // Extract COPY statements
        if (line.includes('COPY ')) {
            const match = line.match(/COPY\s+([A-Z0-9-]+)/);
            if (match) {
                structure.copyStatements.push(match[1]);
            }
        }
        
        // Extract CALL statements
        if (line.includes('CALL ')) {
            const match = line.match(/CALL\s+["']([A-Z0-9-]+)["']/);
            if (match) {
                structure.callStatements.push(match[1]);
            }
        }
        
        // Extract file descriptions
        if (line.match(/^\s*FD\s+/)) {
            const match = line.match(/FD\s+([A-Z0-9-]+)/);
            if (match) {
                structure.fileDescriptions.push(match[1]);
            }
        }
    }
    
    return structure;
}

async function testParser() {
    console.log('Testing COBOL Parser');
    console.log('===================\n');
    
    try {
        // Check if test file exists
        if (!await fs.pathExists(TEST_FILE)) {
            console.error(`Test file not found: ${TEST_FILE}`);
            return;
        }
        
        console.log(`Testing with file: ${TEST_FILE}`);
        
        // Read the file
        const content = await fs.readFile(TEST_FILE, 'utf8');
        console.log(`File size: ${content.length} bytes`);
        
        // Extract structure
        console.log('\nExtracting structure...');
        const structure = extractStructure(content);
        console.log(`Program ID: ${structure.programId || 'Not found'}`);
        console.log(`Divisions: ${structure.divisions.length}`);
        console.log(`Sections: ${structure.sections.length}`);
        console.log(`Copy statements: ${structure.copyStatements.length}`);
        console.log(`Call statements: ${structure.callStatements.length}`);
        
        // Parse the COBOL content
        console.log('\nParsing with cobol-parsers...');
        let ast;
        
        try {
            // Determine if it's a program or copybook
            const isCopybook = TEST_FILE.endsWith('.cpy');
            ast = isCopybook ? CobolParser.copybook.parse(content) : CobolParser.program.parse(content);
            console.log('✓ Successfully parsed!');
        } catch (parseError) {
            console.log('✗ Parser failed, but structure extraction succeeded');
            ast = { error: parseError.message };
        }
        
        // Save test result
        const outputPath = path.join(__dirname, 'test-result.json');
        await fs.writeJson(outputPath, {
            testFile: TEST_FILE,
            parseTimestamp: new Date().toISOString(),
            structure: structure,
            ast: ast
        }, { spaces: 2 });
        
        console.log(`\n✓ Results saved to: test-result.json`);
        
        if (structure.divisions.length > 0) {
            console.log('\nFound divisions:');
            structure.divisions.forEach(d => console.log(`  - ${d}`));
        }
        
        if (structure.copyStatements.length > 0) {
            console.log('\nFound COPY statements:');
            structure.copyStatements.forEach(c => console.log(`  - ${c}`));
        }
        
        if (structure.callStatements.length > 0) {
            console.log('\nFound CALL statements:');
            structure.callStatements.forEach(c => console.log(`  - ${c}`));
        }
        
    } catch (error) {
        console.error('\n✗ Test failed:');
        console.error(error);
    }
}

// Run the test
testParser();