# Muzig

> 面向开发者的 AI 工程深度博客，聚焦 Agent 工具链、MCP、Go 工程与编程语言设计。

## 站点定位

这个仓库承载的是 `Muzig` 的独立技术博客，不是产品官网，也不是零散笔记仓库。

当前内容主轴：

- `AI工程`：Agent 协作、工作流、工程方法论
- `Agent工具链`：OpenClaw、Claude Code、Codex、Cursor 等工具实践
- `MCP`：协议原理、生态对比、实现细节
- `Go工程`：工具链、升级、性能与工程实践
- `编程语言`：语言设计、运行时、编译流程
- `LLM系统`：推理、架构、训练与部署取舍

## 内容模型

仓库内统一采用下面这套内容模型：

- `categories`：主题域，只表达“写的是什么”
- `series`：系列归属，用于组织连续内容
- `articleType`：文章形式，例如 `深度解析`、`实战教程`
- `tags`：检索关键词，只保留产品名、协议名、技术概念

规范细节见 [CONTENT_SCHEMA.md](/Users/ligang/src/github/muzig.github.io/CONTENT_SCHEMA.md)。

## 本地开发

```bash
# 本地预览（包含草稿）
hugo server -D

# 新建文章
./new-post.sh "文章标题"

# 构建生产版本
hugo --minify
```

## 写作入口

- [QUICK_START.md](/Users/ligang/src/github/muzig.github.io/QUICK_START.md)
- [CONTENT_SCHEMA.md](/Users/ligang/src/github/muzig.github.io/CONTENT_SCHEMA.md)
- [content/posts/_template.md](/Users/ligang/src/github/muzig.github.io/content/posts/_template.md)
- [CONTENT_PLAN.md](/Users/ligang/src/github/muzig.github.io/CONTENT_PLAN.md)

## 站点信息

- 博客主页：`https://muzig.io`
- RSS：`https://muzig.io/index.xml`
- GitHub：`https://github.com/muzig`
