const fs = require('fs-extra');
const path = require('path');
const glob = require('glob');

// Configuration
const PROJECT_ROOT = path.join(__dirname, '..');
const OUTPUT_DIR = path.join(__dirname, 'parsed-structures');
const COBOL_PATTERNS = ['**/*.cbl', '**/*.cpy'];
const EXCLUDE_PATTERNS = ['**/node_modules/**', '**/0_COBOL PARSER/**'];

// Statistics
let stats = {
    totalFiles: 0,
    successfullyParsed: 0,
    failedToParse: 0,
    errors: []
};

// Function to extract COBOL structure without full AST
function extractStructure(content) {
    const lines = content.split('\n');
    const structure = {
        programId: null,
        divisions: [],
        sections: [],
        paragraphs: [],
        copyStatements: [],
        callStatements: [],
        fileDescriptions: [],
        performStatements: [],
        dataItems: [],
        workingStorage: []
    };
    
    let inWorkingStorage = false;
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmedLine = line.trim();
        const upperLine = trimmedLine.toUpperCase();
        
        // Skip comments
        if (line.match(/^\s*\*/) || upperLine.startsWith('*>')) continue;
        
        // Extract PROGRAM-ID
        if (upperLine.includes('PROGRAM-ID')) {
            const nextLine = i + 1 < lines.length ? lines[i + 1].trim() : '';
            const match = nextLine.match(/^\s*([A-Za-z0-9-]+)/);
            if (match) {
                structure.programId = match[1];
            }
        }
        
        // Extract divisions
        if (upperLine.match(/^\s*(IDENTIFICATION|ENVIRONMENT|DATA|PROCEDURE)\s+DIVISION/)) {
            structure.divisions.push(trimmedLine);
            inWorkingStorage = upperLine.includes('DATA DIVISION');
        }
        
        // Extract sections
        if (upperLine.match(/^\s*[A-Z0-9-]+\s+SECTION\s*\.?$/)) {
            structure.sections.push(trimmedLine);
            if (upperLine.includes('WORKING-STORAGE')) {
                inWorkingStorage = true;
            } else if (upperLine.includes('LINKAGE') || upperLine.includes('PROCEDURE')) {
                inWorkingStorage = false;
            }
        }
        
        // Extract paragraphs
        if (upperLine.match(/^[A-Z0-9-]+\s*\.$/) && 
            !upperLine.includes('DIVISION') && 
            !upperLine.includes('SECTION') &&
            !upperLine.match(/^\s*(01|05|10|15|20|25|30|35|40|45|50|55|60|65|70|75|77|78|88)/)) {
            structure.paragraphs.push(trimmedLine.replace('.', '').trim());
        }
        
        // Extract COPY statements
        if (upperLine.includes(' COPY ') || upperLine.match(/^\s*COPY\s+/)) {
            // Handle various COPY formats
            let match = upperLine.match(/COPY\s+["']([A-Za-z0-9-]+)["']/);
            if (!match) {
                match = upperLine.match(/COPY\s+([A-Za-z0-9-]+)/);
            }
            if (match) {
                structure.copyStatements.push(match[1]);
            }
        }
        
        // Extract CALL statements
        if (upperLine.includes(' CALL ') || upperLine.match(/^\s*CALL\s+/)) {
            // Try different CALL patterns
            let match = upperLine.match(/CALL\s+["']([A-Za-z0-9-]+)["']/);
            if (!match) {
                match = upperLine.match(/CALL\s+([A-Za-z0-9-]+)/);
            }
            if (match && match[1] !== 'USING') {
                structure.callStatements.push(match[1]);
            }
        }
        
        // Extract PERFORM statements
        if (upperLine.includes(' PERFORM ')) {
            const match = upperLine.match(/PERFORM\s+([A-Za-z0-9-]+)/);
            if (match) {
                structure.performStatements.push(match[1]);
            }
        }
        
        // Extract file descriptions
        if (upperLine.match(/^\s*FD\s+/)) {
            const match = upperLine.match(/FD\s+([A-Za-z0-9-]+)/);
            if (match) {
                structure.fileDescriptions.push(match[1]);
            }
        }
        
        // Extract SELECT statements
        if (upperLine.match(/^\s*SELECT\s+/)) {
            const match = upperLine.match(/SELECT\s+([A-Za-z0-9-]+)/);
            if (match) {
                structure.fileDescriptions.push(`SELECT ${match[1]}`);
            }
        }
        
        // Extract data items (01 level items)
        if (upperLine.match(/^\s*01\s+/)) {
            const match = upperLine.match(/01\s+([A-Za-z0-9-]+)/);
            if (match) {
                structure.dataItems.push(match[1]);
                if (inWorkingStorage) {
                    structure.workingStorage.push(match[1]);
                }
            }
        }
    }
    
    // Remove duplicates
    structure.copyStatements = [...new Set(structure.copyStatements)];
    structure.callStatements = [...new Set(structure.callStatements)];
    structure.performStatements = [...new Set(structure.performStatements)];
    structure.dataItems = [...new Set(structure.dataItems)];
    structure.workingStorage = [...new Set(structure.workingStorage)];
    
    return structure;
}

// Function to parse a single COBOL file
async function parseCobolFile(filePath) {
    try {
        console.log(`Parsing: ${filePath}`);
        const content = await fs.readFile(filePath, 'utf8');
        
        // Extract structure
        const structure = extractStructure(content);
        
        // Generate output filename
        const relativePath = path.relative(PROJECT_ROOT, filePath);
        const outputFileName = relativePath.replace(/[\/\\]/g, '_') + '.json';
        const outputPath = path.join(OUTPUT_DIR, outputFileName);
        
        // Save structure to JSON
        await fs.writeJson(outputPath, {
            sourceFile: relativePath,
            absolutePath: filePath,
            parseTimestamp: new Date().toISOString(),
            fileType: filePath.endsWith('.cpy') ? 'copybook' : 'program',
            structure: structure,
            stats: {
                lines: content.split('\n').length,
                size: content.length
            }
        }, { spaces: 2 });
        
        stats.successfullyParsed++;
        console.log(`✓ Saved structure to: ${outputFileName}`);
        
    } catch (error) {
        stats.failedToParse++;
        stats.errors.push({
            file: filePath,
            error: error.message
        });
        console.error(`✗ Failed to parse ${filePath}: ${error.message}`);
    }
}

// Main function
async function main() {
    console.log('ACAS COBOL Parser (Simplified)');
    console.log('==============================\n');
    
    // Ensure output directory exists
    await fs.ensureDir(OUTPUT_DIR);
    
    // Find all COBOL files
    const cobolFiles = [];
    
    for (const pattern of COBOL_PATTERNS) {
        const files = glob.sync(pattern, {
            cwd: PROJECT_ROOT,
            absolute: true,
            ignore: EXCLUDE_PATTERNS
        });
        cobolFiles.push(...files);
    }
    
    // Remove duplicates
    const uniqueFiles = [...new Set(cobolFiles)];
    stats.totalFiles = uniqueFiles.length;
    
    console.log(`Found ${stats.totalFiles} COBOL files to parse\n`);
    
    // Parse each file
    for (const file of uniqueFiles) {
        await parseCobolFile(file);
    }
    
    // Generate summary report
    const summaryReport = {
        timestamp: new Date().toISOString(),
        statistics: stats,
        fileList: uniqueFiles.map(f => path.relative(PROJECT_ROOT, f))
    };
    
    await fs.writeJson(path.join(OUTPUT_DIR, 'parsing-summary.json'), summaryReport, { spaces: 2 });
    
    // Print summary
    console.log('\n==============================');
    console.log('Parsing Summary:');
    console.log(`Total files: ${stats.totalFiles}`);
    console.log(`Successfully parsed: ${stats.successfullyParsed}`);
    console.log(`Failed to parse: ${stats.failedToParse}`);
    
    if (stats.errors.length > 0) {
        console.log('\nErrors:');
        stats.errors.forEach(err => {
            console.log(`- ${err.file}: ${err.error}`);
        });
    }
}

// Run the parser
main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
});