#!/usr/bin/env python
# -*- coding: utf-8 -*-

def markdown_to_pdf_simple(md_file, pdf_file):
    """简单将Markdown转换为PDF,保留中文"""
    
    try:
        from fpdf import FPDF
    except ImportError:
        try:
            from weasyprint import HTML, CSS
        except ImportError:
            # 使用基本HTML生成
            from html.parser import HTMLParser
            import webbrowser
            
            def convert_html_to_pdf(md_file, pdf_file):
                # 读取Markdown
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 简单的Markdown转HTML
                html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{ font-family: "Microsoft YaHei", "SimSun", sans-serif; font-size: 12pt; line-height: 1.6; }}
    h1 {{ font-size: 24pt; color: #333; border-bottom: 2px solid #333; padding: 10px 0; }}
    h2 {{ font-size: 18pt; color: #444; padding: 8px 0; }}
    h3 {{ font-size: 14pt; color: #555; }}
    p {{ margin: 8px 0; text-align: justify; }}
    table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    th {{ background-color: #f5f5f5; }}
    blockquote {{ border-left: 4px solid #ddd; padding-left: 16px; margin: 10px 0; color: #666; }}
    code {{ background-color: #f4f4f4; padding: 8px; font-family: monospace; }}
</style>
</head>
<body>
{content}
</body>
</html>"""
                
                # 保存HTML
                html_file = md_file.replace('.md', '.html')
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"HTML已生成: {{html_file}}")
                print(f"请使用浏览器打开HTML文件，然后打印/保存为PDF")
                print(f"或使用在线转换工具: https://cloudconvert.com/html-to-pdf")
                
                return html_file
            
            return convert_html_to_pdf(md_file, pdf_file)
    
    # 尝试使用fpdf
    try:
        from fpdf import FPDF
        
        class ChineseFPDF(FPDF):
            def __init__(self):
                super().__init__()
                self.add_font('SimSun', '', 'simsun.ttf')
        
        def convert_with_fpdf(md_file, pdf_file):
            pdf = ChineseFPDF()
            pdf.add_page()
            
            # 设置基本属性
            pdf.set_font('SimSun', '', 10)
            pdf.set_auto_page_break(auto=True, margin=15)
            
            # 读取并处理Markdown
            with open(md_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            x, y = 10, 10
            page_width = 190
            margin = 10
            line_height = 6
            
            for line in lines:
                line = line.rstrip()
                
                # 处理标题
                if line.startswith('#'):
                    level = len(line) - len(line.lstrip('#'))
                    text = line.lstrip('#').strip()
                    
                    if level == 1:
                        pdf.set_font('SimSun', '', 20)
                        pdf.ln(10)
                        y += 15
                        pdf.multi_cell(0, 10, text, 0, 1, 'C', '')
                        y += 10
                        pdf.set_font('SimSun', '', 10)
                        y += 5
                    elif level == 2:
                        pdf.ln(8)
                        pdf.set_font('SimSun', '', 14)
                        pdf.multi_cell(0, 7, text, 0, 1, 'C', '')
                        y += 7
                        pdf.set_font('SimSun', '', 10)
                    else:
                        pdf.ln(5)
                        pdf.set_font('SimSun', '', 12)
                        pdf.multi_cell(0, 6, text, 0, 1, 'C', '')
                        y += 6
                        pdf.set_font('SimSun', '', 10)
                
                # 处理表格
                elif line.startswith('|') and '|' in line:
                    # 简化:跳过表格
                    continue
                
                # 处理列表
                elif line.startswith('-') or line.startswith('*'):
                    text = line.lstrip('-* ').strip()
                    pdf.ln(4)
                    pdf.write(5, y, f"• {{text}}")
                    y += line_height
                
                # 处理空行
                elif line.strip() == '':
                    y += 3
                
                # 处理普通段落
                else:
                    if line.strip():
                        pdf.ln(2)
                        pdf.multi_cell(0, 7, line, 0, 0, 'J', '')
                        y += 7
                
                # 分页检查
                if y > 270:
                    pdf.add_page()
                    y = 10
            
            pdf.output(pdf_file)
            print(f"PDF已创建: {{pdf_file}}")
            return pdf_file
        
        return convert_with_fpdf(md_file, pdf_file)
        
    except Exception as e:
        print(f"FPDF失败: {{e}}")
        # 回退到HTML方案
        from html.parser import HTMLParser
        
        def convert_to_html(md_file, pdf_file):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{ font-family: sans-serif; font-size: 12pt; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
    h1 {{ font-size: 24pt; color: #2c3e50; border-bottom: 3px solid #d4a37; padding: 15px 0; }}
    h2 {{ font-size: 18pt; color: #d4a37; padding: 10px 0; }}
    h3 {{ font-size: 14pt; color: #5d4e37; }}
    p {{ margin: 10px 0; text-align: left; }}
    table {{ border-collapse: collapse; width: 100%; margin: 15px 0; border: 1px solid #ddd; }}
    th {{ background-color: #d4a37; color: white; padding: 10px; text-align: left; }}
    td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    blockquote {{ border-left: 4px solid #d4a37; padding-left: 16px; margin: 15px 0; background-color: #f9f9f9; }}
    hr {{ border: 0; height: 2px; background-color: #ddd; margin: 20px 0; }}
</style>
</head>
<body>
{{content}}
</body>
</html>"""
            
            html_file = md_file.replace('.md', '.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"HTML文件已创建: {{html_file}}")
            print(f"建议: 使用浏览器打开HTML文件，然后'打印'保存为PDF'")
            print(f"文件位置: {{html_file}}")
            
            return html_file
        
        return convert_to_html(md_file, pdf_file.replace('.md', '.html'))

if __name__ == '__main__':
    md_file = "六堡风云-剧本全集.md"
    pdf_file = "六堡风云-剧本全集.pdf"
    
    print("开始转换...")
    result = markdown_to_pdf_simple(md_file, pdf_file)
    print(f"转换完成! 输出文件: {{result}}")
    
    # 复制到手机存储
    import shutil
    import os
    
    phone_dir = "/storage/emulated/0/Download/"
    if os.path.exists(phone_dir):
        result_file = result
        dest_file = os.path.join(phone_dir, os.path.basename(result_file))
        shutil.copy(result_file, dest_file)
        print(f"已复制到手机存储: {{dest_file}}")
    else:
        print(f"手机存储目录不存在: {{phone_dir}}")
