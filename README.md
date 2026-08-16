# Muzig · Digital Field Notes

一个不使用统一文章主题的静态技术博客。每篇文章都是一份独立、可直接发布的单文件 HTML；内容和视觉可以一起演进。

## 目录约定

```text
public/
├── index.html                         # 首页与文章索引
├── posts/_template/index.html         # 新文章起始模板
└── YYYY/MM/DD/article-slug/index.html # 独立文章
```

`public/` 是线上站点的唯一发布源。`content/`、Hugo 配置和主题仅作为旧内容存档保留，不再参与部署。

## 新建文章

```bash
./new-post.sh "文章标题" english-url-slug
```

脚本会创建一份包含完整 HTML、内联 CSS 和 SEO 元信息的文章。生成后：

1. 直接编辑对应的 `index.html`，并按主题自由调整视觉。
2. 在 `public/index.html` 的文章网格中增加入口。
3. 本地预览：

```bash
python3 -m http.server 8080 -d public
```

访问 <http://localhost:8080>。

## 发布

推送到 `main` 或 `master` 后，GitHub Actions 会直接部署 `public/`，不会再运行 Hugo 或覆盖手工 HTML。

## 单文件原则

- 页面逻辑和页面专属样式放在同一个 HTML 文件中。
- 可以引用站内公共字体或图片；关键阅读体验不依赖构建工具。
- 每篇文章应保留返回首页的入口、移动端布局、页面标题和 description。
- 视觉无需统一，但导航语义与可访问性应保持可靠。
