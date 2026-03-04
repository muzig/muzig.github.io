# MEMORY.md - 长期记忆

## 用户：Muzig

---

## 🔄 定期任务

### 每日 HN 英语学习文件创建

**触发指令**:
- "今日英语" → 直接创建学习文件
- "今天的 Hacker News 话题" → 整理完整话题分类
- "新增今天的 daily 文件"
- "创建今天的英语学习"
- "从 HN 找篇文章"
- "daily 文件"

**执行流程**:
1. **自动获取 Hacker News 热门文章**（Top Stories）
2. **智能筛选适合英语学习的文章**（Tech/科普类优先）
3. **按照模板格式创建学习文件**：`templates/Daily - Minimal Tech English (15-20m).md`
4. **保存路径**：`daily/YYYY-MM-DD.md`
5. **可选：单独整理当天所有话题分类**（如果需要更全面的概览）
   - 创建话题整理文件：`hn-topics/hackernews-topics-YYYY-MM-DD.md`
   - **重要：确保每个话题都包含完整的链接和内容信息**
   - 包含话题分类、分析、学习建议

**文章选择标准**:
- 技术/科普类（便于学习 Tech English）
- 有教育价值或有趣的内容
- 难度适中（不要太过专业化）
- 优先选择有交互性、图解的文章（如 ciechanow.ski 的作品）

**Obsidian Vault 路径**:
```
/Users/muzig/Library/Mobile Documents/iCloud~md~obsidian/Documents/learning_english/
```

**文件结构**:
```
learning_english/
├── daily/
│   └── YYYY-MM-DD.md      # 每日学习文件
├── hn-topics/
│   └── hackernews-topics-YYYY-MM-DD.md  # Hacker News 话题整理文件
├── templates/
│   └── Daily - Minimal Tech English (15-20m).md  # 模板
└── ...
```

**HN 话题整理文件质量标准**：
- ✅ 每个话题必须包含完整的标题和链接
- ✅ 显示分数和评论数
- ✅ 分类清晰（AI/机器学习、编程/技术、网络安全、系统/架构、科技产品、其他）
- ✅ 包含内容简介和分析
- ✅ 避免空的话题分类和无链接的文章

**模板关键字段**:
- YAML Frontmatter: type, timebox, status, tags, date
- Input: 来源、链接、摘录、3个问题
- Transform: AI拆解（Simple English / 中文 / 3 key points）
- Output: 3句英文输出
- 打卡确认：完成率追踪

---

## 👤 用户信息

- **姓名**: Muzig
- **时区**: Asia/Shanghai
- **Telegram ID**: 5262122353
- **Obsidian Vault**: learning_english（位于 iCloud）

### 专业背景
- **职业**: Senior Backend Developer（高级后端开发工程师）
- **经验**: 6+ 年游戏后端开发（SLG 游戏）
- **专长**: Go 语言专家、分布式系统、微服务架构、DDD 领域驱动设计
- **技术栈**: Go, Python, Lua, C++, MongoDB, Redis, MySQL, Docker, Kubernetes
- **亮点**: 
  - 跨服通信注解生成器（降低跨服开发复杂度）
  - AI 工具链（Dify + MCP 构建）
  - 微服务解耦架构设计
- **联系方式**: muzig012046@gmail.com
- **博客**: https://muzig.github.io/starrypen
- **GitHub**: https://github.com/muzig/muzig

## 📝 博客项目

- **路径**: /Users/ligang/src/github/muzig.github.io
- **用途**: 发布博客文章
- **规则**: 按照项目文档规则生成博客

## 🎯 学习目标

通过 Hacker News 的技术文章学习英语，重点关注：
- Tech English 词汇
- 复杂句式分析
- 科技/工程领域表达

---

## ⚠️ 重要规则

### 数据查询权限规则

**除非用户明确要求，否则不主动拉取实时数据。**

- ✅ 用户说"查一下实时行情" → 调用 API/搜索获取最新数据
- ✅ 用户说"搜索..." → 使用 Brave 搜索获取信息
- ❌ 禁止行为：主动调用 web_search、web_fetch 获取实时数据
- ✅ 推荐行为：使用本地缓存数据（如 `~/.etf_data_cache.json`）回答查询

**适用场景**：
- ETF/股票实时行情
- 新闻动态
- 价格数据
- 任何需要网络请求的数据

### X/Twitter 链接处理

**遇到 X (Twitter) 链接时，使用 jina 读取：**
```bash
curl -s "https://r.jina.ai/<URL>"
```
例如：`curl -s "https://r.jina.ai/https://x.com/nftcps/status/2029018370197328215"`

**原因**：直接 web_fetch 或浏览器访问可能需要登录，jina 可以无需登录提取内容。

**调用优先级**：
1. **大模型能力**（第一优先）- 我的推理、分析、技术知识
2. **本地缓存**（第二优先）- 已保存的数据文件
3. **Brave 搜索**（最后手段）- 仅以下情况调用

**除非以下情况，否则不主动调用 Brave 接口：**

1. **用户明确要求搜索**："搜索..."、"查一下..."、"找一下..."
2. **大模型无法回答**：我的训练数据不包含，且需要事实性数据支撑
3. **用户提供的链接需要提取内容**："帮我看一下这个链接"
4. **实时性要求**：用户问"今天/最新/实时..."且本地无缓存

**优先使用大模型能力**：
- ✅ 技术分析与建议（代码审查、架构设计）
- ✅ 概念解释（AI Agent、微服务等）
- ✅ 推理判断（职业建议、方案对比）
- ✅ 已讨论项目的深入分析

**不调用 Brave 的场景**：
- ❌ 纯技术讨论（Go 后端优化、系统设计）
- ❌ 概念讲解（什么是 MCP、DDD 等）
- ❌ 基于已有信息的分析（你提供的 ETF 数据）
- ❌ 逻辑推理（投资决策框架、代码逻辑）

### 第三方 API 授权

**已授权服务**：
- ✅ **Raindrop.io API** (Token: 9d6903b7-1c1b-48ab-9c0b-8bbe4852ed4e)
  - 授权时间: 2026-01-30
  - 用途: 书签管理、读取收藏、自动保存、搜索书签
  - 存储位置: 加密保存于本地配置

**使用原则**：
- 仅在用户明确要求时调用第三方 API
- 不泄露 Token 到对话或日志中
- 敏感操作前需二次确认

### Skill 安装规则

**安装到全局目录**（而非 workspace）：
- ✅ 使用 `-g` / `--global` 标志
- ✅ 安装路径：`/Users/ligang/.agents` or `/Users/muzig/.agents`
- ❌ 不要装到 workspace 的 `./skills/`

**原因**：全局技能可供所有 session 使用，workspace 级别的只会影响当前工作区。

**当用户在 Cursor Agent 会话中时**：

- ✅ **仓库操作指令** → 直接让 Cursor Agent 处理（不通过工具介入）
  - Git 操作（commit、push、pull、branch 等）
  - 代码修改、重构
  - 文件操作（创建、删除、移动）
  - 项目构建、测试

- ✅ **信息查询** → 我可以通过工具辅助
  - 查看文件内容
  - 搜索代码
  - 查看日志
  - 检查系统状态

**识别方式**：
- 用户处于 tmux 会话 `tmp` 中
- 会话运行 Cursor Agent
- 用户发出仓库相关指令

**处理方式**：
- 告诉用户 "请直接在 Cursor Agent 中执行"
- 或发送命令到 tmux 会话让 Agent 接收
- 不绕过 Agent 直接操作文件系统

---

## 🎯 个人效能系统

### 📊 项目评估模型

**用于新项目评估的完整决策框架**

#### 📈 核心评估维度
1. **与目标匹配度**（1-5分）：与年度主题的匹配程度
2. **资源需求**（低/中/高）：时间、金钱、精力投入
3. **风险评估**（低/中/高）：潜在风险和障碍
4. **收益预期**（即时/长期）：短期vs长期复利
5. **专业优势**：是否利用你的专业优势（Go、系统设计、AI等）

#### 📊 决策模型
```
价值 = (重要性 × 紧迫性 × 匹配度) / (资源需求 + 风险)
```

#### 📝 评估回复格式
**项目评估结果：**
- **项目名称**：[名称]
- **领域匹配度**：[评分]
- **专业优势**：[分析]
- **资源需求**：[等级]
- **风险评估**：[等级]
- **收益预期**：[类型]
- **建议**：✅/❌ [结论]

---

**最后更新: 2026-02-12**