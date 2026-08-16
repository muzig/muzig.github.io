# 技术博客内容更新规划

## 📌 内容方向定位

基于现有文章分析，博客核心定位：

- **深度技术解析**：不追求快餐式内容，专注技术本质
- **系统化知识**：通过系列文章构建完整知识体系
- **实践与理论结合**：既有原理分析，又有实战案例

### 发布格式约束

本规划中的每个“文章”都指一份手工维护的单文件 HTML：

```text
public/YYYY/MM/DD/slug/index.html
```

- `public/` 是唯一发布源；新内容不再写入 `content/*.md`。
- Hugo 配置、旧 Markdown 和主题只作为历史存档，不参与生产部署。
- 页面从 `public/posts/_template/index.html` 起步，但每篇文章应发展出与主题匹配的独立视觉语言，而不是套用统一皮肤。
- 页面专属 CSS 和 JavaScript 内联到当前 HTML；允许引用 `public/fonts/`、`public/images/` 中的站内资源。
- canonical 与 `og:url` 统一使用 `https://muzig.io`；不得提交 Hugo livereload、`localhost` URL 或 Google Fonts 外链。
- 每篇内容上线时同时维护 `public/index.html`、`public/sitemap.xml`，以及仍在使用的 `public/index.xml`。
- `CONTENT_PLAN.md`、`CONTENT_TRACKER.md` 等仓库管理文档仍可使用 Markdown，它们不是对外发布的文章页面。

---

## 🎯 三大核心主题线

### 1️⃣ MCP 技术深度系列（已启动）

**现有文章**：

- ✅ MCP 基础介绍
- ✅ Go 语言 MCP 实现解析

**规划内容**：

- [ ] MCP 与其他 AI 集成方案对比（LangChain、Function Calling 等）
- [ ] MCP 服务端开发实战：从零实现一个生产级 MCP Server
- [ ] MCP 性能优化：传输层选择与优化策略
- [ ] MCP 安全实践：认证、授权与沙箱机制
- [ ] MCP 生态观察：主流实现对比（Python、TypeScript、Go）
- [ ] 企业级 MCP 应用架构设计

**更新节奏**：每月 1-2 篇（深度文章需要充分准备）

---

### 2️⃣ Go 语言工程实践系列

**现有文章**：

- ✅ Go 语言妆容（makeup）
- ✅ Go 升级检查工具

**规划内容**：

#### 子系列 A：Go 性能优化

- [ ] Go 内存管理深度剖析：从分配到回收
- [ ] Go 并发模型实战：goroutine 调度原理
- [ ] Go 性能分析工具链：pprof、trace 实战
- [ ] Go 编译优化：如何让你的程序更快
- [ ] Go 垃圾回收器演进：从 STW 到并发 GC

#### 子系列 B：Go 工具链深度探索

- [ ] Go 模块系统演进与最佳实践
- [ ] Go 泛型设计哲学与应用场景
- [ ] Go AST 与代码生成实战
- [ ] Go 调试技巧：delve 进阶使用

#### 子系列 C：Go 架构设计

- [ ] Go 微服务架构模式
- [ ] Go 错误处理最佳实践
- [ ] Go 测试金字塔：单元、集成、性能测试
- [ ] Go 依赖注入与接口设计

**更新节奏**：每月 2-3 篇（平衡深度与频率）

---

### 3️⃣ 编程语言原理系列（已启动）

**现有文章**：

- ✅ 编程语言核心要素
- ✅ 编程语言妆容
- ✅ 编程语言过程

**规划内容**：

#### 子系列 A：语言设计对比

- [ ] 类型系统演进：从动态到静态到渐进式
- [ ] 内存管理模型对比：GC vs RAII vs Ownership
- [ ] 并发模型横向对比：线程 vs 协程 vs Actor vs Async
- [ ] 错误处理机制：异常 vs 返回值 vs Effect System
- [ ] 模块化设计：从 include 到 package 到 module

#### 子系列 B：现代语言特性深度解析

- [ ] Rust 所有权系统设计哲学
- [ ] Swift 值类型与引用类型的性能权衡
- [ ] Kotlin 协程实现原理
- [ ] TypeScript 类型推导机制

#### 子系列 C：语言演进案例研究

- [ ] Python 2 → 3 迁移教训与启示
- [ ] Java 长期支持版本策略分析
- [ ] JavaScript 标准化演进历程
- [ ] C++ 向后兼容的代价

**更新节奏**：每月 1-2 篇（研究性内容，需要深入调研）

---

## 📅 内容发布计划（建议）

### 月度节奏（可持续模式）

```
每月产出：4-6 篇文章
- MCP 系列：1 篇
- Go 系列：2-3 篇
- 编程语言系列：1-2 篇

具体安排：
第 1 周：研究与资料收集
第 2 周：撰写初稿（2 篇）
第 3 周：完善与 Review（1-2 篇）
第 4 周：发布与预热下月内容
```

### 季度里程碑

**Q1 (1-3 月)**：

- 完成 MCP 实战系列 2-3 篇
- Go 性能优化子系列启动（2-3 篇）
- 编程语言类型系统对比文章

**Q2 (4-6 月)**：

- MCP 安全与架构文章
- Go 工具链深度探索系列
- 现代语言特性解析（Rust/Swift）

**Q3 (7-9 月)**：

- MCP 生态对比与总结
- Go 架构设计系列
- 语言演进案例研究

**Q4 (10-12 月)**：

- 年度技术趋势总结
- 最佳实践合集
- 下一年规划

---

## 🔥 内容增值策略

### 1. 系列化深耕

- 每个系列至少 5 篇文章，形成知识体系
- 提供系列导航页，方便读者系统学习
- 每个系列结束后整理成 PDF/电子书

### 2. 互动与反馈

- 文章底部添加「下期预告」增加期待
- 开放评论或 GitHub Discussions 收集读者建议
- 定期做读者调研，了解感兴趣的主题

### 3. 多形式呈现

- 深度文章（主打）
- 快速技巧（Quick Tips，轻量级）
- 月度技术观察（News Digest）
- 年度回顾与展望

### 4. SEO 与传播

- 关键词优化：聚焦「Go 性能优化」「MCP 实战」等高价值关键词
- 社交媒体同步：Twitter、掘金、V2EX 等平台
- 技术社区互动：在 Reddit、HackerNews 分享

---

## 📊 质量控制标准

### 文章质量检查清单

- [ ] 技术准确性验证（代码可运行、原理正确）
- [ ] 结构清晰（目录、代码示例、总结）
- [ ] 配图丰富（架构图、对比表、流程图）
- [ ] 代码示例完整可运行
- [ ] 参考资料完备
- [ ] 排版美观（代码高亮、适当留白）

### 深度标准

- **基础介绍**：适合新手，包含背景知识
- **原理解析**：深入源码或设计文档
- **实战案例**：可复现的完整示例
- **性能分析**：Benchmark 数据支撑
- **最佳实践**：经验总结与避坑指南

---

## 🎨 内容创新建议

### 1. 对比分析型

例：《Go vs Rust：系统编程语言的性能与安全权衡》

### 2. 源码解读型

例：《从源码看 Go Channel 的底层实现》

### 3. 实战工具型

例：《打造自己的 Go 代码生成工具》

### 4. 思考总结型

例：《技术选型的 10 个误区》

### 5. 趋势观察型

例：《2026 年编程语言发展趋势观察》

---

## 💡 长期价值积累

### 建立个人技术品牌

- **定位**：深度技术内容创作者
- **差异化**：不做快餐内容，专注系统化知识
- **影响力**：通过高质量内容建立行业认知

### 知识资产沉淀

- 文章归档与标签系统
- 知识图谱建立
- 定期更新老文章（技术演进）

### 社区贡献

- 开源配套示例代码
- 贡献到相关技术文档
- 参与技术会议分享

---

## 🚀 快速启动：下个月的行动计划

### 第一周（研究周）

1. 选定下月主题（从规划中选 3-4 个）
2. 收集资料、阅读源码、准备环境
3. 起草文章大纲

### 第二周（创作周）

1. 完成 2 篇文章初稿
2. 准备代码示例与 Benchmark

### 第三周（打磨周）

1. Review 文章，补充细节
2. 制作配图与图表
3. 完成 1-2 篇额外文章

### 第四周（发布周）

1. 发布文章并推广
2. 回复读者评论
3. 规划下月内容

---

## 📝 单文件 HTML 内容骨架

实际创建请运行 `./new-post.sh "文章标题" english-slug`，并直接编辑生成的 `index.html`。下面只表示内容语义，不规定视觉风格：

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="准确概括文章价值的一句话">
  <link rel="canonical" href="https://muzig.io/YYYY/MM/DD/slug/">
  <meta property="og:type" content="article">
  <meta property="og:title" content="文章标题">
  <meta property="og:description" content="准确概括文章价值的一句话">
  <meta property="og:url" content="https://muzig.io/YYYY/MM/DD/slug/">
  <meta property="article:published_time" content="YYYY-MM-DDTHH:MM:SS+08:00">
  <title>文章标题 · Muzig</title>
  <style>
    /* 为本篇主题设计独立、响应式的视觉系统 */
  </style>
</head>
<body>
  <nav><a href="/">返回首页</a></nav>
  <main>
    <article>
      <header><h1>文章标题</h1></header>
      <section aria-labelledby="context"><h2 id="context">问题与背景</h2></section>
      <section aria-labelledby="concept"><h2 id="concept">核心概念</h2></section>
      <section aria-labelledby="practice"><h2 id="practice">实战与验证</h2></section>
      <section aria-labelledby="summary"><h2 id="summary">总结与延伸</h2></section>
    </article>
  </main>
</body>
</html>
```

HTML 是发布载体，不是内容结构的限制。对比型文章可以采用双栏和矩阵，源码解读可以采用代码剧场，趋势观察可以采用时间轴；基础元信息、语义、可访问性和移动端体验保持可靠即可。

---

## ⚡ 效率提升工具

### 写作工具

- **大纲工具**：Notion、Obsidian
- **代码管理**：GitHub Gist、CodeSandbox
- **图表制作**：Excalidraw、draw.io
- **性能测试**：Go Benchmark、pprof

### 灵感来源

- Go 官方博客与提案
- Rust Blog
- HackerNews
- Reddit (r/golang, r/programming)
- 技术会议演讲（GopherCon、FOSDEM）

---

## 🎯 核心原则

1. **质量优先于数量**：宁可少写，也要保证深度
2. **系列化思维**：单篇成文，系列成书
3. **持续学习**：写作即学习，通过输出倒逼输入
4. **读者导向**：解决真实问题，而非炫技
5. **长期主义**：技术博客是马拉松，不是短跑

---

最后更新：2026-08-16
下次 Review：2026-10-15
