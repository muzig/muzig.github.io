+++
date = '2026-02-05T00:00:00+08:00'
draft = false
title = "OpenClaw 多 Agent 架构深度解析：打造你的 AI 协作团队"
categories = ["AI工程"]
series = ["OpenClaw 深度系列"]
articleType = "架构拆解"
tags = ["OpenClaw", "Agent", "多 Agent", "架构设计", "自动化"]
+++

在日常使用 AI 助手时，我们经常会遇到这样的困扰：一个 AI 既要写代码、又要查资料、还要处理日常事务，结果是什么都做但什么都不精。如果能像人类团队一样，让不同的 AI 各自负责擅长的事情，岂不是更高效？

本文将深入解析 **OpenClaw 的多 Agent 架构**，带你了解如何通过 Agent 分工协作，构建一个高效的 AI 工作流。

---

## 为什么需要多 Agent？

想象这样一个场景：

- **场景 A**：你有一个通用的 AI 助手，但它既要处理 Unity 游戏开发，又要管理家庭日程，结果配置越来越复杂，工具权限难以控制。
- **场景 B**：你希望在 Telegram 上与 AI 深度讨论技术问题，但在 WhatsApp 上只想快速查询信息，不想被长篇大论打扰。
- **场景 C**：有一个复杂的任务，需要同时并行处理多个子任务，单个 AI 串行处理太慢。

**多 Agent 架构的核心价值**：

| 维度 | 单 Agent | 多 Agent |
|------|---------|---------|
| **专业分工** | 通用型，样样通样样松 | 专业型，各司其职 |
| **资源隔离** | 共享配置，容易冲突 | 独立工作区，互不干扰 |
| **安全边界** | 权限难控制 | 细粒度工具控制 |
| **并行处理** | 串行执行 | 多任务并行 |

---

## OpenClaw 的 Agent 架构

### 什么是 Agent？

在 OpenClaw 中，一个 Agent 是一个**完全隔离的 AI 大脑**，拥有：

- **独立工作区**：`~/workspaces/<agent>` —— 文件、配置、记忆
- **独立状态目录**：`~/.openclaw/agents/<agent>/agent` —— 认证、模型配置
- **独立会话存储**：`~/.openclaw/agents/<agent>/sessions` —— 聊天记录
- **独立人格配置**：`AGENTS.md`、`SOUL.md`、`USER.md`

```
~/.openclaw/
├── agents/
│   ├── main/           # 主 Agent
│   │   ├── agent/      # 配置和认证
│   │   └── sessions/   # 会话历史
│   ├── helix/          # 项目专用 Agent
│   │   ├── agent/
│   │   └── sessions/
│   └── unity/          # Unity 开发 Agent
│       ├── agent/
│       └── sessions/
└── workspaces/
    ├── clawd/          # main 的工作区
    ├── helix/          # helix 的工作区
    └── unity/          # unity 的工作区
```

### Agent 类型

OpenClaw 支持三种类型的 Agent 协作：

#### 1. 主 Agent（Main Agent）
- 默认 Agent，处理通用任务
- 负责协调和派发任务给其他 Agent

#### 2. 专用 Agent（Dedicated Agent）
- 针对特定领域或项目
- 例如：Unity 开发 Agent、家庭管理 Agent

#### 3. 子 Agent（Sub-Agent）
- 临时 spawned 出来的 Agent
- 处理并行任务，完成后自动销毁

---

## Agent 路由机制

### 入站路由（Gateway 层）

当消息进入 OpenClaw 时，Gateway 通过 **bindings** 配置决定路由到哪个 Agent：

```json5
// openclaw.json
{
  "agents": {
    "list": [
      { "id": "main", "workspace": "~/workspaces/clawd" },
      { "id": "helix", "workspace": "~/workspaces/helix" },
      { "id": "unity", "workspace": "~/workspaces/unity" }
    ]
  },
  "bindings": [
    // 按账号路由
    { "agentId": "main", "match": { "channel": "telegram", "accountId": "8134174815" } },
    { "agentId": "helix", "match": { "channel": "telegram", "accountId": "8221433362" } },
    { "agentId": "unity", "match": { "channel": "telegram", "accountId": "8444434740" } },
    
    // 按群组路由
    { "agentId": "unity", "match": { 
      "channel": "whatsapp", 
      "peer": { "kind": "group", "id": "xxx@g.us" } 
    }}
  ]
}
```

**路由优先级**（最具体的优先）：
1. `peer` 精确匹配（特定 DM/群组）
2. `guildId` / `teamId`（Discord/Slack）
3. `accountId` 匹配
4. 通道级匹配
5. 默认 Agent

### 出站派发（Agent 主动）

主 Agent 可以主动派发任务给其他 Agent，使用 `sessions_send` 工具：

```go
// 伪代码示意
sessions_send(
  agentId: "helix",
  message: "检查项目状态并生成报告"
)
```

---

## 子 Agent：并行任务处理

### 核心概念

**Sub-Agent** 是从现有 Agent 中 spawned 出来的后台任务：

- 在独立 session 中运行：`agent:<agentId>:subagent:<uuid>`
- 支持并行处理，不阻塞主 Agent
- 完成后自动向请求者汇报结果
- 可设置超时、清理策略

### 使用场景

```
你向 main 发送："帮我同时做三件事：
1. 检查 helix 项目的 git 状态
2. 查询今天的天气
3. 总结一下昨天的会议纪要"

main 的处理流程：
  ├→ spawn sub-agent A → 检查 helix git 状态
  ├→ spawn sub-agent B → 查询天气
  └→ spawn sub-agent C → 总结会议纪要
  
等待所有子 Agent 完成
  ↓
汇总结果并回复你
```

### 配置示例

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": "anthropic/claude-sonnet-4-5",  // 子 Agent 专用模型
        "thinking": "off",
        "maxConcurrent": 4,                      // 最大并发数
        "archiveAfterMinutes": 60                // 自动归档时间
      }
    },
    "list": [{
      "id": "main",
      "subagents": {
        "allowAgents": ["helix", "unity"]  // 允许派发给这些 Agent
      }
    }]
  }
}
```

---

## Agent 间通信

### 启用通信

在 `openclaw.json` 中启用 Agent-to-Agent 通信：

```json5
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "helix", "unity"]  // 允许通信的 Agent 列表
    }
  }
}
```

### 通信工具

| 工具 | 功能 | 使用场景 |
|------|------|---------|
| `sessions_send` | 向其他 Agent 发送消息 | 派发任务、请求协作 |
| `sessions_list` | 查看其他 Agent 的会话 | 检查谁在线 |
| `sessions_history` | 获取其他 Agent 的历史 | 了解上下文 |
| `session_status` | 查看 Agent 状态 | 检查是否忙碌 |

### 通信流程示例

```
你 → main: "让 helix 检查项目状态"
  ↓
main 识别任务应派发给 helix
  ↓
main → helix: "检查 git 状态"
  ↓
helix 执行 git status
  ↓
helix → main: "返回结果"
  ↓
main 汇总 → 你: "helix 项目状态正常，最新提交是..."
```

---

## 安全与隔离

### 工作区隔离

每个 Agent 拥有独立的工作目录，文件互不干扰：

```
main:   ~/workspaces/clawd/
helix:  ~/workspaces/helix/
unity:  ~/workspaces/unity/
```

### 工具权限控制

可以为每个 Agent 设置不同的工具权限：

```json5
{
  "agents": {
    "list": [{
      "id": "unity",
      "tools": {
        "allow": ["read", "exec", "sessions_spawn"],
        "deny": ["write", "edit", "apply_patch", "gateway", "cron"]
      }
    }]
  }
}
```

### 沙箱隔离

支持 Docker 沙箱，限制 Agent 的执行环境：

```json5
{
  "agents": {
    "list": [{
      "id": "unity",
      "sandbox": {
        "mode": "all",      // 总是沙箱
        "scope": "agent"    // 每个 Agent 独立容器
      }
    }]
  }
}
```

---

## 实战案例：Unity 开发工作流

### 场景描述

你正在开发一个 Unity 游戏项目，希望：
- 快速询问代码问题 → 主 Agent
- 深度技术讨论 → Unity 专用 Agent
- 并行检查多个模块 → Sub-Agent

### 配置方案

```json5
// openclaw.json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "通用助手",
        "workspace": "~/workspaces/clawd",
        "model": "anthropic/claude-sonnet-4-5"
      },
      {
        "id": "unity",
        "name": "Unity 专家",
        "workspace": "~/workspaces/unity",
        "model": "anthropic/claude-opus-4-5",
        "tools": {
          "allow": ["read", "exec", "sessions_spawn"],
          "deny": ["gateway", "cron"]
        }
      }
    ]
  },
  "bindings": [
    { "agentId": "main", "match": { "channel": "telegram", "accountId": "main_bot" } },
    { "agentId": "unity", "match": { "channel": "telegram", "accountId": "unity_bot" } }
  ],
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "unity"]
    }
  }
}
```

### 使用流程

```
你 → main: "Unity 项目中如何实现对象池？"
  ↓
main 识别为 Unity 问题
  ↓
main → unity: "解释对象池实现"
  ↓
unity 详细回答并给出代码
  ↓
unity → main: "返回结果"
  ↓
main 整理 → 你: "Unity 对象池的最佳实践是..."
```

---

## 最佳实践

### ✅ 推荐做法

1. **明确分工**：每个 Agent 专注一个领域
2. **合理命名**：Agent ID 要直观（`unity`、`home`、`work`）
3. **最小权限**：只给 Agent 需要的工具权限
4. **文档沉淀**：在每个 Agent 的 `AGENTS.md` 中记录职责

### ❌ 避免的错误

1. **过度拆分**：3-5 个 Agent 足够，太多反而难管理
2. **权限过大**：不要在所有 Agent 上开放危险工具
3. **循环依赖**：避免 Agent A 调用 B，B 又调用 A
4. **忽视隔离**：不要把敏感数据放在共享目录

### 文档建议

在每个 Agent 的 `AGENTS.md` 中添加：

```markdown
## Agent 协作规则

### 职责范围
- 本 Agent 负责：Unity 游戏开发相关任务
- 不处理：家庭日程、通用查询

### 任务派发
当用户提到以下关键词时，派发给对应 Agent：
- "Unity" / "游戏" / "C#" → 本 Agent 处理
- "helix" / "项目 A" → 派发给 helix Agent
- "家庭" / "日程" → 派发给 home Agent

### 工具使用
- ✅ 允许：read, exec, sessions_spawn
- ❌ 禁止：write（避免意外修改配置文件）
```

---

## 常见问题

**Q1: 子 Agent 和独立 Agent 有什么区别？**

A: 
- **子 Agent**：临时 spawned，用完即走，适合并行任务
- **独立 Agent**：长期运行，有独立身份和配置，适合不同场景

**Q2: Agent 之间能共享数据吗？**

A: 默认隔离，但可以通过：
- `sessions_send` 传递消息
- 共享文件目录（不推荐）
- 主 Agent 汇总转发

**Q3: 一个 WhatsApp 号能绑定多个 Agent 吗？**

A: 可以，通过 `peer` 匹配不同 DM/群组，但回复都用同一个号码发送。

**Q4: 子 Agent 失败后怎么办？**

A: 可以设置 `runTimeoutSeconds` 超时，或使用 `cleanup: "delete"` 自动清理。

---

## 总结

本文核心要点：

1. **多 Agent 架构**解决了单 Agent 的权限混乱和专业性不足问题
2. **Agent 路由**通过 bindings 配置实现入站消息的智能分发
3. **子 Agent**支持并行任务处理，提高整体效率
4. **Agent 间通信**通过工具调用实现协作，保持隔离性
5. **安全边界**通过工作区隔离、工具控制、沙箱实现

### 关键收获

多 Agent 不是炫技，而是**让 AI 像团队一样工作**——各司其职、协同配合。从单 Agent 到多 Agent 的演进，本质上是从"万能助手"到"专业团队"的升级。

### 延伸阅读

- [OpenClaw 官方文档 - Multi-Agent](https://docs.openclaw.ai/concepts/multi-agent)
- [OpenClaw 子 Agent 文档](https://docs.openclaw.ai/tools/subagents)
- [OpenClaw 工具配置](https://docs.openclaw.ai/gateway/configuration)

---

## 参考资料

1. [OpenClaw Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent)
2. [OpenClaw Sub-Agents](https://docs.openclaw.ai/tools/subagents)
3. [OpenClaw Tools Documentation](https://docs.openclaw.ai/tools)
4. [OpenClaw Configuration](https://docs.openclaw.ai/gateway/configuration)

---

> 💡 **下期预告**：深入解析 OpenClaw 的 Node 系统——如何在多设备间远程控制你的 AI 助手

> 📬 **订阅更新**：关注公众号或订阅 RSS，获取最新技术文章
