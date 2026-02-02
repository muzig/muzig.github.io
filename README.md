# StarryPen 🌟

> 个人技术博客，记录 AI、编程语言与工程实践的深度思考

[![Blog](https://img.shields.io/badge/blog-muzig.github.io-blue)](https://muzig.github.io)
[![Hugo](https://img.shields.io/badge/powered_by-Hugo-ff4088)](https://gohugo.io)
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## 🚀 快速访问

- **博客主页**: https://muzig.github.io
- **最新文章**: https://muzig.github.io/posts
- **RSS 订阅**: https://muzig.github.io/index.xml

---

## 📚 写作指南

> 📖 **新手？** 5 分钟快速开始 → [QUICK_START.md](./QUICK_START.md)

### 一键创建文章

```bash
# 交互式创建（推荐）
./new-post.sh "文章标题"

# 示例
./new-post.sh "深入理解 Go 内存模型"
```

### 内容管理体系

```
📋 核心文档
│
├─ 🌟 QUICK_START.md       ← 5 分钟快速上手
├─ 📅 CONTENT_PLAN.md       ← 长期内容规划
├─ 📊 CONTENT_TRACKER.md    ← 文章进度追踪
└─ 📝 content/posts/_template.md  ← 标准模板
```

---

## 📂 项目结构

```
.
├── content/posts/           # 博客文章
├── static/                  # 静态资源（图片等）
├── themes/                  # Hugo 主题
├── public/                  # 构建输出（GitHub Pages）
├── hugo.toml               # 站点配置
└── new-post.sh             # 文章创建脚本
```

---

## 🛠 本地开发

### 环境要求
- [Hugo](https://gohugo.io/installation/) (Extended 版本)
- Git

### 启动开发服务器

```bash
# 克隆仓库
git clone https://github.com/muzig/muzig.github.io.git
cd muzig.github.io

# 启动本地预览
hugo server -D

# 访问 http://localhost:1313
```

### 新建文章

```bash
# 方法 1：使用脚本（推荐）
./new-post.sh "文章标题"

# 方法 2：Hugo 命令
hugo new content/posts/my-article.md

# 方法 3：复制模板
cp content/posts/_template.md content/posts/my-article.md
```

---

## ✍️ 内容规范

### 文章元数据

```toml
+++
date = '2026-02-02T19:00:00+08:00'
draft = false
title = '文章标题'
tags = ['Tag1', 'Tag2']
categories = ['技术深度']  # 或 '技术文章'
+++
```

### 内容系列

| 系列 | 主题 | 状态 |
|------|------|------|
| MCP 技术深度 | Model Context Protocol 原理与实战 | 连载中 |
| Go 工程实践 | 性能优化、工具链、架构设计 | 连载中 |
| 编程语言原理 | 语言设计对比、特性解析 | 连载中 |

> 详见 [CONTENT_PLAN.md](./CONTENT_PLAN.md)

---

## 📤 发布流程

```bash
# 1. 编写文章
cp content/posts/_template.md content/posts/my-new-post.md
# ... 编辑内容 ...

# 2. 本地预览
hugo server -D

# 3. 提交发布
git add content/posts/my-new-post.md
git commit -m "Add: 文章标题"
git push

# 4. GitHub Actions 自动部署
# 访问 https://muzig.github.io/posts/my-new-post/
```

---

## 📝 隐私检查清单

发布文章前请检查：

- [ ] 移除用户名（如 `/Users/name/` → `~/`）
- [ ] 移除个人域名（如 `name.github.io` → `your-blog.github.io`）
- [ ] 移除具体项目名称
- [ ] 移除个人身份信息
- [ ] 检查 API Key 和密钥

---

## 🎨 主题配置

使用 [Ananke 主题](https://github.com/theNewDynamic/gohugo-theme-ananke)

主要配置：`hugo.toml`

```toml
[params]
  primary_color = "#0044ff"
  show_hero = true
```

---

## 📈 构建状态

- **自动构建**: GitHub Actions
- **部署目标**: GitHub Pages
- **构建时间**: 约 1 分钟

---

## 🔗 相关链接

- [Hugo 文档](https://gohugo.io/documentation/)
- [Markdown 语法](https://www.markdownguide.org/)
- [Ananke 主题](https://github.com/theNewDynamic/gohugo-theme-ananke)

---

<p align="center">
  Built with ❤️ using <a href="https://gohugo.io">Hugo</a>
</p>
