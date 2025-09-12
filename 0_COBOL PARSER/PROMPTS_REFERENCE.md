# COBOL Parser Prompts Reference

This document contains useful prompts for working with the ACAS COBOL Parser.

## 1. Basic Parser Creation

```
Create a Node.js COBOL parser that extracts structural information from COBOL source files including:
- Program identification
- Divisions, sections, and paragraphs
- CALL and COPY statements
- File descriptions
- Generate JSON output for each file
```

## 2. Analysis Tool Enhancement

```
Analyze the parsed COBOL structures to:
- Map program dependencies via CALL statements
- Identify unused copybooks
- Group programs by subsystem
- Generate call graphs and system overview
- Identify Data Access Layer patterns (MT, LD, UNL, RES modules)
```

## 3. Visualization Suite

```
Create interactive visualizations for COBOL analysis:
- Network graph for program dependencies
- Flowcharts for procedure flow
- Subsystem relationship diagrams
- Export to multiple formats (HTML, DOT, SVG)
```

## 4. Metrics and Dashboard

```
Build a metrics dashboard that calculates:
- Cyclomatic complexity
- Halstead metrics (volume, difficulty, effort)
- Maintainability index
- Lines of code and comment ratios
- Store in SQLite database
- Create web interface with charts
```

## 5. Documentation Generation

```
Generate comprehensive documentation from parsed COBOL:
- System overview with statistics
- Subsystem-specific documentation
- Program inventory with descriptions
- Dependency matrices
- Unused resource reports
- Output in both Markdown and HTML
```

## 6. Testing and Validation

```
Create test utilities to:
- Validate parser output
- Test individual COBOL files
- Verify JSON structure integrity
- Check for parsing errors
- Generate parsing reports
```

## 7. Performance Optimization

```
Optimize the parser for large codebases:
- Use streaming for large files
- Implement caching mechanisms
- Parallelize where possible
- Memory-efficient processing
- Progress indicators
```

## 8. Error Recovery

```
Implement robust error handling:
- Continue parsing on errors
- Log detailed error information
- Provide recovery suggestions
- Generate error summary reports
- Handle various COBOL dialects
```

## 9. Integration Points

```
Add integration capabilities:
- Export to graph databases
- Generate PlantUML diagrams
- Create Graphviz DOT files
- Export metrics to monitoring systems
- API endpoints for querying
```

## 10. Advanced Analysis

```
Implement advanced analysis features:
- Dead code detection
- Circular dependency identification
- Complexity hotspot detection
- Change impact analysis
- Technical debt indicators
```

## Usage Tips

1. Start with the basic parser to extract structure
2. Add analysis capabilities incrementally
3. Build visualizations on top of the analysis
4. Use metrics for quality assessment
5. Generate documentation for stakeholders

## Common Patterns to Look For

- **Menu Programs**: Main entry points (ACAS.cbl, sales.cbl, etc.)
- **DAL Modules**: Data access layer (*MT.cbl, *LD.cbl, *UNL.cbl, *RES.cbl)
- **Business Logic**: Core functionality (sl*.cbl, pl*.cbl, st*.cbl, etc.)
- **Common Utilities**: Shared functions in common/ directory
- **Copybooks**: Reusable code snippets (.cpy files)

## Troubleshooting Prompts

```
Debug parser issues:
- Add verbose logging
- Test with single files first
- Check for special characters
- Validate JSON output
- Compare with expected structure
```

```
Fix visualization problems:
- Verify data format
- Check for circular references
- Test with smaller datasets
- Validate HTML/JavaScript
- Check browser console
```