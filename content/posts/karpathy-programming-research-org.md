+++
date = '2026-02-28T08:20:00+08:00'
draft = false
title = '当 Andrej Karpathy 开始"编程一个研究组织"'
tags = ['AI', 'Agent', 'Karpathy', '研究组织', '工程']
categories = ['技术深度']
+++

最近，Andrej Karpathy 在 nanochat 上做了一个非常有代表性的实验。

他没有只运行一个 agent。而是一次性运行了 8 个：
- 4 个 Claude
- 4 个 Codex
- 每个分配 1 块 GPU
- 目标：删除 logit softcap，同时不引入回归

他的 TL;DR 很直接：**目前不太行。有点混乱。**

但从系统角度看，这个实验非常有意思。

---

## 实验：用 AI 组织做研究

Karpathy 尝试了几种组织结构：

**1. 8 个独立研究员**
每个 agent 自主开分支，独立探索。

**2. 1 个 Chief Scientist + 8 个 Junior**
一个 agent 负责拆解任务和分配工作，其余执行。

这已经不是在"用 AI 写代码"。而是在测试：**AI 组织是否能做研究？**

---

## 工程基础设施：极简但系统化

整个研究组织建立在非常简单的基础设施上：

- 每个 research program 是一个 git branch
- 每个 scientist fork 成 feature branch
- 使用 git worktrees 做隔离
- 简单文件作为通信机制
- 不用 Docker / VM（指令约束已足够）
- 所有 agent 运行在 tmux 网格中

这看起来像一个"AI 研究办公室"——可以实时观察每个 agent 的工作，也可以随时接管。

视觉上非常优雅。但结果并不优雅。

---

## 为什么目前效果不好？

问题不是执行能力。**问题是研究能力。**

Karpathy 观察到，这些 agent：
- 不会严谨设计实验
- baseline 不够强
- 不做系统 ablation
- 不控制 compute
- 不归一 FLOPs
- 容易产生"伪发现"

一个典型例子：

某个 agent "发现"增大 hidden size 会降低 validation loss。但：
- 更大模型训练更久
- compute 未对齐
- 对照实验不足
- 结论不可归因

这是典型的 **spurious result**。agent 很擅长实现想法，但不会严格审视想法。

---

## 真正的转变：从写代码到编程组织

这次实验的核心洞察并不是："AI 研究员还不够好"。

而是：**工程师开始在编程一个组织。**

这里的"源码"变成了：
- prompts
- roles
- tools
- communication protocol
- review 机制
- standup 流程

甚至每天的 standup，本质上也是"org code"。

nanochat 只是一个 eval。真正的问题是：**给定任意任务，这个研究组织能否持续地产生有效进展？**

---

## 一个更大的趋势

从更宏观的角度看，这可能预示着工程范式的变化：

1. **过去**：编程函数
2. **现在**：编程 agent
3. **下一步**：编程组织

未来的工程师，不只是写代码的人。而是**设计系统的人**。

Karpathy 的实验目前结论很现实：
- agent 执行力很强
- 创造性研究能力仍然不足

但方向已经清晰：**真正的杠杆在于组织设计。**

---

## 延伸方向

如果你感兴趣，这篇还可以升级成：
- 更偏技术深度分析版（讲研究方法论）
- 更偏未来趋势判断版
- 更偏 AI 组织工程实操指南版
- 或者更偏 Twitter thread 风格
