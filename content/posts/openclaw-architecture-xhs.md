+++
date = '2026-02-03T16:40:00+08:00'
draft = false
title = 'OpenClaw 架构揭秘：1个大脑 N个手脚，AI 这么玩才香 🔥'
tags = ['OpenClaw', 'AI', 'Agent', '架构', '工具']
categories = ['技术文章']
+++

> 💡 一句话总结：OpenClaw 让你的 AI 拥有多个"专家人格"和多个"远程手脚"

## 🤔 先讲个场景

想象一下：
- 你在家用手机对 AI 说："拍张客厅照片，分析一下布置，然后写个改造建议发我邮箱"
- AI 自动调用**手机摄像头**拍照 → **分析模型**看图 → **写作模型**生成报告 → **电脑**发邮件

全程无缝衔接，就像有个 24 小时待命的团队 ⚡

这就是 OpenClaw 想做的事。

---

## 🧠 核心概念：Agent vs Node

很多人搞混这两个概念，其实特别简单：

| | **Agent（智能体）** | **Node（节点）** |
|---|:---:|:---:|
| **是什么** | 不同的"专家大脑" | 不同的"操作终端" |
| **负责** | 怎么思考、怎么决策 | 在哪执行、用什么工具 |
| **例子** | 编程专家、写作专家、分析师 | 家里 Mac、办公室 PC、手机 |

**记忆口诀：**
> 🧠 Agent = 能力维度（擅长什么）
> 📍 Node = 位置维度（在哪干活）

---

## 👥 多 Agent：一个平台，多种专家

OpenClaw 的 Gateway（网关）是总控制中心，你可以配置多个 Agent：

```
┌─────────────────┐
│    Gateway      │  ← 总指挥
│   （总控制中心）  │
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┐
    ▼         ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│编程专家│ │写作专家│ │分析专家│ │客服专家│
└───────┘ └───────┘ └───────┘ └───────┘
```

### 实际配置示例

在 `~/.openclaw/openclaw.json` 中：

```json
{
  "agents": {
    "defaults": { "agentId": "general" },
    "routing": {
      "coding@example.com": { 
        "agentId": "pi", 
        "workspace": "code" 
      },
      "writing@example.com": { 
        "agentId": "writer", 
        "workspace": "docs" 
      }
    }
  }
}
```

**根据发件人自动路由到不同专家** ✨

---

## 📱 多 Node：AI 的远程手脚

你的 AI 不只能在自己电脑上跑，还能控制其他设备：

| Node | 位置 | 能做的事 |
|------|------|---------|
| 🏠 Node A | 家里 Mac | 浏览器、文件、摄像头 |
| 🏢 Node B | 办公室 PC | 大屏、内网资源 |
| 📱 Node C | 手机 | 相机、位置、移动场景 |
| ☁️ Node D | 服务器 | 24h 在线、定时任务 |

### 真实场景举例

**场景 1：远程监控**
```
你说："看看家里猫在干嘛"
→ Agent 调用 Node A（家里 Mac）摄像头
→ 拍照 → 分析 → 回复你
```

**场景 2：跨设备工作流**
```
你说："把这份报告发到公司群"
→ Agent 在家里电脑上编辑
→ 调用办公室 Node 发送到企业微信
```

**场景 3：分布式任务**
```
你说："分析服务器日志，有问题就打电话通知我"
→ 服务器 Node 持续监控
→ 发现问题 → 手机 Node 拨打电话
```

---

## 🔄 两者组合：1+1 > 2

真正的威力在于**Agent + Node 的组合**：

```
用户请求
    │
    ▼
┌─────────────┐
│   Gateway   │  ← 路由决策
└──────┬──────┘
       │
       ▼
┌──────────────┐
│  Agent 3     │  ← 分析专家
│ （分析意图）  │
└──────┬───────┘
       │
       ▼ 调用
┌──────────────┐
│   Node C     │  ← 手机摄像头
│  （拍照）     │
└──────┬───────┘
       │
       ▼ 返回结果
┌──────────────┐
│  Agent 2     │  ← 写作专家
│ （生成报告）  │
└──────┬───────┘
       │
       ▼ 调用
┌──────────────┐
│   Node D     │  ← 服务器
│ （保存文件）  │
└──────────────┘
```

**一句话：不同的任务用不同的专家，不同的设备干不同的活** 🎯

---

## 🚀 快速上手指南

### 1. 配置多 Agent

```bash
# 编辑配置文件
vim ~/.openclaw/openclaw.json

# 添加路由规则（根据需求自动分配）
{
  "agents": {
    "routing": {
      "*.code": { "agentId": "pi", "workspace": "coding" },
      "*.write": { "agentId": "writer", "workspace": "docs" }
    }
  }
}
```

### 2. 启动 Node 设备

要让一台设备成为 Node，首先要在该设备上启动 Node 守护进程：

**方式一：前台启动（调试/临时使用）**
```bash
openclaw node run --host <gateway-host> --port 18789 --display-name "家里 Mac"
```

**方式二：通过 SSH 隧道连接（Gateway 绑定到 loopback 时）**
```bash
# 终端 A：建立隧道（保持运行）
ssh -N -L 18790:127.0.0.1:18789 user@gateway-host

# 终端 B：通过隧道连接
export OPENCLAW_GATEWAY_TOKEN="<gateway-token>"
openclaw node run --host 127.0.0.1 --port 18790 --display-name "办公室 PC"
```

**方式三：后台服务启动（推荐长期运行）**
```bash
openclaw node install --host <gateway-host> --port 18789 --display-name "服务器 Node"
openclaw node restart
```

启动后，Node 会自动向 Gateway 发起配对请求。

### 3. 配对 Node 设备

在 Gateway 端批准配对：

```bash
# 查看待配对设备
openclaw nodes pending

# 批准配对
openclaw nodes approve <device-id>

# 查看已配对节点
openclaw nodes status
```

### 4. 跨 Node 调用测试

```bash
# 在手机上拍照
openclaw nodes camera_snap --node=phone-node --facing=back

# 在服务器上执行命令
openclaw nodes run --node=server-node --command="df -h"
```

---

## 💡 关键洞察

| 你想实现 | 配置什么 |
|---------|---------|
| 不同任务用不同 AI 模式 | **多 Agent** |
| 在不同设备上执行操作 | **多 Node** |
| 复杂工作流（任务+设备组合） | **两者都用** |

### 类比理解 🎭

- **Agent** = 公司里的不同部门（技术部/市场部/设计部）
- **Node** = 不同城市的分公司（北京/上海/深圳）
- **Gateway** = 总公司调度中心

一个项目可以：北京技术部开发 → 上海市场部推广 → 深圳分公司执行

---

## 📝 总结

OpenClaw 的架构设计很清晰：

1. **Agent 解决"谁来做"** —— 不同专家处理不同任务
2. **Node 解决"在哪做"** —— 不同设备执行不同操作
3. **Gateway 解决"怎么分配"** —— 智能路由，无缝调度

这种设计让 AI 从"单机版"变成了"分布式网络版"，能力边界直接翻倍 🚀

**未来已来，只是分布不均。**

---

## 🔧 常见问题与实战排错

### 1. Node 启动报错 `ECONNREFUSED`

**原因**：Gateway 默认只绑定到 `127.0.0.1`，其他设备无法连接。

**解决**：修改 Gateway 绑定到 LAN：
```bash
# 在 Gateway 机器上执行
openclaw config set gateway.bind lan
# 然后重启 Gateway
```

**注意**：`lan` 比 `0.0.0.0` 更安全，只监听局域网地址。

---

### 2. 报错 `pairing required`

**原因**：Node 已连上 Gateway，但需要管理员批准配对。

**解决**：
```bash
# 在 Gateway 端查看配对请求（注意是 devices，不是 nodes）
openclaw devices list
openclaw devices approve <requestId>

# 或者一键批准所有
openclaw devices approve --all
```

---

### 3. Windows 作为 Node 如何设置 Token

**PowerShell**：
```powershell
$env:OPENCLAW_GATEWAY_TOKEN="<your-token>"
openclaw node run --host <gateway-ip> --port 18789 --display-name "Windows PC"
```

**CMD**：
```cmd
set OPENCLAW_GATEWAY_TOKEN=<your-token>
openclaw node run --host <gateway-ip> --port 18789 --display-name "Windows PC"
```

**获取 Token**：
```bash
# 在 Gateway 端
openclaw config get gateway.auth.token
```

---

### 4. 防火墙配置

**测试连通性**（Windows）：
```powershell
Test-NetConnection -ComputerName <gateway-ip> -Port 18789
```

**Mac 端防火墙**（如果 LAN 设备连不上）：
```bash
# 检查状态
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# 临时关闭测试（记得开回来）
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off
```

---

### 5. 执行命令超时/需要批准

首次在新 Node 上执行命令可能需要**执行批准**。两种方式：

**方式一**：实时批准（Windows 端会弹出提示）

**方式二**：配置免批准（开发环境）：
```bash
# 在 Node 机器上
openclaw approvals allowlist add --node <node-id> "/usr/bin/uname"
```

---

### 6. 检查 Node 是否连接成功

**Gateway 端查看**：
```bash
openclaw nodes status --connected
openclaw nodes describe --node "Windows PC"
```

**执行测试命令**：
```bash
openclaw nodes run --node "Windows PC" --raw "hostname"
```

---

## 📌 延伸阅读
- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [MCP 协议介绍](/posts/mcp/)
- [Go 语言 MCP 实现](/posts/go-mcp/)

---

*有问题欢迎评论交流 👇*
