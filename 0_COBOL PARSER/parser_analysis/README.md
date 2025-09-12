# COBOL Parser Analysis Suite

This suite provides comprehensive visualization, documentation, and analysis tools for the parsed COBOL project.

## Features

### 1. Code Visualization
- **Call Graph**: Interactive network visualization showing program dependencies
- **Flowcharts**: Procedure flow diagrams for each COBOL program
- **Dependency Maps**: Visual representation of COPYBOOK usage

### 2. Automated Documentation
- Complete system documentation in Markdown and HTML
- Subsystem-specific documentation
- Program and copybook indexes
- Dependency analysis reports

### 3. Metrics Dashboard
- Interactive web dashboard with real-time metrics
- Complexity analysis (Cyclomatic, Halstead)
- Maintainability index calculations
- SQLite database for metrics storage
- Visual charts using Plotly and D3.js

## Installation

```bash
cd parser_analysis
npm install
```

## Usage

### Run All Analysis (Recommended)

```bash
npm run all
```

This will execute all analysis steps in sequence.

### Run Individual Components

```bash
# Generate call graph visualization
npm run generate-callgraph

# Generate procedure flowcharts
npm run generate-flowcharts

# Generate documentation
npm run generate-docs

# Analyze metrics and populate database
npm run analyze-metrics

# Build dashboard
npm run build-dashboard

# Start dashboard server
npm run start-dashboard
```

## Output Structure

```
parser_analysis/
├── visualizations/
│   ├── call-graph.html         # Interactive call graph
│   ├── call-graph.dot          # DOT format for Graphviz
│   ├── call-graph-data.json    # Raw graph data
│   └── flowcharts/
│       ├── index.html          # Flowchart index
│       └── *-flowchart.html    # Individual program flowcharts
│
├── docs/
│   ├── index.html              # Main documentation (HTML)
│   ├── COBOL-Documentation.md  # Main documentation (Markdown)
│   └── *-documentation.md      # Subsystem docs
│
└── dashboard/
    ├── index.html              # Dashboard interface
    ├── server.js               # Express server
    ├── data/
    │   ├── metrics.db          # SQLite database
    │   ├── metrics.json        # Metrics data
    │   └── metrics-report.md   # Metrics summary
    └── static/
        ├── dashboard.js        # Dashboard logic
        └── dashboard.css       # Dashboard styles
```

## Viewing Results

### Call Graph
Open `visualizations/call-graph.html` in a web browser. Click and drag to pan, scroll to zoom.

### Flowcharts
Open `visualizations/flowcharts/index.html` to see all available flowcharts.

### Documentation
Open `docs/index.html` for formatted documentation or view the Markdown files directly.

### Dashboard
```bash
npm run start-dashboard
```
Then open http://localhost:3000 in your browser.

## Metrics Explained

### Cyclomatic Complexity
Measures the number of linearly independent paths through the program. Higher values indicate more complex code.

### Halstead Metrics
- **Volume**: Program size based on operators and operands
- **Difficulty**: How hard the program is to understand
- **Effort**: Mental effort required to develop/maintain

### Maintainability Index
A composite metric (0-100) indicating how maintainable the code is:
- 0-20: Low maintainability
- 20-40: Moderate maintainability  
- 40-60: Good maintainability
- 60-80: High maintainability
- 80-100: Excellent maintainability

## Database Schema

The SQLite database contains two main tables:

### metrics
- Program-level metrics (complexity, size, dependencies)
- One row per COBOL file

### dependencies
- Dependency relationships (CALL, COPY)
- Source and target files

## Customization

### Adding New Metrics
Edit `scripts/analyze-metrics.js` to add new metric calculations.

### Changing Visualizations
- Call graph: Edit `scripts/generate-callgraph.js`
- Flowcharts: Edit `scripts/generate-flowcharts.js`
- Dashboard charts: Edit `scripts/build-dashboard.js`

### Extending Documentation
Edit `scripts/generate-documentation.js` to add new sections or analysis.