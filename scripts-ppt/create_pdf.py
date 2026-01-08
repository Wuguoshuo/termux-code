#!/usr/bin/env python
# -*- coding: utf-8 -*-

def create_simple_pdf(md_file, pdf_file):
    """创建简单PDF文档"""
    try:
        from fpdf import FPDF
    except ImportError:
        print("FPDF未安装，请运行: pip install fpdf")
        return False
    
    # 读取Markdown文件
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建PDF
    pdf = FPDF()
    pdf.add_page()
    
    # 设置中文字体
    pdf.set_font('Arial', '', 10)
    
    # 分页设置
    margin_left = 15
    margin_top = 15
    margin_right = 15
    margin_bottom = 15
    page_width = 210 - margin_left - margin_right
    y_position = margin_top + 10
    x_position = margin_left
    
    # 处理Markdown内容
    lines = content.split('\n')
    
    for line in lines:
        # 标题处理
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('#').strip()
            if y_position > 50:
                pdf.add_page()
                y_position = margin_top + 10
            if level == 1:
                pdf.set_font_size(20)
                pdf.set_text_color(50, 50, 50)
                pdf.text(text, x_position, y_position)
                y_position += 12
            elif level == 2:
                pdf.set_font_size(16)
                pdf.set_text_color(50, 50, 50)
                pdf.text(text, x_position, y_position)
                y_position += 10
            else:
                pdf.set_font_size(14)
                pdf.set_text_color(80, 80, 80)
                pdf.text(text, x_position, y_position)
                y_position += 8
        
        # 表格行处理
        elif line.startswith('|') and '|' in line:
            # 跳过表格
            continue
        
        # 列表处理
        elif line.startswith('-') or line.startswith('*'):
            text = line.lstrip('-* ').strip()
            pdf.text(f"• {text}", x_position, y_position)
            y_position += 7
        
        # 空行处理
        elif line.strip() == '':
            y_position += 5
        
        # 普通段落
        else:
            if line.strip():
                words = line.split()
                current_line = ""
                for word in words:
                    if current_line:
                        test_width = pdf.get_string_width(current_line + " " + word)
                    else:
                        test_width = pdf.get_string_width(word)
                    
                    if x_position + test_width > page_width:
                        pdf.text(current_line, x_position, y_position)
                        y_position += 7
                        x_position = margin_left
                        current_line = word + " "
                    else:
                        current_line += word + " "
                
                if current_line:
                    pdf.text(current_line, x_position, y_position)
                    y_position += 7
        
        # 检查是否需要新页面
        if y_position > 280:
            pdf.add_page()
            y_position = margin_top + 10
            x_position = margin_left
    
    # 保存PDF
    pdf.output(pdf_file)
    print(f"PDF已创建: {pdf_file}")
    return True

if __name__ == '__main__':
    md_file = "六堡风云-剧本全集.md"
    pdf_file = "六堡风云-剧本全集.pdf"
    
    result = create_simple_pdf(md_file, pdf_file)
    
    if result:
        # 复制到手机存储
        import shutil
        import os
        
        phone_dir = "/storage/emulated/0/Download/"
        if os.path.exists(phone_dir):
            dest_file = os.path.join(phone_dir, os.path.basename(pdf_file))
            shutil.copy(pdf_file, dest_file)
            print(f"已复制到手机存储: {dest_file}")
        else:
            print(f"手机存储目录不存在: {phone_dir}")
