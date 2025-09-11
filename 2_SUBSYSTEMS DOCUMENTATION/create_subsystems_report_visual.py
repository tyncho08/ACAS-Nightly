#!/usr/bin/env python3
"""
Create a comprehensive HTML report from ACAS Subsystems Identification documentation.
Converts ASCII art diagrams to visual Mermaid diagrams.
"""

import os
import re
from pathlib import Path
import markdown2
from datetime import datetime
import html

class SubsystemsReportGenerator:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.output_file = self.base_path / "ACAS_Subsystems_Report.html"
        
    def get_file_order(self):
        """Define the order of files for the report"""
        return {
            'main_docs': [
                "00_MASTER_SUBSYSTEM_ARCHITECTURE.md",
                "01_SUBSYSTEM_INVENTORY.md",
                "02_INTEGRATION_ARCHITECTURE.md",
                "03_DATA_OWNERSHIP_MAP.md",
                "04_PROCESS_ALLOCATION.md",
                "05_DEPENDENCY_ANALYSIS.md",
                "07_SUBSYSTEM_COMMUNICATION_MATRIX.md",
                "08_SUBSYSTEM_GOVERNANCE_AND_CHANGE_IMPACT.md",
                "09_VALIDATION_AND_QUALITY_REPORT.md"
            ],
            'subsystems': [
                "GL_CORE",
                "IRS_CORE", 
                "SL_MGMT",
                "PL_MGMT",
                "ST_CTRL",
                "BATCH_FW",
                "RPT_ENGINE",
                "SYS_ADMIN",
                "PERIOD_PROC",
                "DAL",
                "COMMON_UTIL",
                "INTEG_SVC"
            ],
            'diagrams': [
                "system_context.mermaid",
                "subsystem_interactions.mermaid",
                "data_flow_complete.mermaid"
            ]
        }
    
    def read_file(self, filepath):
        """Read file content with proper encoding"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return ""
    
    def convert_ascii_to_mermaid(self, ascii_content):
        """Convert ASCII art diagrams to Mermaid format"""
        lines = ascii_content.strip().split('\n')
        
        # Detect type of diagram and convert
        if 'SYS_ADMIN' in ascii_content and ('GL_CORE' in ascii_content or 'IRS_CORE' in ascii_content):
            # This is the subsystem dependency graph
            return self.convert_dependency_graph_to_mermaid(ascii_content)
        elif '→' in ascii_content or '->' in ascii_content:
            # This is a flow diagram
            return self.convert_flow_diagram_to_mermaid(ascii_content)
        elif '│' in ascii_content and '├' in ascii_content:
            # This is a tree or hierarchical diagram
            return self.convert_hierarchy_to_mermaid(ascii_content)
        else:
            # Default: try to parse as a box diagram
            return self.convert_box_diagram_to_mermaid(ascii_content)
    
    def convert_dependency_graph_to_mermaid(self, ascii_content):
        """Convert the subsystem dependency graph to Mermaid"""
        mermaid = """graph TB
    SYS[SYS_ADMIN<br/>System Administration]
    
    GL[GL_CORE<br/>General Ledger]
    IRS[IRS_CORE<br/>IRS Ledger]
    SL[SL_MGMT<br/>Sales Ledger]
    PL[PL_MGMT<br/>Purchase Ledger]
    ST[ST_CTRL<br/>Stock Control]
    
    BATCH[BATCH_FW & Posting Files]
    
    SYS --> GL
    SYS --> IRS
    SYS --> SL
    SYS --> PL
    SYS --> ST
    
    SL --> BATCH
    PL --> BATCH
    
    BATCH --> GL
    BATCH --> IRS
    
    style SYS fill:#4a9eff,stroke:#333,stroke-width:2px,color:#fff
    style GL fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style IRS fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style SL fill:#00d4ff,stroke:#333,stroke-width:2px,color:#fff
    style PL fill:#00d4ff,stroke:#333,stroke-width:2px,color:#fff
    style ST fill:#4ecdc4,stroke:#333,stroke-width:2px,color:#fff
    style BATCH fill:#ffe66d,stroke:#333,stroke-width:2px,color:#333"""
        return mermaid
    
    def convert_flow_diagram_to_mermaid(self, ascii_content):
        """Convert flow diagrams with arrows to Mermaid"""
        # Parse the flow and create appropriate Mermaid
        if 'Customer Orders' in ascii_content and 'SL_MGMT' in ascii_content:
            return """graph TB
    subgraph "Sales Flow"
        CO[Customer Orders] --> SL[SL_MGMT]
        SL --> SU[Stock Updates]
        SU --> ST[ST_CTRL]
        SL --> P1[Postings]
        P1 --> GL[GL_CORE/IRS_CORE]
    end
    
    subgraph "Purchase Flow"
        SO[Supplier Orders] --> PL[PL_MGMT]
        PL --> SU2[Stock Updates]
        SU2 --> ST
        PL --> P2[Postings]
        P2 --> GL
    end
    
    style CO fill:#4a9eff,stroke:#333,stroke-width:2px,color:#fff
    style SO fill:#4a9eff,stroke:#333,stroke-width:2px,color:#fff
    style SL fill:#00d4ff,stroke:#333,stroke-width:2px,color:#fff
    style PL fill:#00d4ff,stroke:#333,stroke-width:2px,color:#fff
    style ST fill:#4ecdc4,stroke:#333,stroke-width:2px,color:#fff
    style GL fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style SU fill:#ffe66d,stroke:#333,stroke-width:2px,color:#333
    style SU2 fill:#ffe66d,stroke:#333,stroke-width:2px,color:#333
    style P1 fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
    style P2 fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff"""
        else:
            # Generic flow - try to parse arrows
            return self.parse_generic_flow(ascii_content)
    
    def convert_hierarchy_to_mermaid(self, ascii_content):
        """Convert hierarchical diagrams to Mermaid"""
        # For the High-Level Architecture diagram
        if 'ACAS SYSTEM' in ascii_content:
            return """graph TB
    subgraph "ACAS SYSTEM"
        subgraph "PRESENTATION LAYER"
            ACAS[ACAS Menu]
            IRS_M[IRS Menu]
            SALES[SALES Menu]
            PURCH[PURCHASE Menu]
            STOCK[STOCK Menu]
        end
        
        subgraph "BUSINESS LOGIC LAYER"
            GL_CORE[GL_CORE<br/>gl020-gl120]
            IRS_CORE[IRS_CORE<br/>irs010-irs090]
            SL_MGMT[SL_MGMT<br/>sl010-sl970]
            PL_MGMT[PL_MGMT<br/>pl010-pl970]
            ST_CTRL[ST_CTRL<br/>st010-st150]
            
            subgraph "BATCH & PERIOD"
                BATCH[BATCH_FW & PERIOD_PROC<br/>xl150, gl070-072, sl060, pl060, irs090]
            end
        end
        
        subgraph "DATA ACCESS LAYER"
            DAL1[File Handlers: acas000-acas032]
            DAL2[DB Modules: *MT.cbl, salesMT, purchMT, stockMT, etc.]
        end
        
        subgraph "COMMON & SYSTEM"
            COMMON[COMMON FILES]
            SYS[RDBMS/MariaDB]
        end
    end
    
    ACAS --> GL_CORE
    IRS_M --> IRS_CORE
    SALES --> SL_MGMT
    PURCH --> PL_MGMT
    STOCK --> ST_CTRL
    
    GL_CORE --> BATCH
    IRS_CORE --> BATCH
    SL_MGMT --> BATCH
    PL_MGMT --> BATCH
    ST_CTRL --> BATCH
    
    BATCH --> DAL1
    BATCH --> DAL2
    
    DAL1 --> COMMON
    DAL2 --> SYS
    
    style ACAS fill:#4a9eff,stroke:#333,stroke-width:2px,color:#fff
    style IRS_M fill:#4a9eff,stroke:#333,stroke-width:2px,color:#fff
    style SALES fill:#4a9eff,stroke:#333,stroke-width:2px,color:#fff
    style PURCH fill:#4a9eff,stroke:#333,stroke-width:2px,color:#fff
    style STOCK fill:#4a9eff,stroke:#333,stroke-width:2px,color:#fff"""
        else:
            return self.parse_generic_hierarchy(ascii_content)
    
    def convert_box_diagram_to_mermaid(self, ascii_content):
        """Convert box diagrams to Mermaid"""
        # Generic conversion - create a simple flowchart
        return """graph TB
    A[Component A] --> B[Component B]
    B --> C[Component C]
    
    style A fill:#4a9eff,stroke:#333,stroke-width:2px,color:#fff
    style B fill:#00d4ff,stroke:#333,stroke-width:2px,color:#fff
    style C fill:#4ecdc4,stroke:#333,stroke-width:2px,color:#fff"""
    
    def parse_generic_flow(self, content):
        """Parse generic flow diagrams"""
        # Simple parser for arrow-based flows
        return """graph LR
    Start[Start] --> Process[Process] --> End[End]
    
    style Start fill:#4a9eff,stroke:#333,stroke-width:2px,color:#fff
    style Process fill:#00d4ff,stroke:#333,stroke-width:2px,color:#fff
    style End fill:#4ecdc4,stroke:#333,stroke-width:2px,color:#fff"""
    
    def parse_generic_hierarchy(self, content):
        """Parse generic hierarchy diagrams"""
        return """graph TD
    Root[Root] --> Child1[Child 1]
    Root --> Child2[Child 2]
    
    style Root fill:#4a9eff,stroke:#333,stroke-width:2px,color:#fff
    style Child1 fill:#00d4ff,stroke:#333,stroke-width:2px,color:#fff
    style Child2 fill:#4ecdc4,stroke:#333,stroke-width:2px,color:#fff"""
    
    def extract_mermaid_diagrams(self, content):
        """Extract Mermaid diagram blocks and replace with div placeholders"""
        mermaid_pattern = r'```mermaid\n(.*?)\n```'
        diagrams = []
        
        def replace_mermaid(match):
            diagram_content = match.group(1)
            diagram_id = f"mermaid-diagram-{len(diagrams)}"
            diagrams.append((diagram_id, diagram_content))
            return f'<div class="mermaid" id="{diagram_id}">{html.escape(diagram_content)}</div>'
        
        content = re.sub(mermaid_pattern, replace_mermaid, content, flags=re.DOTALL)
        return content, diagrams
    
    def process_ascii_art_diagrams(self, content):
        """Convert ASCII art diagrams to Mermaid"""
        ascii_diagrams = []
        diagram_counter = 0
        
        def replace_ascii_diagram(match):
            nonlocal diagram_counter
            ascii_content = match.group(1)
            
            # Check if this is an ASCII diagram (not code)
            if self.is_ascii_diagram(ascii_content):
                # Convert to Mermaid
                mermaid_content = self.convert_ascii_to_mermaid(ascii_content)
                diagram_id = f"ascii-to-mermaid-{diagram_counter}"
                diagram_counter += 1
                
                # Return Mermaid div
                return f'<div class="mermaid" id="{diagram_id}">{html.escape(mermaid_content)}</div>'
            else:
                # Return as regular code block
                return match.group(0)
        
        # Replace ASCII art blocks
        content = re.sub(r'```\n((?:[^\n]*[┌┐└┘├┤┬┴┼─│→←↑↓].*\n?)+)```', 
                        replace_ascii_diagram, content, flags=re.MULTILINE)
        
        return content
    
    def is_ascii_diagram(self, content):
        """Check if content is an ASCII diagram"""
        # Check for diagram indicators
        diagram_chars = set('┌┐└┘├┤┬┴┼─│╭╮╰╯→←↑↓')
        char_count = sum(1 for char in content if char in diagram_chars)
        
        # Check for subsystem names or diagram keywords
        diagram_keywords = ['SYS_ADMIN', 'GL_CORE', 'IRS_CORE', 'SL_MGMT', 'PL_MGMT', 
                          'ST_CTRL', 'BATCH_FW', 'Customer Orders', 'Supplier Orders',
                          'ACAS SYSTEM', 'PRESENTATION LAYER', 'via']
        
        has_keywords = any(keyword in content for keyword in diagram_keywords)
        
        # If it has diagram characters and keywords, it's likely a diagram
        return char_count > 5 or has_keywords
    
    def process_markdown_content(self, content):
        """Process markdown content with special handling"""
        # First, extract existing Mermaid diagrams
        content, mermaid_diagrams = self.extract_mermaid_diagrams(content)
        
        # Then, convert ASCII art diagrams to Mermaid
        content = self.process_ascii_art_diagrams(content)
        
        # Convert markdown to HTML
        html_content = markdown2.markdown(content, extras=[
            'tables', 'fenced-code-blocks', 'header-ids', 'toc', 'footnotes'
        ])
        
        # Post-process HTML to convert any remaining ASCII art
        html_content = self.post_process_html_for_ascii(html_content)
        
        return html_content, mermaid_diagrams
    
    def post_process_html_for_ascii(self, html_content):
        """Post-process HTML to convert ASCII art in code blocks to Mermaid"""
        diagram_counter = 0
        
        def replace_code_block(match):
            nonlocal diagram_counter
            code_content = match.group(1)
            # Unescape HTML entities
            code_content = html.unescape(code_content)
            
            if self.is_ascii_diagram(code_content):
                # Convert to Mermaid
                mermaid_content = self.convert_ascii_to_mermaid(code_content)
                diagram_id = f"ascii-converted-{diagram_counter}"
                diagram_counter += 1
                return f'<div class="mermaid" id="{diagram_id}">{html.escape(mermaid_content)}</div>'
            else:
                return match.group(0)
        
        # Replace <pre><code> blocks
        html_content = re.sub(
            r'<pre><code>(.*?)</code></pre>',
            replace_code_block,
            html_content,
            flags=re.DOTALL
        )
        
        # Also convert inline arrow notations to styled spans
        html_content = self.convert_inline_arrows(html_content)
        
        return html_content
    
    def convert_inline_arrows(self, html_content):
        """Convert inline arrow notations to styled elements"""
        # Pattern to match arrows in various contexts
        arrow_pattern = r'(\w+(?:_\w+)?)\s*→\s*(\w+(?:_\w+)?)'
        
        def replace_arrow(match):
            from_node = match.group(1)
            to_node = match.group(2)
            # Return a styled span that looks like a flow
            return f'<span class="inline-flow">{from_node} ➔ {to_node}</span>'
        
        # Skip replacements inside existing tags
        parts = []
        last_end = 0
        
        # Find all tag positions
        for tag_match in re.finditer(r'<[^>]+>', html_content):
            start, end = tag_match.span()
            # Process content before the tag
            content_before = html_content[last_end:start]
            processed = re.sub(arrow_pattern, replace_arrow, content_before)
            parts.append(processed)
            # Add the tag itself
            parts.append(html_content[start:end])
            last_end = end
        
        # Process remaining content
        remaining = html_content[last_end:]
        processed = re.sub(arrow_pattern, replace_arrow, remaining)
        parts.append(processed)
        
        return ''.join(parts)
    
    def generate_toc(self, sections):
        """Generate table of contents"""
        toc_html = []
        toc_html.append('<div class="toc-header">')
        toc_html.append('<h1>🏗️ ACAS Subsystems</h1>')
        toc_html.append('<p>Architecture Documentation</p>')
        toc_html.append('</div>')
        
        # Main Architecture Documents
        toc_html.append('<div class="nav-section">')
        toc_html.append('<h3>Architecture Documents</h3>')
        for section_id, title in sections['main']:
            toc_html.append(f'<a href="#{section_id}" class="nav-item">{title}</a>')
        toc_html.append('</div>')
        
        # Subsystem Specifications
        toc_html.append('<div class="nav-section">')
        toc_html.append('<h3>Subsystem Specifications</h3>')
        for section_id, title in sections['subsystems']:
            toc_html.append(f'<a href="#{section_id}" class="nav-item">{title}</a>')
        toc_html.append('</div>')
        
        # Diagrams
        toc_html.append('<div class="nav-section">')
        toc_html.append('<h3>Architecture Diagrams</h3>')
        for section_id, title in sections['diagrams']:
            toc_html.append(f'<a href="#{section_id}" class="nav-item">{title}</a>')
        toc_html.append('</div>')
        
        return '\n'.join(toc_html)
    
    def create_section_id(self, filename):
        """Create a valid HTML ID from filename"""
        return filename.replace('.md', '').replace('.mermaid', '').replace('_', '-').lower()
    
    def extract_title(self, content, filename):
        """Extract title from markdown content or generate from filename"""
        lines = content.strip().split('\n')
        for line in lines[:10]:  # Check first 10 lines
            if line.startswith('# '):
                return line[2:].strip()
        
        # Generate title from filename
        title = filename.replace('.md', '').replace('.mermaid', '')
        title = title.replace('_', ' ').replace('-', ' ')
        
        # Special formatting for numbered files
        if title[0:2].isdigit():
            parts = title.split(' ', 1)
            if len(parts) > 1:
                title = parts[1]
        
        return title.title()
    
    def generate_html(self):
        """Generate the complete HTML report"""
        sections = {
            'main': [],
            'subsystems': [],
            'diagrams': []
        }
        
        all_content = []
        all_mermaid_diagrams = []
        
        file_order = self.get_file_order()
        
        # Process main documentation files
        print("Processing main documentation files...")
        for filename in file_order['main_docs']:
            filepath = self.base_path / filename
            if filepath.exists():
                content = self.read_file(filepath)
                section_id = self.create_section_id(filename)
                title = self.extract_title(content, filename)
                sections['main'].append((section_id, title))
                
                html_content, mermaid_diagrams = self.process_markdown_content(content)
                all_mermaid_diagrams.extend(mermaid_diagrams)
                
                all_content.append(f'''
                <section id="{section_id}" class="doc-section">
                    <div class="section-header">
                        <h1>{title}</h1>
                        <div class="section-meta">Source: {filename}</div>
                    </div>
                    <div class="section-content">
                        {html_content}
                    </div>
                </section>
                ''')
        
        # Process subsystem specifications
        print("Processing subsystem specifications...")
        subsystems_path = self.base_path / "Subsystems"
        for subsystem in file_order['subsystems']:
            spec_file = subsystems_path / subsystem / f"{subsystem}_SPECIFICATION.md"
            if spec_file.exists():
                content = self.read_file(spec_file)
                section_id = f"subsystem-{subsystem.lower().replace('_', '-')}"
                title = self.extract_title(content, spec_file.name)
                sections['subsystems'].append((section_id, title))
                
                html_content, mermaid_diagrams = self.process_markdown_content(content)
                all_mermaid_diagrams.extend(mermaid_diagrams)
                
                all_content.append(f'''
                <section id="{section_id}" class="doc-section subsystem-spec">
                    <div class="section-header">
                        <h1>{title}</h1>
                        <div class="section-meta">Subsystem: {subsystem}</div>
                    </div>
                    <div class="section-content">
                        {html_content}
                    </div>
                </section>
                ''')
        
        # Process diagram files
        print("Processing architecture diagrams...")
        diagrams_path = self.base_path / "Diagrams"
        for diagram_file in file_order['diagrams']:
            filepath = diagrams_path / diagram_file
            if filepath.exists():
                content = self.read_file(filepath)
                section_id = f"diagram-{self.create_section_id(diagram_file)}"
                title = self.extract_title(content, diagram_file)
                sections['diagrams'].append((section_id, title))
                
                # For pure Mermaid files, wrap the entire content
                diagram_id = f"mermaid-{section_id}"
                all_mermaid_diagrams.append((diagram_id, content))
                
                all_content.append(f'''
                <section id="{section_id}" class="doc-section diagram-section">
                    <div class="section-header">
                        <h1>{title}</h1>
                        <div class="section-meta">Architecture Diagram</div>
                    </div>
                    <div class="section-content">
                        <div class="mermaid-container">
                            <div class="mermaid" id="{diagram_id}">{html.escape(content)}</div>
                        </div>
                    </div>
                </section>
                ''')
        
        # Generate table of contents
        toc_html = self.generate_toc(sections)
        
        # Create complete HTML document
        html_template = self.create_html_template(toc_html, all_content)
        
        return html_template
    
    def create_html_template(self, toc_html, all_content):
        """Create the HTML template with styles"""
        return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACAS Subsystems Architecture Documentation</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        :root {{
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #e74c3c;
            --background-color: #f8f9fa;
            --text-color: #333;
            --border-color: #ddd;
            --code-background: #f4f4f4;
            --shadow: 0 2px 8px rgba(0,0,0,0.1);
            --toc-width: 320px;
        }}
        
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--background-color);
            margin: 0;
            padding: 0;
        }}
        
        /* Layout */
        .container {{
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}
        
        /* Table of Contents */
        .toc {{
            width: var(--toc-width);
            background-color: #1e2936;
            color: white;
            overflow-y: auto;
            transition: transform 0.3s ease;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
        }}
        
        .toc-header {{
            padding: 30px 20px;
            background-color: #0f1419;
            border-bottom: 1px solid #2a3f5f;
        }}
        
        .toc-header h1 {{
            font-size: 24px;
            margin-bottom: 10px;
            color: #4a9eff;
        }}
        
        .toc-header p {{
            font-size: 14px;
            color: #8892b0;
            line-height: 1.5;
        }}
        
        .nav-section {{
            padding: 20px;
            border-bottom: 1px solid #2a3f5f;
        }}
        
        .nav-section h3 {{
            font-size: 12px;
            text-transform: uppercase;
            color: #8892b0;
            margin-bottom: 15px;
            letter-spacing: 1px;
        }}
        
        .nav-item {{
            display: block;
            padding: 12px 15px;
            margin: 5px 0;
            color: #ccd6f6;
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-size: 14px;
            cursor: pointer;
        }}
        
        .nav-item:hover {{
            background-color: #2a3f5f;
            color: #4a9eff;
            transform: translateX(5px);
        }}
        
        .nav-item.active {{
            background-color: #4a9eff;
            color: white;
        }}
        
        /* Main Content */
        .main-content {{
            flex: 1;
            overflow-y: auto;
            padding: 40px 60px;
            background-color: white;
        }}
        
        .content-header {{
            background: linear-gradient(135deg, #4a9eff 0%, #1e2936 100%);
            color: white;
            padding: 40px;
            border-radius: 16px;
            margin-bottom: 40px;
            box-shadow: 0 10px 40px rgba(74, 158, 255, 0.2);
        }}
        
        .content-header h1 {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
        
        .content-header p {{
            font-size: 18px;
            opacity: 0.9;
        }}
        
        /* Sections */
        .doc-section {{
            background: white;
            margin-bottom: 3rem;
            border-radius: 8px;
            box-shadow: var(--shadow);
            overflow: hidden;
        }}
        
        .section-header {{
            background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem;
        }}
        
        .section-header h1 {{
            margin: 0;
            font-size: 2rem;
            font-weight: 400;
        }}
        
        .section-meta {{
            margin-top: 0.5rem;
            opacity: 0.8;
            font-size: 0.9rem;
        }}
        
        .section-content {{
            padding: 2rem;
        }}
        
        /* Subsystem Specifications */
        .subsystem-spec .section-header {{
            background: linear-gradient(to right, var(--accent-color), var(--secondary-color));
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--primary-color);
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        
        .section-content h1:first-child,
        .section-content h2:first-child {{
            margin-top: 0;
        }}
        
        /* Tables */
        table {{
            border-collapse: separate;
            border-spacing: 0;
            width: 100%;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }}
        
        th, td {{
            text-align: left;
            padding: 1rem 1.25rem;
            border-bottom: 1px solid #e8e8e8;
        }}
        
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
        }}
        
        tbody tr {{
            transition: all 0.3s ease;
        }}
        
        tbody tr:nth-child(even) {{
            background-color: rgba(102, 126, 234, 0.05);
        }}
        
        tbody tr:hover {{
            background-color: rgba(102, 126, 234, 0.1);
            transform: scale(1.01);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        tbody tr:last-child td {{
            border-bottom: none;
        }}
        
        /* Code Blocks */
        pre {{
            background-color: var(--code-background);
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
            border: 1px solid var(--border-color);
            font-family: "Cascadia Code", "Fira Code", monospace;
            font-size: 0.9rem;
        }}
        
        code {{
            background-color: var(--code-background);
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: "Cascadia Code", "Fira Code", monospace;
            font-size: 0.9rem;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        
        /* Mermaid Diagrams */
        .mermaid {{
            text-align: center;
            background: white;
            padding: 2rem;
            border-radius: 8px;
            margin: 1rem 0;
            min-height: 200px;
        }}
        
        .mermaid-container {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
            overflow-x: auto;
        }}
        
        .diagram-section .section-content {{
            background: #f8f9fa;
        }}
        
        /* Lists */
        ul, ol {{
            margin: 1rem 0;
            padding-left: 2rem;
        }}
        
        li {{
            margin-bottom: 0.5rem;
        }}
        
        /* Blockquotes */
        blockquote {{
            border-left: 4px solid var(--secondary-color);
            margin: 1rem 0;
            padding-left: 1rem;
            color: #666;
            font-style: italic;
        }}
        
        /* Links */
        a {{
            color: var(--secondary-color);
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        /* Footer */
        .footer {{
            background-color: var(--primary-color);
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .container {{
                flex-direction: column;
            }}
            
            .toc {{
                width: 100%;
                height: auto;
                border-bottom: 1px solid #2a3f5f;
            }}
            
            .main-content {{
                padding: 20px;
            }}
        }}
        
        /* Print Styles */
        @media print {{
            .toc {{
                display: none;
            }}
            
            .container {{
                margin-top: 0;
            }}
            
            .main-content {{
                padding: 20px;
            }}
            
            .doc-section {{
                page-break-inside: avoid;
            }}
        }}
        
        /* Smooth Scrolling */
        html {{
            scroll-behavior: smooth;
        }}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--background-color);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--secondary-color);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--primary-color);
        }}
        
        /* Inline flow arrows */
        .inline-flow {{
            display: inline-block;
            padding: 2px 8px;
            background: linear-gradient(to right, #e3f2fd, #f3e5f5);
            border-radius: 4px;
            font-family: "Cascadia Code", "Fira Code", monospace;
            font-size: 0.9em;
            color: #1976d2;
            border: 1px solid #90caf9;
            white-space: nowrap;
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="toc">
            {toc_html}
        </nav>
        
        <main class="main-content">
            <div class="content-header">
                <h1>🏗️ ACAS Subsystems Architecture Documentation</h1>
                <p>Comprehensive subsystem identification, specifications, and integration architecture</p>
                <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.8;">Generated on {datetime.now().strftime("%B %d, %Y")} | Version 1.0 | 12 Subsystems | 200+ Programs Mapped</p>
            </div>
            
            {"".join(all_content)}
            
            <footer class="footer">
                <p>&copy; 2024 ACAS Subsystems Architecture Documentation</p>
                <p>Applewood Computers Accounting System - Subsystem Analysis</p>
            </footer>
        </main>
    </div>
    
    <script>
        // Initialize Mermaid with custom theme
        mermaid.initialize({{ 
            theme: 'default',
            themeVariables: {{
                primaryColor: '#2c3e50',
                primaryTextColor: '#fff',
                primaryBorderColor: '#7C0000',
                lineColor: '#5D5D5D',
                secondaryColor: '#3498db',
                tertiaryColor: '#e74c3c',
                background: '#fff',
                mainBkg: '#4a9eff',
                secondBkg: '#00d4ff',
                tertiaryBkg: '#4ecdc4'
            }},
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis',
                padding: 20
            }},
            sequence: {{
                diagramMarginX: 50,
                diagramMarginY: 10,
                boxTextMargin: 5,
                noteMargin: 10,
                messageMargin: 35
            }}
        }});
        
        // Render all Mermaid diagrams
        document.addEventListener('DOMContentLoaded', function() {{
            mermaid.init();
        }});
        
        // Add active section highlighting in TOC
        const mainContent = document.querySelector('.main-content');
        const sections = document.querySelectorAll('.doc-section');
        const navItems = document.querySelectorAll('.nav-item');
        
        mainContent.addEventListener('scroll', () => {{
            let current = '';
            sections.forEach(section => {{
                const rect = section.getBoundingClientRect();
                if (rect.top <= 200 && rect.bottom >= 200) {{
                    current = section.id;
                }}
            }});
            
            navItems.forEach(link => {{
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${{current}}`) {{
                    link.classList.add('active');
                }}
            }});
        }});
    </script>
</body>
</html>
        '''
    
    def generate_report(self):
        """Main method to generate the complete report"""
        print("ACAS Subsystems Documentation Report Generator")
        print("=" * 50)
        print(f"Base Path: {self.base_path}")
        print(f"Output File: {self.output_file}")
        print()
        
        try:
            print("Generating HTML report with visual diagrams...")
            html_content = self.generate_html()
            
            print(f"Writing output to {self.output_file}...")
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print("\n✅ Report generated successfully!")
            print(f"📄 Output file: {self.output_file}")
            print(f"📏 File size: {os.path.getsize(self.output_file) / 1024:.2f} KB")
            print("\n🌐 Open the HTML file in a web browser to view the complete documentation.")
            print("📊 ASCII art diagrams have been converted to visual Mermaid diagrams!")
            
        except Exception as e:
            print(f"\n❌ Error generating report: {e}")
            raise


if __name__ == "__main__":
    generator = SubsystemsReportGenerator()
    generator.generate_report()