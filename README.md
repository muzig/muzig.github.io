# Muzig · Digital Field Notes

Muzig 是一个由 Astro 生成纯静态 HTML 的中文技术博客。公共结构由组件维护，每篇文章仍可通过 `design` 字段选择不同视觉主题；历史 Hugo 内容仅作为资料保留，不参与构建。

## 发布结构

```text
src/content/blog/       # 新文章 Markdown / MDX
src/layouts/            # 公共页面与文章骨架
src/components/         # 导航、页脚等公共组件
src/styles/             # 公共视觉系统
public/                 # 字体、图片、脚本和站点验证文件
legacy-pages/           # 暂未迁移的旧 HTML 页面
dist/                   # Astro 构建出的唯一部署产物（不提交）
```

`content/`、`themes/`、`archetypes/`、`resources/` 和 `hugo.toml` 属于历史 Hugo 系统。不要用 Hugo 覆盖 `public/` 或 `dist/`。

## 新建文章

```bash
./new-post.sh "文章标题" english-url-slug
```

脚本会在 `src/content/blog/` 创建 Markdown 草稿，并生成稳定的日期 URL。完成内容和元数据后，将 `draft` 改为 `false` 即可发布。首页、RSS 和 Sitemap 会自动更新。

核心元数据：

```yaml
title: 文章标题
description: 一句话说明文章解决的问题
publishedAt: 2026-09-01T10:00:00+08:00
draft: true
category: AI工程
articleType: 深度解析
tags: [Astro, AI工程]
design: standard
path: /2026/09/01/english-url-slug/
legacyUrls: []
featured: false
```

`design` 支持 `standard`、`editorial` 和 `manifesto`。极特殊页面可以直接创建独立 `.astro` 页面或使用 MDX 组件。

## 首页（个人主页）

首页按 X 网页版的三栏结构做成英文个人主页：左侧导航、中间是封面、头像、简介、Now 和文章时间线，右侧是 About、Series 和 Topics。设计规格见 `docs/superpowers/specs/2026-10-30-x-style-profile-home-design.md`。

- 个人信息只改 `src/data/profile.json`：简介、链接、Now、Start here 文章列表和系列英文名。
- 旧文章在 `src/data/legacy-posts.json` 中需要 `titleEn`、`excerptEn`；`readMinutes`、`series`、`topicEn` 由 `scripts/enrich-legacy-posts.mjs` 生成，脚本不会覆盖已有翻译。
- 新文章可在 front matter 中填写 `titleEn`、`excerptEn`，阅读时长在构建时自动计算。
- 缺少英文标题或摘要、或 Start here 指向不存在的文章时，构建会失败。
- 首页不展示任何虚构数据（点赞、浏览量、评论数）。AI 读者评论区上线前，相关区块保持隐藏。
- 首页使用 `lang="en"`；文章页保持中文。

## 本地开发

```bash
npm install
npm run dev
```

`npm run dev` 只预览 Astro 管理的页面。要同时检查旧 HTML 兼容层：

```bash
npm run build
npm run preview
```

## 验证与发布

```bash
npm run check
```

该命令会检查 Astro 类型、重新构建 `dist/`，并验证 UTF-8、首页元信息、旧文章 URL、RSS、Sitemap、草稿排除和 `/posts/*` 兼容重定向。

推送到 `main` 或 `master` 后，GitHub Actions 使用 Node.js 构建并部署 `dist/`。旧 HTML 通过 `scripts/copy-legacy.mjs` 复制到构建结果；路径冲突会直接中止构建，防止旧页面覆盖 Astro 页面。

## 渐进迁移规则

- 新文章只写入 `src/content/blog/`。
- 旧日期 URL 在迁移前保持不变。
- 迁移某篇旧文章时，从 `legacy-pages/` 删除对应 HTML，并在内容文件中继续使用原 `path`。
- `legacy-pages/posts/*` 只生成指向 canonical 日期 URL 的轻量重定向。
- `noindex` 旧草稿和 `legacy-pages/posts/_template/` 不会进入 `dist/`。
- 不要手工编辑或提交 `dist/`。
