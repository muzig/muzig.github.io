# 单文件 HTML 博客快速开始

> 新文章从创建到预览、发布的唯一有效流程。

## 先记住这条规则

所有线上文章都必须是一份可独立打开的 HTML 文件，固定放在：

```text
public/YYYY/MM/DD/slug/index.html
```

- `public/` 是 GitHub Pages 的唯一发布源。
- 新文章不再创建 `content/posts/*.md`，也不需要 Front Matter。
- 不再运行 Hugo 构建或 `hugo server`。
- `content/`、`hugo.toml`、`themes/` 仅保留为历史资料，不参与新文章创作和部署。
- 项目管理文档可以继续使用 Markdown；“只使用 HTML”特指对外发布的博客页面。

## 创建新文章

### 1. 运行创建脚本

```bash
./new-post.sh "你的文章标题" english-url-slug
```

建议显式提供简短、稳定的英文 slug，例如：

```bash
./new-post.sh "Agent 记忆系统的三种边界" agent-memory-boundaries
```

脚本会询问主题和一句话摘要，并在当天目录生成：

```text
public/2026/08/16/agent-memory-boundaries/index.html
```

若省略 slug，脚本会尝试从标题生成；纯中文标题可能回退为时间型 slug。发布后不要随意修改 slug，否则旧链接会失效。

### 2. 直接编辑 HTML

```bash
code public/2026/08/16/agent-memory-boundaries/index.html
```

以 `public/posts/_template/index.html` 为起点，但不要把模板当成统一主题。每篇文章应根据内容选择自己的排版、色彩、信息层次和必要交互。

单页至少包含：

- `<!doctype html>`、`<html lang="zh-CN">`、UTF-8 和 viewport。
- 唯一且准确的 `<title>`、`meta description` 和一个 `<h1>`。
- 文章正文的 `<main>` / `<article>` 语义结构。
- 发布日期、返回首页的链接和移动端布局。
- 页面专属 CSS 放在当前文件的 `<style>` 中；页面专属 JavaScript 放在当前文件的 `<script>` 中。
- 图片使用有意义的 `alt`；纯装饰图片使用 `alt=""`。
- 动画兼容 `prefers-reduced-motion`，交互元素可以用键盘操作。
- 不得保留 Hugo generator、livereload、`localhost` URL 或 Google Fonts 外链等旧构建残留。

字体和图片可以引用 `public/fonts/`、`public/images/` 等站内资源。核心阅读体验不能依赖 Hugo、打包器或运行时模板。

### 3. 更新入口与索引

文章页面完成后：

1. 在 `public/index.html` 增加文章入口，标题、主题、日期和 URL 必须与文章一致。
2. 更新 `public/sitemap.xml` 中对应的正式 URL 和 `lastmod`。
3. 若继续提供 RSS，再同步更新 `public/index.xml`。
4. 在 `CONTENT_TRACKER.md` 记录文章状态和最终路径。

`public/` 中的文件会被原样部署，不存在 `draft = true`。未完成文章请保留在本地未提交改动或独立分支中；不要把草稿提交到默认分支。

## 本地预览

```bash
python3 -m http.server 8080 -d public
```

访问 <http://localhost:8080/>，从首页进入文章。不要直接双击 HTML：本地 HTTP 服务更接近线上路径行为。

发布前至少检查桌面端和窄屏：

- 首页入口能打开正确页面。
- 页面内目录、锚点和返回首页链接可用。
- 正文、代码块、表格和图片不会横向撑破页面。
- 浏览器控制台没有资源 404 或 JavaScript 错误。

## SEO 与结构检查

```bash
./check-seo.sh
```

脚本检查 `public/`、日期目录中的文章、基础元信息、canonical、Open Graph、robots 和 sitemap。详细要求见 `SEO_GUIDE.md`。

如果正式域名发生变化，可临时指定检查目标：

```bash
SITE_ORIGIN="https://example.com" ./check-seo.sh
```

## 发布

```bash
git status --short
git diff --check
git add public/YYYY/MM/DD/slug/index.html public/index.html public/sitemap.xml CONTENT_TRACKER.md
git commit -m "Add article: 文章标题"
git push
```

推送到 `main` 或 `master` 后，GitHub Actions 会直接上传 `public/`。部署流程不会运行 Hugo，也不会把 Markdown 转换为 HTML。

## 文件速查

| 文件或目录 | 用途 | 是否参与线上发布 |
| --- | --- | --- |
| `public/index.html` | 首页和主要文章索引 | 是 |
| `public/YYYY/MM/DD/slug/index.html` | 正式文章 | 是 |
| `public/posts/_template/index.html` | 新文章起始模板 | 是，但不作为文章入口 |
| `public/sitemap.xml` | 搜索引擎 URL 索引 | 是 |
| `public/index.xml` | RSS（若继续维护） | 是 |
| `CONTENT_PLAN.md` | 长期选题与内容规划 | 否 |
| `CONTENT_TRACKER.md` | 写作状态与发布记录 | 否 |
| `content/`、`themes/`、`hugo.toml` | 历史 Hugo 资料 | 否 |

## 发布前清单

- [ ] 路径严格为 `public/YYYY/MM/DD/slug/index.html`
- [ ] 页面内容是完整 HTML，不含未替换的 `{{PLACEHOLDER}}`
- [ ] 视觉方案服务于本篇主题，与其他文章有明确差异
- [ ] 标题、摘要、发布日期、canonical 和分享元信息正确
- [ ] canonical 与 `og:url` 均使用 `https://muzig.io` 正式主域
- [ ] 页面不含 Hugo livereload、`localhost` 或 Google Fonts 外链
- [ ] 只有一个 `<h1>`，正文标题层级连续
- [ ] 代码示例已经运行或核对
- [ ] 图片有尺寸约束和正确 `alt`
- [ ] 桌面端、移动端和键盘导航可用
- [ ] 返回首页及站内链接无误
- [ ] 首页、sitemap 和 RSS（如使用）已经同步
- [ ] `./check-seo.sh` 没有 FAIL
- [ ] `CONTENT_TRACKER.md` 已更新为 Published

## 常见问题

### 为什么项目里还存在 Markdown 和 Hugo 文件？

它们记录了旧站点的历史内容和配置，暂不删除。但新文章只编辑 `public/` 下的 HTML，部署也只读取 `public/`。

### 可以复用上一篇文章的样式吗？

可以复用可靠的可访问性和响应式做法，但不要复制成统一皮肤。先确定文章的视觉概念，再调整版式、字体尺度、颜色、图形和交互。

### 如何处理未完成文章？

默认分支里的 `public/` 就是发布内容，没有草稿开关。草稿应留在本地未提交改动或独立分支，完成检查后再合入。

### 发布后发现错误怎么办？

直接修正对应的 `index.html`，必要时在正文中写明更新日期；如果标题或摘要改变，同时更新首页和 sitemap。

---

最后更新：2026-08-16
