+++
date = '2026-02-28T21:30:00+08:00'
draft = false
title = "Karpathy microGPT：200行纯Python实现完整GPT"
categories = ["LLM系统"]
series = ["LLM 系统拆解"]
articleType = "深度解析"
tags = ["LLM", "GPT", "Transformer", "Python", "Karpathy"]
+++

> *"The most atomic way to train and run inference for a GPT in pure, dependency-free Python. This file is the complete algorithm. Everything else is just efficiency."* — Andrej Karpathy

最近 Andrej Karpathy 发布了一个极简 GPT 实现：**microgpt.py** —— 仅 200 行纯 Python 代码，无任何外部依赖（只用标准库 `os`, `math`, `random`），却包含了完整的训练、推理流程。

这不是玩具代码，而是一个**教学杰作**：它剥离了所有工程复杂性，让你看到 GPT 的算法本质。

<!--more-->

---

## 为什么是这 200 行？

Karpathy 在注释中写道：

> *"This file is the complete algorithm. Everything else is just efficiency."*

现代 LLM 框架（PyTorch, Transformers, etc.）封装了太多细节。当你读 nanoGPT 时，仍然需要理解：
- PyTorch 的 autograd 机制
- CUDA kernel 调用
- 分布式训练逻辑

而 microgpt.py 把一切都**显式化**了 —— 每个数学运算、每个梯度计算都清晰可见。

---

## 架构全景

```
┌─────────────────────────────────────────────────────────────┐
│                        microGPT.py                          │
├─────────────────────────────────────────────────────────────┤
│  1. Data Pipeline                                           │
│     └── 下载人名数据集 → 字符级Tokenizer → BOS标记           │
│                                                             │
│  2. Autograd Engine (Value类)                               │
│     ├── __add__, __mul__, __pow__                          │
│     ├── exp, log, relu                                     │
│     └── backward() ← 拓扑排序+链式法则                      │
│                                                             │
│  3. Model Architecture                                      │
│     ├── Embeddings (wte, wpe)                              │
│     ├── Transformer Layer × n_layer                        │
│     │   ├── RMSNorm                                        │
│     │   ├── Multi-Head Attention (Q, K, V, O)             │
│     │   └── MLP (fc1 → ReLU → fc2)                        │
│     └── LM Head                                            │
│                                                             │
│  4. Training Loop                                           │
│     ├── Forward: build computation graph                   │
│     ├── Loss: cross-entropy                                │
│     ├── Backward: grad propagation                         │
│     └── Adam optimizer with LR decay                       │
│                                                             │
│  5. Inference                                               │
│     ├── KV-cache (keys, values accumulation)               │
│     ├── Temperature sampling                               │
│     └── Token-by-token generation                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心实现拆解

### 1. 手写自动微分：Value 类

microgpt.py 不依赖 PyTorch 的 autograd，而是自己实现了一个**标量级**自动微分引擎：

```python
class Value:
    __slots__ = ('data', 'grad', '_children', '_local_grads')
    
    def __init__(self, data, children=(), local_grads=()):
        self.data = data          # 前向计算值
        self.grad = 0             # 梯度（dL/dself）
        self._children = children # 计算图子节点
        self._local_grads = local_grads  # 局部梯度
    
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data + other.data, 
                    (self, other), (1, 1))  # ∂(a+b)/∂a = 1
    
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data * other.data, 
                    (self, other), (other.data, self.data))
```

**关键点**：
- `__slots__` 优化内存使用
- 每个操作记录**子节点**和**局部梯度**
- 支持 `+`, `*`, `**`, `exp`, `log`, `relu` 等运算

### 2. 反向传播：拓扑排序

```python
def backward(self):
    # 拓扑排序构建反向图
    topo = []
    visited = set()
    def build_topo(v):
        if v not in visited:
            visited.add(v)
            for child in v._children:
                build_topo(child)
            topo.append(v)
    build_topo(self)
    
    self.grad = 1  # dL/dL = 1
    for v in reversed(topo):
        for child, local_grad in zip(v._children, v._local_grads):
            child.grad += local_grad * v.grad  # 链式法则
```

这个实现清晰展示了**反向传播的本质**：
1. 拓扑排序确定计算顺序
2. 从 loss 节点开始，梯度=1
3. 按逆序遍历，将梯度通过链式法则传递

### 3. Transformer 核心

```python
def gpt(token_id, pos_id, keys, values):
    # Embedding
    tok_emb = state_dict['wte'][token_id]
    pos_emb = state_dict['wpe'][pos_id]
    x = [t + p for t, p in zip(tok_emb, pos_emb)]
    x = rmsnorm(x)
    
    for li in range(n_layer):
        x_residual = x
        x = rmsnorm(x)
        
        # Multi-Head Attention
        q = linear(x, state_dict[f'layer{li}.attn_wq'])
        k = linear(x, state_dict[f'layer{li}.attn_wk'])
        v = linear(x, state_dict[f'layer{li}.attn_wv'])
        
        keys[li].append(k)      # KV-cache
        values[li].append(v)
        
        # 多头并行
        x_attn = []
        for h in range(n_head):
            q_h = q[h * head_dim:(h+1) * head_dim]
            k_h = [ki[h * head_dim:(h+1) * head_dim] for ki in keys[li]]
            v_h = [vi[h * head_dim:(h+1) * head_dim] for vi in values[li]]
            
            # Attention: Q @ K^T / sqrt(d)
            attn_logits = [sum(q_h[j] * k_h[t][j] for j in range(head_dim)) 
                          / head_dim**0.5 for t in range(len(k_h))]
            attn_weights = softmax(attn_logits)
            
            # Weighted sum
            head_out = [sum(attn_weights[t] * v_h[t][j] 
                           for t in range(len(v_h))) for j in range(head_dim)]
            x_attn.extend(head_out)
        
        x = linear(x_attn, state_dict[f'layer{li}.attn_wo'])
        x = [a + b for a, b in zip(x, x_residual)]
        
        # MLP
        x_residual = x
        x = rmsnorm(x)
        x = linear(x, state_dict[f'layer{li}.mlp_fc1'])
        x = [xi.relu() for xi in x]
        x = linear(x, state_dict[f'layer{li}.mlp_fc2'])
        x = [a + b for a, b in zip(x, x_residual)]
    
    return linear(x, state_dict['lm_head'])
```

**值得注意的细节**：
- 使用 **RMSNorm**（LLaMA 风格）替代 LayerNorm
- 显式的 **KV-cache** 机制
- **单token前向**：每次处理一个 token，而非整个序列

### 4. RMSNorm：极简归一化

```python
def rmsnorm(x):
    ms = sum(xi * xi for xi in x) / len(x)  # 均方
    scale = (ms + 1e-5) ** -0.5             # 1/√(ms+ε)
    return [xi * scale for xi in x]
```

比 LayerNorm 更简洁，省去了减均值步骤，效果相近。

---

## 社区探索：效率阶梯

评论区有人做了不同实现的性能对比：

| 实现 | 相对速度 | 关键优化 |
|------|----------|----------|
| **原版 (Python scalar)** | 1× | 手写标量autograd |
| **NumPy 版** | ~250× | 矩阵运算 + BLAS |
| **PyTorch CPU** | ~200× | 框架优化 |
| **PyTorch GPU (小模型)** | 更慢 | Kernel启动开销 > 计算收益 |

> 原文：*"microGPT is compute-light and memory-light. For small models, CPU vectorization (BLAS) is often enough. GPU and distributed scaling only become clearly advantageous once arithmetic intensity increases via larger models or larger batch sizes."*

**核心洞察**：小模型瓶颈在「计算图开销」，而非语言/硬件。NumPy 版本通过**消除标量autograd**和**解释器开销**，获得了 250 倍加速。

---

## 为什么值得精读？

1. **教育价值**：没有任何黑盒，每个数学运算都显式可见
2. **工程智慧**：用最小代码展示 GPT 的完整 pipeline
3. **性能启示**：识别真正的瓶颈，避免过早优化

如果你刚接触 Transformer，读完这 200 行，你会对以下概念有**直观理解**：
- 什么是计算图？反向传播如何工作？
- KV-cache 为什么重要？
- 多头注意力如何并行计算？
- Adam 优化器的偏差修正是什么？

---

## 完整代码

```python
"""
The most atomic way to train and run inference for a GPT in pure, dependency-free Python.
This file is the complete algorithm.
Everything else is just efficiency.

@karpathy
"""

import os # os.path.exists
import math # math.log, math.exp
import random # random.seed, random.choices, random.gauss, random.shuffle
random.seed(42) # Let there be order among chaos

# Let there be a Dataset `docs`: list[str] of documents (e.g. a list of names)
if not os.path.exists('input.txt'):
    import urllib.request
    names_url = 'https://raw.githubusercontent.com/karpathy/makemore/988aa59/names.txt'
    urllib.request.urlretrieve(names_url, 'input.txt')
docs = [line.strip() for line in open('input.txt') if line.strip()]
random.shuffle(docs)
print(f"num docs: {len(docs)}")

# Let there be a Tokenizer to translate strings to sequences of integers ("tokens") and back
uchars = sorted(set(''.join(docs))) # unique characters in the dataset become token ids 0..n-1
BOS = len(uchars) # token id for a special Beginning of Sequence (BOS) token
vocab_size = len(uchars) + 1 # total number of unique tokens, +1 is for BOS
print(f"vocab size: {vocab_size}")

# Let there be Autograd to recursively apply the chain rule through a computation graph
class Value:
    __slots__ = ('data', 'grad', '_children', '_local_grads') # Python optimization for memory usage

    def __init__(self, data, children=(), local_grads=()):
        self.data = data # scalar value of this node calculated during forward pass
        self.grad = 0 # derivative of the loss w.r.t. this node, calculated in backward pass
        self._children = children # children of this node in the computation graph
        self._local_grads = local_grads # local derivative of this node w.r.t. its children

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data + other.data, (self, other), (1, 1))

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data * other.data, (self, other), (other.data, self.data))

    def __pow__(self, other): return Value(self.data**other, (self,), (other * self.data**(other-1),))
    def log(self): return Value(math.log(self.data), (self,), (1/self.data,))
    def exp(self): return Value(math.exp(self.data), (self,), (math.exp(self.data),))
    def relu(self): return Value(max(0, self.data), (self,), (float(self.data > 0),))
    def __neg__(self): return self * -1
    def __radd__(self, other): return self + other
    def __sub__(self, other): return self + (-other)
    def __rsub__(self, other): return other + (-self)
    def __rmul__(self, other): return self * other
    def __truediv__(self, other): return self * other**-1
    def __rtruediv__(self, other): return other * self**-1

    def backward(self):
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._children:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        self.grad = 1
        for v in reversed(topo):
            for child, local_grad in zip(v._children, v._local_grads):
                child.grad += local_grad * v.grad

# Initialize the parameters, to store the knowledge of the model
n_layer = 1 # depth of the transformer neural network (number of layers)
n_embd = 16 # width of the network (embedding dimension)
block_size = 16 # maximum context length of the attention window (note: the longest name is 15 characters)
n_head = 4 # number of attention heads
head_dim = n_embd // n_head # derived dimension of each head
matrix = lambda nout, nin, std=0.08: [[Value(random.gauss(0, std)) for _ in range(nin)] for _ in range(nout)]
state_dict = {'wte': matrix(vocab_size, n_embd), 'wpe': matrix(block_size, n_embd), 'lm_head': matrix(vocab_size, n_embd)}
for i in range(n_layer):
    state_dict[f'layer{i}.attn_wq'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.attn_wk'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.attn_wv'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.attn_wo'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.mlp_fc1'] = matrix(4 * n_embd, n_embd)
    state_dict[f'layer{i}.mlp_fc2'] = matrix(n_embd, 4 * n_embd)
params = [p for mat in state_dict.values() for row in mat for p in row] # flatten params into a single list[Value]
print(f"num params: {len(params)}")

# Define the model architecture: a function mapping tokens and parameters to logits over what comes next
# Follow GPT-2, blessed among the GPTs, with minor differences: layernorm -> rmsnorm, no biases, GeLU -> ReLU
def linear(x, w):
    return [sum(wi * xi for wi, xi in zip(wo, x)) for wo in w]

def softmax(logits):
    max_val = max(val.data for val in logits)
    exps = [(val - max_val).exp() for val in logits]
    total = sum(exps)
    return [e / total for e in exps]

def rmsnorm(x):
    ms = sum(xi * xi for xi in x) / len(x)
    scale = (ms + 1e-5) ** -0.5
    return [xi * scale for xi in x]

def gpt(token_id, pos_id, keys, values):
    tok_emb = state_dict['wte'][token_id] # token embedding
    pos_emb = state_dict['wpe'][pos_id] # position embedding
    x = [t + p for t, p in zip(tok_emb, pos_emb)] # joint token and position embedding
    x = rmsnorm(x) # note: not redundant due to backward pass via the residual connection

    for li in range(n_layer):
        # 1) Multi-head Attention block
        x_residual = x
        x = rmsnorm(x)
        q = linear(x, state_dict[f'layer{li}.attn_wq'])
        k = linear(x, state_dict[f'layer{li}.attn_wk'])
        v = linear(x, state_dict[f'layer{li}.attn_wv'])
        keys[li].append(k)
        values[li].append(v)
        x_attn = []
        for h in range(n_head):
            hs = h * head_dim
            q_h = q[hs:hs+head_dim]
            k_h = [ki[hs:hs+head_dim] for ki in keys[li]]
            v_h = [vi[hs:hs+head_dim] for vi in values[li]]
            attn_logits = [sum(q_h[j] * k_h[t][j] for j in range(head_dim)) / head_dim**0.5 for t in range(len(k_h))]
            attn_weights = softmax(attn_logits)
            head_out = [sum(attn_weights[t] * v_h[t][j] for t in range(len(v_h))) for j in range(head_dim)]
            x_attn.extend(head_out)
        x = linear(x_attn, state_dict[f'layer{li}.attn_wo'])
        x = [a + b for a, b in zip(x, x_residual)]
        # 2) MLP block
        x_residual = x
        x = rmsnorm(x)
        x = linear(x, state_dict[f'layer{li}.mlp_fc1'])
        x = [xi.relu() for xi in x]
        x = linear(x, state_dict[f'layer{li}.mlp_fc2'])
        x = [a + b for a, b in zip(x, x_residual)]

    logits = linear(x, state_dict['lm_head'])
    return logits

# Let there be Adam, the blessed optimizer and its buffers
learning_rate, beta1, beta2, eps_adam = 0.01, 0.85, 0.99, 1e-8
m = [0.0] * len(params) # first moment buffer
v = [0.0] * len(params) # second moment buffer

# Repeat in sequence
num_steps = 1000 # number of training steps
for step in range(num_steps):

    # Take single document, tokenize it, surround it with BOS special token on both sides
    doc = docs[step % len(docs)]
    tokens = [BOS] + [uchars.index(ch) for ch in doc] + [BOS]
    n = min(block_size, len(tokens) - 1)

    # Forward the token sequence through the model, building up the computation graph all the way to the loss
    keys, values = [[] for _ in range(n_layer)], [[] for _ in range(n_layer)]
    losses = []
    for pos_id in range(n):
        token_id, target_id = tokens[pos_id], tokens[pos_id + 1]
        logits = gpt(token_id, pos_id, keys, values)
        probs = softmax(logits)
        loss_t = -probs[target_id].log()
        losses.append(loss_t)
    loss = (1 / n) * sum(losses) # final average loss over the document sequence. May yours be low.

    # Backward the loss, calculating the gradients with respect to all model parameters
    loss.backward()

    # Adam optimizer update: update the model parameters based on the corresponding gradients
    lr_t = learning_rate * (1 - step / num_steps) # linear learning rate decay
    for i, p in enumerate(params):
        m[i] = beta1 * m[i] + (1 - beta1) * p.grad
        v[i] = beta2 * v[i] + (1 - beta2) * p.grad ** 2
        m_hat = m[i] / (1 - beta1 ** (step + 1))
        v_hat = v[i] / (1 - beta2 ** (step + 1))
        p.data -= lr_t * m_hat / (v_hat ** 0.5 + eps_adam)
        p.grad = 0

    print(f"step {step+1:4d} / {num_steps:4d} | loss {loss.data:.4f}", end='\r')

# Inference: may the model babble back to us
temperature = 0.5 # in (0, 1], control the "creativity" of generated text, low to high
print("\n--- inference (new, hallucinated names) ---")
for sample_idx in range(20):
    keys, values = [[] for _ in range(n_layer)], [[] for _ in range(n_layer)]
    token_id = BOS
    sample = []
    for pos_id in range(block_size):
        logits = gpt(token_id, pos_id, keys, values)
        probs = softmax([l / temperature for l in logits])
        token_id = random.choices(range(vocab_size), weights=[p.data for p in probs])[0]
        if token_id == BOS:
            break
        sample.append(uchars[token_id])
    print(f"sample {sample_idx+1:2d}: {''.join(sample)}")
```

---

## 总结

microgpt.py 是理解 GPT 的**最佳入门材料**：

1. **零依赖**：只用 Python 标准库，任何人都能运行
2. **完整性**：包含训练、推理、优化器，是真正的 end-to-end
3. **教育性**：每个概念都有对应代码，没有黑盒

如果你想深入理解 Transformer，不要从 PyTorch 文档开始 —— **从这 200 行开始**。

---

## 参考资料

- [microGPT Gist](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95)
- [microGPT-efficiency 基准测试](https://github.com/chanjoongx/microgpt-efficiency)
- [Karpathy's makemore](https://github.com/karpathy/makemore)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

---

> 💡 **下期预告**：用 NumPy 加速 microGPT —— 250 倍性能提升背后的原理

> 📬 **订阅更新**：关注公众号获取最新技术文章
