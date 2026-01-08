# iFlow CLI 上下文文件

> 生成时间：2026-01-08
> 环境：Android Termux

---

## 项目概述

这是一个运行在 Android Termux 环境下的个人开发工作区，主要用于：
- Web 应用开发（前端、全栈）
- API 服务开发
- 脚本和工具开发
- 小说创作项目
- 原创短剧创作项目
- AI 工作流资源管理
- CodeBuddy 和 iFlow CLI 开发环境

---

## 环境信息

### 操作系统
- **平台**: Android (Termux)
- **内核**: Linux 5.4.254-qgki-g6c6ff6f12ce6

### 已安装工具
- **Node.js**: v24.12.0
- **npm**: v11.6.2
- **Python**: v3.12.12
- **pip**: v25.3
- **Git**: v2.52.0
- **Vim**: v9.1.2000
- **Make**: v4.4.1-1
- **Clang/LLVM**: v21.1.8
- 其他工具: curl, wget, htop, tree, unzip

### 配置文件
- **npm 配置**: `~/.npmrc` - 设置 `foreground-scripts=true`
- **Git 配置**: `~/.gitconfig`
  - 用户名: wuguoshuo
  - 邮箱: wugs@qq.com
  - 默认分支: main
  - 默认编辑器: vim

---

## 项目结构

```
/data/data/com.termux/files/home/
├── projects/              # 所有项目的主目录
│   ├── web/              # Web 应用项目
│   │   ├── novel-writing/  # 小说写作项目（含 9 个小说 Skills + 6 个剧本改编 Skills）
│   │   └── short-drama/    # 原创短剧创作项目（含 7 个 Skills + 7 个 Coze 工作流）
│   ├── api/              # API 服务项目
│   ├── scripts/          # 脚本和工具
│   ├── utils/            # 工具库项目
│   ├── learning/         # 学习和实验项目
│   ├── market/           # 市场相关项目
│   └── writing/          # 写作相关项目
├── AI-Narration-Master-Coze/  # AI 电影解说 Coze 模板
├── cozeworkflows/        # 200+ Coze 工作流集合
├── scripts-ppt/          # PPT 脚本和幻灯片
├── .codebuddy/           # CodeBuddy 状态和配置
│   ├── skills/           # 20 个全局 Skills
│   ├── projects/         # CodeBuddy 项目管理
│   ├── logs/             # 日志文件
│   └── plugins/          # 插件
├── .claude-mem/          # Claude-Mem 配置
├── .iflow/               # iFlow CLI 配置和缓存
├── CODEBUDDY.md          # CodeBuddy 使用指南
├── SKILLS-CHECKLIST.md   # Skills 完整清单
├── convert_pdf.py        # PDF 转换脚本
├── ubuntu.sh             # Ubuntu 环境脚本
└── ubuntu.tar.gz         # Ubuntu 镜像文件
```

---

## 主要项目说明

### 1. 小说写作项目 (projects/web/novel-writing/)

**类型**: Web 应用 / 创作工具

**状态**: 第二阶段已完成，第三阶段进行中

**核心功能**:
- 基于两层判断机制的任务路由
- 9 个小说创作 Skills（全部已实现）
- 6 个剧本改编 Skills（全部已实现）
- 个人素材库（经历、观点、金句）
- 协作文档支持
- 知识库和调研功能

**已实现 Skills**:
1. `01-save-outline.md` - 需求理解与大纲保存 ✅
2. `02-research-knowledge.md` - 信息搜索与知识管理 ✅
3. `03-discuss-chapter.md` - 章节规划与讨论 ✅
4. `04-create-collab-doc.md` - 创作协作文档 ✅
5. `05-learn-style.md` - 学习作者风格 ✅
6. `06-use-personal-materials.md` - 使用个人素材库 ✅
7. `07-write-draft.md` - 创作章节初稿 ✅
8. `08-three-pass-review.md` - 三轮审阅 ✅
9. `09-illustrate-publish.md` - 配图与发布 ✅

**剧本改编 Skills**:
10. `10-analyze-novel.md` - 小说分析 ✅
11. `11-structure-analysis.md` - 结构分析 ✅
12. `12-character-adaptation.md` - 人物改编 ✅
13. `13-scene-outline.md` - 场景大纲 ✅
14. `14-write-script.md` - 剧本创作 ✅
15. `15-script-review.md` - 剧本审校 ✅

**项目结构**:
```
novel-writing/
├── _briefs/              # 小说设定和大纲
├── _knowledge_base/     # 知识库
├── _collab_docs/        # 协作文档
├── _scripts/            # 剧本改编工作区
│   ├── _briefs/         # 剧本设定文档
│   ├── adaptations/     # 改编计划
│   ├── drafts/          # 剧本草稿
│   ├── published/       # 成品剧本
│   └── _logs/           # 改编日志
├── skills/              # 小说写作 Skills（9 个）
├── script-skills/       # 剧本改编 Skills（6 个）
├── materials/           # 个人素材库
├── drafts/              # 小说草稿区
├── published/           # 小说成品区
├── images/              # 配图
└── _logs/               # 小说日志
```

**使用方式**:
```bash
cd projects/web/novel-writing
# 直接与 AI 对话即可开始创作
```

**文档**: 详见 `projects/web/novel-writing/CLAUDE.md` 和 `README.md`

---

### 2. 原创短剧创作项目 (projects/web/short-drama/)

**类型**: 创作工具 / Coze 工作流模板

**状态**: 已完成，可立即使用

**核心功能**:
- 原创短剧从构思到剧本的完整创作流程
- 7 个对话式 Skills 引导创作
- 7 个 Coze 工作流 JSON 可直接导入使用
- 任务路由系统，自动识别创作阶段

**已实现 Skills**:
1. `01-short-drama-concept.md` - 短剧选题 ✅
2. `02-character-setting.md` - 角色设定 ✅
3. `03-story-outline.md` - 故事大纲 ✅
4. `04-episode-outline.md` - 分集大纲 ✅
5. `05-scene-outline.md` - 场景大纲 ✅
6. `06-write-script.md` - 剧本创作 ✅
7. `07-script-review.md` - 剧本审校 ✅

**Coze 工作流**:
- `workflow-01-short-drama-concept.json` - 短剧选题 ✅
- `workflow-02-character-setting.json` - 角色设定 ✅
- `workflow-03-story-outline.json` - 故事大纲 ✅
- `workflow-04-episode-outline.json` - 分集大纲 ✅
- `workflow-05-scene-outline.json` - 场景大纲 ✅
- `workflow-06-write-script.json` - 剧本创作 ✅
- `workflow-07-script-review.json` - 剧本审校 ✅

**项目结构**:
```
short-drama/
├── CLAUDE.md              # 总纲：任务路由、完整流程
├── skills/                # 7 个 Skills
├── _briefs/               # 设定文档
├── drafts/                # 草稿
├── published/             # 成品
├── _logs/                 # 审校日志
└── coze-workflows/        # 7 个 Coze 工作流 JSON
```

**使用方式**:
```bash
cd projects/web/short-drama
# 对话式 Skills：直接与 AI 对话
# Coze 工作流：导入 JSON 文件到 Coze 平台
```

**创作流程**:
1. 选题 → 2. 角色设定 → 3. 故事大纲 → 4. 分集大纲 → 5. 场景大纲 → 6. 剧本创作 → 7. 剧本审校

**文档**: 详见 `projects/web/short-drama/CLAUDE.md`

---

### 3. AI 电影解说模板 (AI-Narration-Master-Coze/)

**类型**: Coze 工作流模板

**功能**: 一站式自动生成完整爆款影视解说视频

**核心能力**:
- 自动生成爆款级电影解说文案
- AI 配音（多声音、多风格）
- 智能画面匹配
- BGM 自动适配
- 自动生成字幕

**部署要求**:
- MySQL 数据库（必须）
- Coze 平台账号

**文档**: 详见 `AI-Narration-Master-Coze/README.md`

---

### 4. Coze 工作流集合 (cozeworkflows/)

**类型**: 工作流资源库

**数量**: 200+ 实用生产力工作流

**分类**:
- 视频生成（书单号、治愈视频、像素风、古风水墨等）
- 文档处理（抖音文案提取、小红书内容仿写）
- 图片生成（小红书图文、表情包、海报）
- 表格处理（飞书多维表格、云表格）
- 声音克隆
- 音乐生成

**使用方式**:
1. 下载工作流 `.zip` 文件
2. 在 Coze 平台的"资源库"中导入
3. 在 Bot 中使用

**文档**: 详见 `cozeworkflows/README.md`

---

### 5. Claude-Mem 插件 (projects/utils/claude-mem/)

**类型**: Claude Code 插件

**版本**: 6.5.0

**功能**: 持久化记忆压缩系统，在 Claude Code 会话之间保持上下文

**核心功能**:
- 🧠 持久化记忆 - 上下文在会话之间保持
- 📊 渐进式披露 - 分层记忆检索
- 🔍 基于技能的搜索 - 使用自然语言查询项目历史
- 🔒 隐私控制 - 使用 `<private>` 标签排除敏感内容

**注意**: 由于 Bun 运行时不支持 Android 平台，完整的 worker 服务无法在 Termux 上运行。主要功能需要依赖外部环境。

**文档**: https://docs.claude-mem.ai/

---

### 6. PPT 脚本 (scripts-ppt/)

**类型**: 演示文稿工具

**内容**:
- PDF 转换脚本（`convert_pdf.py`, `create_pdf.py`, `make_pdf.py`）
- 14 张幻灯片（`slide1.html` 到 `slide14.html`）
- 剧本全集（`六堡风云-剧本全集.html` 和 `.md`）

---

## CodeBuddy Skills 体系

### 全局 Skills (20 个)

位置: `~/.codebuddy/skills/`

**创意与设计类** (4 个):
- `algorithmic-art`: 使用 p5.js 创建算法艺术
- `brand-guidelines`: 应用 Anthropic 官方品牌颜色
- `canvas-design`: 创建视觉艺术
- `frontend-design`: 创建高质量前端界面

**文档处理类** (4 个):
- `docx`: Word 文档创建、编辑和分析
- `pdf`: PDF 操作工具包
- `pptx`: 演示文稿创建、编辑和分析
- `xlsx`: 电子表格创建、编辑和分析

**开发工具类** (2 个):
- `mcp-builder`: 创建 MCP 服务器
- `skill-creator`: 创建有效的 skills

**沟通与文档类** (2 个):
- `doc-coauthoring`: 协作文档结构化工作流程
- `internal-comms`: 内部沟通写作资源

**质量保证类** (3 个):
- `code-review`: 代码审查专家
- `debug-assistant`: 调试助手专家
- `docs-generator`: 文档生成专家

**专用工具类** (5 个):
- `slack-gif-creator`: 为 Slack 创建动画 GIF
- `theme-factory`: 主题工厂
- `web-artifacts-builder`: 使用 React、Tailwind CSS、shadcn/ui 创建构件
- `webapp-testing`: 使用 Playwright 测试 Web 应用

### 项目级 Skills (22 个)

#### 小说创作工作流 (9 个)
位置: `projects/web/novel-writing/skills/`

1. `novel-setup` - 小说设定与大纲创建 ✅
2. `novel-knowledge-research` - 知识调研与验证 ✅
3. `novel-chapter-planning` - 章节规划与讨论 ✅
4. `novel-collaboration-doc` - 协作文档创建 ✅
5. `novel-style-learning` - 写作风格学习 ✅
6. `novel-personal-materials` - 个人素材库集成 ✅
7. `novel-chapter-writing` - 章节初稿撰写 ✅
8. `novel-three-pass-review` - 三轮审阅 ✅
9. `novel-illustration-publish` - 配图与发布 ✅

#### 剧本改编工作流 (6 个)
位置: `projects/web/novel-writing/script-skills/`

10. `novel-analyze-novel` - 小说分析 ✅
11. `novel-structure-analysis` - 结构分析 ✅
12. `novel-character-adaptation` - 人物改编 ✅
13. `novel-scene-outline` - 场景大纲 ✅
14. `novel-write-script` - 剧本创作 ✅
15. `novel-script-review` - 剧本审校 ✅

#### 原创短剧创作工作流 (7 个)
位置: `projects/web/short-drama/skills/`

1. `short-drama-concept` - 短剧选题 ✅
2. `short-drama-character` - 角色设定 ✅
3. `short-drama-story` - 故事大纲 ✅
4. `short-drama-episode` - 分集大纲 ✅
5. `short-drama-scene` - 场景大纲 ✅
6. `short-drama-write` - 剧本创作 ✅
7. `short-drama-review` - 剧本审校 ✅

**详情**: 详见 `SKILLS-CHECKLIST.md`

---

## 常用命令

### Node.js 项目
```bash
# 初始化新项目
npm init -y

# 安装依赖
npm install

# 运行开发服务器
npm run dev

# 运行生产构建
npm run build

# 运行测试
npm test
```

### Python 项目
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install <package-name>

# 导出依赖
pip freeze > requirements.txt
```

### Git 操作
```bash
# 初始化仓库
git init

# 添加文件
git add .

# 提交更改
git commit -m "commit message"

# 查看状态
git status

# 查看日志
git log

# 克隆仓库
git clone <repository-url>

# 拉取更新
git pull origin main

# 推送更改
git push origin main
```

### Termux 包管理
```bash
# 更新包列表
pkg update

# 升级已安装的包
pkg upgrade

# 安装新包
pkg install <package-name>

# 搜索包
pkg search <package-name>

# 列出已安装的包
pkg list-installed
```

---

## 开发规范

### 项目创建
- 所有项目应在 `projects/` 目录下的相应子目录中创建
- Web 应用 → `projects/web/`
- API 服务 → `projects/api/`
- 脚本工具 → `projects/scripts/`
- 工具库 → `projects/utils/`
- 学习项目 → `projects/learning/`

### Python 开发
- 建议使用虚拟环境
- 使用 `pip` 管理依赖
- 导出依赖到 `requirements.txt`

### Git 使用
- 已配置基础设置（用户名、邮箱、默认分支）
- 推荐使用 `main` 作为默认分支
- 提交信息应清晰描述变更内容

### 文件权限
- 使用 Android 权限模型
- 注意 Termux 环境的特殊性

---

## 特殊说明

### Bun 运行时限制
由于 Android 平台不支持 Bun 运行时，以下功能无法在 Termux 上完整运行：
- Claude-Mem 的 worker 服务
- 依赖 Bun 的其他工具

### Ubuntu 环境
- 提供了 `ubuntu.sh` 和 `ubuntu.tar.gz` 用于在 Termux 中运行 Ubuntu 环境
- 可以用于运行不支持 Android 平台的工具

### Claude-Mem 插件
- 已安装但功能受限
- 主要功能（会话记录、上下文检索）需要外部环境支持
- 配置文件位于 `~/.claude-mem/settings.json`

---

## Git 仓库信息

- **远程 URL**: git@github.com:Wuguoshuo/termux-code.git
- **当前分支**: main
- **当前 HEAD**: 4632029f0d657df1db3994569df5af60ed49c68e

---

## 相关文档

- **CODEBUDDY.md**: CodeBuddy 使用指南和开发环境说明
- **SKILLS-CHECKLIST.md**: Skills 完整清单和使用建议
- **projects/web/novel-writing/CLAUDE.md**: 小说写作项目总纲
- **projects/web/novel-writing/README.md**: 小说写作项目文档
- **projects/web/short-drama/CLAUDE.md**: 原创短剧创作系统文档
- **AI-Narration-Master-Coze/README.md**: AI 电影解说模板文档
- **cozeworkflows/README.md**: Coze 工作流集合文档
- **projects/utils/claude-mem/README.md**: Claude-Mem 插件文档

---

## 快速开始

### 创建新项目
```bash
cd projects/web  # 或其他相应目录
npm init -y
npm install <dependencies>
```

### 开始小说创作
```bash
cd projects/web/novel-writing
# 直接与 AI 对话： "我想写一部关于..."
```

### 开始原创短剧创作
```bash
cd projects/web/short-drama
# 直接与 AI 对话： "我想写一个甜宠短剧..."
```

### 使用 Coze 工作流
```bash
cd cozeworkflows/工作流200+合集分享
# 下载工作流文件，然后在 Coze 平台导入
```

### 查看项目状态
```bash
git status
git log -n 5
```

---

## 维护者

- **用户**: wuguoshuo
- **邮箱**: wugs@qq.com
- **环境**: Android Termux

---

**最后更新**: 2026-01-08