# Original Analysis Prompt

This prompt was used to create the advanced analysis suite for the COBOL parser.

## Prompt:

Create a comprehensive analysis and visualization suite for the parsed COBOL structures. The suite should include:

1. **Code Visualization**
   - Call graph showing program dependencies
   - Flowcharts for procedure flow
   - Dependency maps for COPYBOOK usage

2. **Automated Documentation**
   - System-level documentation
   - Subsystem-specific documentation
   - Program and copybook indexes
   - Dependency analysis reports

3. **Metrics Dashboard**
   - Interactive web dashboard
   - Complexity analysis (Cyclomatic, Halstead)
   - Maintainability index calculations
   - Visual charts and graphs

4. **Database Storage**
   - SQLite database for metrics
   - Queryable structure for custom analysis
   - Dependency relationships tracking

The analysis should work with the existing parsed JSON structures in the parsed-structures/ directory and generate outputs in a new parser_analysis/ directory.

## Expected Outputs:

- visualizations/ - Interactive graphs and charts
- docs/ - Generated documentation
- dashboard/ - Web-based metrics dashboard
- scripts/ - Individual analysis scripts
- package.json - Dependencies and run scripts

All tools should be runnable individually or as a complete suite using npm scripts.