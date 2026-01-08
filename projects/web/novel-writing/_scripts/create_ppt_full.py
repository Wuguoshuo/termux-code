#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create PPT with all scripts - including full script content"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# Read all script files
import os

script_files = [
    "第1集-命运的安排.md",
    "第2集-学艺的日子.md",
    "第3集-渥堆初体验.md",
    "第4集-陈化的等待.md",
    "第5集-分歧的开始.md",
    "第6集-风波来了.md",
    "第7集-出走的决定.md",
    "第8集-外面的世界.md",
    "第9集-归来的决定.md",
    "第10集-传承的开始.md"
]

scripts_dir = "/data/data/com.termux/files/home/projects/web/novel-writing/_scripts/drafts/"

# Read script content
def read_script_file(filename):
    filepath = os.path.join(scripts_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

# Create presentation
prs = Presentation()
prs.slide_width = Inches(16)
prs.slide_height = Inches(9)

# Define colors
BLUE = (0, 112, 192)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Function to create title slide
def create_title_slide(title, subtitle):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    
    # Get title and subtitle placeholders
    title_placeholder = slide.placeholders[0]
    subtitle_placeholder = slide.placeholders[1]
    
    title_placeholder.text = title
    subtitle_placeholder.text = subtitle
    
    return slide

# Function to create table of contents slide
def create_toc_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank layout
    
    # Add title
    left = Inches(1)
    top = Inches(1)
    width = Inches(14)
    height = Inches(1)
    
    title_box = slide.shapes.add_textbox(left, top, width, height)
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "《六堡风云》短剧剧本目录"
    p.font.size = Pt(36)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = BLUE
    
    # Add table of contents
    left = Inches(1)
    top = Inches(2.5)
    width = Inches(14)
    height = Inches(5)
    
    toc_box = slide.shapes.add_textbox(left, top, width, height)
    tf = toc_box.text_frame
    tf.word_wrap = True
    
    episodes = [
        "第1集：命运的安排",
        "第2集：学艺的日子",
        "第3集：渥堆初体验",
        "第4集：陈化的等待",
        "第5集：分歧的开始",
        "第6集：风波来了",
        "第7集：出走的决定",
        "第8集：外面的世界",
        "第9集：归来的决定",
        "第10集：传承的开始"
    ]
    
    for episode in episodes:
        p = tf.add_paragraph()
        p.text = episode
        p.font.size = Pt(24)
        p.level = 0
    
    return slide

# Function to create episode slide with full script
def create_episode_slide_full(episode_num, episode_title, script_content):
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank layout
    
    # Add title
    left = Inches(1)
    top = Inches(0.5)
    width = Inches(14)
    height = Inches(0.8)
    
    title_box = slide.shapes.add_textbox(left, top, width, height)
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"第{episode_num}集：{episode_title}"
    p.font.size = Pt(28)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = BLUE
    
    # Add content
    left = Inches(0.5)
    top = Inches(1.5)
    width = Inches(15)
    height = Inches(7)
    
    content_box = slide.shapes.add_textbox(left, top, width, height)
    tf = content_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = script_content
    p.font.size = Pt(14)
    p.font.name = "Microsoft YaHei UI"
    p.alignment = PP_ALIGN.LEFT
    
    return slide

# Function to create summary slide
def create_summary_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    
    # Add title
    left = Inches(1)
    top = Inches(0.5)
    width = Inches(14)
    height = Inches(0.8)
    
    title_box = slide.shapes.add_textbox(left, top, width, height)
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "剧本总结"
    p.font.size = Pt(28)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = BLUE
    
    # Add content
    left = Inches(0.5)
    top = Inches(2)
    width = Inches(15)
    height = Inches(6)
    
    content_box = slide.shapes.add_textbox(left, top, width, height)
    tf = content_box.text_frame
    tf.word_wrap = True
    
    content = """
《六堡风云》短剧剧本

基本信息：
- 总集数：10集
- 单集时长：5分钟
- 总时长：50分钟
- 对应小说：第1-10章
- 类型：喜剧/成长/传承

主要人物：
- 陈阿三：18-30岁，茶厂学徒→接班人
- 刘师傅：50-60岁，制茶师傅
- 王胖子：18-30岁，学徒
- 李小花：20-28岁，技术员
- 周经理：40-50岁，茶厂经理

核心主题：
- 传承：传统六堡茶技艺的传承
- 成长：陈阿三从学徒到接班人的成长
- 选择：坚持传统 vs 追求现代化的选择

风格特点：
- 轻喜剧：轻松幽默，让人会心一笑
- 温馨感人：有笑有泪，最后温馨收尾
- 90年代语境：符合时代背景

剧本文件：
- 10集完整剧本，每集5个场景
- 保存在：drafts/目录
- 格式：Markdown (.md)
- 文件命名：第{集数}集-标题.md

改编流程：
1. Skill 10：小说分析
2. Skill 11：结构分析
3. Skill 12：人物改编
4. Skill 13：场景大纲
5. Skill 14：剧本创作
6. Skill 15：剧本审校
    """
    
    p = tf.paragraphs[0]
    p.text = content
    p.font.size = Pt(14)
    
    return slide

# Create slides
print("Creating presentation with full script content...")

# Title slide
create_title_slide("《六堡风云》短剧剧本", "共10集，总时长50分钟，包含完整剧本")
print("✅ Created title slide")

# Table of contents
create_toc_slide()
print("✅ Created table of contents")

# Read scripts and create episode slides
for i, script_file in enumerate(script_files, 1):
    print(f"Reading script {i}: {script_file}...")
    script_content = read_script_file(script_file)
    
    episode_title = script_file.split("-")[1].replace(".md", "")
    create_episode_slide_full(i, episode_title, script_content)
    print(f"✅ Created episode {i} slide with full content")

# Summary slide
create_summary_slide()
print("✅ Created summary slide")

# Save presentation
output_file = "/data/data/com.termux/files/home/projects/web/novel-writing/_scripts/六堡风云-短剧剧本-完整版.pptx"
prs.save(output_file)
print(f"\n✅ Presentation saved to: {output_file}")
print(f"✅ Total slides: {len(prs.slides)}")
print(f"✅ Total file size: {(os.path.get(output_file) / 1024):.2f} KB")

# Copy to phone storage
import shutil
phone_storage = "/storage/emulated/0/Download/"
try:
    shutil.copy2(output_file, phone_storage + "六堡风云-短剧剧本-完整版.pptx")
    print(f"✅ Copied to phone storage: {phone_storage}六堡风云-短剧剧本-完整版.pptx")
except Exception as e:
    print(f"⚠️  Failed to copy to phone storage: {e}")

print("\n🎉 Presentation creation completed!")
print("\n📋 Features:")
print("  - 包含所有10集的完整剧本内容")
print("  - 总共13页幻灯片")
print(f"  - 文件大小: {(os.path.get(output_file) / 1024):.2f} KB")
print(f"  - 位置: {output_file}")
print(f"  - 手机储存: {phone_storage}六堡风云-短剧剧本-完整版.pptx")
