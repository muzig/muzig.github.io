+++
date = '2026-02-03T17:45:00+08:00'
draft = false
title = 'llama.cpp vs vLLM：边缘部署与云端服务的架构抉择'
tags = ['LLM', 'Inference', 'llama.cpp', 'vLLM', 'Edge-Computing', 'GPU']
categories = ['技术深度']
+++

**llama.cpp** 和 **vLLM** 代表了两种截然不同的设计哲学，选择取决于你的部署场景是**边缘单用户**还是**云端高并发**。

---

## 核心架构差异

| 维度 | llama.cpp | vLLM |
|------|-----------|------|
| **设计语言** | C/C++（零依赖）| Python + CUDA |
| **核心创新** | GGUF 格式 + 内存映射 | PagedAttention + 连续批处理 |
| **内存管理** | 静态分配，mmap 按需加载 | 动态非连续块分配（类似 OS 虚拟内存）|
| **首要目标** | 单流效率与跨平台便携性 | 多用户吞吐量与 GPU 利用率 |
| **模型格式** | GGUF（专用量化格式）| HuggingFace 原生（支持 AWQ/GPTQ）|

---

## 性能特征对比

### 1. 吞吐量与并发

**vLLM**：在高并发下吞吐量呈线性增长。**在 H200 上，64 并发时 vLLM 的吞吐量是 llama.cpp 的 35 倍以上**。支持迭代级调度，GPU 利用率可达 85-92%。

**llama.cpp**：吞吐量几乎不随并发增加而增长（平坦曲线），采用队列模型处理请求。

### 2. 延迟表现

| 指标 | llama.cpp | vLLM |
|------|-----------|------|
| **首 token 延迟 (TTFT)** | 随并发指数级增长（排队等待）| 高并发下稳定在 <100ms |
| **Token 间延迟 (ITL)** | 单请求 ITL 更低（无 Python GIL 开销）| 为追求吞吐量会略微增加单个请求的 ITL |

### 3. 内存效率

在 **Jetson Orin Nano (8GB)** 实测：

| 框架 | 内存占用 | 并发用户数 |
|------|----------|------------|
| **llama.cpp** | 4.2 GB | **4 并发** |
| **vLLM** | 6.4 GB（预分配 90% VRAM）| **17 并发** |

> **关键差异**：vLLM 的 PagedAttention 通过非连续内存块减少 20-27% 的 KV Cache 浪费，但会预分配大量显存；llama.cpp 使用 mmap 按需加载，静态内存占用更低。

---

## 硬件与生态支持

| 特性 | llama.cpp | vLLM |
|------|-----------|------|
| **GPU 支持** | CUDA/Metal/ROCm/Vulkan | 主要是 CUDA（部分支持 ROCm）|
| **CPU 推理** | ✅ 原生优化（AVX/AVX2/NEON）| ⚠️ 实验性支持，性能较差 |
| **边缘设备** | ✅ 树莓派、手机、Jetson 全系列 | ⚠️ 需 Jetson 专用容器，ARM 支持有限 |
| **量化支持** | 极丰富（2-8 bit，多种算法）| 支持主流量化（AWQ/GPTQ/FP8）|
| **模型加载** | 内存映射，秒级启动 | 传统加载，需预热 |
| **API 兼容性** | OpenAI-like（需配置）| 原生 OpenAI 兼容 |

---

## 适用场景

### 选择 llama.cpp 当：

- ✅ **内存受限**：边缘设备（Jetson Nano、树莓派）或消费级 GPU
- ✅ **单用户/低并发**：个人助手、离线批处理、嵌入式应用
- ✅ **跨平台需求**：需要同时在 x86、ARM、macOS 部署
- ✅ **快速启动**：GGUF 的 mmap 实现秒级模型切换
- ✅ **稳定性优先**：内存占用可预测，不易 OOM

### 选择 vLLM 当：

- ✅ **高并发服务**：多租户 API、聊天机器人服务
- ✅ **吞吐量优先**：需要最大化 GPU 利用率（数据中心场景）
- ✅ **长上下文**：PagedAttention 对长序列内存管理更高效
- ✅ **生产级特性**：需要张量并行、流水线并行、投机解码等企业功能

---

## Nano Super 部署建议

对于 **Jetson Orin Nano Super**（8GB）跑 **GLM-OCR**：

### 推荐 llama.cpp 的情况：

- 作为单用户桌面应用的 OCR 后端
- 需要同时运行其他 AI 服务（留内存给 YOLO 等）
- 追求极致稳定性（vLLM 在边缘设备上仍可能出现内存碎片问题）

### 推荐 vLLM 的情况：

- 构建多用户文档处理服务（如局域网共享 OCR API）
- 需要 OpenAI 兼容接口快速集成现有生态
- 能接受更高的内存占用换取并发能力

### 实测数据参考（Orin Nano 上 1.2B 模型）：

| 指标 | llama.cpp | vLLM |
|------|-----------|------|
| 原始生成速度 | 24-40 tok/sec | 24-40 tok/sec |
| 并发能力 | 4 并发 | 17 并发 |
| 内存占用 | 4.2 GB | 6.4 GB |
| **内存节省** | **基准** | **+34%** |

---

## 结论

GLM-OCR（0.9B）模型很小，在 Nano Super 上两者性能差距不大。

- **llama.cpp** 更适合原型开发和单用户场景
- **vLLM** 适合构建共享服务，但需仔细调优内存参数（`gpu-memory-utilization 0.4` 以下）

架构选择的核心：**没有银弹，只有适合场景的权衡**。

---

## 延伸阅读

- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
- [vLLM Documentation](https://docs.vllm.ai/)
- [PagedAttention Paper](https://arxiv.org/abs/2309.06180)
