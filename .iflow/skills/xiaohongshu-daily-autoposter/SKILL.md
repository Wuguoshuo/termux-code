---
name: xiaohongshu-daily-autoposter
description: Automated daily content generation and posting for Xiaohongshu (Little Red Book). Uses AI-powered viral content templates, scheduled execution, and automated image generation to create and publish high-engagement posts every day. Use when users need to automate Xiaohongshu content creation including: (1) Daily automated posting workflows, (2) Viral title and content generation based on proven patterns, (3) Automated cover image generation with design templates, (4) Scheduled content calendar management, and (5) Content optimization based platform best practices.
license: MIT
---

# Xiaohongshu Daily Autoposter

Automated daily content generation and posting for Xiaohongshu (小红书), China's leading lifestyle social platform with 200M+ active users.

## Overview

This skill provides a complete automation pipeline for creating viral Xiaohongshu content:

1. **Content Generation**: AI-powered viral文案 generation using proven patterns
2. **Image Creation**: Automated cover image generation with themed templates
3. **Scheduling**: Daily automated execution with configurable timing
4. **Optimization**: Platform-specific best practices integration

## When to Use This Skill

Use this skill when:
- Creating daily automated content for Xiaohongshu
- Generating viral titles using proven formulas
- Automating cover image creation with consistent branding
- Managing content calendars with scheduled posting
- Optimizing content for Xiaohongshu's unique platform culture

## Core Components

### 1. Content Generator (`scripts/content_generator.py`)
Generates viral Xiaohongshu posts using proven patterns:
- Title templates (二极管标题法, 数字利诱法)
- Opening hooks (提问式, 经验分享式)
- Body structures (步骤说明, 情感共鸣)
- Closing calls-to-action

See [TEMPLATES.md](references/TEMPLATES.md) for all available patterns.

### 2. Image Generator (`scripts/image_generator.py`)
Creates platform-optimized cover images:
- Multiple theme templates (modern, vintage, minimal, vibrant)
- Viral text overlay styles
- Platform-specific dimensions (1000x1500 recommended)
- Color palette management

See [THEMES.md](references/THEMES.md) for theme details.

### 3. Scheduler (`scripts/scheduler.py`)
Manages automated execution:
- Daily execution at configurable time (default: 08:00)
- Content calendar management
- Failure recovery and logging
- Manual trigger support

### 4. Autoposter (`scripts/autoposter.py`)
Orchestrates the complete workflow:
1. Generate content using templates
2. Create matching cover image
3. Output ready-to-post package

## Quick Start

### Basic Usage
```bash
# Generate today's content
python scripts/autoposter.py --mode daily

# Generate specific topic
python scripts/autoposter.py --topic "职场效率" --output ./output

# Run with custom theme
python scripts/autoposter.py --theme modern-minimalist --time "10:30"

# Manual trigger
python scripts/autoposter.py --trigger-now

# Preview mode (no files created)
python scripts/autoposter.py --preview
```

### Configuration
Edit `scripts/config.yaml` to customize:
```yaml
posting:
  default_time: "08:00"      # Daily posting time
  timezone: "Asia/Shanghai"  # Platform timezone
  
content:
  topics:                    # Content topics
    - "职场效率"
    - "生活美学"
    - "学习成长"
  templates: viral           # Content style
  
image:
  default_theme: vibrant     # Visual theme
  dimensions: "1000x1500"    # Platform optimal
  quality: 95                # Output quality
```

## Content Templates

### Title Patterns (标题模式)

**二极管标题法** (Extreme Contrast)
- Formula: 问题 + 极端结果 + 紧迫感
- Example: "你不XXX，绝对会后悔（天大损失）+ 紧迫感"
- Usage: Leverages loss aversion and negative bias

**数字利诱法** (Numeric Appeal)
- Formula: 数字 + 具体收益 + 行动词
- Example: "3天学会XXX，爽到飞起"
- Usage: Quantifiable results attract clicks

**情绪共鸣法** (Emotional Hook)
- Formula: 情绪词 + 痛点 + 解决方案
- Example: "绝绝子！这个方法真的救了我的XXX"
- Usage: Creates immediate connection

**权威背书法** (Authority Reference)
- Formula: 权威/名人 + 同款 + 效果承诺
- Example: "XX明星都在用的XXX，效果惊艳"
- Usage: Leverages social proof

See [TEMPLATES.md](references/TEMPLATES.md) for complete patterns.

### Opening Hooks (开头模式)

**痛点直击**
直接描述用户面临的问题，引发共鸣：
```
emoji 你是否也有这样的困扰？
每次XXX，结果总是XXX...
今天分享一个我的解决方案...
```

**经验分享**
以个人经历开场，增加可信度：
```
emoji 作为一个XXX（身份）...
经历了XXX次失败后...
终于找到了正确的方法...
```

**数字冲击**
用具体数字吸引注意力：
```
emoji 3个月前，我的XXX还是XXX...
现在竟然达到了XXX！
这个方法太神奇了...
```

### Body Structures (正文结构)

**步骤说明式**
1. 痛点引入
2. 方法介绍（3-5步）
3. 效果展示
4. 互动引导

**故事叙述式**
1. 背景铺垫
2. 转折/挑战
3. 解决过程
4. 最终成果
5. 经验总结

### Closing CTA (结尾互动)

**求助式**
"你们有遇到过类似的情况吗？评论区告诉我吧！"

**挑战式**
"如果你也想要XXX，就从今天开始行动吧！"

**预告式**
"下期分享更精彩的XXX，记得关注不迷路！"

## Image Themes

### Available Themes

1. **Vibrant Pop** - 高饱和度，适合美妆、时尚
2. **Modern Minimalist** - 极简风格，适合职场、生活
3. **Warm Vintage** - 暖色调，适合美食、旅行
4. **Tech Blue** - 科技感，适合数码、学习
5. **Nature Green** - 自然清新，适合健身、养生

Each theme includes:
- Color palette (5-7 colors)
- Font pairing (header + body)
- Layout templates (3 variants)
- Emoji style guide

See [THEMES.md](references/THEMES.md) for theme details.

## Platform Guidelines

### Xiaohongshu Best Practices

**Dimensions & Specs**
- Cover image: 1000x1500px (3:4 ratio)
- Aspect ratio: 3:4 vertical preferred
- File format: PNG or JPG
- File size: <10MB recommended

**Content Length**
- Title: <20 characters (with emoji)
- Body: 300-800 characters optimal
- Tags: 3-5 relevant hashtags

**Posting Times** (Best Engagement)
- 07:00-09:00 早高峰
- 12:00-14:00 午间休息
- 20:00-22:00 晚高峰
- Weekend: All day higher engagement

**Algorithm Tips**
- First 2 hours critical for initial traction
- Engagement rate matters more than impressions
- Consistency > virality (regular posting wins)
- Use trending topics when relevant

## Output Structure

Generated content follows this structure:
```
output/
└── 2024-01-06/
    ├── content.md              # Full post with title, body, tags
    ├── title_options.md        # 5 alternative titles
    ├── cover_image.png         # Generated cover image
    └── metadata.json           # Post metadata for tracking
```

## Advanced Usage

### Content Calendar Management
```python
from scheduler import ContentCalendar

calendar = ContentCalendar()
calendar.add_post("2024-01-15", topic="春节旅行")
calendar.get_schedule("2024-01")
calendar.export_ics("schedule.ics")
```

### A/B Testing
Generate multiple title variants:
```python
from content_generator import TitleGenerator

generator = TitleGenerator()
titles = generator.generate_variants(
    topic="职场沟通",
    count=10,
    styles=["emotional", "numeric", "contrast"]
)
```

### Custom Templates
Create topic-specific templates in `references/custom/`:
```
references/custom/
├── 美食.md      # Food & dining templates
├── 旅行.md      # Travel templates
├── 职场.md      # Career templates
└── 美妆.md      # Beauty templates
```

## Integration Points

### External APIs (Future)
- Xiaohongshu Creator Tools API
- Image generation (DALL-E, Midjourney)
- Analytics platforms
- Content optimization services

### Local Tools
- Image processing (PIL, OpenCV)
- Text processing (NLP libraries)
- File management (local storage)
- Notification systems (email, Slack)

## Troubleshooting

### Common Issues

**Content Not Generating**
- Check API keys if using external services
- Verify template files exist
- Review error logs in `logs/`

**Image Generation Fails**
- Ensure PIL/Pillow installed
- Check font files in `assets/fonts/`
- Verify output directory writable

**Scheduler Not Running**
- Confirm cron/crontab configured
- Check process running: `ps aux | grep scheduler`
- Review scheduler logs

### Logs Location
- Scheduler: `logs/scheduler.log`
- Generator: `logs/generator.log`
- Errors: `logs/errors.log`

## Dependencies

```bash
# Core dependencies
pip install pillow numpy python-dateutil

# Optional for advanced features
pip install apscheduler pytest pytest-cov
```

## File Structure

```
xiaohongshu-daily-autoposter/
├── SKILL.md                      # This file
├── skill.json                    # Metadata
├── scripts/
│   ├── autoposter.py            # Main entry point
│   ├── content_generator.py     # Viral content generation
│   ├── image_generator.py       # Cover image creation
│   ├── scheduler.py             # Task scheduling
│   └── config.yaml              # Configuration
├── references/
│   ├── TEMPLATES.md             # Content templates
│   ├── THEMES.md                # Image themes
│   ├── GUIDELINES.md            # Platform guidelines
│   └── custom/                  # Custom templates
└── assets/
    ├── themes/                  # Theme configurations
    ├── templates/               # Image templates
    └── fonts/                   # Custom fonts
```

## Version History

- **1.0.0**: Initial release with core automation
- **1.1.0**: Added 5 new content templates
- **1.2.0**: Introduced A/B title testing
- **1.3.0**: Added custom template support

## License

MIT License - See LICENSE file for details
