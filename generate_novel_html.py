#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

# 创建HTML格式的小说
def create_novel_html():
    # HTML文件路径
    html_path = '/data/data/com.termux/files/home/六堡风云-完整版.html'
    phone_path = '/storage/emulated/0/Download/六堡风云-完整版.html'

    # HTML模板
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>六堡风云 - 完整版</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", "SimSun", "Noto Sans CJK", sans-serif;
            font-size: 12pt;
            line-height: 1.8;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #f5f5f5;
        }}

        .container {{
            background-color: white;
            padding: 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        h1 {{
            font-size: 28pt;
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #d4a574;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}

        .author {{
            text-align: center;
            color: #666;
            margin-bottom: 40px;
        }}

        h2 {{
            font-size: 18pt;
            color: #d4a574;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
            margin-top: 40px;
            margin-bottom: 20px;
        }}

        h3 {{
            font-size: 16pt;
            color: #5d4e37;
            margin-top: 30px;
            margin-bottom: 15px;
        }}

        p {{
            margin: 10px 0;
            text-align: justify;
            text-indent: 2em;
        }}

        .intro {{
            background-color: #f9f9f9;
            padding: 20px;
            border-left: 4px solid #d4a574;
            margin-bottom: 30px;
        }}

        .intro p {{
            text-indent: 0;
        }}

        .chapter {{
            page-break-before: always;
        }}

        .chapter-info {{
            text-align: right;
            color: #999;
            font-size: 10pt;
            margin-top: 20px;
            border-top: 1px solid #eee;
            padding-top: 10px;
        }}

        @media print {{
            body {{
                background-color: white;
            }}
            .container {{
                box-shadow: none;
                padding: 0;
            }}
            .chapter {{
                page-break-before: always;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>六堡风云</h1>
        <div class="author">
            <p>作者: 陈阿三</p>
            <p>创作时间: 2025年</p>
        </div>

        <div class="intro">
            <h2>简介</h2>
            <p>这是一个关于六堡茶传承的故事，讲述了陈阿三从学徒到茶厂厂长的成长历程。</p>
            <p>在这个过程中，他经历了友情、背叛、坚持和传承。</p>
            <p>六堡茶不仅是一种茶，更是一种文化，一种根。</p>
            <p>根不能丢，传承不能断。</p>
        </div>

        {chapters_content}
    </div>
</body>
</html>
"""

    # 章节列表
    chapters = [
        ("第 1 章：命运的安排", 1),
        ("第 2 章：学艺的日子", 2),
        ("第 3 章：渥堆初体验", 3),
        ("第 4 章：陈化的等待", 4),
        ("第 5 章：分歧的开始", 5),
        ("第 6 章：风波来了", 6),
        ("第 7 章：出走的决定", 7),
        ("第 8 章：外面的世界", 8),
        ("第 9 章：归来的决定", 9),
        ("第 10 章：传承的开始", 10)
    ]

    # 读取所有章节
    base_path = '/data/data/com.termux/files/home/projects/web/novel-writing/drafts'
    chapters_content = []

    for chapter_title, chapter_num in chapters:
        chapter_file = f'{base_path}/六堡风云-第{chapter_num}章-{chapter_title.split("：")[1]}.md'

        if os.path.exists(chapter_file):
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 移除Markdown标题(# 第 X 章：...)
            lines = content.split('\n')
            content_lines = []
            for line in lines:
                if not line.startswith('# 第') and not line.startswith('**'):
                    content_lines.append(line)

            content = '\n'.join(content_lines)

            # 将Markdown转换为HTML格式
            html_content = content.replace('\n\n', '</p><p>').replace('\n', '<br/>')
            html_content = f'<p>{html_content}</p>'

            # 添加章节
            chapter_html = f'''
        <div class="chapter">
            <h2>{chapter_title}</h2>
            {html_content}
        </div>
'''
            chapters_content.append(chapter_html)
        else:
            chapters_content.append(f'<div class="chapter"><h2>{chapter_title}</h2><p>章节文件未找到: {chapter_file}</p></div>')

    # 生成完整HTML
    full_html = html_template.format(chapters_content=''.join(chapters_content))

    # 保存HTML文件
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

        print(f"✓ HTML已创建: {html_path}")
        print(f"  文件大小: {os.path.getsize(html_path)/1024:.2f} KB")

        # 复制到手机存储
        if os.path.exists('/storage/emulated/0/Download/'):
            shutil.copy2(html_path, phone_path)
            print(f"✓ 已复制到手机存储: {phone_path}")
        else:
            print(f"✗ 手机存储目录不存在")

        return True
    except Exception as e:
        print(f"✗ 创建HTML失败: {e}")
        return False

if __name__ == '__main__':
    print("开始生成《六堡风云》完整版HTML...")
    print("-" * 50)

    success = create_novel_html()

    print("-" * 50)
    if success:
        print("✓ HTML生成完成!")
        print("\n使用说明:")
        print("1. 在浏览器中打开 HTML 文件")
        print("2. 按 Ctrl+P (或菜单中的打印)")
        print("3. 选择'保存为 PDF'")
        print("4. 保存即可得到 PDF 文档")
    else:
        print("✗ HTML生成失败!")