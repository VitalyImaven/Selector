"""
Create Confluence-ready HTML from MASTER_TUTORIAL.md
"""
import re
from pathlib import Path


def markdown_to_confluence_html(markdown_file: Path, html_file: Path):
    """Convert markdown to Confluence-compatible HTML."""
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Automation Studio Selector - Complete Guide</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            color: #172b4d;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #0052cc;
            border-bottom: 3px solid #0052cc;
            padding-bottom: 10px;
            margin-top: 40px;
        }
        h2 {
            color: #00875a;
            border-bottom: 2px solid #00875a;
            padding-bottom: 8px;
            margin-top: 30px;
        }
        h3 {
            color: #172b4d;
            margin-top: 25px;
        }
        code {
            background-color: #f4f5f7;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 13px;
        }
        pre {
            background-color: #f4f5f7;
            border: 1px solid #dfe1e6;
            border-left: 4px solid #0052cc;
            padding: 16px;
            border-radius: 3px;
            overflow-x: auto;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 13px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }
        th {
            background-color: #f4f5f7;
            padding: 10px;
            text-align: left;
            border: 1px solid #dfe1e6;
            font-weight: 600;
        }
        td {
            padding: 10px;
            border: 1px solid #dfe1e6;
        }
        ul, ol {
            padding-left: 30px;
        }
        li {
            margin: 8px 0;
        }
        .info-box {
            background-color: #deebff;
            border-left: 4px solid #0052cc;
            padding: 16px;
            margin: 20px 0;
            border-radius: 3px;
        }
        .warning-box {
            background-color: #fffae6;
            border-left: 4px solid #ff991f;
            padding: 16px;
            margin: 20px 0;
            border-radius: 3px;
        }
        .success-box {
            background-color: #e3fcef;
            border-left: 4px solid #00875a;
            padding: 16px;
            margin: 20px 0;
            border-radius: 3px;
        }
        .cover-page {
            text-align: center;
            padding: 100px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            margin-bottom: 40px;
        }
        .cover-title {
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .cover-subtitle {
            font-size: 24px;
            margin-bottom: 30px;
        }
        .cover-info {
            font-size: 16px;
            opacity: 0.9;
        }
    </style>
</head>
<body>
"""
    
    # Add cover page
    html += """
    <div class="cover-page">
        <div class="cover-title">Automation Studio Selector</div>
        <div class="cover-subtitle">Complete User Guide</div>
        <div class="cover-info">
            Version 1.1.0<br>
            Created by Vitaly Grosman<br>
            Indigo R&D Division<br>
            © 2025
        </div>
    </div>
"""
    
    # Process markdown
    lines = content.split('\n')
    in_code_block = False
    in_table = False
    
    for line in lines:
        line = line.rstrip()
        
        # Skip metadata at top
        if line.startswith('**Version**') or line.startswith('**Created by**') or \
           line.startswith('**Organization**') or line.startswith('**©'):
            continue
        
        # Code blocks
        if line.startswith('```'):
            if in_code_block:
                html += "</pre>\n"
                in_code_block = False
            else:
                html += "<pre><code>"
                in_code_block = True
            continue
        
        if in_code_block:
            html += line + "\n"
            continue
        
        # Headers
        if line.startswith('# '):
            html += f"<h1>{clean_text(line[2:])}</h1>\n"
        elif line.startswith('## '):
            html += f"<h2>{clean_text(line[3:])}</h2>\n"
        elif line.startswith('### '):
            html += f"<h3>{clean_text(line[4:])}</h3>\n"
        elif line.startswith('#### '):
            html += f"<h4>{clean_text(line[5:])}</h4>\n"
        
        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            html += f"<li>{format_text(line[2:])}</li>\n"
        elif re.match(r'^\d+\. ', line):
            html += f"<li>{format_text(re.sub(r'^\d+\. ', '', line))}</li>\n"
        
        # Horizontal rules
        elif line.strip() == '---':
            html += "<hr>\n"
        
        # Regular paragraphs
        elif line.strip():
            if not line.startswith('#') and not line.startswith('|'):
                html += f"<p>{format_text(line)}</p>\n"
    
    html += """
</body>
</html>
"""
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Confluence HTML created: {html_file}")
    return True


def clean_text(text):
    """Remove markdown formatting."""
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text.strip()


def format_text(text):
    """Format inline markdown."""
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    
    # Check marks and X marks
    text = text.replace('✅', '<span style="color: #00875a;">✓</span>')
    text = text.replace('❌', '<span style="color: #de350b;">✗</span>')
    text = text.replace('☑', '<span style="color: #00875a;">☑</span>')
    
    return text


if __name__ == "__main__":
    markdown_file = Path("MASTER_TUTORIAL.md")
    html_file = Path("MASTER_TUTORIAL_Confluence.html")
    
    if markdown_to_confluence_html(markdown_file, html_file):
        print(f"\n[OK] SUCCESS!")
        print(f"HTML file created: {html_file.absolute()}")
        print(f"\nTo use in Confluence:")
        print(f"1. Open {html_file} in your web browser")
        print(f"2. Press Ctrl+A to select all")
        print(f"3. Press Ctrl+C to copy")
        print(f"4. Paste into Confluence page")
        print(f"\nOr import HTML directly into Confluence")
