# 🚀 小红书每日自动化发布工具 - 快速入门指南

## 简介

这是一个专为小红书内容创作者设计的自动化工具，可以帮助你：
- 每日自动生成爆款文案
- 自动生成匹配的封面图片
- 支持定时自动执行
- 管理内容日历

## 📦 安装

```bash
# 进入 skill 目录
cd /data/data/com.termux/files/home/.iflow/skills/xiaohongshu-daily-autoposter

# 安装依赖
pip install -r requirements.txt

# 运行设置脚本（可选：配置定时任务）
bash setup.sh
```

## 🎯 核心功能

### 1. 生成每日内容
```bash
# 生成今天的随机话题内容
python scripts/autoposter.py --mode daily

# 生成指定话题
python scripts/autoposter.py --mode generate --topic "职场效率"

# 立即触发（测试用）
python scripts/autoposter.py --trigger-now
```

### 2. 启动定时调度
```bash
# 每天早上 8:00 自动执行
python scripts/autoposter.py --mode schedule --time 08:00

# 指定其他时间
python scripts/autoposter.py --mode schedule --time 10:30
```

### 3. 自定义选项
```bash
# 指定主题
python scripts/autoposter.py --topic "学习成长" --theme modern-minimalist

# 预览模式（不生成文件）
python scripts/autoposter.py --mode daily --preview

# 指定输出目录
python scripts/autoposter.py --output /path/to/output
```

## 📁 输出示例

生成的内容将保存在 `output/日期/` 目录下：

```
output/
└── 2024-01-06/
    ├── content.md          # 完整文案
    ├── title_options.md    # 标题变体
    ├── cover.png           # 封面图片
    └── metadata.json       # 元数据
```

### content.md 示例

```markdown
# ✨ 你不提升效率，绝对会后悔！这个方法太绝了！

---
**话题**: 职场效率
**生成时间**: 2024-01-06T10:30:00

---
## 正文

✨ 你是否也有这样的困扰？...

## 话题标签
#职场效率 #工作效率 #时间管理 #职场干货 #打工人

---
## 标题变体（供选择）

1. 你不提升效率，绝对会后悔！这个方法太绝了！
2. 5个高效工作法，小白也能学会，效率翻倍！
3. 救命！终于让我找到了职场效率的秘诀！
...
```

## ⚙️ 配置说明

编辑 `scripts/config.yaml` 自定义设置：

```yaml
posting:
  default_time: "08:00"      # 每日执行时间
  timezone: "Asia/Shanghai"  # 时区
  output_dir: "./output"     # 输出目录

content:
  topics:                    # 内容话题池
    - "职场效率"
    - "生活美学"
    - "学习成长"
    - "时间管理"
    - "个人成长"
  templates: viral           # 文案风格
  min_length: 300           # 正文最小长度
  max_length: 800           # 正文最大长度

image:
  default_theme: vibrant     # 视觉主题
  dimensions: "1000x1500"   # 图片尺寸
  quality: 95               # 图片质量
```

## 🎨 主题选择

| 主题 | 适合领域 | 色彩风格 |
|------|---------|---------|
| vibrant | 美妆、时尚 | 鲜艳活力 |
| modern-minimalist | 职场、学习 | 简约专业 |
| warm-vintage | 美食、旅行 | 温暖复古 |
| tech-blue | 数码、科技 | 科技现代 |
| nature-green | 健身、养生 | 自然清新 |

## 📊 调度器使用

```python
from scheduler import Scheduler

# 创建调度器
scheduler = Scheduler()

# 安排特定日期的内容
scheduler.schedule_post("2024-01-15", "春节旅行")

# 获取状态
status = scheduler.get_status()
print(status)

# 手动触发
result = scheduler.trigger_now(topic="职场效率")
```

## 🧪 测试

```bash
# 运行完整测试
python test_skill.py
```

## 📝 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--mode` | 运行模式 | daily/generate/schedule/calendar |
| `--topic` | 指定话题 | --topic "职场效率" |
| `--time` | 执行时间 | --time "08:00" |
| `--output` | 输出目录 | --output "./output" |
| `--theme` | 视觉主题 | --theme "vibrant" |
| `--preview` | 预览模式 | 不生成文件 |
| `--trigger-now` | 立即执行 | 测试用 |
| `--config` | 配置文件 | --config "./config.yaml" |

## 🔧 高级用法

### 作为 Python 模块使用

```python
from autoposter import Autoposter

# 创建实例
autoposter = Autoposter()

# 生成内容
result = autoposter.run_daily(topic="学习成长")

# 生成特定话题
result = autoposter.generate_specific("时间管理")

# 查看可用话题
topics = autoposter.list_topics()
print(topics)
```

### 自定义内容模板

在 `references/` 目录下添加自定义模板：
```
references/
├── TEMPLATES.md       # 文案模板
├── THEMES.md          # 图片主题
└── custom/            # 自定义模板
    ├── 美食.md
    ├── 旅行.md
    └── 职场.md
```

## 📈 最佳实践

1. **定时执行**: 建议设置在用户活跃时段（7:00-9:00, 12:00-14:00, 20:00-22:00）
2. **话题轮换**: 配置多个话题，保持内容多样性
3. **A/B 测试**: 使用 `title_options.md` 中的多个标题变体进行测试
4. **定期检查**: 查看 `logs/` 目录下的日志文件

## ⚠️ 注意事项

1. 首次运行前请安装依赖：`pip install -r requirements.txt`
2. 确保输出目录可写
3. 定时任务需要系统支持 cron
4. 图片生成需要安装 PIL/Pillow

## 📄 文件结构

```
xiaohongshu-daily-autoposter/
├── SKILL.md              # Skill 主文档
├── QUICKSTART.md         # 本快速入门指南
├── test_skill.py         # 测试脚本
├── setup.sh              # 设置脚本
├── requirements.txt      # Python 依赖
├── skill.json            # Skill 元数据
├── scripts/
│   ├── autoposter.py     # 主入口
│   ├── content_generator.py  # 文案生成
│   ├── image_generator.py    # 图片生成
│   ├── scheduler.py      # 调度器
│   ├── config_loader.py  # 配置加载
│   └── config.yaml       # 默认配置
├── references/
│   ├── TEMPLATES.md      # 文案模板参考
│   └── THEMES.md         # 图片主题参考
└── assets/               # 资源文件
    ├── themes/           # 主题配置
    └── templates/        # 模板文件
```

## 🎉 成功案例

使用本工具可以：
- ✅ 每天自动生成 1 篇高质量文案
- ✅ 每次生成 5 个标题变体供选择
- ✅ 自动生成匹配的封面图片
- ✅ 支持话题轮换和日程管理
- ✅ 减少 80% 的内容创作时间

## 📞 支持

如有问题，请查看：
1. `SKILL.md` 完整文档
2. `logs/` 目录下的错误日志
3. 运行 `python test_skill.py` 进行测试

---

**祝你创作愉快！🚀**
