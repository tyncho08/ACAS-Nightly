import os
import json

# Read all markdown files
docs_path = "/Users/MartinGonella/Desktop/Demos/ACAS-Nightly/FUNCTIONAL DOCUMENTATION"
documents = {}

# List of files in order
files = [
    "ACAS_Executive_Summary.md",
    "ACAS_Program_Catalog.md", 
    "ACAS_Architecture_Diagrams.md",
    "ACAS_Business_Flows_Enhanced.md",
    "ACAS_Data_Dictionary.md",
    "ACAS_Technical_Debt_Assessment.md",
    "ACAS_Accounting_Analysis.md",
    "ACAS_Documentation_Index.md",
    "Original_Documentation_Prompt.md"
]

# Read each file
for filename in files:
    filepath = os.path.join(docs_path, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Escape backticks and backslashes for JavaScript
            content = content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
            documents[filename] = content

# Create the HTML content
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACAS Functional Documentation</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/4.3.0/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            display: flex;
            height: 100vh;
            overflow: hidden;
        }
        
        /* Sidebar Navigation */
        .sidebar {
            width: 320px;
            background-color: #1e2936;
            color: white;
            overflow-y: auto;
            transition: transform 0.3s ease;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
        }
        
        .sidebar-header {
            padding: 30px 20px;
            background-color: #0f1419;
            border-bottom: 1px solid #2a3f5f;
        }
        
        .sidebar-header h1 {
            font-size: 24px;
            margin-bottom: 10px;
            color: #4a9eff;
        }
        
        .sidebar-header p {
            font-size: 14px;
            color: #8892b0;
            line-height: 1.5;
        }
        
        .nav-section {
            padding: 20px;
            border-bottom: 1px solid #2a3f5f;
        }
        
        .nav-section h3 {
            font-size: 12px;
            text-transform: uppercase;
            color: #8892b0;
            margin-bottom: 15px;
            letter-spacing: 1px;
        }
        
        .nav-item {
            display: block;
            padding: 12px 15px;
            margin: 5px 0;
            color: #ccd6f6;
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-size: 14px;
            cursor: pointer;
        }
        
        .nav-item:hover {
            background-color: #2a3f5f;
            color: #4a9eff;
            transform: translateX(5px);
        }
        
        .nav-item.active {
            background-color: #4a9eff;
            color: white;
        }
        
        .nav-item-desc {
            font-size: 12px;
            color: #8892b0;
            margin-top: 2px;
        }
        
        /* Main Content Area */
        .content {
            flex: 1;
            overflow-y: auto;
            padding: 40px 60px;
            background-color: white;
        }
        
        .content-header {
            background: linear-gradient(135deg, #4a9eff 0%, #1e2936 100%);
            color: white;
            padding: 40px;
            border-radius: 16px;
            margin-bottom: 40px;
            box-shadow: 0 10px 40px rgba(74, 158, 255, 0.2);
        }
        
        .content-header h1 {
            font-size: 36px;
            margin-bottom: 10px;
        }
        
        .content-header p {
            font-size: 18px;
            opacity: 0.9;
        }
        
        /* Markdown Content Styling */
        .markdown-content {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .markdown-content h1 {
            font-size: 32px;
            color: #1e2936;
            margin: 40px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #e1e4e8;
        }
        
        .markdown-content h2 {
            font-size: 26px;
            color: #2a3f5f;
            margin: 30px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid #e1e4e8;
        }
        
        .markdown-content h3 {
            font-size: 20px;
            color: #4a9eff;
            margin: 25px 0 10px 0;
        }
        
        .markdown-content h4 {
            font-size: 16px;
            color: #666;
            margin: 20px 0 10px 0;
        }
        
        .markdown-content p {
            margin: 15px 0;
            line-height: 1.8;
            color: #444;
        }
        
        .markdown-content ul, .markdown-content ol {
            margin: 15px 0;
            padding-left: 30px;
        }
        
        .markdown-content li {
            margin: 8px 0;
            line-height: 1.6;
        }
        
        .markdown-content code {
            background-color: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 90%;
            color: #e74c3c;
        }
        
        .markdown-content pre {
            background-color: #1e2936;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .markdown-content pre code {
            background-color: transparent;
            color: #ccd6f6;
            padding: 0;
            font-size: 14px;
        }
        
        .markdown-content table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .markdown-content th {
            background-color: #4a9eff;
            color: white;
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
        }
        
        .markdown-content td {
            padding: 12px 15px;
            border-bottom: 1px solid #e1e4e8;
        }
        
        .markdown-content tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        .markdown-content tr:hover {
            background-color: #e8f4fd;
        }
        
        .markdown-content blockquote {
            border-left: 4px solid #4a9eff;
            padding-left: 20px;
            margin: 20px 0;
            color: #666;
            font-style: italic;
            background-color: #f8f9fa;
            padding: 15px 20px;
            border-radius: 0 8px 8px 0;
        }
        
        .markdown-content strong {
            color: #1e2936;
            font-weight: 600;
        }
        
        /* Mermaid Diagram Styling */
        .mermaid {
            text-align: center;
            margin: 20px 0;
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
        }
        
        /* Loading State */
        .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            font-size: 18px;
            color: #666;
        }
        
        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4a9eff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Mobile Responsive */
        .menu-toggle {
            display: none;
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1000;
            background-color: #4a9eff;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        @media (max-width: 768px) {
            .menu-toggle {
                display: block;
            }
            
            .sidebar {
                position: fixed;
                left: 0;
                top: 0;
                height: 100%;
                transform: translateX(-100%);
                z-index: 999;
            }
            
            .sidebar.active {
                transform: translateX(0);
            }
            
            .content {
                padding: 20px;
                margin-left: 0;
            }
            
            .content-header {
                margin-top: 60px;
                padding: 20px;
            }
            
            .content-header h1 {
                font-size: 24px;
            }
            
            .markdown-content h1 {
                font-size: 24px;
            }
            
            .markdown-content h2 {
                font-size: 20px;
            }
        }
        
        /* Print Styles */
        @media print {
            .sidebar, .menu-toggle {
                display: none;
            }
            
            .content {
                padding: 20px;
            }
            
            .content-header {
                background: none;
                color: black;
                box-shadow: none;
                border: 1px solid #ddd;
            }
        }
        
        /* Smooth Scrolling */
        html {
            scroll-behavior: smooth;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
    </style>
</head>
<body>
    <button class="menu-toggle" onclick="toggleSidebar()">☰ Menu</button>
    
    <div class="container">
        <!-- Sidebar Navigation -->
        <nav class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <h1>ACAS Documentation</h1>
                <p>Comprehensive functional documentation for the Applewood Computers Accounting System</p>
            </div>
            
            <div class="nav-section">
                <h3>Overview</h3>
                <a class="nav-item" onclick="loadDocument('home')" data-doc="home">
                    Welcome
                    <div class="nav-item-desc">Documentation overview and guide</div>
                </a>
                <a class="nav-item" onclick="loadDocument('ACAS_Executive_Summary.md')" data-doc="ACAS_Executive_Summary.md">
                    Executive Summary
                    <div class="nav-item-desc">High-level system overview</div>
                </a>
            </div>
            
            <div class="nav-section">
                <h3>Technical Documentation</h3>
                <a class="nav-item" onclick="loadDocument('ACAS_Program_Catalog.md')" data-doc="ACAS_Program_Catalog.md">
                    Program Catalog
                    <div class="nav-item-desc">Complete program listing & dependencies</div>
                </a>
                <a class="nav-item" onclick="loadDocument('ACAS_Architecture_Diagrams.md')" data-doc="ACAS_Architecture_Diagrams.md">
                    Architecture Diagrams
                    <div class="nav-item-desc">Visual system representations</div>
                </a>
                <a class="nav-item" onclick="loadDocument('ACAS_Data_Dictionary.md')" data-doc="ACAS_Data_Dictionary.md">
                    Data Dictionary
                    <div class="nav-item-desc">Field-level documentation</div>
                </a>
                <a class="nav-item" onclick="loadDocument('ACAS_Technical_Debt_Assessment.md')" data-doc="ACAS_Technical_Debt_Assessment.md">
                    Technical Debt Assessment
                    <div class="nav-item-desc">Code quality & modernization</div>
                </a>
            </div>
            
            <div class="nav-section">
                <h3>Business Documentation</h3>
                <a class="nav-item" onclick="loadDocument('ACAS_Business_Flows_Enhanced.md')" data-doc="ACAS_Business_Flows_Enhanced.md">
                    Business Flows
                    <div class="nav-item-desc">End-to-end process documentation</div>
                </a>
                <a class="nav-item" onclick="loadDocument('ACAS_Accounting_Analysis.md')" data-doc="ACAS_Accounting_Analysis.md">
                    Accounting Analysis
                    <div class="nav-item-desc">Compliance & calculations</div>
                </a>
            </div>
            
            <div class="nav-section">
                <h3>Reference</h3>
                <a class="nav-item" onclick="loadDocument('ACAS_Documentation_Index.md')" data-doc="ACAS_Documentation_Index.md">
                    Documentation Index
                    <div class="nav-item-desc">Master index of all documents</div>
                </a>
                <a class="nav-item" onclick="loadDocument('Original_Documentation_Prompt.md')" data-doc="Original_Documentation_Prompt.md">
                    Original Prompt
                    <div class="nav-item-desc">Documentation requirements</div>
                </a>
            </div>
        </nav>
        
        <!-- Main Content Area -->
        <main class="content" id="content">
            <div class="loading">
                <div class="loading-spinner"></div>
                Loading documentation...
            </div>
        </main>
    </div>
    
    <script>
        // Initialize Mermaid with proper configuration
        mermaid.initialize({ 
            startOnLoad: false,
            theme: 'default',
            themeVariables: {
                primaryColor: '#4a9eff',
                primaryTextColor: '#fff',
                primaryBorderColor: '#2a3f5f',
                lineColor: '#666',
                secondaryColor: '#f8f9fa',
                tertiaryColor: '#e8f4fd'
            },
            flowchart: {
                htmlLabels: true,
                curve: 'basis'
            },
            sequence: {
                diagramMarginX: 50,
                diagramMarginY: 10,
                actorMargin: 50,
                width: 150,
                height: 65,
                boxMargin: 10,
                boxTextMargin: 5,
                noteMargin: 10,
                messageMargin: 35,
                mirrorActors: true
            }
        });
        
        // Marked configuration
        marked.setOptions({
            breaks: true,
            gfm: true,
            highlight: function(code, lang) {
                if (Prism.languages[lang]) {
                    return Prism.highlight(code, Prism.languages[lang], lang);
                }
                return code;
            }
        });
        
        // Home page content
        const homeContent = `
# Welcome to ACAS Functional Documentation

## About This Documentation

This comprehensive documentation suite provides detailed functional and technical documentation for the **ACAS (Applewood Computers Accounting System)**, a mature COBOL-based accounting system that has been in continuous development since 1976.

### Documentation Overview

This documentation package includes:

1. **Executive Summary** - High-level overview for decision makers
2. **Program Catalog** - Complete listing of 200+ programs with dependencies
3. **Architecture Diagrams** - Visual representations of system structure
4. **Data Dictionary** - Field-level documentation of all files and tables
5. **Business Flows** - End-to-end process documentation
6. **Technical Debt Assessment** - Modernization analysis and recommendations
7. **Accounting Analysis** - Compliance features and calculation engines

### System Highlights

- **47+ years** of continuous development (1976-2025)
- **200+ COBOL programs** organized in modular architecture
- **5 integrated modules**: Sales, Purchase, Stock, General Ledger, and IRS
- **Dual architecture** supporting both COBOL files and MySQL/MariaDB
- **Complete accounting** functionality for small to medium businesses

### How to Use This Documentation

#### For Executives
Start with the **Executive Summary** for a high-level overview of the system's capabilities, current state, and modernization opportunities.

#### For Architects
Review the **Architecture Diagrams** and **Technical Debt Assessment** to understand the system structure and plan modernization strategies.

#### For Developers
Use the **Program Catalog** and **Data Dictionary** to navigate the codebase and understand data structures.

#### For Business Analysts
Explore the **Business Flows** and **Accounting Analysis** to understand business processes and compliance features.

### Key Findings Summary

#### Strengths
- ✅ Complete accounting functionality
- ✅ Proven reliability over 47 years
- ✅ Modular architecture
- ✅ Strong data validation
- ✅ Comprehensive integration

#### Areas for Improvement
- ❌ No built-in security/authentication
- ❌ Character-based UI only
- ❌ Missing GL programs (gl040, gl130, gl190)
- ❌ Technical debt (GO TO patterns)
- ❌ Limited integration capabilities

### Navigation Guide

Use the sidebar on the left to navigate through the documentation. Each section is designed to provide specific insights:

- **Overview** sections provide high-level understanding
- **Technical** sections detail system implementation
- **Business** sections explain functional capabilities
- **Reference** sections provide comprehensive listings

---

*This documentation was generated through comprehensive analysis of the ACAS codebase to enable technical teams to understand the system, create architectural diagrams, and develop modernization strategies.*
        `;
        
        // Embedded documents
        const documents = {
'''

# Add each document to the JavaScript object
for filename, content in documents.items():
    html_content += f'            "{filename}": `{content}`,\n'

html_content += '''        };
        
        // Load document function
        async function loadDocument(docName) {
            const contentDiv = document.getElementById('content');
            
            // Update active navigation
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // Find and activate the clicked item
            const clickedItem = document.querySelector(`[data-doc="${docName}"]`);
            if (clickedItem) {
                clickedItem.classList.add('active');
            }
            
            // Close sidebar on mobile
            if (window.innerWidth <= 768) {
                document.getElementById('sidebar').classList.remove('active');
            }
            
            // Show loading state
            contentDiv.innerHTML = '<div class="loading"><div class="loading-spinner"></div>Loading documentation...</div>';
            
            // Small delay to show loading animation
            await new Promise(resolve => setTimeout(resolve, 100));
            
            try {
                let content;
                
                if (docName === 'home') {
                    content = homeContent;
                } else if (documents[docName]) {
                    content = documents[docName];
                } else {
                    throw new Error('Document not found');
                }
                
                // Extract title from content
                const titleMatch = content.match(/^#\\s+(.+)$/m);
                const title = titleMatch ? titleMatch[1] : docName.replace('.md', '').replace(/_/g, ' ');
                
                // Render the markdown content
                let html = marked.parse(content);
                
                // Process mermaid diagrams
                const mermaidRegex = /<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g;
                let mermaidIndex = 0;
                const mermaidDiagrams = [];
                
                html = html.replace(mermaidRegex, (match, diagram) => {
                    const id = `mermaid-${mermaidIndex++}`;
                    mermaidDiagrams.push({ id, diagram: diagram.trim() });
                    return `<div class="mermaid" id="${id}">Loading diagram...</div>`;
                });
                
                // Set the content
                contentDiv.innerHTML = `
                    <div class="content-header">
                        <h1>${title}</h1>
                        <p>ACAS Functional Documentation</p>
                    </div>
                    <div class="markdown-content">
                        ${html}
                    </div>
                `;
                
                // Render Mermaid diagrams
                for (const { id, diagram } of mermaidDiagrams) {
                    try {
                        const element = document.getElementById(id);
                        if (element) {
                            element.innerHTML = diagram;
                            await mermaid.run({
                                nodes: [element]
                            });
                        }
                    } catch (error) {
                        console.error('Mermaid render error:', error);
                        document.getElementById(id).innerHTML = `<pre>${diagram}</pre>`;
                    }
                }
                
                // Re-run Prism for syntax highlighting
                if (typeof Prism !== 'undefined') {
                    Prism.highlightAll();
                }
                
                // Scroll to top
                contentDiv.scrollTop = 0;
                
            } catch (error) {
                contentDiv.innerHTML = `
                    <div class="content-header">
                        <h1>Error Loading Document</h1>
                        <p>Unable to load the requested documentation</p>
                    </div>
                    <div class="markdown-content">
                        <p>Sorry, we couldn't load the document: <strong>${docName}</strong></p>
                        <p>Error: ${error.message}</p>
                        <p>Please try selecting another document from the navigation menu.</p>
                    </div>
                `;
            }
        }
        
        // Toggle sidebar for mobile
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('active');
        }
        
        // Load home page on startup
        window.addEventListener('DOMContentLoaded', async function() {
            // Wait a bit to ensure everything is loaded
            await new Promise(resolve => setTimeout(resolve, 100));
            await loadDocument('home');
        });
    </script>
</body>
</html>'''

# Write the HTML file
output_path = os.path.join(docs_path, "Functional_Documentation_Report.html")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Created fixed HTML file: {output_path}")
print(f"Total size: {len(html_content):,} bytes")