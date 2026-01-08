#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from weasyprint import HTML, CSS

# 使用weasyprint生成PDF
def create_script_pdf():
    # PDF文件路径
    pdf_path = '/data/data/com.termux/files/home/六堡风云-剧本全集-完整版.pdf'
    phone_path = '/storage/emulated/0/Download/六堡风云-剧本全集-完整版.pdf'

    # 读取剧本文件
    script_file = '/data/data/com.termux/files/home/scripts-ppt/六堡风云-剧本全集.md'

    with open(script_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 将Markdown转换为HTML
    html_content = content.replace('\n\n', '</p><p>').replace('\n', '<br/>')
    html_content = f'<p>{html_content}</p>'

    # HTML模板
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>六堡风云 - 剧本全集</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}

        body {{
            font-family: "Microsoft YaHei", "SimSun", "Noto Sans CJK", sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }}

        h1 {{
            font-size: 24pt;
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #d4a574;
            padding-bottom: 20px;
            margin-bottom: 30px;
            page-break-after: avoid;
        }}

        h2 {{
            font-size: 18pt;
            color: #d4a574;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
            margin-top: 40px;
            margin-bottom: 20px;
            page-break-after: avoid;
        }}

        h3 {{
            font-size: 14pt;
            color: #5d4e37;
            margin-top: 25px;
            margin-bottom: 15px;
            page-break-after: avoid;
        }}

        p {{
            margin: 8px 0;
            text-align: justify;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            border: 1px solid #ddd;
        }}

        th {{
            background-color: #d4a574;
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: bold;
        }}

        td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}

        blockquote {{
            border-left: 4px solid #d4a574;
            padding-left: 16px;
            margin: 15px 0;
            background-color: #f9f9f9;
            font-style: italic;
        }}

        hr {{
            border: 0;
            height: 2px;
            background-color: #ddd;
            margin: 30px 0;
        }}

        .scene {{
            background-color: #f5f5f5;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #d4a574;
        }}

        .scene p {{
            text-indent: 0;
        }}

        .dialogue {{
            margin: 10px 0;
            padding-left: 20px;
        }}

        .action {{
            margin: 10px 0;
            font-style: italic;
            color: #666;
        }}

        .episode {{
            page-break-before: always;
        }}

        .episode-info {{
            text-align: right;
            color: #999;
            font-size: 10pt;
            margin-top: 20px;
            border-top: 1px solid #eee;
            padding-top: 10px;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""

    # 生成PDF
    try:
        html_doc = HTML(string=html_template)
        html_doc.write_pdf(pdf_path)

        print(f"✓ PDF已创建: {pdf_path}")
        print(f"  文件大小: {os.path.getsize(pdf_path)/1024:.2f} KB")

        # 复制到手机存储
        if os.path.exists('/storage/emulated/0/Download/'):
            shutil.copy2(pdf_path, phone_path)
            print(f"✓ 已复制到手机存储: {phone_path}")
        else:
            print(f"✗ 手机存储目录不存在")

        return True
    except Exception as e:
        print(f"✗ 创建PDF失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("开始生成《六堡风云》剧本全集PDF...")
    print("-" * 50)

    success = create_script_pdf()

    print("-" * 50)
    if success:
        print("✓ PDF生成完成!")
    else:
        print("✗ PDF生成失败!")
