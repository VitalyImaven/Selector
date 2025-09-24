"""
Script to create an HTML version of the USER_TUTORIAL.md file that can be opened in Word.
"""
import re
from pathlib import Path


def markdown_to_html(markdown_file: Path, html_file: Path):
    """Convert markdown to HTML that Word can import."""
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Start HTML document
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Automation Studio Selector - User Tutorial</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            page-break-before: always;
        }
        h2 {
            color: #34495e;
            border-bottom: 2px solid #16a085;
            padding-bottom: 5px;
            margin-top: 30px;
        }
        h3 {
            color: #2c3e50;
            margin-top: 25px;
        }
        h4 {
            color: #34495e;
            margin-top: 20px;
        }
        .title-page {
            text-align: center;
            page-break-after: always;
            margin-top: 100px;
        }
        .main-title {
            font-size: 36px;
            color: #2c3e50;
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 24px;
            color: #7f8c8d;
            margin-bottom: 40px;
        }
        .version {
            font-size: 18px;
            color: #34495e;
            margin-bottom: 30px;
        }
        .author {
            font-size: 16px;
            color: #7f8c8d;
        }
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        ul, ol {
            margin-left: 20px;
        }
        li {
            margin-bottom: 5px;
        }
        .warning {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        .info {
            background-color: #e8f6f3;
            border-left: 4px solid #16a085;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        .error {
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin-left: 0;
            padding-left: 20px;
            color: #7f8c8d;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f8f9fa;
        }
    </style>
</head>
<body>
"""
        
        # Add title page
        html += """
    <div class="title-page">
        <div class="main-title">Automation Studio Selector</div>
        <div class="subtitle">Complete User Tutorial</div>
        <div class="version">Version 1.1.0</div>
        <div class="author">
            Created by: Vitaly Grosman<br>
            Indigo R&D Division<br>
            © 2025
        </div>
    </div>
"""
        
        # Process markdown content
        lines = content.split('\n')
        in_code_block = False
        
        for line in lines:
            line = line.rstrip()
            
            # Skip the markdown title and metadata at the top
            if line.startswith('# Automation Studio Selector') or \
               line.startswith('![Logo]') or \
               line.startswith('**Created by**') or \
               line.startswith('**Organization**') or \
               line.startswith('**Version**') or \
               line == '---':
                continue
            
            # Handle code blocks
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
            
            # Handle headers
            if line.startswith('##### '):
                html += f"<h5>{clean_header_text(line[6:])}</h5>\n"
            elif line.startswith('#### '):
                html += f"<h4>{clean_header_text(line[5:])}</h4>\n"
            elif line.startswith('### '):
                html += f"<h3>{clean_header_text(line[4:])}</h3>\n"
            elif line.startswith('## '):
                html += f"<h2>{clean_header_text(line[3:])}</h2>\n"
            elif line.startswith('# '):
                html += f"<h1>{clean_header_text(line[2:])}</h1>\n"
            
            # Handle lists
            elif line.startswith('- ') or line.startswith('* '):
                item_text = clean_markdown_text(line[2:])
                html += f"<li>{item_text}</li>\n"
            elif re.match(r'^\d+\. ', line):
                item_text = clean_markdown_text(re.sub(r'^\d+\. ', '', line))
                html += f"<li>{item_text}</li>\n"
            
            # Handle empty lines
            elif not line.strip():
                html += "<br>\n"
            
            # Handle regular paragraphs
            else:
                if line.strip() and not line.startswith('#'):
                    clean_line = clean_markdown_text(line)
                    if clean_line.strip():
                        html += f"<p>{clean_line}</p>\n"
        
        # Close HTML
        html += """
</body>
</html>
"""
        
        # Write HTML file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"HTML file created: {html_file}")
        return True
        
    except Exception as e:
        print(f"Error creating HTML file: {e}")
        return False


def clean_header_text(text):
    """Clean header text."""
    # Remove emojis
    text = re.sub(r'[🎯🚀🖥️⚡🔧💡📋📁📝📊🏠⚙️🔄👁️📦🔍🛡️⏰🔴🚪📄💾🔘❌✅📚🎨📐🎛️]', '', text)
    # Remove markdown bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    return text.strip()


def clean_markdown_text(text):
    """Clean markdown formatting."""
    # Remove emojis
    text = re.sub(r'[🎯🚀🖥️⚡🔧💡📋📁📝📊🏠⚙️🔄👁️📦🔍🛡️⏰🔴🚪📄💾🔘❌✅📚🎨📐🎛️]', '', text)
    # Convert bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Convert italic
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # Convert inline code
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text.strip()


if __name__ == "__main__":
    markdown_file = Path("USER_TUTORIAL.md")
    html_file = Path("Automation_Studio_Selector_Tutorial.html")
    
    if markdown_to_html(markdown_file, html_file):
        print(f"SUCCESS: Tutorial converted to HTML")
        print(f"File: {html_file.absolute()}")
        print(f"\nTo convert to Word:")
        print(f"1. Open {html_file} in your web browser")
        print(f"2. Press Ctrl+A to select all")
        print(f"3. Press Ctrl+C to copy")
        print(f"4. Open Microsoft Word")
        print(f"5. Press Ctrl+V to paste")
        print(f"6. Save as .docx file")
        print(f"\nAlternatively:")
        print(f"1. Open Microsoft Word")
        print(f"2. File → Open → {html_file}")
        print(f"3. Save As → Word Document (.docx)")
    else:
        print("ERROR: Failed to create tutorial")
