const { generateCallGraph } = require('./scripts/generate-callgraph');
const { generateFlowcharts } = require('./scripts/generate-flowcharts');
const { generateDocumentation } = require('./scripts/generate-documentation');
const { analyzeMetrics } = require('./scripts/analyze-metrics');
const { buildDashboard } = require('./scripts/build-dashboard');

async function runAll() {
    console.log('=================================');
    console.log('COBOL Parser Analysis Suite');
    console.log('=================================\n');
    
    try {
        console.log('Step 1/5: Generating Call Graph...');
        await generateCallGraph();
        console.log('\n');
        
        console.log('Step 2/5: Generating Flowcharts...');
        await generateFlowcharts();
        console.log('\n');
        
        console.log('Step 3/5: Generating Documentation...');
        await generateDocumentation();
        console.log('\n');
        
        console.log('Step 4/5: Analyzing Metrics...');
        await analyzeMetrics();
        console.log('\n');
        
        console.log('Step 5/5: Building Dashboard...');
        await buildDashboard();
        console.log('\n');
        
        console.log('=================================');
        console.log('✅ All tasks completed successfully!');
        console.log('=================================\n');
        
        console.log('📊 View outputs:');
        console.log('   - Call Graph: parser_analysis/visualizations/call-graph.html');
        console.log('   - Flowcharts: parser_analysis/visualizations/flowcharts/index.html');
        console.log('   - Documentation: parser_analysis/docs/index.html');
        console.log('   - Dashboard: parser_analysis/dashboard/index.html');
        console.log('\nTo start the dashboard server: npm run start-dashboard');
        
    } catch (error) {
        console.error('❌ Error:', error);
        process.exit(1);
    }
}

// Run all tasks
runAll();