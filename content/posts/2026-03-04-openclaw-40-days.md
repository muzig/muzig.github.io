+++
date = '2026-03-04T08:00:00+08:00'
draft = false
title = '从 Vibe Coding 到 Agentic Engineering：AI Agent 的 40 天进化之路'
tags = ['AI Agent', 'OpenClaw', 'Agentic Engineering', '生产力']
categories = ['技术思考']
+++

> "我唯一做的事，就是跟它们说话。不是调 prompt，不是换模型，就是说话、给反馈、看着它们记下来。"
> — Shubham Saboo

最近读到一篇非常有意思的文章，来自 @Shubham Saboo 的 40 天 OpenClaw 实战总结。他展示了如何用一套简单的 markdown 文件系统，让 AI Agent 团队 24/7 帮他干活。这篇文章让我重新思考了"人机协作"这件事。

---

## 核心哲学：文件系统就是操作系统

Shubham 的方法论极其简洁：**不需要 orchestration framework，不需要 message queue，不需要 database，文件系统就是集成层。**

模型还是那个模型（第 1 天和第 40 天用的是同一个），但周围的 markdown 文件越来越丰富，Agent 越来越"懂"他。

> 这让我想到一句话：与其不断增加工具数量，不如提升 AI 自主获取信息的能力。给它一根鱼竿，比每天给它送鱼有用得多。

---

## 三层架构：Identity → Operations → Knowledge

### Layer 1: Identity（我是谁）

- **SOUL.md** — Agent 的灵魂，定义它是谁、做什么、怎么表现
- **IDENTITY.md** — 快速参考卡，名字、角色、风格
- **USER.md** — Agent 服务的人是谁，有什么偏好

```markdown
# SOUL.md (Dwight)

## Core Identity
Dwight — the research brain. Named after Dwight Schrute because you share his
intensity: thorough to a fault, knows EVERYTHING in your domain.

## Your Principles
1. NEVER Make Things Up — Every claim has a source link
2. Signal Over Noise — Not everything trending matters
3. Prioritize relevance to AI/agents
```

一个有趣的技巧：**用电视剧角色给 Agent 命名**。当你告诉 Claude "你有 Dwight Schrute 的能量"，它从训练数据里就知道这是什么特质——30 季的角色 development 免费加载。

### Layer 2: Operations（怎么干活）

- **AGENTS.md** — 行为规则，启动流程，文件读取顺序
- **HEARTBEAT.md** — 自愈检查，监控 cron job、browser 状态

### Layer 3: Knowledge（学到了什么）

- **MEMORY.md** — 长期记忆，蒸馏后的关键教训
- **memory/YYYY-MM-DD.md** — 日常日志
- **shared-context/** — 跨 Agent 共享知识层

---

## 真正有效的 Memory 系统

很多人在 Agent 里塞各种 memory 功能，但 Shubham 的方法出奇地简单：

**Tier 1: MEMORY.md**
不是原始日志，是提炼后的"硬教训"：

```markdown
## Hard Lessons
- NEVER delete project folders without asking Shubham.
  On Feb 26, deleted Ross's gemini-council React app during cleanup.
  React version was lost. Always ask before removing anything.
```

Agent 自己写"错题本"，下次就不再犯。

**Tier 2: memory/YYYY-MM-DD.md**
每天的原始记录，做了什么、反馈是什么。

**Tier 3: shared-context/**
跨 Agent 共享的上下文：
- THESIS.md — 你当前的世界观
- FEEDBACK-LOG.md — 跨 Agent 的纠正
- SIGNALS.md — 你在追踪的趋势

---

## 一个关键洞察：渐进披露

Claude Code 团队学到的最重要一课：

**不是一次性把所有信息倒给 AI，而是让它按需发现。**

- 最初用 RAG 向量数据库 → 发现 AI 是被动接受上下文
- 后来改成给 AI 一个 Grep 工具 → 让它自己搜索
- 效果出人意料地好

这就是"渐进披露"（Progressive Disclosure）：教 AI 如何自己找答案，而不是喂答案。

---

## 40 天节奏建议

| 时间 | 做什么 |
|------|--------|
| Day 1 | 安装 + 写 SOUL.md/IDENTITY.md/USER.md |
| Day 3 | 开始给具体反馈，确保写到 memory 文件 |
| Week 1 | 创建 AGENTS.md，定义启动流程 |
| Week 2 | 开始 MEMORY.md，提炼重复的纠正 |
| Week 3 | 加第二个 Agent，搭建文件协调 |
| Week 4 | 加 HEARTBEAT.md（等第一次出问题后） |

> "别想太复杂，每天跟 Agent 聊，文件自己就会变丰富。"

---

## 写在最后

2026 年了，我们跟 AI 协作的方式，是不是从根上就搞错了？

与其给 Agent 塞 100 个工具，不如：
1. 少工具，多观察
2. 用文件代替记忆
3. 把 AI 当新员工培养，而不是当软件部署

Karpathy 说的 "Agentic Engineering" 就是这个意思：**AI 负责执行，人类负责架构、质量和正确性。**

不是让 AI 来适应你的思维方式，而是你先学会像智能体一样看世界。

---

## 参考来源

- [Shubham Saboo: How to set up OpenClaw Agents that actually get better Over Time](https://x.com/Saboo_Shubham_/status/2027463195150131572)
- [Anthropic Engineering Blog: Building Effective Agents](https://www.anthropic.com/engineering)
