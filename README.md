# StarryPen 静态网站

## 本地开发

```bash
# 启动开发服务器
hugo server -D

# 访问本地调试地址
open http://localhost:1313
```

## 📂 项目结构

```
.
├── content/         # 内容文档
├── themes/          # Hugo主题
├── static/          # 静态资源
├── public/          # 构建输出目录
├── hugo.toml        # 主配置文件
└── archetypes/      # 内容模板
```

## 📝 内容管理

创建新文章：

```bash
hugo new content content/posts/<new-content>.md
```

文章元数据模板：

```markdown
---
title: "文章标题"
date: {{ .Date }}
draft: true
tags: ["标签1", "标签2"]
---
```

## 🎨 主题配置

当前使用[Ananke主题](https://github.com/theNewDynamic/gohugo-theme-ananke)，主要配置项见：

```toml
[params]
  primary_color = "#0044ff"  # 主色调
  show_hero = true           # 显示首页大图
  social_links = [           # 社交媒体链接
    { platform = "github", url = "https://github.com/yourprofile" }
  ]
```

## 🛠 构建部署

生成生产环境静态文件：

```bash
hugo --minify
```

部署到Gitea Pages：

```bash
git add .
git commit -m "发布新版本"
git push
```

## 📌 注意事项

- 草稿文章需添加`draft: true`头信息
- 图片资源请存放至`static/images/`目录
- 修改主题配置后需重启Hugo服务
