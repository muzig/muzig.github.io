# AGENTS.md

This repository is the source for `Muzig`, a Hugo-based technical blog published at `https://muzig.io`.

## Purpose

- This is a content repository, not a product app.
- The main job here is writing, editing, organizing, and publishing technical blog posts.
- The current editorial focus is AI engineering, agent toolchains, MCP, Go engineering, programming languages, and LLM systems.

## Source Of Truth

- Site config: `hugo.toml`
- Content schema: `CONTENT_SCHEMA.md`
- Writing workflow: `QUICK_START.md`
- Post template: `content/posts/_template.md`
- Content planning: `CONTENT_PLAN.md`

## Content Rules

Use the normalized front matter schema for posts:

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
- Keep tag naming consistent, for example `OpenClaw`, `Claude Code`, `MCP`, `Go`.

## Allowed Categories

- `AI工程`
- `Agent工具链`
- `MCP`
- `Go工程`
- `编程语言`
- `LLM系统`
- `软件架构`

## Recommended Article Types

- `深度解析`
- `实战教程`
- `入门指南`
- `架构拆解`
- `对比分析`
- `方法论`
- `观点评论`
- `故障排查`

## Working Rules

- Default to Chinese for user-facing content unless the task clearly requires English.
- Prefer editing source files under `content/`, config files, and docs.
- Do not hand-edit generated files in `public/`; regenerate them instead.
- If you change taxonomy, templates, metadata, or content that affects output, rebuild the site.
- The canonical domain is `https://muzig.io`; avoid reintroducing `muzig.github.io` in active site docs and config.
- `hugo.yaml` has been removed; use `hugo.toml` only.

## Commands

```bash
# local preview with drafts
hugo server -D

# create a new post
./new-post.sh "文章标题"

# production build
hugo --minify --cleanDestinationDir
```

## Theme Submodule

- The theme lives in `themes/yinyang` and is a git submodule.
- If you modify files inside `themes/yinyang`, that is a submodule change and must be handled intentionally.

## Validation

Before finishing substantial changes, run:

```bash
hugo --minify --cleanDestinationDir
```

If content schema or writing rules are involved, check `CONTENT_SCHEMA.md` as the final authority.
