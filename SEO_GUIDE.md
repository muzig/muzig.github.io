# 单文件 HTML 博客 SEO 指南

## 1. 适用范围

本站不再由 Hugo 生成。GitHub Pages 会原样发布 `public/`，所以 SEO 元信息、结构化数据、内部链接和索引文件都必须存在于最终 HTML 或 `public/` 下的静态文件中。

正式文章路径固定为：

```text
public/YYYY/MM/DD/slug/index.html
```

对应 URL 为：

```text
https://muzig.github.io/YYYY/MM/DD/slug/
```

如果以后启用自定义域名，必须一次性同步所有 canonical、Open Graph URL、`robots.txt`、`sitemap.xml` 和 Search Console 资源，不能混用多个主域名。

## 2. 每篇文章的 `<head>`

每个 `index.html` 至少包含：

```html
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="清楚说明文章解决什么问题，避免堆砌关键词。">

<link rel="canonical" href="https://muzig.github.io/YYYY/MM/DD/slug/">

<meta property="og:type" content="article">
<meta property="og:title" content="文章标题">
<meta property="og:description" content="与正文一致的分享摘要">
<meta property="og:url" content="https://muzig.github.io/YYYY/MM/DD/slug/">
<meta property="article:published_time" content="YYYY-MM-DDTHH:MM:SS+08:00">

<title>文章标题 · Muzig</title>
```

有合适的分享图时再增加 `og:image`。图片应使用绝对 HTTPS URL，并保证线上可访问；没有合适图片时不要填空地址。

推荐加入 JSON-LD：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "文章标题",
  "description": "文章摘要",
  "datePublished": "YYYY-MM-DDTHH:MM:SS+08:00",
  "dateModified": "YYYY-MM-DDTHH:MM:SS+08:00",
  "author": { "@type": "Person", "name": "Muzig" },
  "mainEntityOfPage": "https://muzig.github.io/YYYY/MM/DD/slug/"
}
</script>
```

JSON 必须合法，且内容要与页面可见信息一致。文章更新时同步 `dateModified`。

## 3. 内容与语义结构

- 每页只有一个 `<h1>`，标题要准确描述主题，不为点击率牺牲含义。
- 使用 `<main>`、`<article>`、`<header>`、`<nav>`、`<section>`、`<footer>` 等语义元素。
- 标题按 `h1 → h2 → h3` 组织，避免仅为了字号跳级。
- 摘要应是自然语言，说明问题、对象和价值；不要机械追求关键词密度。
- 代码示例使用 `<pre><code>`，表格包含表头，引用标明来源。
- 图片文件名应可读，内容图片提供准确 `alt`，纯装饰图片使用空 `alt`。
- 链接文字要能脱离上下文理解，外部新窗口链接使用 `rel="noreferrer"` 或更严格策略。
- 至少提供一个清晰的返回首页入口，并在相关主题之间建立有意义的内部链接。

## 4. 单文件与独立视觉

每篇文章可以有完全不同的视觉语言，但技术底线一致：

- 页面专属 CSS 放进当前 HTML 的 `<style>`。
- 页面专属 JavaScript 放进当前 HTML 的 `<script>`，正文在禁用 JavaScript 时仍应可读。
- 可引用 `public/fonts/`、`public/images/` 等站内静态资源；不要依赖 Hugo 主题、模板 partial 或构建产物才能显示正文。
- 字体应使用 `public/fonts/` 中的本地文件或系统字体栈，不得提交 `fonts.googleapis.com`、`fonts.gstatic.com` 等 Google Fonts 外链。
- 删除所有 Hugo 开发残留，包括 `meta name="generator"`、livereload 脚本和指向 `localhost` 的 URL。
- 使用响应式布局，避免固定宽度导致移动端横向滚动。
- 设置图片尺寸或 `aspect-ratio`，减少布局偏移。
- 为动画提供 `prefers-reduced-motion` 降级。
- 保持足够颜色对比度、可见焦点和键盘可操作性。

SEO 不要求页面长得一致；清晰语义、可访问性、性能和内容质量才是共同约束。

## 5. 首页、sitemap 与 RSS

单文件模式没有构建器自动同步索引。每次发布或修改 URL 时需要手工维护：

1. `public/index.html`：新增或更新文章入口。
2. `public/sitemap.xml`：使用正式 HTTPS URL，禁止出现 `localhost`；更新 `lastmod`。
3. `public/index.xml`：如果继续提供 RSS，同步标题、摘要、链接和发布时间。
4. 文章内部相关链接：使用最终 URL，不链接到本地文件路径或 Markdown 源文件。

删除或迁移已发布 URL 时应保留兼容入口或规划重定向，避免直接制造 404。

## 6. robots 与站点验证

`public/robots.txt` 应引用正式 sitemap：

```text
User-agent: *
Allow: /

Sitemap: https://muzig.github.io/sitemap.xml
```

Google Search Console 的 HTML 验证文件直接放在 `public/` 根目录：

```text
public/googlexxxxxxxxxxxxxxxx.html
```

不要放到旧的 `static/`，因为部署不会再复制该目录。部署后先在正式域名打开验证文件，再在 Search Console 提交 `https://muzig.github.io/sitemap.xml`。

Bing Webmaster Tools 也提交同一个正式 sitemap。

## 7. 本地预览与自动检查

启动静态服务器：

```bash
python3 -m http.server 8080 -d public
```

运行仓库检查脚本：

```bash
./check-seo.sh
```

自定义正式域名：

```bash
SITE_ORIGIN="https://example.com" ./check-seo.sh
```

脚本中的结果含义：

- `FAIL`：缺少发布必需文件或关键 HTML 结构，应在发布前修复。
- `WARN`：页面可以显示，但 canonical、分享元信息、语言、索引或可访问性仍需检查。
- `PASS`：自动规则通过，仍需要浏览器人工检查内容与视觉。

## 8. 发布前检查

- [ ] 文件路径为 `public/YYYY/MM/DD/slug/index.html`
- [ ] title、description、一个 h1 和正文内容彼此一致
- [ ] canonical、`og:url`、发布时间使用正式 URL 与时区
- [ ] HTML 中没有 Hugo generator/livereload、`localhost`、本地绝对路径、Google Fonts 外链或模板占位符
- [ ] 首页入口、返回首页、目录和内部链接可用
- [ ] sitemap 与 RSS（如使用）已经同步
- [ ] 图片 alt、代码块、表格和标题层级正确
- [ ] 桌面、手机、键盘和 reduced motion 场景可用
- [ ] 浏览器控制台没有 404 和脚本错误
- [ ] `./check-seo.sh` 没有 FAIL

## 9. 定期维护

- 在 Search Console 检查索引覆盖、Core Web Vitals 和失效 URL。
- 定期检查外链、站内链接、sitemap 与首页是否一致。
- 技术内容发生变化时更新正文、`dateModified` 和必要的摘要。
- 使用 Lighthouse 或同类工具抽查性能、SEO 和可访问性。
- 自定义域名、URL 或目录规则变化时，先更新本文档和检查脚本，再迁移页面。

## 参考资料

- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Google Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article)
- [Open Graph protocol](https://ogp.me/)
- [Schema.org BlogPosting](https://schema.org/BlogPosting)

---

更新日期：2026-08-16
版本：2.0（单文件 HTML）
