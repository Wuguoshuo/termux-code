# CODEBUDDY.md

This file provides guidance to CodeBuddy Code when working with code in this repository.

## Environment Overview

This directory (`/data/data/com.termux/files/home`) is the primary development directory for all projects on this Termux Android environment.

## Development Environment

### Installed Tools
- **Node.js**: v24.12.0
- **npm**: v11.6.2
- **Python**: v3.12.12
- **pip**: v25.3
- **Git**: v2.52.0
- **Vim**: v9.1.2000
- **Make**: v4.4.1-1
- **Clang/LLVM**: v21.1.8
- **其他工具**: curl, wget, htop, tree, unzip

### npm 配置
- 配置文件: `.npmrc`
- 设置: `foreground-scripts=true`

### Git 配置
- 配置文件: `.gitconfig`
- 用户名: `wuguoshuo`
- 邮箱: `wugs@qq.com`
- 默认分支: `main`
- 默认编辑器: `vim`

## Project Structure

所有项目都组织在 `projects/` 目录下：

```
projects/
├── web/       # Web 应用项目（前端、全栈）
├── api/       # API 服务项目
├── scripts/   # 脚本和工具
├── utils/     # 工具库项目
└── learning/  # 学习和实验项目
```

创建新项目时，应该在相应的子目录下创建项目文件夹。

## Common Commands

### Node.js Projects
```bash
# 初始化新项目
npm init -y

# 安装依赖
npm install

# 运行开发服务器（根据项目配置）
npm run dev

# 运行生产构建
npm run build

# 运行测试
npm test

# 全局安装包
npm install -g <package-name>
```

### Python Projects
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install <package-name>

# 导出依赖
pip freeze > requirements.txt

# 从依赖文件安装
pip install -r requirements.txt
```

### Git Operations
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

### Termux Package Management
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

# 删除包
pkg uninstall <package-name>
```

### System Utilities
```bash
# 查看目录结构
tree

# 查看进程
htop

# 编辑文件
vim <filename>

# 查看文件内容
cat <filename>

# 查找文件
find . -name "<filename>"
```

## CodeBuddy Configuration

CodeBuddy stores its state in `.codebuddy/` directory:
- `history.jsonl`: 对话历史记录
- `user-state.json`: 用户状态信息
- `logs/`: CodeBuddy 日志文件
- `projects/`: CodeBuddy 项目管理
- `plugins/`: CodeBuddy 插件

## Notes

- 这是一个 Termux (Android) 环境，运行在 Android 平台上
- Node.js、Python、Git 都已配置并可用
- 所有项目都应该在 `projects/` 目录下的相应子目录中创建
- 文件权限使用 Android 权限模型
- 建议使用虚拟环境进行 Python 开发
- Git 已配置好基础设置，可根据需要修改用户信息

## Claude-Mem Plugin

已安装 Claude-Mem 插件（版本 8.0.6），用于在 Claude Code 会话之间保持上下文记忆。

**位置**: `projects/utils/claude-mem/`

**配置文件**: `~/.claude-mem/settings.json`

**注意**: 由于 Bun 运行时不支持 Android 平台，完整的 worker 服务无法在 Termux 上运行。主要功能（如会话记录和上下文检索）需要依赖外部环境。

**核心功能**:
- 🧠 持久化记忆 - 上下文在会话之间保持
- 📊 渐进式披露 - 分层记忆检索
- 🔍 基于技能的搜索 - 使用自然语言查询项目历史
- 🔒 隐私控制 - 使用 `<private>` 标签排除敏感内容

详见: https://docs.claude-mem.ai/
