+++
date = '2026-02-03T17:12:00+08:00'
draft = false
title = 'OpenClaw Node 执行权限配置详解'
tags = ['OpenClaw', 'Node', 'Security', 'Config']
categories = ['技术文章']
+++

在使用 OpenClaw 远程控制 Node（如 Windows PC）时，执行命令的权限管理是一个关键安全问题。本文介绍如何配置 exec-approvals 来实现精细化的命令执行控制。

---

## 问题背景

当 OpenClaw Agent 尝试在远程 Node 上执行系统命令时，默认情况下会被拒绝：

```text
Exec denied (node=..., allowlist-miss): cmd /c "dir /ad D:\"
```

这是因为 Node 的安全策略默认使用 `allowlist` 模式，只有通过批准的命令才能执行。

---

## 配置文件结构

OpenClaw Node 的执行权限配置文件通常位于：

```
%USERPROFILE%\.openclaw\exec-approvals.json
```

完整配置示例：

```json
{
  "version": 1,
  "socket": {
    "path": "C:\\Users\\<username>\\.openclaw\\exec-approvals.sock",
    "token": "<your-secret-token>"
  },
  "defaults": {
    "security": "full",
    "ask": "off"
  },
  "agents": {
    "main": {
      "security": "full"
    }
  }
}
```

---

## 核心配置项解析

### 1. Security 模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `full` | 完全允许所有命令 | 私有可信环境 |
| `allowlist` | 仅允许批准列表中的命令 | 生产/多用户环境 |
| `deny` | 完全拒绝所有命令 | 只读模式 |

### 2. Ask 设置

控制命令执行前是否需要用户确认：

- `"ask": "off"` - 直接执行，无需确认（推荐用于自动化）
- `"ask": "on"` - 每次执行前弹出确认对话框

### 3. Agent 级配置

可以为不同 Agent 设置不同权限：

```json
"agents": {
  "main": {
    "security": "full"
  },
  "sub-agent-1": {
    "security": "allowlist",
    "ask": "on"
  }
}
```

---

## 配置步骤

### 步骤 1：定位配置文件

在 Windows PowerShell 中：

```powershell
$env:USERPROFILE\.openclaw\exec-approvals.json
```

如果文件不存在，创建目录和文件：

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.openclaw"
```

### 步骤 2：编辑配置文件

根据需求选择合适的 `security` 级别：

**方案 A：开发环境（完全信任）**

```json
{
  "version": 1,
  "defaults": {
    "security": "full",
    "ask": "off"
  }
}
```

**方案 B：受控环境（白名单模式）**

```json
{
  "version": 1,
  "defaults": {
    "security": "allowlist",
    "ask": "off"
  },
  "approvals": [
    "powershell -Command *",
    "cmd /c dir *",
    "git *"
  ]
}
```

### 步骤 3：重启 Node 服务

修改配置后需要重启 OpenClaw Node 服务使配置生效。

---

## 验证配置

配置完成后，测试命令执行：

```powershell
# 测试简单命令
openclaw-node exec -- powershell -Command "Get-Location"

# 测试 Agent 远程执行
# （通过 OpenClaw Agent 发送命令到 Node）
```

---

## 最佳实践

### ✅ 推荐做法

1. **分层权限**：对敏感操作使用 `allowlist`，日常操作使用 `full`
2. **最小权限原则**：仅授予必要的命令执行权限
3. **定期审计**：检查批准列表，移除不再需要的条目
4. **Token 安全**：定期更换 socket token，避免硬编码在代码中

### ❌ 避免的错误

1. 不要将 `exec-approvals.json` 提交到 Git 仓库
2. 不要在公共网络暴露 Node 服务端口
3. 不要对所有 Agent 使用 `full` 权限而不加区分

---

## 常见问题

**Q: 修改配置后不生效？**

A: 需要重启 OpenClaw Node 服务。在 Windows 上，重启 OpenClaw Node 应用程序。

**Q: 如何临时允许一个命令？**

A: 使用命令行批准：

```powershell
openclaw-node approve "your-command-here"
```

**Q: 如何查看当前批准列表？**

A: 检查配置文件中的 `approvals` 数组，或使用：

```powershell
openclaw-node approvals list
```

---

## 总结

OpenClaw 的执行权限配置提供了灵活的安全控制：

1. **Security 模式**决定命令执行的宽松程度
2. **Ask 设置**控制执行前是否需人工确认
3. **Agent 级配置**实现细粒度权限管理
4. **白名单模式**适合生产环境的精细化控制

根据实际使用场景选择合适的配置，在便利性和安全性之间取得平衡。

---

## 参考资料

1. [OpenClaw 官方文档](https://docs.openclaw.ai)
2. [OpenClaw GitHub 仓库](https://github.com/openclaw/openclaw)
