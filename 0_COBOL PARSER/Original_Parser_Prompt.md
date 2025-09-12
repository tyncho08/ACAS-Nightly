# Original Parser Prompt

This prompt was used to create the initial COBOL parser for the ACAS project.

## Prompt:

Create a Node.js-based COBOL parser that can process the ACAS (Applewood Computers Accounting System) codebase. The parser should:

1. **File Discovery**
   - Find all COBOL source files (.cbl, .cpy, .CPY extensions)
   - Process files across all subdirectories (common/, sales/, purchase/, stock/, general/, irs/, copybooks/)
   - Handle both programs and copybooks

2. **Structure Extraction**
   - Extract program identification
   - Parse divisions (IDENTIFICATION, ENVIRONMENT, DATA, PROCEDURE)
   - Identify sections and paragraphs
   - Extract CALL statements to map program dependencies
   - Extract COPY statements to track copybook usage
   - Identify PERFORM statements for flow analysis
   - Parse file descriptions (SELECT, FD)
   - Extract data definitions

3. **Output Format**
   - Generate individual JSON files for each COBOL source
   - Create a parsing summary with statistics
   - Use a naming convention that preserves the source path (e.g., sales_sl000.cbl.json)
   - Include parse timestamps and file metadata

4. **Error Handling**
   - Continue parsing even if individual files fail
   - Log all errors to the summary
   - Provide detailed error information for debugging

5. **Performance**
   - Use efficient pattern matching rather than full AST parsing
   - Process files sequentially to avoid memory issues
   - Provide progress feedback during parsing

## Implementation Requirements:

- Use the cobol-parsers npm package or similar
- Create these main scripts:
  - parse-cobol-simple.js - Main parser
  - analyze-structures.js - Analysis tool
  - test-parser.js - Single file test utility
- Include proper package.json with npm scripts
- Generate clean, structured JSON output

The parser should be robust enough to handle various COBOL dialects and coding styles found in legacy systems.