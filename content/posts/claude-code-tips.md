+++
date = '2026-02-02T19:00:00+08:00'
draft = false
title = "Claude Code 团队使用技巧：10 个核心实践"
categories = ["Agent工具链"]
series = ["Claude Code 实战"]
articleType = "实战教程"
tags = ["Claude Code", "AI 工具", "开发效率", "编程助手"]
+++

> 本文整理自 Boris Cherny（Claude Code 创建者）在 Twitter/X 上分享的团队内部使用技巧。

Claude Code 是 Anthropic 推出的智能编程助手，其团队在长期使用中总结出了一套高效的工作流程。以下是 10 个核心技巧，帮助你最大化 Claude Code 的生产力。

---

## 1. 🔥 并行处理 (Do more in parallel)

**这是团队认为最大的生产力提升点。**

同时开启 **3-5 个 git worktrees**，每个运行独立的 Claude 会话：

```bash
# 创建 worktree 示例
git worktree add .claude/worktrees/my-worktree origin/main
```

- 个人可以使用多个 git checkouts，但团队偏好 worktrees
- 每个 worktree 完全独立，可以同时处理不同任务

---

## 2. 📝 以计划模式开始复杂任务 (Plan mode first)

**核心原则：先计划，后执行。**

对每个复杂任务：
1. 开启 **Plan Mode**（`plan mode on`，使用 `shift+Tab` 切换）
2. 倾注精力制定详细计划
3. 让 Claude **"one-shot"**（一次性）完成实现

**进阶玩法**：
- 用第一个 Claude 写计划
- 用第二个 Claude 作为"高级工程师"审查计划
- 出现偏差时随时切换回计划模式

---

## 3. 🧠 投资你的 CLAUDE.md

**让 Claude 记住教训，避免重复犯错。**

每次修正错误后，以这句话结尾：

> *"Update your CLAUDE.md so you don't make that mistake again"*

不断迭代编辑 CLAUDE.md：

| 级别 | 路径 | Token 限制 |
|------|------|------------|
| 全局 | `~/.claude/CLAUDE.md` | 76 tokens |
| 项目级 | `CLAUDE.md` | 4k tokens |

使用 `/memory` 命令管理记忆文件。

---

## 4. 🛠️ 创建自定义 Skills 并提交到 Git

**黄金规则：如果每天做某件事超过一次，将其变成 Skill 或斜杠命令。**

创建自己的技能并提交到 git，实现跨项目复用：

**示例**：构建 `/techdebt` 斜杠命令，每次会话结束时自动查找并消除重复代码。

---

## 5. 🔧 让 Claude 自主修复 Bug

**不要微观管理，直接告诉 Claude 目标。**

| 场景 | 指令 |
|------|------|
| **Slack 集成** | 粘贴 bug 讨论串，只说 `"fix"` |
| **CI 测试** | `"Go fix the failing CI tests"` |
| **Docker 日志** | 指向日志，让它自己分析 |

Claude 会自动理解上下文并执行修复。

---

## 6. 💬 提升提示词技巧 (Level up prompting)

### 严格审查模式

> `"Grill me on these changes and don't make a PR until I pass your test"`

让 Claude 成为你的代码审查员。

### 行为验证

> `"Prove to me this works"`

让 Claude 比较 main 分支和你的功能分支的行为差异。

---

## 7. 💻 终端与环境设置

| 组件 | 推荐 |
|------|------|
| **终端** | [Ghostty](https://ghostty.org) - 同步渲染、24位颜色、Unicode 支持 |
| **状态栏** | `/statusline` - 显示**上下文使用量** + **当前 git 分支** |

显示 git 分支方便在多个 Claude 会话间快速识别上下文。

---

## 8. 🤖 使用子代理 (Subagents)

**在需要"投入更多计算"的任务后附加 `"use subagents"`。**

**核心用途**：
- **任务卸载** — 将单个任务卸载给子代理，保持主代理上下文窗口干净
- **权限路由** — 通过 hook 将权限请求路由到 **Opus 4.5** 处理
- **并行探索** — 同时启动多个代理分析不同维度

**并行探索示例**（5 个代理同时工作）：
- 入口点分析
- React 组件梳理
- 工具实现审查
- 状态管理检查
- 测试基础设施评估

---

## 9. 📊 使用 Claude 进行数据分析

**一句话搞定数据分析：**

要求 Claude 使用 `bq`（BigQuery CLI）实时拉取和分析指标。

团队将 BigQuery 技能 check-in 到代码库，所有人直接在 Claude Code 中运行查询，真正做到了：

> 💬 *"没有写一行代码"*

---

## 10. 📚 与 Claude 一起学习

| 方式 | 操作 |
|------|------|
| **解释模式** | `/config` → `"Explanatory"` 或 `"Learning"` 风格 |
| **可视化学习** | 让 Claude 生成 HTML 演示解释概念 |

启用解释模式后，Claude 会解释其更改背后的"为什么"。

---

## 💡 额外建议

> **Bob Sheth 建议**：为每个 Claude 会话添加自动评估和评分，长期积累最佳实践。

---

## 🎯 核心理念

> *"There is no one right way to use Claude Code -- everyone's setup is different. You should experiment to see what works for you!"*

**没有一种唯一正确的使用方式，每个人的设置都不同，应该实验找到适合你的方法！**

---

## 参考资料

1. [Boris Cherny on X](https://x.com/bcherny) - 原始分享
2. [Claude Code 官网](https://claude.ai/code)
3. [Anthropic 官方文档](https://docs.anthropic.com/)
