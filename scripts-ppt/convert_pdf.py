import markdown
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, pt
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Chinese fonts (will use standard if not available)
try:
    chinese_font = TTFont('Chinese', '/system/fonts/SourceHanSansCN-Regular.otf', '')
    pdfmetrics.registerFont(chinese_font)
except:
    chinese_font = None
    print("Warning: Chinese font not found, using Helvetica")

def markdown_to_pdf(markdown_file, pdf_file):
    """Convert Markdown file to PDF with Chinese support"""
    
    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate(pdf_file, pagesize=A4, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    
    # Convert markdown to HTML first (simple approach)
    html_content = markdown.markdown(md_content)
    
    # Parse basic markdown
    lines = md_content.split('\n')
    story = []
    
    for line in lines:
        if line.startswith('# '):
            # Heading
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('#').strip()
            if level == 1:
                p = Paragraph(text, styles['Heading1'])
            elif level == 2:
                p = Paragraph(text, styles['Heading2'])
            elif level == 3:
                p = Paragraph(text, styles['Heading3'])
            else:
                p = Paragraph(text, styles['Heading4'])
            story.append(p)
            story.append(Spacer(1, 0.2*inch))
        elif line.startswith('|') and '|' in line:
            # Table row - skip for now
            continue
        elif line.startswith('-') or line.startswith('*'):
            # Bullet point
            text = line.lstrip('-* ').strip()
            p = Paragraph(text, styles['Bullet'])
            story.append(p)
        elif line.strip() == '':
            # Empty line
            story.append(Spacer(1, 0.1*inch))
        else:
            # Regular text
            if line.strip():
                p = Paragraph(line, styles['BodyText'])
                story.append(p)
    
    # Build PDF
    doc.build(story)
    print(f"PDF created: {pdf_file}")

if __name__ == "__main__":
    markdown_to_pdf("六堡风云-剧本全集.md", "六堡风云-剧本全集.pdf")
