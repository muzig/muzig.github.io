+++
date = '2026-03-05T10:00:00+08:00'
draft = false
title = "6个反直觉的Agent工程原则"
categories = ["AI工程"]
series = ["AI 工程观察"]
articleType = "方法论"
tags = ["Agent", "AI 工程", "Claude Code", "提示词工程"]
+++

> 原文来自 @systematicls 的 Twitter，分享了他对 Agent 工程实践的深度思考。

几条反直觉的观点：

1. **上下文是一切** — 你的 CLAUDE.md 不该是百科全书，而是 IF-ELSE 导航：什么场景读什么规则。

2. **研究和执行必须分离** — "帮我建认证系统" 是错的。正确流程：研究方案 → 决策 → 新上下文执行。

3. **Agent 天生想讨好你** — 问"找 bug"，它会编造 bug。用中性提示词，或用对抗 Agent 互相验证。

4. **Agent 知道怎么开始，不知道怎么结束** — 用测试 + 截图 + 合同文件定义"完成"。

5. **规则会越加越乱** — 定期让 Agent 帮你整理合并，清除矛盾。

6. **少即是多** — 简化你的提示词和工作流。

---

**Bonus**：如果某个功能真的重要，OpenAI 和 Anthropic 会把它做进产品。所以别焦虑"新工具"，更新 CLI、读更新日志就够了。

---

## 参考资料

- [How To Be A World-Class Agentic Engineer](https://www.andyvora.com/world-class-agentic-engineer)
- 推文链接：https://x.com/KKaWSB/status/2029269334993088820
