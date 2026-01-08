#!/usr/bin/env python
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
import os

# 检查中文字体
def find_chinese_font():
    """查找可用的中文字体"""
    font_paths = [
        '/system/fonts/NotoSansCJK-Regular.ttc',
        '/system/fonts/DroidSansFallback.ttf',
        '/data/fonts/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            return font_path

    return None

# 创建PDF
def create_novel_pdf():
    # PDF文件路径
    pdf_path = '/data/data/com.termux/files/home/六堡风云-完整版.pdf'
    phone_path = '/storage/emulated/0/Download/六堡风云-完整版.pdf'

    # 创建PDF文档
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)

    # 获取样式
    styles = getSampleStyleSheet()

    # 查找中文字体
    chinese_font = find_chinese_font()

    if chinese_font:
        # 注册中文字体
        pdfmetrics.registerFont(TTFont('ChineseFont', chinese_font))
        font_name = 'ChineseFont'
    else:
        # 如果没有找到中文字体,使用默认字体
        font_name = 'Helvetica'

    # 创建自定义样式
    title_style = ParagraphStyle(
        'NovelTitle',
        parent=styles['Title'],
        fontName=font_name,
        fontSize=24,
        leading=30,
        spaceAfter=20,
        alignment=1  # 居中
    )

    chapter_title_style = ParagraphStyle(
        'ChapterTitle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=18,
        leading=24,
        spaceBefore=20,
        spaceAfter=12,
        textColor='#2c3e50'
    )

    body_style = ParagraphStyle(
        'NovelBody',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=11,
        leading=18,
        spaceAfter=8,
        alignment=0  # 左对齐
    )

    # 小说内容
    story = []

    # 添加书名
    story.append(Paragraph("六堡风云", title_style))
    story.append(Spacer(1, 1*cm))

    # 添加作者信息
    story.append(Paragraph("作者: 陈阿三", body_style))
    story.append(Paragraph("创作时间: 2025年", body_style))
    story.append(Spacer(1, 1*cm))

    # 添加简介
    story.append(Paragraph("简介", chapter_title_style))
    intro_text = """
    这是一个关于六堡茶传承的故事，讲述了陈阿三从学徒到茶厂厂长的成长历程。
    在这个过程中，他经历了友情、背叛、坚持和传承。
    六堡茶不仅是一种茶，更是一种文化，一种根。
    根不能丢，传承不能断。
    """
    story.append(Paragraph(intro_text, body_style))
    story.append(Spacer(1, 0.5*cm))

    # 章节列表
    chapters = [
        "第 1 章：命运的安排",
        "第 2 章：学艺的日子",
        "第 3 章：渥堆初体验",
        "第 4 章：陈化的等待",
        "第 5 章：分歧的开始",
        "第 6 章：风波来了",
        "第 7 章：出走的决定",
        "第 8 章：外面的世界",
        "第 9 章：归来的决定",
        "第 10 章：传承的开始"
    ]

    # 读取所有章节
    base_path = '/data/data/com.termux/files/home/projects/web/novel-writing/drafts'

    for i, chapter in enumerate(chapters, 1):
        # 添加章节标题
        story.append(Paragraph(chapter, chapter_title_style))

        # 读取章节内容
        chapter_file = f'{base_path}/六堡风云-第{i}章-{chapter.split("：")[1]}.md'

        if os.path.exists(chapter_file):
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 移除Markdown标题(# 第 X 章：...)
            lines = content.split('\n')
            content_lines = []
            for line in lines:
                if not line.startswith('# 第'):
                    content_lines.append(line)

            content = '\n'.join(content_lines)

            # 将Markdown转换为HTML格式
            html_content = content.replace('\n\n', '<br/><br/>').replace('\n', '<br/>')

            # 添加章节内容
            story.append(Paragraph(html_content, body_style))
        else:
            story.append(Paragraph(f"章节文件未找到: {chapter_file}", body_style))

        # 添加分页符(除了最后一章)
        if i < len(chapters):
            story.append(PageBreak())

    # 生成PDF
    try:
        doc.build(story)
        print(f"✓ PDF已创建: {pdf_path}")
        print(f"  文件大小: {os.path.getsize(pdf_path)/1024:.2f} KB")

        # 复制到手机存储
        if os.path.exists('/storage/emulated/0/Download/'):
            import shutil
            shutil.copy2(pdf_path, phone_path)
            print(f"✓ 已复制到手机存储: {phone_path}")
        else:
            print(f"✗ 手机存储目录不存在")

        return True
    except Exception as e:
        print(f"✗ 创建PDF失败: {e}")
        return False

if __name__ == '__main__':
    print("开始生成《六堡风云》完整版PDF...")
    print("-" * 50)

    success = create_novel_pdf()

    print("-" * 50)
    if success:
        print("✓ PDF生成完成!")
    else:
        print("✗ PDF生成失败!")
