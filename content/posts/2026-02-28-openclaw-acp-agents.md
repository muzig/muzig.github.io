+++
date = '2026-02-28T22:30:00+08:00'
draft = false
title = "OpenClaw ACP Agents：打通 Claude Code、Codex、Gemini CLI 的终极方案"
categories = ["Agent工具链"]
series = ["OpenClaw 深度系列"]
articleType = "实战教程"
tags = ["OpenClaw", "ACP", "Claude Code", "Codex", "Gemini CLI", "MCP"]
+++

## 为什么需要 ACP Agents？

如果你和我一样，在日常开发中频繁使用 Claude Code、Codex、Gemini CLI 等 AI 编程助手，你可能已经遇到了一个痛点：**如何在一个统一的界面中调度这些不同的工具？**

每个工具都有自己的交互方式：
- Claude Code 有它自己的终端界面
- Codex 通过命令行运行
- Gemini CLI 又是另一种体验

**OpenClaw 的 ACP (Agent Client Protocol) Agents** 正是为了解决这个问题而生。它让你能够通过统一的接口，在 Discord、Telegram 等聊天界面中直接驱动这些外部 AI 编程助手。

---

## 什么是 ACP？

**ACP** 全称 **Agent Client Protocol**，是一个标准化的协议，允许 OpenClaw 通过后端插件与外部 coding harnesses 进行通信。

目前支持的 harnesses 包括：
- **Pi** (由 Anthropic 开发)
- **Claude Code** (Anthropic 的终端编程助手)
- **Codex** (OpenAI 的代码生成工具)
- **OpenCode** (开源编码助手)
- **Gemini CLI** (Google 的命令行 AI 工具)

### ACP vs 原生 Sub-agents

| 特性 | ACP Session | Sub-agent Run |
|------|-------------|---------------|
| **运行时** | ACP 后端插件 (如 acpx) | OpenClaw 原生 sub-agent 运行时 |
| **Session Key** | `agent:<agentId>:acp:<uuid>` | `agent:<agentId>:subagent:<uuid>` |
| **主命令** | `/acp ...` | `/subagents ...` |
| **Spawn 工具** | `sessions_spawn` 配合 `runtime: "acp"` | `sessions_spawn` (默认 runtime) |

**简单总结**：如果你想要外部专业工具的 runtime，用 ACP；如果你想要 OpenClaw 原生的轻量级并发执行，用 sub-agents。

---

## 快速上手

### 1. 配置 ACP 后端

首先安装并启用 acpx 插件：

```bash
openclaw plugins install @openclaw/acpx
openclaw config set plugins.entries.acpx.enabled true
```

然后在 OpenClaw 配置中添加 ACP 基础配置：

```yaml
acp:
  enabled: true
  dispatch:
    enabled: true
  backend: "acpx"
  defaultAgent: "codex"
  allowedAgents: ["pi", "claude", "codex", "opencode", "gemini"]
  maxConcurrentSessions: 8
  stream:
    coalesceIdleMs: 300
    maxChunkChars: 1200
  runtime:
    ttlMinutes: 120
```

验证配置是否正确：

```bash
/acp doctor
```

### 2. 启动 ACP Session

在 Discord（或其他支持的聊天平台）中，你可以用自然语言启动 ACP session：

> "Start a persistent Codex session in a thread here and keep it focused."

或者使用命令式的方式：

```bash
/acp spawn codex --mode persistent --thread auto
```

常用参数说明：
- `--mode persistent|oneshot`: 持久会话或一次性运行
- `--thread auto|here|off`: 自动绑定/当前线程/不绑定线程
- `--cwd <path>`: 设置工作目录
- `--label <name>`: 给会话设置标签

### 3. 与 ACP Session 交互

一旦 ACP session 启动并绑定到线程，后续在该线程中的所有消息都会自动路由到这个 session：

```
你: "帮我重构这个函数，提高可读性"
ACP Agent: [分析代码并提出重构建议]

你: "把变量名改得更语义化一些"
ACP Agent: [继续基于上下文进行修改]
```

### 4. 管理 ACP Session

```bash
# 查看当前 session 状态
/acp status

# 调整运行时选项
/acp model anthropic/claude-opus-4-5
/acp permissions strict
/acp timeout 120

# 给运行中的 session 发送指令
/acp steer "tighten logging and continue"

# 停止当前任务
/acp cancel

# 关闭 session 并解绑线程
/acp close

# 列出所有 ACP sessions
/acp sessions
```

---

## Thread-Bound Sessions：频道无关的持久化

ACP 最强大的特性之一是 **Thread-bound sessions**。它的工作原理：

1. OpenClaw 将一个 thread 绑定到目标 ACP session
2. 该 thread 中的后续消息自动路由到绑定的 ACP session
3. ACP 输出自动返回到同一个 thread
4. 取消关注/关闭/归档/超时后，绑定自动解除

这意味着你可以在 Discord 的一个 thread 里和 Claude Code 持续对话，就像在本地终端使用它一样自然。

### 支持的频道

目前内置支持 Thread binding 的频道：
- **Discord**

其他插件频道可以通过相同的绑定接口添加支持。

---

## 通过 sessions_spawn 程序化启动

如果你想从 agent turn 或工具调用中启动 ACP session，可以使用 `sessions_spawn`：

```json
{
  "task": "Open the repo and summarize failing tests",
  "runtime": "acp",
  "agentId": "codex",
  "thread": true,
  "mode": "session"
}
```

关键参数：
- `task` (必需): 初始提示词
- `runtime` (ACP 必需): 必须设置为 `"acp"`
- `agentId` (可选): ACP 目标 harness ID，省略时使用 `acp.defaultAgent`
- `thread` (可选, 默认 false): 是否请求线程绑定
- `mode` (可选): `run` (一次性) 或 `session` (持久化)
- `cwd` (可选): 工作目录
- `label` (可选): 操作员可见的标签

---

## 完整命令速查表

| 命令 | 功能 | 示例 |
|------|------|------|
| `/acp spawn` | 创建 ACP session，可选 thread 绑定 | `/acp spawn codex --mode persistent --thread auto --cwd /repo` |
| `/acp cancel` | 取消目标 session 的正在执行的 turn | `/acp cancel agent:codex:acp:<uuid>` |
| `/acp steer` | 给运行中的 session 发送指令 | `/acp steer --session support inbox prioritize failing tests` |
| `/acp close` | 关闭 session 并解绑 thread | `/acp close` |
| `/acp status` | 显示后端、模式、状态、运行时选项 | `/acp status` |
| `/acp set-mode` | 设置目标 session 的运行时模式 | `/acp set-mode plan` |
| `/acp set` | 通用运行时配置写入 | `/acp set model openai/gpt-5.2` |
| `/acp cwd` | 设置运行时工作目录覆盖 | `/acp cwd /Users/user/Projects/repo` |
| `/acp permissions` | 设置审批策略 profile | `/acp permissions strict` |
| `/acp timeout` | 设置运行时超时（秒） | `/acp timeout 120` |
| `/acp model` | 设置运行时模型覆盖 | `/acp model anthropic/claude-opus-4-5` |
| `/acp reset-options` | 移除 session 运行时选项覆盖 | `/acp reset-options` |
| `/acp sessions` | 从 store 列出最近的 ACP sessions | `/acp sessions` |
| `/acp doctor` | 后端健康、能力、可操作的修复 | `/acp doctor` |
| `/acp install` | 打印确定性安装和启用步骤 | `/acp install` |

---

## 故障排除

| 症状 | 可能原因 | 解决方案 |
|------|----------|----------|
| `ACP runtime backend is not configured` | 后端插件缺失或禁用 | 安装并启用后端插件，然后运行 `/acp doctor` |
| `ACP is disabled by policy` | ACP 全局禁用 | 设置 `acp.enabled=true` |
| `ACP dispatch is disabled by policy` | 从普通 thread 消息分派禁用 | 设置 `acp.dispatch.enabled=true` |
| `ACP agent "<id>" is not allowed by policy` | Agent 不在允许列表中 | 使用允许的 `agentId` 或更新 `acp.allowedAgents` |
| `Unable to resolve session target: ...` | Key/ID/Label token 错误 | 运行 `/acp sessions`，复制精确的 key/label，重试 |
| `--thread here requires running /acp spawn inside an active thread` | 在 thread 上下文外使用了 `--thread here` | 移动到目标 thread 或使用 `--thread auto/off` |
| `Only <user-id> can rebind this thread` | 其他用户拥有 thread binding | 以所有者身份重新绑定或使用不同的 thread |
| `Thread bindings are unavailable for <channel>` | 适配器缺少 thread binding 能力 | 使用 `--thread off` 或移动到支持的适配器/频道 |
| `Missing ACP metadata for bound session` | 过期/删除的 ACP session 元数据 | 使用 `/acp spawn` 重新创建，然后重新绑定/聚焦 thread |

---

## 实际应用场景

### 场景 1：Discord 中的代码审查

在 Discord 的 thread 中启动 Claude Code：

```bash
/acp spawn claude --mode persistent --thread here --cwd /path/to/repo
```

然后直接贴代码片段，让 Claude 帮你审查：

> "帮我审查这段代码，看看有没有并发安全问题"

### 场景 2：并行使用不同工具

- 在 Thread A 用 Codex 生成测试代码
- 在 Thread B 用 Claude Code 重构旧代码
- 在 Thread C 用 Gemini CLI 分析性能

每个 session 独立运行，互不干扰。

### 场景 3：团队协作

团队成员可以在同一个 Discord 服务器的不同 thread 中同时使用不同的 AI 工具，所有对话历史都保存在 thread 中，方便后续查阅。

---

## 总结

OpenClaw 的 ACP Agents 为我们提供了一种统一、标准化的方式来集成和调度各种外部 AI 编程助手。

**核心要点：**

1. **标准化协议**：通过 ACP 协议，OpenClaw 可以与 Pi、Claude Code、Codex、OpenCode、Gemini CLI 等工具无缝集成

2. **Thread-bound Sessions**：支持将 ACP session 绑定到 Discord 等平台的 thread，实现持久化、上下文连续的对话体验

3. **灵活的控制**：丰富的 `/acp` 命令集让你可以精细控制每个 session 的行为

4. **与 Sub-agents 互补**：ACP 用于外部专业工具 runtime，Sub-agents 用于原生轻量级并发，两者相辅相成

如果你正在寻找一个统一调度多个 AI 编程助手的解决方案，ACP Agents 值得一试。

---

## 参考资料

1. [OpenClaw ACP Agents 官方文档](https://docs.openclaw.ai/tools/acp-agents)
2. [OpenClaw 官网](https://openclaw.ai/)
3. [GitHub: openclaw/openclaw](https://github.com/openclaw/openclaw)
4. [Agent Client Protocol](https://agentclientprotocol.com/)

---

> 💡 **下期预告**：深入探讨 OpenClaw 的 Sub-agents 机制，以及如何设计高效的多 Agent 协作系统

> 📬 **订阅更新**：欢迎 Star [GitHub 仓库](https://github.com/muzig/muzig.github.io) 获取最新文章推送
