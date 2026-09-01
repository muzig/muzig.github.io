# AGENTS.md

This repository is the source for `Muzig`, a technical blog published at `https://muzig.io`.

## Purpose

- This is a content repository, not a product app.
- The main job here is writing, editing, designing, organizing, and publishing technical blog posts.
- The current editorial focus is AI engineering, agent toolchains, MCP, Go engineering, programming languages, and LLM systems.

## Publishing Model

The repository intentionally keeps two systems:

1. The current standalone HTML publishing system lives in `public/`.
2. The historical Hugo system lives in `content/`, `themes/`, `archetypes/`, `resources/`, and `hugo.toml`.

These systems are not required to stay synchronized. Do not assume that changing one should update the other.

### Current HTML System

- `public/` is the source of truth for the live site.
- GitHub Actions deploys `public/` directly and does not run Hugo.
- Each article is a standalone HTML page with its own layout and page-specific styles.
- New articles and visual design work should target `public/` unless the task explicitly requests Hugo maintenance.
- Shared fonts, images, and scripts may live under `public/fonts/`, `public/images/`, and `public/js/`.
- Follow `README.md` for the current writing, preview, and publishing workflow.

### Historical Hugo System

- The Hugo tree is retained as an archive of earlier source content and site structure.
- Do not delete, migrate, or regenerate the Hugo tree unless the task explicitly requests it.
- Do not run Hugo in a way that overwrites the hand-authored pages in `public/`.
- Hugo content rules below apply only when editing the historical Hugo system.
- `hugo.toml` is the only Hugo configuration file; do not reintroduce `hugo.yaml`.
- The theme in `themes/yinyang` is a Git submodule. Treat changes inside it as intentional submodule changes.

## Source Of Truth

### Current publishing

- Deployment source: `public/`
- Deployment workflow: `.github/workflows/hugo.yml`
- Current workflow and page conventions: `README.md`
- New standalone article template: `public/posts/_template/index.html`

### Historical Hugo archive

- Site config: `hugo.toml`
- Content schema: `CONTENT_SCHEMA.md`
- Historical writing workflow: `QUICK_START.md`
- Historical post template: `content/posts/_template.md`
- Content planning: `CONTENT_PLAN.md`

## HTML Working Rules

- Default to Chinese for user-facing content unless the task clearly requires English.
- Prefer editing final pages directly under `public/` for new content and design work.
- Keep each article's core reading experience self-contained; page-specific HTML and CSS belong in the article's `index.html`.
- Maintain a working return link to the homepage, responsive behavior, accessible navigation, a meaningful page title, and a meta description.
- Update `public/index.html` when a new article needs to appear in the homepage index.
- Preserve the canonical domain `https://muzig.io`; do not reintroduce `muzig.github.io` in active pages or configuration.
- Do not introduce a build framework or package manager unless the task explicitly requires one.

## Historical Hugo Content Rules

When editing posts under `content/`, use the normalized front matter schema:

```toml
+++
date = '2026-04-22T10:00:00+08:00'
draft = true
title = '文章标题'
description = '一句话说明文章解决的问题'
categories = ['Agent工具链']
series = ['OpenClaw 深度系列']
articleType = '实战教程'
tags = ['OpenClaw', 'Agent', '工作区设计']
+++
```

Follow these rules:

- `categories` means topic domain, not article depth.
- `series` means content series.
- `articleType` means article format.
- `tags` are search keywords only.
- Do not reintroduce old category values such as `技术深度`, `技术文章`, `技术思考`, or `技术经济`.
- Do not use Hugo `type` as a replacement for `articleType`.
- Keep tag naming consistent, for example `OpenClaw`, `Claude Code`, `MCP`, and `Go`.

Allowed categories:

- `AI工程`
- `Agent工具链`
- `MCP`
- `Go工程`
- `编程语言`
- `LLM系统`
- `软件架构`

Recommended article types:

- `深度解析`
- `实战教程`
- `入门指南`
- `架构拆解`
- `对比分析`
- `方法论`
- `观点评论`
- `故障排查`

## Commands

```bash
# Create a standalone HTML article
./new-post.sh "文章标题" english-url-slug

# Preview the current published site
python3 -m http.server 8080 -d public

# Historical Hugo preview; use only for explicit Hugo maintenance
hugo server -D
```

## Validation

For changes to the current HTML system:

- Parse or open every changed HTML file.
- Verify UTF-8 readability, internal links, responsive layout, title, and description.
- Preview from `public/` when visual behavior changes.
- Do not run Hugo as the validation step for standalone HTML changes.

For explicit changes to the historical Hugo system:

- Check `CONTENT_SCHEMA.md` as the final authority for content metadata.
- Build to a temporary destination rather than overwriting `public/`.
- Verify that the current standalone HTML publishing tree remains unchanged.
