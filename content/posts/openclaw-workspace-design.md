+++
date = '2026-02-02T19:30:00+08:00'
draft = false
title = 'OpenClaw 工作区设计：两级 Memory 与目录组织最佳实践'
tags = ['OpenClaw', 'AI工具', '工作区设计', '最佳实践']
categories = ['技术文章']
+++

> 本文分享在使用 OpenClaw 过程中总结的工作区设计经验，包括两级 Memory 架构、目录组织策略和多项目管理办法。

---

## 问题背景

在使用 AI 编程助手时，经常会遇到这样的问题：
- 多个项目如何管理？
- AI 的记忆放在哪里？
- 如何区分系统配置和项目数据？

OpenClaw 通过**两级 Memory** 和**集中式工作区**的设计很好地解决了这些问题。

---

## 核心设计：两级 Memory 架构

```
┌─────────────────────────────────────────────────────────┐
│  🔵 系统级 (System)                                      │
│  ~/.openclaw/                                           │
│  └── 跨所有工作区共享                                     │
├─────────────────────────────────────────────────────────┤
│  🟢 项目级 (Workspace)                                   │
│  ~/workspaces/project/                                  │
│  └── 仅当前工作区有效                                     │
└─────────────────────────────────────────────────────────┘
```

### 🔵 系统级 Memory (`~/.openclaw/`)

**用途**: AI 运行时数据、跨项目共享

```
~/.openclaw/
├── agents/
│   └── main/
│       ├── sessions/          # 所有会话历史
│       └── memory-*.jsonl     # 提取的记忆片段
├── skills/                    # 安装的 skill
├── openclaw.json              # 全局配置
└── exec-approvals.json        # 执行授权
```

**特点**:
- 自动管理，无需手动编辑
- 临时/可重建，重装软件时可清理
- 包含 API 密钥、认证信息

### 🟢 项目级 Memory (`~/workspaces/project/`)

**用途**: 当前项目的专属内容

```
~/workspaces/default/
├── MEMORY.md          # 手动编辑的长期记忆
├── SOUL.md            # AI 人设
├── USER.md            # 用户信息
├── AGENTS.md          # 工作区指南
├── TOOLS.md           # 工具配置
├── HEARTBEAT.md       # 定时任务
├── BOOTSTRAP.md       # 首次启动脚本
└── memory/            # 每日笔记
```

**特点**:
- 用户完全控制
- 需要版本控制（git）
- 项目专属知识库

---

## 目录组织最佳实践

### ❌ 不推荐：分散式

```
~/
├── project-a/                # 项目1
├── project-b/                # 项目2
├── project-c/                # 项目3
├── project-d/                # 项目4
└── ...                       # 主目录杂乱
```

**问题**:
- 主目录项目太多，难以管理
- 分不清哪些是 AI 工作区
- 备份时需要一个个找

### ✅ 推荐：集中式

```
~/
└── workspaces/               # 统一入口
    ├── default/              # 通用/默认项目
    ├── project-a/            # 项目 A
    ├── project-b/            # 项目 B
    └── project-c/            # 项目 C
```

**优势**:
- 一目了然的目录结构
- 方便批量备份
- 符合 Unix 哲学（一切皆文件）

---

## 配置实现

### 配置文件：`~/.openclaw/openclaw.json`

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/workspaces/default"
    },
    "list": [
      {
        "id": "main"
      },
      {
        "id": "project-a",
        "name": "project-a",
        "workspace": "~/workspaces/project-a",
        "agentDir": "~/.openclaw/agents/project-a/agent"
      }
    ]
  }
}
```

### 多 Agent 配置

| Agent ID | 工作目录 | 用途 |
|----------|----------|------|
| `main` | `~/workspaces/default` | 默认/通用项目 |
| `project-a` | `~/workspaces/project-a` | 项目 A |
| `project-b` | `~/workspaces/project-b` | 项目 B |
| `project-c` | `~/workspaces/project-c` | 项目 C |

### 启动方式

```bash
# 默认启动（使用 main）
openclaw

# 指定 Agent 启动
openclaw --agent helix

# 临时切换工作区
openclaw -w ~/workspaces/blog
```

---

## 迁移实战

### 场景：将分散的项目迁移到 workspaces

**步骤 1**: 创建集中目录
```bash
mkdir -p ~/workspaces
```

**步骤 2**: 移动现有项目
```bash
# 移动项目 A
mv ~/project-a ~/workspaces/project-a

# 移动项目 B
mv ~/.openclaw/workspace-project-b ~/workspaces/project-b

# 移动其他项目
mv ~/project-c ~/workspaces/project-c
```

**步骤 3**: 更新配置
编辑 `~/.openclaw/openclaw.json`:
```json
{
  "agents": {
    "defaults": {
      "workspace": "~/workspaces/default"
    },
    "list": [
      {
        "id": "project-a",
        "workspace": "~/workspaces/project-a"
      }
    ]
  }
}
```

**步骤 4**: 清理旧目录
```bash
rm -rf ~/.openclaw/workspace-helix
```

---

## 设计原理总结

### 为什么分两级？

| 层级 | 管理方 | 生命周期 | 备份策略 |
|------|--------|----------|----------|
| 系统级 | OpenClaw | 临时/可重建 | 低优先级 |
| 项目级 | 用户 | 长期/资产 | 高优先级 |

### 为什么集中 workspaces？

1. **清晰**: 一眼看到所有项目
2. **备份**: `rsync -av ~/workspaces/ backup/` 即可
3. **隔离**: 项目间不会互相污染
4. **扩展**: 新项目按标准创建即可

---

## 常见问题

### Q: 系统级 Memory 和项目级 Memory 会冲突吗？

不会。OpenClaw 会同时搜索两者：
- `memory_search` → 搜索 `~/.openclaw/` 的自动记忆
- `read MEMORY.md` → 读取项目的 `~/workspaces/xxx/MEMORY.md`

### Q: 我应该把什么放到 MEMORY.md？

- 项目相关的决策记录
- 常用命令和工作流
- 工具配置和 API 密钥
- 经验教训和最佳实践

### Q: 不同工作区之间如何共享知识？

- 系统级配置（`~/.openclaw/`）全局共享
- 通用知识放在 `~/workspaces/default/MEMORY.md`
- 项目专属知识放在各自 `MEMORY.md`

---

## 总结

OpenClaw 的两级 Memory 和集中式工作区设计，实现了：

1. **系统与数据分离** → 软件升级不影响项目
2. **全局与局部共存** → 通用配置 + 项目定制
3. **集中管理** → 清晰、可备份、可扩展

**核心理念**: 让 AI 管理运行时，让用户掌控知识资产。

---

## 参考

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [Claude Code 团队使用技巧](/posts/claude-code-tips/)
