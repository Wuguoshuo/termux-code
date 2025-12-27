# CodeBuddy Skills 完整清单

**生成时间**: 2025-12-26
**总数**: 30 个 Skills
- 全局 Skills: 20 个
- 项目级 Skills: 10 个

---

## 一、全局 Skills（Global Skills）

**位置**: `~/.codebuddy/skills/`
**数量**: 20 个
**适用范围**: 所有项目

### 1. 创意与设计类（4 个）

| 序号 | Skill 名称 | 功能描述 |
|-----|-----------|---------|
| 1 | algorithmic-art | 使用 p5.js 创建算法艺术，支持种子随机性和交互式参数探索 |
| 2 | brand-guidelines | 应用 Anthropic 官方品牌颜色和排版到作品 |
| 3 | canvas-design | 使用设计哲学在 .png 和 .pdf 文档中创建视觉艺术 |
| 4 | frontend-design | 创建高质量前端界面，避免通用 AI 美学 |

### 2. 文档处理类（4 个）

| 序号 | Skill 名称 | 功能描述 |
|-----|-----------|---------|
| 5 | docx | Word 文档创建、编辑和分析，支持修订、注释、格式保留 |
| 6 | pdf | PDF 操作工具包，提取文本/表格、创建/合并/拆分文档、处理表单 |
| 7 | pptx | 演示文稿创建、编辑和分析 |
| 8 | xlsx | 电子表格创建、编辑和分析，支持公式、格式、数据分析和可视化 |

### 3. 开发工具类（2 个）

| 序号 | Skill 名称 | 功能描述 |
|-----|-----------|---------|
| 9 | mcp-builder | 创建高质量 MCP 服务器，让 LLM 与外部服务交互 |
| 10 | skill-creator | 创建有效的 skills，扩展 Claude 的能力 |

### 4. 沟通与文档类（2 个）

| 序号 | Skill 名称 | 功能描述 |
|-----|-----------|---------|
| 11 | doc-coauthoring | 协作文档的结构化工作流程，用于撰写文档、提案、技术规范等 |
| 12 | internal-comms | 内部沟通写作资源，状态报告、领导更新、公司通讯等 |

### 5. 质量保证类（3 个）

| 序号 | Skill 名称 | 功能描述 |
|-----|-----------|---------|
| 13 | code-review | 代码审查专家，分析代码质量、可维护性、安全性和最佳实践 |
| 14 | debug-assistant | 调试助手专家，分析错误消息、堆栈跟踪和异常行为 |
| 15 | docs-generator | 文档生成专家，生成技术文档、API 参考、用户指南和代码注释 |

### 6. 专用工具类（5 个）

| 序号 | Skill 名称 | 功能描述 |
|-----|-----------|---------|
| 16 | slack-gif-creator | 为 Slack 创建优化的动画 GIF |
| 17 | theme-factory | 主题工厂，使用 10 个预设主题或动态生成新主题 |
| 18 | web-artifacts-builder | 使用 React、Tailwind CSS、shadcn/ui 创建复杂的 HTML 构件 |
| 19 | webapp-testing | 使用 Playwright 与本地 Web 应用交互和测试 |

---

## 二、项目级 Skills（Project-Specific Skills）

**位置**: `projects/web/novel-writing/.codebuddy/skills/`
**数量**: 10 个
**适用范围**: novel-writing 项目

### 小说创作完整工作流（10 个）

| 序号 | Skill 名称 | 功能描述 |
|-----|-----------|---------|
| 1 | novel-setup | 小说设定与大纲创建，收集类型、世界观、人物、冲突 |
| 2 | novel-knowledge-research | 知识调研与验证，确保技术细节、历史事实的准确性 |
| 3 | novel-chapter-planning | 章节规划与讨论，提供 3-4 个情节方案，避免方向错误 |
| 4 | novel-collaboration-doc | 协作文档创建，支持多人工作流、大纲、人物卡、世界设定 |
| 5 | novel-style-learning | 写作风格学习，分析语调、声音、句子结构、词汇、节奏 |
| 6 | novel-personal-materials | 个人素材库集成，降低 AI 味，增加人味 |
| 7 | novel-chapter-writing | 章节初稿撰写，基于确认的规划创作章节 |
| 8 | novel-three-pass-review | 三轮审阅，系统化降低 AI 检测率，增加人味 |
| 9 | novel-illustration-publish | 配图与发布，添加插图、准备出版 |

---

## 三、技能分类统计

### 按功能分类

| 分类 | 数量 | Skills |
|-----|------|--------|
| 文档处理 | 5 | docx, pdf, pptx, xlsx, doc-coauthoring |
| 开发工具 | 6 | code-review, debug-assistant, mcp-builder, skill-creator, webapp-testing, web-artifacts-builder |
| 创意设计 | 4 | algorithmic-art, brand-guidelines, canvas-design, frontend-design |
| 小说创作 | 10 | novel-* 系列（10 个） |
| 专用工具 | 5 | internal-comms, slack-gif-creator, theme-factory, docs-generator |

### 按来源分类

| 来源 | 数量 | 说明 |
|-----|------|------|
| Claude 官方 | 16 | anthropics/skills 仓库 |
| CodeBuddy 自定义 | 3 | debug-assistant, code-review, docs-generator |
| 小说项目 | 10 | novel-writing 项目专用 |
| 合计 | 29 | （实际总数 30 个） |

---

## 四、技能优先级

### 高频使用（推荐优先掌握）

1. **开发必备**（3 个）
   - code-review - 代码审查
   - debug-assistant - 调试助手
   - docs-generator - 文档生成

2. **小说创作核心**（5 个）
   - novel-setup - 小说设定
   - novel-chapter-planning - 章节规划
   - novel-chapter-writing - 章节撰写
   - novel-three-pass-review - 三轮审阅
   - novel-personal-materials - 个人素材

3. **文档处理**（2 个）
   - docx - Word 文档
   - pdf - PDF 文档

### 按需使用

- 创意设计类：有视觉需求时使用
- 协作文档类：多人协作时使用
- Web 应用类：前端开发时使用

---

## 五、技能工作流

### 小说创作完整流程

```
开始
  ↓
novel-setup (创建设定)
  ↓
novel-knowledge-research (验证知识) [可选]
  ↓
novel-chapter-planning (规划章节)
  ↓
novel-collaboration-doc (协作文档) [可选]
  ↓
novel-style-learning (学习风格) [可选]
  ↓
novel-personal-materials (准备素材) [可选]
  ↓
novel-chapter-writing (撰写初稿)
  ↓
novel-three-pass-review (三轮审阅)
  ↓
novel-illustration-publish (配图发布)
  ↓
完成
```

### 开发工作流

```
代码开发
  ↓
code-review (审查代码)
  ↓
debug-assistant (调试问题) [如需要]
  ↓
docs-generator (生成文档) [如需要]
  ↓
完成
```

---

## 六、使用建议

### 1. 自动加载

- 全局 Skills：所有项目自动可用
- 项目级 Skills：在项目目录下工作自动加载

### 2. 智能调用

根据任务类型自动选择：
- 写小说 → novel-* 系列
- 审查代码 → code-review
- 处理文档 → docx/pdf/pptx/xlsx
- 调试问题 → debug-assistant
- 生成文档 → docs-generator

### 3. 明确指定

也可以在任务中明确指定：
```
"用 code-review 审查这段代码"
"用 novel-chapter-planning 计划下一章"
"用 debug-assistant 分析这个错误"
```

---

## 七、维护建议

### 定期更新

- 每季度检查官方 skills 更新
- 根据使用反馈优化自定义 skills
- 及时删除不常用的 skills

### 版本管理

- 对重要的 skills 进行版本跟踪
- 记录修改历史和原因
- 保持与官方格式同步

---

**清单版本**: v1.0
**最后更新**: 2025-12-26
**维护者**: CodeBuddy
