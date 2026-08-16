# 博客项目

- **本地路径**：`/Users/muzig/src/muzig.github.io`
- **正式主域**：`https://muzig.io/`
- **用途**：发布独立设计的技术博客文章
- **唯一发布源**：`public/`

## 不可变规则

1. 所有新文章都是完整的单文件 HTML，路径只能是：

   ```text
   public/YYYY/MM/DD/slug/index.html
   ```

2. 不为新文章创建 `content/posts/*.md`，不使用 Front Matter、Hugo archetype、Hugo server 或 Hugo build。
3. `content/`、`hugo.toml`、`themes/` 只保留为旧站历史，不参与生产部署，也不能用 Hugo 重新生成并覆盖 `public/`。
4. `public/posts/_template/index.html` 只提供可靠的起点，不是统一主题。每篇文章应根据内容重新设计排版、色彩、信息结构和适量交互。
5. 页面专属 CSS、JavaScript 放在当前 `index.html`；字体和图片可以引用 `public/fonts/`、`public/images/` 中的站内资源。
6. 每篇文章必须有完整 head 元信息、一个 h1、语义化正文、发布日期、返回首页链接、移动端布局和基本可访问性。
7. canonical、`og:url`、robots 和 sitemap 统一使用 `https://muzig.io`，不得提交 Hugo generator/livereload、`localhost` URL 或 Google Fonts 外链。
8. 发布文章时同步维护 `public/index.html`、`public/sitemap.xml`，以及继续提供时的 `public/index.xml`。
9. `public/` 会被原样部署，没有 `draft` 开关。草稿保留在未提交改动或独立分支。
10. “文章必须使用 HTML”不包括仓库内部的 README、规划、追踪和记忆文档；这些管理文档可以继续使用 Markdown。

## 标准流程

```bash
./new-post.sh "文章标题" english-slug
python3 -m http.server 8080 -d public
./check-seo.sh
```

生成后直接编辑 `public/YYYY/MM/DD/slug/index.html`，从首页验证实际入口，再提交到默认分支。GitHub Actions 直接部署 `public/`，不会运行 Hugo。

## 规范入口

- 快速流程：`QUICK_START.md`
- 内容与视觉规划：`CONTENT_PLAN.md`
- 发布状态：`CONTENT_TRACKER.md`
- SEO 与页面结构：`SEO_GUIDE.md`

---

最后更新：2026-08-16
