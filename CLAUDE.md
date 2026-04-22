# CLAUDE.md

This repository is a Hugo blog for `Muzig`, published at `https://muzig.io`.

## What To Optimize For

- Maintain a clean technical blog content system.
- Preserve the normalized metadata model already established in the repo.
- Keep branding, taxonomy, and editorial structure consistent.

## Read First

- `CONTENT_SCHEMA.md`
- `README.md`
- `QUICK_START.md`
- `hugo.toml`

## Repo-Specific Rules

### 1. Post Metadata

Every post should use:

- `categories`: topic domain
- `series`: series grouping
- `articleType`: article format
- `tags`: search keywords

Do not use:

- `技术深度`
- `技术文章`
- `技术思考`
- `技术经济`

as active category values.

Do not use Hugo `type` to represent article format.

### 2. Topic Categories

Use only these topic categories unless the user explicitly requests a schema change:

- `AI工程`
- `Agent工具链`
- `MCP`
- `Go工程`
- `编程语言`
- `LLM系统`
- `软件架构`

### 3. Article Types

Preferred `articleType` values:

- `深度解析`
- `实战教程`
- `入门指南`
- `架构拆解`
- `对比分析`
- `方法论`
- `观点评论`
- `故障排查`

### 4. Tags

- Keep tags stable and intentional.
- Prefer product names, protocols, languages, and technical concepts.
- Keep casing consistent, such as `OpenClaw`, `Claude Code`, `MCP`, `Go`.

## Editing Guidance

- Prefer editing source content and docs, not generated output.
- Do not manually edit `public/` unless the user explicitly asks for generated artifacts to be committed and you regenerate them.
- If changing templates, taxonomy, or front matter conventions, rebuild the site.
- Use `hugo.toml` as the only site config file.
- The canonical site URL is `https://muzig.io`.

## Commands

```bash
# preview drafts locally
hugo server -D

# create a new post using the repo's schema
./new-post.sh "文章标题"

# rebuild generated site output
hugo --minify --cleanDestinationDir
```

## Theme Note

- `themes/yinyang` is a git submodule.
- Changes inside it are not normal root-repo edits; treat them as submodule updates.

## Default Content Style

- Write user-facing content in Chinese unless the task clearly calls for English.
- Keep prose technically precise and avoid fluff.
- This repo is a blog source repo, so consistency of metadata and editorial structure matters as much as prose.
