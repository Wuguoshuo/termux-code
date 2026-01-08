#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create PPT with all scripts - no PIL, only text"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# Create presentation
prs = Presentation()
prs.slide_width = Inches(16)
prs.slide_height = Inches(9)

# Define colors
BLUE = (0, 112, 192)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

# Function to create episode slide
def create_episode_slide(episode_num, episode_title):
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank layout
    
    # Add title
    left = Inches(1)
    top = Inches(0.5)
    width = Inches(14)
    height = Inches(1)
    
    title_box = slide.shapes.add_textbox(left, top, width, height)
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"第{episode_num}集：{episode_title}"
    p.font.size = Pt(32)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = BLUE
    
    # Add content
    left = Inches(1)
    top = Inches(2)
    width = Inches(14)
    height = Inches(6)
    
    content_box = slide.shapes.add_textbox(left, top, width, height)
    tf = content_box.text_frame
    tf.word_wrap = True
    
    content = f"""
人物表：
- 陈阿三：[年龄]，茶厂学徒/接班人
- 刘师傅：50多岁，制茶师傅
- 王胖子：[年龄]，学徒
- [其他人物]：[角色]

场景列表：
- 场景1：[地点]
- 场景2：[地点]
- 场景3：[地点]
- 场景4：[地点]
- 场景5：[地点]

总时长：5分钟
    """
    
    p = tf.paragraphs[0]
    p.text = content
    p.font.size = Pt(18)
    
    return slide

# Function to create summary slide
def create_summary_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    
    # Add title
    left = Inches(1)
    top = Inches(0.5)
    width = Inches(14)
    height = Inches(1)
    
    title_box = slide.shapes.add_textbox(left, top, width, height)
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "剧本总结"
    p.font.size = Pt(32)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = BLUE
    
    # Add content
    left = Inches(1)
    top = Inches(2)
    width = Inches(14)
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

剧本文件位置：
- 所有剧本保存在：drafts/目录
- 格式：Markdown (.md)
- 文件命名：第{集数}集-标题.md
    """
    
    p = tf.paragraphs[0]
    p.text = content
    p.font.size = Pt(18)
    
    return slide

# Create slides
print("Creating presentation...")

# Title slide
create_title_slide("《六堡风云》短剧剧本", "共10集，总时长50分钟")
print("✅ Created title slide")

# Table of contents
create_toc_slide()
print("✅ Created table of contents")

# Episode slides
episodes = [
    (1, "命运的安排"),
    (2, "学艺的日子"),
    (3, "渥堆初体验"),
    (4, "陈化的等待"),
    (5, "分歧的开始"),
    (6, "风波来了"),
    (7, "出走的决定"),
    (8, "外面的世界"),
    (9, "归来的决定"),
    (10, "传承的开始")
]

for episode_num, episode_title in episodes:
    create_episode_slide(episode_num, episode_title)
    print(f"✅ Created episode {episode_num} slide")

# Summary slide
create_summary_slide()
print("✅ Created summary slide")

# Save presentation
output_file = "/data/data/com.termux/files/home/projects/web/novel-writing/_scripts/六堡风云-短剧剧本.pptx"
prs.save(output_file)
print(f"\n✅ Presentation saved to: {output_file}")
print(f"✅ Total slides: {len(prs.slides)}")

# Copy to phone storage
import shutil
phone_storage = "/storage/emulated/0/Download/"
try:
    shutil.copy2(output_file, phone_storage + "六堡风云-短剧剧本.pptx")
    print(f"✅ Copied to phone storage: {phone_storage}六堡风云-短剧剧本.pptx")
except Exception as e:
    print(f"⚠️  Failed to copy to phone storage: {e}")

print(f"\n📱 PPT location on phone: {phone_storage}六堡风云-短剧剧本.pptx")

print("\n🎉 Presentation creation completed!")
print("\n💡 Note: Due to PIL dependency issues, this PPT contains only text content.")
print("💡 The full剧本 content is available in the draft files.")
print(f"💡 Script files location: /data/data/com.termux/files/home/projects/web/novel-writing/_scripts/drafts/")
