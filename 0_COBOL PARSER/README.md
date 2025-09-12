# ACAS COBOL Parser and Analysis Suite

A comprehensive Node.js-based COBOL parser and analysis toolkit for the ACAS (Applewood Computers Accounting System) project.

## Overview

This suite provides powerful tools to parse, analyze, and visualize the ACAS COBOL codebase, which consists of 288 COBOL source files across multiple subsystems. The parser extracts structural information from COBOL programs and copybooks, while the analysis tools generate insights, documentation, and visualizations.

## Features

### Core Parser
- **100% Success Rate**: Successfully parses all 288 COBOL files without errors
- **Structural Extraction**: Extracts programs, divisions, sections, paragraphs, CALL statements, COPY statements, and file descriptions
- **JSON Output**: Generates structured JSON representations for each COBOL file
- **Pattern-Based**: Uses efficient pattern matching rather than full AST parsing

### Analysis Tools
- **System Overview**: Analyzes program dependencies and system architecture
- **Call Graph Generation**: Maps program-to-program relationships
- **Subsystem Analysis**: Breaks down code by functional areas (IRS, Sales, Purchase, Stock, General, Common)
- **DAL Pattern Recognition**: Identifies Data Access Layer modules (MT, LD, UNL, RES)
- **Unused Resource Detection**: Finds unused copybooks and resources

### Advanced Visualization (parser_analysis)
- **Interactive Call Graph**: Network visualization of program dependencies
- **Procedure Flowcharts**: Visual representation of program flow
- **Metrics Dashboard**: Complexity and maintainability analysis
- **Documentation Generator**: Auto-generates system documentation

## System Structure

### Analyzed Codebase Statistics
- **Total Files**: 288 (279 programs, 9 copybooks)
- **Subsystems**:
  - IRS (Internal Revenue): 16 programs
  - Sales Ledger: 37 programs
  - Purchase Ledger: 38 programs
  - Stock Control: 12 programs
  - General Ledger: 18 programs
  - Common/Shared: 158 programs

### Data Access Layer Architecture
The system uses a consistent DAL pattern:
- **MT modules** (34): Main Table access - handles both COBOL files and RDBMS
- **LD modules** (28): Load data from COBOL to RDBMS
- **UNL modules** (25): Unload data from RDBMS to COBOL
- **RES modules** (25): Reserve/restore operations

### Main Entry Points
- `ACAS.cbl` - Main system menu
- `irs.cbl` - IRS subsystem menu
- `sales.cbl` - Sales subsystem menu
- `purchase.cbl` - Purchase subsystem menu
- `stock.cbl` - Stock subsystem menu
- `general.cbl` - General Ledger menu

## Installation

```bash
# Install dependencies for the main parser
npm install

# Install dependencies for advanced analysis tools
cd parser_analysis
npm install
cd ..
```

## Usage

### Basic Parsing and Analysis

1. **Parse all COBOL files**:
   ```bash
   npm start
   # or
   node parse-cobol-simple.js
   ```

2. **Analyze parsed structures**:
   ```bash
   npm run analyze
   # or
   node analyze-structures.js
   ```

3. **Test parser on single file**:
   ```bash
   npm test
   # or
   node test-parser.js
   ```

### Advanced Analysis (parser_analysis)

Run all analysis tools:
```bash
cd parser_analysis
npm run all
```

Or run individual components:
```bash
# Generate interactive call graph
npm run generate-callgraph

# Generate procedure flowcharts
npm run generate-flowcharts

# Generate documentation
npm run generate-docs

# Analyze code metrics
npm run analyze-metrics

# Build metrics dashboard
npm run build-dashboard

# Start dashboard server
npm run start-dashboard
```

## Output Files

### Basic Parser Output
```
0_COBOL PARSER/
├── parsed-structures/      # JSON files for each COBOL source
│   ├── common_*.json       # Common module structures
│   ├── sales_*.json        # Sales module structures
│   ├── purchase_*.json     # Purchase module structures
│   ├── stock_*.json        # Stock module structures
│   ├── general_*.json      # General ledger structures
│   ├── irs_*.json          # IRS module structures
│   └── copybooks_*.json    # Copybook structures
│
└── analysis-results/       # Analysis outputs
    ├── parsing-summary.json      # Parser statistics
    ├── structure-analysis.json   # Detailed system analysis
    ├── system-call-graph.json    # Call dependencies
    └── test-result.json          # Test output
```

### Advanced Analysis Output
```
parser_analysis/
├── visualizations/
│   ├── call-graph.html         # Interactive dependency graph
│   ├── call-graph.dot          # Graphviz format
│   └── flowcharts/             # Program flow diagrams
│
├── docs/
│   ├── index.html              # Main documentation
│   ├── COBOL-Documentation.md  # System overview
│   └── *-documentation.md      # Subsystem docs
│
└── dashboard/
    ├── index.html              # Metrics dashboard
    └── data/
        ├── metrics.db          # SQLite metrics database
        └── metrics-report.md   # Analysis summary
```

## Viewing Results

### Static Files
All HTML files can be opened directly in a web browser:
```bash
# View call graph
open visualizations/call-graph.html

# View documentation
open docs/index.html

# View dashboard
open dashboard/index.html
```

### Interactive Dashboard
For the best dashboard experience:
```bash
cd parser_analysis
npm run start-dashboard
# Then open http://localhost:3000
```

## Key Findings

### System Architecture
- The system follows a modular architecture with clear separation between subsystems
- Common modules are extensively shared across all subsystems
- Each subsystem has its own menu program and follows consistent naming conventions

### Code Organization
- Programs follow systematic naming (e.g., sl000-sl970 for sales)
- Consistent use of DAL pattern for data access abstraction
- Clear separation between business logic and data access layers

### Unused Resources
All 9 copybooks appear to be unused in the current codebase:
- FileStat-Msgs.cpy
- MySQL-SQLCA.cpy
- mysql-procedures.cpy
- mysql-procedures-2.cpy
- mysql-variables.cpy
- screenio.cpy
- selprint-2.cpy
- statcodes.cpy
- statcodes2.cpy

## Troubleshooting

### Parser Issues
- If parsing fails, check error details in `parsing-summary.json`
- Run test parser on problematic files to debug
- Ensure COBOL files follow standard syntax

### Visualization Errors
- Some advanced analysis scripts may encounter errors with certain file structures
- Basic parsing and analysis tools are more robust
- Check console output for specific error messages

## Dependencies

### Main Parser
- cobol-parsers: ^1.0.12
- fs-extra: ^11.2.0
- glob: ^10.3.10
- path: ^0.12.7

### Analysis Suite
- express: ^4.18.2 (for dashboard server)
- sqlite3: ^5.1.6 (for metrics database)

## Contributing

To extend the parser or analysis tools:

1. **Parser Enhancement**: Modify `parse-cobol-simple.js` to extract additional patterns
2. **Analysis Extension**: Update `analyze-structures.js` for new insights
3. **Visualization**: Edit scripts in `parser_analysis/scripts/` for custom visualizations
4. **Metrics**: Add new calculations to `analyze-metrics.js`

## Notes

- The parser uses pattern matching for efficiency and reliability
- File names with special characters (like underscores) are handled correctly
- The system supports both traditional COBOL indexed files and RDBMS backends
- Analysis results are cached in JSON format for quick access

## License

Part of the ACAS (Applewood Computers Accounting System) project.