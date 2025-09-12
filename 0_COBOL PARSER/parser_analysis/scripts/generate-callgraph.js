const fs = require('fs-extra');
const path = require('path');
const glob = require('glob');

// Paths
const PARSED_DIR = path.join(__dirname, '../../parsed-structures');
const OUTPUT_DIR = path.join(__dirname, '../visualizations');

// Ensure output directory exists
fs.ensureDirSync(OUTPUT_DIR);

async function generateCallGraph() {
    console.log('Generating COBOL Call Graph...\n');
    
    // Load all parsed JSON files
    const jsonFiles = glob.sync('*.json', { cwd: PARSED_DIR });
    
    // Data structures for the graph
    const nodes = new Map();
    const edges = [];
    const subsystems = {
        irs: { color: '#ff6b6b', label: 'IRS' },
        sales: { color: '#4ecdc4', label: 'Sales' },
        purchase: { color: '#45b7d1', label: 'Purchase' },
        stock: { color: '#96ceb4', label: 'Stock' },
        general: { color: '#dda15e', label: 'General' },
        common: { color: '#c9ada7', label: 'Common' }
    };
    
    // First pass: collect all valid program names
    const validPrograms = new Set();
    for (const file of jsonFiles) {
        const data = await fs.readJson(path.join(PARSED_DIR, file));
        if (!data.sourceFile) continue; // Skip if no sourceFile
        const programName = path.basename(data.sourceFile, path.extname(data.sourceFile));
        validPrograms.add(programName.toLowerCase());
    }
    
    // Second pass: process each file
    for (const file of jsonFiles) {
        const data = await fs.readJson(path.join(PARSED_DIR, file));
        if (!data.sourceFile) continue; // Skip if no sourceFile
        const programName = path.basename(data.sourceFile, path.extname(data.sourceFile));
        const subsystem = getSubsystem(data.sourceFile);
        
        // Add node
        nodes.set(programName, {
            id: programName,
            label: programName,
            group: subsystem,
            color: subsystems[subsystem]?.color || '#999999',
            shape: data.fileType === 'copybook' ? 'box' : 'circle',
            size: data.fileType === 'copybook' ? 15 : 25,
            font: { size: 12 }
        });
        
        // Add edges for CALL statements
        if (data.structure.callStatements) {
            for (const called of data.structure.callStatements) {
                const calledLower = called.toLowerCase();
                // Only add edge if the called program exists in our system
                if (validPrograms.has(calledLower)) {
                    // Find the actual program name with correct case
                    let targetProgram = calledLower;
                    for (const prog of validPrograms) {
                        if (prog.toLowerCase() === calledLower) {
                            // Find the original case from nodes
                            for (const [nodeName, nodeData] of nodes) {
                                if (nodeName.toLowerCase() === calledLower) {
                                    targetProgram = nodeName;
                                    break;
                                }
                            }
                            break;
                        }
                    }
                    
                    edges.push({
                        from: programName,
                        to: targetProgram,
                        arrows: 'to',
                        color: { color: '#666666' },
                        smooth: { type: 'curvedCW', roundness: 0.2 }
                    });
                }
            }
        }
        
        // Add edges for COPY statements (different style)
        if (data.structure.copyStatements) {
            for (const copied of data.structure.copyStatements) {
                const copiedLower = copied.toLowerCase();
                // Only add edge if the copybook exists in our system
                if (validPrograms.has(copiedLower)) {
                    // Find the actual copybook name with correct case
                    let targetCopybook = copiedLower;
                    for (const [nodeName, nodeData] of nodes) {
                        if (nodeName.toLowerCase() === copiedLower) {
                            targetCopybook = nodeName;
                            break;
                        }
                    }
                    
                    edges.push({
                        from: programName,
                        to: targetCopybook,
                        arrows: 'to',
                        dashes: true,
                        color: { color: '#999999' },
                        smooth: { type: 'curvedCW', roundness: 0.2 }
                    });
                }
            }
        }
    }
    
    // Log statistics
    console.log(`Total nodes: ${nodes.size}`);
    console.log(`Total edges: ${edges.length}`);
    console.log(`Programs with connections: ${new Set(edges.map(e => e.from)).size}`);
    
    // Generate HTML visualization
    const htmlContent = `<!DOCTYPE html>
<html>
<head>
    <title>ACAS COBOL Call Graph</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        #mynetwork {
            width: 100%;
            height: 90vh;
            border: 1px solid lightgray;
        }
        .legend {
            position: absolute;
            top: 10px;
            right: 10px;
            background: white;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
        }
        .legend-item {
            margin: 5px 0;
        }
        .legend-color {
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 5px;
            vertical-align: middle;
            border-radius: 50%;
        }
        .info {
            height: 10vh;
            padding: 10px;
            background: #f0f0f0;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div id="mynetwork"></div>
    <div class="legend">
        <h3>Subsystems</h3>
        ${Object.entries(subsystems).map(([key, value]) => 
            `<div class="legend-item">
                <span class="legend-color" style="background-color: ${value.color}"></span>
                ${value.label}
            </div>`
        ).join('')}
        <hr>
        <div class="legend-item">
            <span style="display: inline-block; width: 20px; height: 20px; margin-right: 5px; border: 2px solid #666; border-radius: 50%;"></span>
            Program
        </div>
        <div class="legend-item">
            <span style="display: inline-block; width: 20px; height: 20px; margin-right: 5px; border: 2px solid #666;"></span>
            Copybook
        </div>
        <div class="legend-item">
            <span style="display: inline-block; width: 30px; border-bottom: 2px solid #666; margin-right: 5px;"></span>
            CALL
        </div>
        <div class="legend-item">
            <span style="display: inline-block; width: 30px; border-bottom: 2px dashed #999; margin-right: 5px;"></span>
            COPY
        </div>
    </div>
    <div class="info">
        <strong>Instructions:</strong> Click and drag to pan, scroll to zoom. Click on nodes to highlight connections.
        <br><strong>Total Programs:</strong> ${Array.from(nodes.values()).filter(n => n.shape === 'circle').length}
        <strong>| Total Copybooks:</strong> ${Array.from(nodes.values()).filter(n => n.shape === 'box').length}
        <strong>| Total Connections:</strong> ${edges.length}
    </div>

    <script type="text/javascript">
        // Create the data
        var nodes = new vis.DataSet(${JSON.stringify(Array.from(nodes.values()))});
        var edges = new vis.DataSet(${JSON.stringify(edges)});

        // Create the network
        var container = document.getElementById('mynetwork');
        var data = {
            nodes: nodes,
            edges: edges
        };
        
        var options = {
            physics: {
                stabilization: {
                    enabled: true,
                    iterations: 1000,
                    updateInterval: 25
                },
                barnesHut: {
                    gravitationalConstant: -5000,
                    centralGravity: 0.3,
                    springLength: 200,
                    springConstant: 0.04,
                    damping: 0.09
                }
            },
            interaction: {
                hover: true,
                tooltipDelay: 200,
                hideEdgesOnDrag: true
            },
            nodes: {
                borderWidth: 2,
                borderWidthSelected: 4
            }
        };
        
        var network = new vis.Network(container, data, options);
        
        // Add click handler
        network.on("click", function(params) {
            if (params.nodes.length > 0) {
                var nodeId = params.nodes[0];
                var connectedNodes = network.getConnectedNodes(nodeId);
                var allNodes = nodes.get();
                
                // Create a map to preserve original colors
                var originalColors = {};
                allNodes.forEach(function(node) {
                    originalColors[node.id] = subsystems[node.group] ? subsystems[node.group].color : '#999999';
                });
                
                // Update node colors
                allNodes.forEach(function(node) {
                    if (node.id === nodeId) {
                        node.color = '#ff0000';
                    } else if (connectedNodes.includes(node.id)) {
                        node.color = '#ffa500';
                    } else {
                        node.color = originalColors[node.id];
                    }
                });
                
                nodes.update(allNodes);
            }
        });
    </script>
</body>
</html>`;
    
    await fs.writeFile(path.join(OUTPUT_DIR, 'call-graph.html'), htmlContent);
    
    // Also generate a simplified DOT file for other tools
    const dotContent = generateDotFile(nodes, edges);
    await fs.writeFile(path.join(OUTPUT_DIR, 'call-graph.dot'), dotContent);
    
    // Generate JSON data for further processing
    const graphData = {
        nodes: Array.from(nodes.values()),
        edges: edges,
        statistics: {
            totalPrograms: Array.from(nodes.values()).filter(n => n.shape === 'circle').length,
            totalCopybooks: Array.from(nodes.values()).filter(n => n.shape === 'box').length,
            totalCalls: edges.filter(e => !e.dashes).length,
            totalCopies: edges.filter(e => e.dashes).length,
            subsystemCounts: {}
        }
    };
    
    // Count by subsystem
    for (const [key, value] of Object.entries(subsystems)) {
        graphData.statistics.subsystemCounts[key] = Array.from(nodes.values())
            .filter(n => n.group === key).length;
    }
    
    await fs.writeJson(path.join(OUTPUT_DIR, 'call-graph-data.json'), graphData, { spaces: 2 });
    
    console.log(`✓ Call graph generated: ${OUTPUT_DIR}/call-graph.html`);
    console.log(`✓ DOT file generated: ${OUTPUT_DIR}/call-graph.dot`);
    console.log(`✓ Graph data saved: ${OUTPUT_DIR}/call-graph-data.json`);
    
    return graphData;
}

function getSubsystem(filePath) {
    if (filePath.includes('irs/')) return 'irs';
    if (filePath.includes('sales/')) return 'sales';
    if (filePath.includes('purchase/')) return 'purchase';
    if (filePath.includes('stock/')) return 'stock';
    if (filePath.includes('general/')) return 'general';
    return 'common';
}

function generateDotFile(nodes, edges) {
    let dot = 'digraph COBOL_Call_Graph {\n';
    dot += '  rankdir=LR;\n';
    dot += '  node [fontsize=10];\n\n';
    
    // Add nodes grouped by subsystem
    const subsystems = {};
    for (const node of nodes.values()) {
        if (!subsystems[node.group]) {
            subsystems[node.group] = [];
        }
        subsystems[node.group].push(node);
    }
    
    // Generate subgraphs
    for (const [subsystem, nodeList] of Object.entries(subsystems)) {
        dot += `  subgraph cluster_${subsystem} {\n`;
        dot += `    label="${subsystem.toUpperCase()}";\n`;
        dot += `    style=filled;\n`;
        dot += `    fillcolor=lightgray;\n`;
        
        for (const node of nodeList) {
            const shape = node.shape === 'box' ? 'box' : 'ellipse';
            dot += `    "${node.id}" [shape=${shape}];\n`;
        }
        
        dot += '  }\n\n';
    }
    
    // Add edges
    for (const edge of edges) {
        const style = edge.dashes ? 'dashed' : 'solid';
        dot += `  "${edge.from}" -> "${edge.to}" [style=${style}];\n`;
    }
    
    dot += '}\n';
    return dot;
}

// Run if called directly
if (require.main === module) {
    generateCallGraph().catch(console.error);
}

module.exports = { generateCallGraph };