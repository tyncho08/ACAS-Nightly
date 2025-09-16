#!/usr/bin/env python3
"""
Final version of HTML generator with complete markdown parsing
"""

import re
from datetime import datetime

def read_manual():
    """Read the markdown manual"""
    with open('MANUAL.md', 'r', encoding='utf-8') as f:
        return f.read()

def preprocess_markdown(text):
    """Preprocess markdown to handle special cases"""
    # First, extract all code blocks to protect them
    code_blocks = []
    code_counter = 0
    
    # Match code blocks with or without language
    def replace_code_block(match):
        nonlocal code_counter
        full_block = match.group(0)
        lang = match.group(1) if match.group(1) else ''
        code = match.group(2)
        
        if lang == 'mermaid':
            placeholder = f"[[MERMAID_{code_counter}]]"
            code_blocks.append(('mermaid', code, placeholder))
        else:
            placeholder = f"[[CODE_{code_counter}]]"
            code_blocks.append(('code', (lang, code), placeholder))
        
        code_counter += 1
        return placeholder
    
    # Extract all code blocks first
    text = re.sub(r'```(\w*)\n(.*?)```', replace_code_block, text, flags=re.DOTALL)
    
    return text, code_blocks

def convert_lists(text):
    """Convert markdown lists to HTML"""
    lines = text.split('\n')
    output = []
    list_stack = []
    in_list = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Check if line is a list item
        list_match = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.+)$', line)
        
        if list_match:
            indent_level = len(list_match.group(1)) // 2
            marker = list_match.group(2)
            content = list_match.group(3)
            
            # Process inline markdown in the content
            content = process_inline_elements(content)
            
            list_type = 'ul' if marker in ['-', '*', '+'] else 'ol'
            
            # Manage list nesting
            if not in_list:
                output.append(f'<{list_type}>')
                list_stack.append((list_type, 0))
                in_list = True
            else:
                # Handle nesting changes
                while list_stack and list_stack[-1][1] > indent_level:
                    closed = list_stack.pop()
                    output.append(f'</{closed[0]}>')
                    output.append('</li>')
                
                if list_stack and list_stack[-1][1] < indent_level:
                    output.append(f'<{list_type}>')
                    list_stack.append((list_type, indent_level))
            
            output.append(f'<li>{content}</li>')
        
        else:
            # Not a list item - close any open lists
            if in_list and stripped and not stripped.startswith('[['):
                while list_stack:
                    closed = list_stack.pop()
                    output.append(f'</{closed[0]}>')
                in_list = False
            
            output.append(line)
    
    # Close any remaining lists
    while list_stack:
        closed = list_stack.pop()
        output.append(f'</{closed[0]}>')
    
    return '\n'.join(output)

def process_inline_elements(text):
    """Process inline markdown elements"""
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # Italic
    text = re.sub(r'\*([^*\n]+)\*', r'<em>\1</em>', text)
    
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    return text

def convert_markdown_to_html(text, code_blocks):
    """Convert markdown to HTML with better handling"""
    lines = text.split('\n')
    output = []
    in_paragraph = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            if in_paragraph:
                output.append('</p>')
                in_paragraph = False
            output.append('')
            i += 1
            continue
        
        # Headers
        if line.startswith('#'):
            if in_paragraph:
                output.append('</p>')
                in_paragraph = False
                
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                content = process_inline_elements(match.group(2))
                anchor = create_anchor(match.group(2))
                output.append(f'<h{level} id="{anchor}">{content}</h{level}>')
                i += 1
                continue
        
        # Horizontal rules
        if line.strip() in ['---', '***', '___']:
            if in_paragraph:
                output.append('</p>')
                in_paragraph = False
            output.append('<hr>')
            i += 1
            continue
        
        # Tables
        if '|' in line and i + 1 < len(lines) and '|' in lines[i + 1] and '-' in lines[i + 1]:
            if in_paragraph:
                output.append('</p>')
                in_paragraph = False
                
            table_html = parse_table(lines, i)
            if table_html:
                output.append(table_html)
                # Skip table lines
                while i < len(lines) and '|' in lines[i]:
                    i += 1
                continue
        
        # Code block placeholders
        if line.strip().startswith('[[CODE_') or line.strip().startswith('[[MERMAID_'):
            if in_paragraph:
                output.append('</p>')
                in_paragraph = False
            output.append(line)
            i += 1
            continue
        
        # Regular text
        if line.strip():
            processed = process_inline_elements(line)
            
            # Check if it's a citation
            if line.strip().startswith('*Source:') or (line.strip().startswith('*') and line.strip().endswith('*')):
                if in_paragraph:
                    output.append('</p>')
                    in_paragraph = False
                output.append(f'<p class="source-citation">{processed}</p>')
            else:
                if not in_paragraph:
                    output.append('<p>')
                    in_paragraph = True
                output.append(processed)
        
        i += 1
    
    if in_paragraph:
        output.append('</p>')
    
    # Convert lists
    html_text = '\n'.join(output)
    html_text = convert_lists(html_text)
    
    # Restore code blocks
    for block_type, content, placeholder in code_blocks:
        if block_type == 'mermaid':
            replacement = f'<div class="mermaid">\n{content}\n</div>'
        else:
            lang, code = content
            if lang:
                replacement = f'<pre><code class="language-{lang}">{html_escape(code)}</code></pre>'
            else:
                replacement = f'<pre><code>{html_escape(code)}</code></pre>'
        
        html_text = html_text.replace(placeholder, replacement)
    
    return html_text

def html_escape(text):
    """Escape HTML special characters"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))

def create_anchor(text):
    """Create URL-safe anchor from text"""
    # Remove markdown formatting
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    # Convert to lowercase and replace spaces
    anchor = text.lower()
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    anchor = re.sub(r'\s+', '-', anchor)
    anchor = anchor.strip('-')
    
    return anchor

def parse_table(lines, start_index):
    """Parse markdown table"""
    if start_index >= len(lines):
        return None
        
    header_line = lines[start_index]
    if '|' not in header_line:
        return None
        
    # Check for separator line
    if start_index + 1 >= len(lines) or '|' not in lines[start_index + 1]:
        return None
        
    separator_line = lines[start_index + 1]
    if not re.search(r'-+', separator_line):
        return None
    
    # Parse headers
    headers = [cell.strip() for cell in header_line.split('|') if cell.strip()]
    
    # Start table
    html = '<table>\n<thead>\n<tr>\n'
    for header in headers:
        html += f'<th>{process_inline_elements(header)}</th>\n'
    html += '</tr>\n</thead>\n<tbody>\n'
    
    # Parse body rows
    i = start_index + 2
    while i < len(lines) and '|' in lines[i]:
        cells = [cell.strip() for cell in lines[i].split('|') if cell.strip()]
        if cells:
            html += '<tr>\n'
            for cell in cells:
                html += f'<td>{process_inline_elements(cell)}</td>\n'
            html += '</tr>\n'
        i += 1
    
    html += '</tbody>\n</table>'
    return html

def extract_toc(content):
    """Extract table of contents from markdown"""
    toc = []
    for line in content.split('\n'):
        if line.startswith('#'):
            match = re.match(r'^(#{1,3})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                text = match.group(2)
                # Remove markdown formatting
                clean_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
                clean_text = re.sub(r'\*([^*]+)\*', r'\1', clean_text)
                anchor = create_anchor(text)
                toc.append((level, clean_text, anchor))
    return toc

def build_toc_html(toc):
    """Build HTML for table of contents"""
    if not toc:
        return ''
    
    html = []
    current_level = 0
    
    for level, text, anchor in toc:
        if level > current_level:
            # Open new level
            for _ in range(current_level, level):
                html.append('<ul>')
        elif level < current_level:
            # Close levels
            for _ in range(level, current_level):
                html.append('</ul>')
        
        html.append(f'<li><a href="#{anchor}">{text}</a></li>')
        current_level = level
    
    # Close remaining levels
    for _ in range(current_level):
        html.append('</ul>')
    
    return '\n'.join(html)

def create_html_manual(markdown_content):
    """Create complete HTML manual"""
    # Remove YAML frontmatter
    if markdown_content.startswith('---'):
        end = markdown_content.find('---', 3)
        markdown_content = markdown_content[end + 3:].strip()
    
    # Extract TOC
    toc = extract_toc(markdown_content)
    toc_html = build_toc_html(toc)
    
    # Preprocess to extract code blocks
    processed_content, code_blocks = preprocess_markdown(markdown_content)
    
    # Convert to HTML
    html_content = convert_markdown_to_html(processed_content, code_blocks)
    
    # Create complete HTML
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACAS Technical Manual</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        /* Reset and base styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #24292e;
            background-color: #f6f8fa;
        }}
        
        /* Layout */
        .container {{
            display: flex;
            min-height: 100vh;
        }}
        
        /* Sidebar Navigation */
        .sidebar {{
            width: 350px;
            background-color: #ffffff;
            border-right: 1px solid #e1e4e8;
            padding: 24px;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}
        
        .sidebar h2 {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #24292e;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Table of Contents */
        .sidebar > ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .sidebar ul ul {{
            list-style: none;
            padding-left: 20px;
            margin-top: 4px;
        }}
        
        .sidebar li {{
            margin: 4px 0;
        }}
        
        .sidebar a {{
            color: #0969da;
            text-decoration: none;
            display: block;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 14px;
            transition: all 0.2s ease;
        }}
        
        .sidebar a:hover {{
            background-color: #f3f4f6;
            color: #0550ae;
        }}
        
        .sidebar a.active {{
            background-color: #dbeafe;
            color: #0550ae;
            font-weight: 500;
        }}
        
        /* Main Content */
        .main-content {{
            margin-left: 350px;
            flex: 1;
            background-color: #ffffff;
            min-height: 100vh;
        }}
        
        .header {{
            background: linear-gradient(135deg, #0969da 0%, #0550ae 100%);
            color: white;
            padding: 48px 0;
            text-align: center;
            border-bottom: 1px solid #e1e4e8;
        }}
        
        .header h1 {{
            font-size: 40px;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }}
        
        .header .subtitle {{
            font-size: 20px;
            opacity: 0.9;
            font-weight: 300;
        }}
        
        .header .version {{
            margin-top: 16px;
            font-size: 14px;
            opacity: 0.8;
        }}
        
        .content {{
            padding: 32px 48px;
            max-width: 980px;
            margin: 0 auto;
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
            color: #24292e;
        }}
        
        h1 {{
            font-size: 32px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e1e4e8;
            margin-top: 32px;
        }}
        
        h2 {{
            font-size: 24px;
            margin-top: 32px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e1e4e8;
        }}
        
        h3 {{
            font-size: 20px;
            margin-top: 24px;
        }}
        
        h4 {{
            font-size: 16px;
        }}
        
        p {{
            margin-bottom: 16px;
            line-height: 1.7;
        }}
        
        /* Lists */
        ul, ol {{
            margin-left: 24px;
            margin-bottom: 16px;
        }}
        
        li {{
            margin-bottom: 4px;
            line-height: 1.7;
        }}
        
        /* Code */
        pre {{
            background-color: #f6f8fa;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            margin: 16px 0;
            font-family: 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 14px;
            line-height: 1.45;
        }}
        
        code {{
            background-color: rgba(175,184,193,0.2);
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 85%;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            font-size: 14px;
        }}
        
        /* Tables */
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
            font-size: 14px;
        }}
        
        th, td {{
            border: 1px solid #e1e4e8;
            padding: 8px 16px;
            text-align: left;
        }}
        
        th {{
            background-color: #f6f8fa;
            font-weight: 600;
        }}
        
        tr:nth-child(even) {{
            background-color: #f6f8fa;
        }}
        
        /* Mermaid Diagrams */
        .mermaid {{
            margin: 24px 0;
            text-align: center;
            background-color: #f6f8fa;
            padding: 24px;
            border-radius: 6px;
            border: 1px solid #e1e4e8;
            overflow-x: auto;
        }}
        
        /* Links */
        a {{
            color: #0969da;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        /* Source citations */
        .source-citation {{
            color: #57606a;
            font-style: italic;
            font-size: 14px;
            margin-top: -8px;
        }}
        
        /* Strong text */
        strong {{
            font-weight: 600;
            color: #24292e;
        }}
        
        /* HR */
        hr {{
            margin: 32px 0;
            border: 0;
            border-top: 1px solid #e1e4e8;
        }}
        
        /* Status badges */
        .status-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
            margin-left: 8px;
            vertical-align: middle;
        }}
        
        .not-implemented {{
            background-color: #fb8500;
            color: white;
        }}
        
        .complete {{
            background-color: #2da44e;
            color: white;
        }}
        
        /* Print styles */
        @media print {{
            .sidebar {{
                display: none;
            }}
            
            .main-content {{
                margin-left: 0;
            }}
            
            .header {{
                background: none;
                color: black;
                border-bottom: 2px solid black;
            }}
            
            pre {{
                border: 1px solid #ccc;
            }}
            
            .mermaid {{
                page-break-inside: avoid;
            }}
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .sidebar {{
                position: relative;
                width: 100%;
                height: auto;
                border-right: none;
                border-bottom: 1px solid #e1e4e8;
            }}
            
            .main-content {{
                margin-left: 0;
            }}
            
            .content {{
                padding: 24px;
            }}
        }}
        
        /* Syntax highlighting */
        .language-bash {{
            color: #032f62;
        }}
        
        .language-sql {{
            color: #0550ae;
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="sidebar">
            <h2>📚 Table of Contents</h2>
            {toc_html}
        </nav>
        
        <main class="main-content">
            <header class="header">
                <h1>ACAS Technical Manual</h1>
                <div class="subtitle">Applewood Computers Accounting System</div>
                <div class="version">Version 1.0 • {datetime.now().strftime('%B %d, %Y')}</div>
            </header>
            
            <div class="content">
                {html_content}
            </div>
        </main>
    </div>
    
    <script>
        // Initialize Mermaid
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            themeVariables: {{
                primaryColor: '#0969da',
                primaryTextColor: '#fff',
                primaryBorderColor: '#0550ae',
                lineColor: '#57606a',
                secondaryColor: '#f6f8fa',
                tertiaryColor: '#dbeafe'
            }}
        }});
        
        // Smooth scrolling
        document.querySelectorAll('.sidebar a').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const target = document.getElementById(targetId);
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});
        
        // Highlight NOT IMPLEMENTED
        document.addEventListener('DOMContentLoaded', function() {{
            document.querySelectorAll('strong').forEach(el => {{
                const text = el.textContent;
                if (text.includes('NOT IMPLEMENTED')) {{
                    el.innerHTML = text.replace(/NOT IMPLEMENTED:?/g, '<span class="status-badge not-implemented">NOT IMPLEMENTED</span>');
                }}
                if (text.includes('COMPLETE')) {{
                    el.innerHTML = text.replace(/COMPLETE:?/g, '<span class="status-badge complete">COMPLETE</span>');
                }}
            }});
        }});
        
        // Active section highlighting
        function updateActiveSection() {{
            const sections = document.querySelectorAll('h1[id], h2[id], h3[id]');
            const tocLinks = document.querySelectorAll('.sidebar a');
            
            let currentSection = null;
            const scrollPosition = window.scrollY + 100;
            
            sections.forEach(section => {{
                if (section.offsetTop <= scrollPosition) {{
                    currentSection = section.id;
                }}
            }});
            
            tocLinks.forEach(link => {{
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + currentSection) {{
                    link.classList.add('active');
                }}
            }});
        }}
        
        window.addEventListener('scroll', updateActiveSection);
        updateActiveSection();
    </script>
</body>
</html>'''
    
    return html_template

def main():
    """Generate the HTML manual"""
    print("Reading manual...")
    manual_content = read_manual()
    
    print("Generating final HTML with complete markdown parsing...")
    html_content = create_html_manual(manual_content)
    
    print("Writing HTML file...")
    output_file = 'ACAS_Technical_Manual.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    file_size = len(html_content) / 1024 / 1024
    print(f"Done! HTML manual created as {output_file} ({file_size:.2f} MB)")

if __name__ == '__main__':
    main()