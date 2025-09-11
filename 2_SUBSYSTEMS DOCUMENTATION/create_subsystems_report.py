#!/usr/bin/env python3
"""
Create a comprehensive HTML report from ACAS Subsystems Identification documentation.
Combines all markdown files into a single, navigable HTML document with proper
rendering of Mermaid diagrams and ASCII art.
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
    
    def process_markdown_content(self, content):
        """Process markdown content with special handling"""
        # Extract and handle Mermaid diagrams
        content, mermaid_diagrams = self.extract_mermaid_diagrams(content)
        
        # Convert markdown to HTML FIRST
        # Note: Not using 'codehilite' to avoid syntax highlighting on plain code blocks
        html_content = markdown2.markdown(content, extras=[
            'tables', 'fenced-code-blocks', 'header-ids', 'toc', 'footnotes'
        ])
        
        # THEN post-process the HTML to style ASCII art blocks
        html_content = self.post_process_ascii_art(html_content)
        
        return html_content, mermaid_diagrams
    
    def post_process_ascii_art(self, html_content):
        """Post-process HTML to identify and style ASCII art blocks"""
        ascii_art_count = 0
        total_blocks_checked = 0
        
        def check_if_ascii_art(content):
            """Determine if a code block contains ASCII art"""
            # Check for box-drawing characters (expanded set)
            box_chars = '┌┐└┘├┤┬┴┼─│╭╮╰╯═║╔╗╚╝╠╣╦╩╬'
            if any(char in content for char in box_chars):
                return True, 'ascii-art-box'
            
            # Check for heavy box drawing
            if any(char in content for char in '━┃┏┓┗┛┣┫┳┻╋'):
                return True, 'ascii-art-box'
            
            # Check for arrow characters and flow patterns
            arrow_chars = '→←↑↓⟶⟵⟷↔▶◀▲▼'
            if any(char in content for char in arrow_chars):
                return True, 'ascii-art-arrows'
            
            # Check for simple arrow patterns (->)
            if re.search(r'[-=]+>', content) or re.search(r'<[-=]+', content):
                return True, 'ascii-art-arrows'
            
            # Check for tree patterns
            if re.search(r'[│├└─]{2,}', content):
                return True, 'ascii-art-tree'
            
            # Check for table patterns with +, -, |
            if re.search(r'[+\-|]{3,}', content) and re.search(r'\+[-+]+\+', content):
                return True, 'ascii-art-table'
            
            # Check for diagrams by structure
            lines = content.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            
            if len(non_empty_lines) > 2:
                # Check for subsystem names (architecture diagrams)
                subsystem_names = ['SYS_ADMIN', 'GL_CORE', 'IRS_CORE', 'SL_MGMT', 'PL_MGMT', 
                                 'ST_CTRL', 'BATCH_FW', 'RPT_ENGINE', 'DAL', 'PERIOD_PROC', 
                                 'COMMON_UTIL', 'INTEG_SVC']
                subsystem_count = sum(1 for name in subsystem_names if name in content)
                if subsystem_count >= 3:
                    return True, 'ascii-art-box'
                
                # Check for centered/aligned content
                if non_empty_lines:
                    leading_spaces = [len(line) - len(line.lstrip()) for line in non_empty_lines if line.strip()]
                    if leading_spaces and max(leading_spaces) > 8:
                        # Check if it's actually a diagram (not just indented code)
                        avg_line_length = sum(len(line.strip()) for line in non_empty_lines) / len(non_empty_lines)
                        if avg_line_length < 60 and 'via' in content.lower():
                            return True, 'ascii-art'
            
            return False, None
        
        # Process simple <pre><code> blocks (no syntax highlighting)
        def replace_simple_code_blocks(match):
            nonlocal ascii_art_count, total_blocks_checked
            total_blocks_checked += 1
            full_block = match.group(0)
            code_content = match.group(1)
            
            # Unescape HTML entities
            code_content_unescaped = html.unescape(code_content)
            
            is_ascii, css_class = check_if_ascii_art(code_content_unescaped)
            if is_ascii:
                ascii_art_count += 1
                return f'<pre class="{css_class}">{code_content}</pre>'
            else:
                return full_block
        
        # Process code blocks with syntax highlighting (codehilite)
        def replace_highlighted_code_blocks(match):
            nonlocal ascii_art_count, total_blocks_checked
            total_blocks_checked += 1
            full_block = match.group(0)
            code_content = match.group(1)
            
            # Remove all HTML tags to get clean text
            clean_text = re.sub(r'<[^>]+>', '', code_content)
            # Unescape HTML entities
            clean_text = html.unescape(clean_text)
            
            is_ascii, css_class = check_if_ascii_art(clean_text)
            if is_ascii:
                ascii_art_count += 1
                # For highlighted blocks, we need to preserve the text but remove syntax highlighting
                return f'<pre class="{css_class}">{html.escape(clean_text)}</pre>'
            else:
                return full_block
        
        # Replace simple code blocks that might contain ASCII art
        html_content = re.sub(
            r'<pre><code>(.*?)</code></pre>',
            replace_simple_code_blocks,
            html_content,
            flags=re.DOTALL
        )
        
        # Also process codehilite blocks (syntax-highlighted code)
        # First pattern: with <span></span><code>
        html_content = re.sub(
            r'<div class="codehilite">\s*<pre><span></span><code>(.*?)</code></pre>\s*</div>',
            replace_highlighted_code_blocks,
            html_content,
            flags=re.DOTALL
        )
        
        # Second pattern: direct <pre> without <code>
        html_content = re.sub(
            r'<div class="codehilite">\s*<pre>(.*?)</pre>\s*</div>',
            replace_highlighted_code_blocks,
            html_content,
            flags=re.DOTALL
        )
        
        if total_blocks_checked > 0:
            print(f"  → Checked {total_blocks_checked} code blocks, styled {ascii_art_count} as ASCII art")
        
        return html_content
    
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
        html_template = f'''
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
        
        /* ASCII Art - Base Style */
        .ascii-art, .ascii-art-box, .ascii-art-arrows, .ascii-art-tree, .ascii-art-table {{
            background: linear-gradient(145deg, #0a0e27 0%, #1a1e3a 100%);
            color: #00ff41;
            padding: 2rem;
            border-radius: 12px;
            overflow-x: auto;
            font-family: "Cascadia Code", "Fira Code", "Consolas", "Courier New", monospace;
            font-size: 0.9rem;
            line-height: 1.4;
            box-shadow: 
                0 8px 32px rgba(31, 38, 135, 0.37),
                inset 0 2px 4px rgba(0,0,0,0.3);
            border: 1px solid rgba(0, 255, 65, 0.3);
            position: relative;
            margin: 1.5rem 0;
            white-space: pre;
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        }}
        
        /* Terminal-like header effect */
        .ascii-art::before, .ascii-art-box::before, .ascii-art-arrows::before, 
        .ascii-art-tree::before, .ascii-art-table::before {{
            content: "◉ ◉ ◉";
            position: absolute;
            top: 10px;
            left: 15px;
            color: #ff5f56;
            font-size: 0.8rem;
            letter-spacing: 5px;
        }}
        
        /* Different color schemes for different types */
        .ascii-art-box {{
            color: #00d4ff;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
            border-color: rgba(0, 212, 255, 0.3);
        }}
        
        .ascii-art-arrows {{
            color: #ff6b6b;
            text-shadow: 0 0 10px rgba(255, 107, 107, 0.5);
            border-color: rgba(255, 107, 107, 0.3);
        }}
        
        .ascii-art-tree {{
            color: #4ecdc4;
            text-shadow: 0 0 10px rgba(78, 205, 196, 0.5);
            border-color: rgba(78, 205, 196, 0.3);
        }}
        
        .ascii-art-table {{
            color: #ffe66d;
            text-shadow: 0 0 10px rgba(255, 230, 109, 0.5);
            border-color: rgba(255, 230, 109, 0.3);
        }}
        
        /* Enhanced hover effect */
        .ascii-art:hover, .ascii-art-box:hover, .ascii-art-arrows:hover, 
        .ascii-art-tree:hover, .ascii-art-table:hover {{
            box-shadow: 
                0 8px 40px rgba(31, 38, 135, 0.5),
                inset 0 2px 4px rgba(0,0,0,0.3),
                0 0 80px rgba(0, 255, 65, 0.1);
            transform: translateY(-2px);
            transition: all 0.3s ease;
        }}
        
        /* Matrix-like animation for ASCII art */
        @keyframes matrix-glow {{
            0%, 100% {{ opacity: 0.8; }}
            50% {{ opacity: 1; }}
        }}
        
        .ascii-art::after {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(
                0deg,
                transparent 0%,
                rgba(0, 255, 65, 0.03) 50%,
                transparent 100%
            );
            animation: matrix-glow 2s ease-in-out infinite;
            pointer-events: none;
        }}
        
        /* Mermaid Diagrams */
        .mermaid {{
            text-align: center;
            background: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        
        .mermaid-container {{
            background: white;
            border-radius: 8px;
            padding: 1rem;
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
        // Initialize Mermaid
        mermaid.initialize({{ 
            theme: 'default',
            themeVariables: {{
                primaryColor: '#2c3e50',
                primaryTextColor: '#fff',
                primaryBorderColor: '#7C0000',
                lineColor: '#5D5D5D',
                secondaryColor: '#3498db',
                tertiaryColor: '#e74c3c'
            }},
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
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
        
        return html_template
    
    def generate_report(self):
        """Main method to generate the complete report"""
        print("ACAS Subsystems Documentation Report Generator")
        print("=" * 50)
        print(f"Base Path: {self.base_path}")
        print(f"Output File: {self.output_file}")
        print()
        
        try:
            print("Generating HTML report...")
            html_content = self.generate_html()
            
            print(f"Writing output to {self.output_file}...")
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print("\n✅ Report generated successfully!")
            print(f"📄 Output file: {self.output_file}")
            print(f"📏 File size: {os.path.getsize(self.output_file) / 1024:.2f} KB")
            print("\n🌐 Open the HTML file in a web browser to view the complete documentation.")
            
        except Exception as e:
            print(f"\n❌ Error generating report: {e}")
            raise


if __name__ == "__main__":
    generator = SubsystemsReportGenerator()
    generator.generate_report()