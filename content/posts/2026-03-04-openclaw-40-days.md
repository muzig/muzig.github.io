+++
date = '2026-03-04T08:00:00+08:00'
draft = false
title = "从 Vibe Coding 到 Agentic Engineering：AI Agent 的 40 天进化之路"
categories = ["AI工程"]
series = ["OpenClaw 深度系列"]
articleType = "观点评论"
tags = ["OpenClaw", "Agent", "Agentic Engineering", "生产力"]
+++

> "我唯一做的事，就是跟它们说话。不是调 prompt，不是换模型，就是说话、给反馈、看着它们记下来。"
> — Shubham Saboo

最近读到一篇非常有意思的文章，来自 @Shubham Saboo 的 40 天 OpenClaw 实战总结。他展示了如何用一套简单的 markdown 文件系统，让 AI Agent 团队 24/7 帮他干活。这篇文章让我重新思考了"人机协作"这件事。

---

## 核心哲学：文件系统就是操作系统

Shubham 的方法论极其简洁：**不需要 orchestration framework，不需要 message queue，不需要 database，文件系统就是集成层。**

模型还是那个模型（第 1 天和第 40 天用的是同一个），但周围的 markdown 文件越来越丰富，Agent 越来越"懂"他。

---

## 三层架构：Identity → Operations → Knowledge

### Layer 1: Identity（我是谁）
- **SOUL.md** — Agent 的灵魂
- **IDENTITY.md** — 快速参考卡
- **USER.md** — Agent 服务的人

### Layer 2: Operations（怎么干活）
- **AGENTS.md** — 行为规则
- **HEARTBEAT.md** — 自愈检查

### Layer 3: Knowledge（学到了什么）
- **MEMORY.md** — 长期记忆
- **memory/YYYY-MM-DD.md** — 日常日志
- **shared-context/** — 跨 Agent 共享

---

## 真正有效的 Memory 系统

Agent 自己写"错题本"，下次就不再犯。

### 40 天节奏建议

| 时间 | 做什么 |
|------|--------|
| Day 1 | 安装 + 写 SOUL.md/IDENTITY.md/USER.md |
| Day 3 | 开始给具体反馈 |
| Week 1 | 创建 AGENTS.md |
| Week 2 | 开始 MEMORY.md |
| Week 3 | 加第二个 Agent |
| Week 4 | 加 HEARTBEAT.md |

---

## 写在最后

与其给 Agent 塞 100 个工具，不如：
1. 少工具，多观察
2. 用文件代替记忆
3. 把 AI 当新员工培养

不是让 AI 来适应你的思维方式，而是你先学会像智能体一样看世界。

---

## 参考来源

- [Shubham Saboo: How to set up OpenClaw Agents that actually get better Over Time](https://x.com/Saboo_Shubham_/status/2027463195150131572)
