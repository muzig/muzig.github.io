# AGENTS.md

This repository is the source for `Muzig`, a technical blog published at `https://muzig.io`.

## Purpose

- This is a content repository, not a product app.
- The main job here is writing, editing, designing, organizing, and publishing technical blog posts.
- The current editorial focus is AI engineering, agent toolchains, MCP, Go engineering, programming languages, and LLM systems.

## Publishing Model

The repository intentionally keeps three layers:

1. The current Astro source lives in `src/` and generates `dist/`.
2. Unmigrated standalone HTML pages live in `legacy-pages/` and are copied into `dist/` during the build.
3. The historical Hugo system lives in `content/`, `themes/`, `archetypes/`, `resources/`, and `hugo.toml`.

These systems are not required to stay synchronized. Do not assume that changing one should update the other.

### Current Astro System

- `src/` and `legacy-pages/` are source inputs; `dist/` is the generated deployment artifact.
- GitHub Actions runs `npm run check` and deploys `dist/`. It does not run Hugo.
- New articles belong in `src/content/blog/` as Markdown or MDX.
- Shared layouts and components belong in `src/layouts/` and `src/components/`; reusable styles belong in `src/styles/`.
- Shared fonts, images, scripts, and site verification files live in `public/`.
- Each article can select `standard`, `editorial`, or `manifesto` through its `design` field. Exceptional pages may use a dedicated Astro page or MDX component.
- Follow `README.md` for the current writing, preview, and publishing workflow.

### Legacy HTML Compatibility Layer

- Keep unmigrated pages in `legacy-pages/` at their existing paths.
- Do not add new articles to `legacy-pages/`.
- `scripts/copy-legacy.mjs` prevents legacy files from overwriting Astro output, excludes noindex drafts and the old public template, and turns `/posts/*` content copies into canonical redirects.
- When migrating an old page, preserve its current date URL in the Astro content `path` before removing the legacy file.

### Historical Hugo System

- The Hugo tree is retained as an archive of earlier source content and site structure.
- Do not delete, migrate, or regenerate the Hugo tree unless the task explicitly requests it.
- Do not run Hugo in a way that overwrites `public/`, `legacy-pages/`, or `dist/`.
- Hugo content rules below apply only when editing the historical Hugo system.
- `hugo.toml` is the only Hugo configuration file; do not reintroduce `hugo.yaml`.
- The theme in `themes/yinyang` is a Git submodule. Treat changes inside it as intentional submodule changes.

## Source Of Truth

### Current publishing

- Content and page source: `src/`
- Legacy page source: `legacy-pages/`
- Static assets: `public/`
- Deployment artifact: `dist/`
- Deployment workflow: `.github/workflows/hugo.yml`
- Current workflow and page conventions: `README.md`
- New article template: `src/content/blog/_template.md`

### Historical Hugo archive

- Site config: `hugo.toml`
- Content schema: `CONTENT_SCHEMA.md`
- Historical writing workflow: `QUICK_START.md`
- Historical post template: `content/posts/_template.md`
- Content planning: `CONTENT_PLAN.md`

## Astro Working Rules

- Default to Chinese for user-facing content unless the task clearly requires English.
- Prefer Markdown or MDX under `src/content/blog/` for new content.
- Put shared structure in components and layouts; keep genuinely page-specific design close to the article or its dedicated layout.
- Maintain a working return link to the homepage, responsive behavior, accessible navigation, a meaningful page title, and a meta description.
- Do not manually update the homepage, RSS, or Sitemap for Astro content; they are generated from the collection.
- Keep drafts marked `draft: true`; drafts must not enter `dist/`.
- Preserve the canonical domain `https://muzig.io`; do not reintroduce `muzig.github.io` in active pages or configuration.
- Do not hand-edit or commit `dist/`.

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
# Create an Astro Markdown draft
./new-post.sh "文章标题" english-url-slug

# Develop Astro-managed pages
npm run dev

# Build and preview Astro plus legacy pages
npm run build
npm run preview

# Full validation
npm run check

# Historical Hugo preview; use only for explicit Hugo maintenance
hugo server -D
```

## Validation

For changes to the current Astro system:

- Run `npm run check`.
- Verify UTF-8 readability, internal links, responsive layout, title, and description.
- Preview the built `dist/` when visual behavior changes so legacy compatibility is included.
- Do not run Hugo as the validation step for Astro changes.

For explicit changes to the historical Hugo system:

- Check `CONTENT_SCHEMA.md` as the final authority for content metadata.
- Build to a temporary destination rather than overwriting `public/`.
- Verify that the current Astro and legacy publishing inputs remain unchanged.
