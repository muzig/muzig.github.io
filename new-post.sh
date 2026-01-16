#!/bin/bash

# 新文章创建脚本
# 用法: ./new-post.sh "文章标题"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查参数
if [ -z "$1" ]; then
    echo -e "${YELLOW}用法: $0 \"文章标题\"${NC}"
    echo -e "${YELLOW}示例: $0 \"Go 内存管理深度剖析\"${NC}"
    exit 1
fi

TITLE="$1"

# 生成文件名（将空格替换为连字符，转为小写）
FILENAME=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g')
FILEPATH="content/posts/${FILENAME}.md"

# 检查文件是否已存在
if [ -f "$FILEPATH" ]; then
    echo -e "${YELLOW}⚠️  文件已存在: ${FILEPATH}${NC}"
    read -p "是否覆盖? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}取消创建${NC}"
        exit 0
    fi
fi

# 获取当前日期时间
DATETIME=$(date "+%Y-%m-%dT%H:%M:%S+08:00")

# 交互式选择分类
echo -e "${BLUE}选择文章分类:${NC}"
echo "1) 技术深度"
echo "2) 技术文章"
read -p "请选择 (1/2，默认 1): " CATEGORY_CHOICE

case $CATEGORY_CHOICE in
    2)
        CATEGORY="技术文章"
        ;;
    *)
        CATEGORY="技术深度"
        ;;
esac

# 交互式选择系列
echo -e "\n${BLUE}选择文章系列:${NC}"
echo "1) MCP 系列"
echo "2) Go 系列"
echo "3) 编程语言系列"
echo "4) 其他"
read -p "请选择 (1-4，默认 4): " SERIES_CHOICE

case $SERIES_CHOICE in
    1)
        TAGS="['MCP', 'Model Context Protocol']"
        ;;
    2)
        TAGS="['Go', 'Golang']"
        ;;
    3)
        TAGS="['Programming Language', 'Language Design']"
        ;;
    *)
        TAGS="['Tag1', 'Tag2']"
        ;;
esac

# 创建文章文件
cat > "$FILEPATH" << EOF
+++
date = '$DATETIME'
draft = true
title = '$TITLE'
tags = $TAGS
categories = ['$CATEGORY']
+++

## 文章背景

[在这里介绍为什么写这篇文章，要解决什么问题]

---

## 核心内容

### 概念 1

[解释核心概念]

\`\`\`go
// 代码示例
package main

func main() {
    // TODO: 添加示例代码
}
\`\`\`

### 概念 2

[深入解释]

---

## 实战案例

### 案例背景

[描述使用场景]

### 完整实现

\`\`\`go
// 完整可运行示例
package main

import "fmt"

func main() {
    fmt.Println("Example")
}
\`\`\`

---

## 最佳实践

**✅ 推荐做法**：
1. 建议 1
2. 建议 2

**❌ 避免的错误**：
1. 反模式 1
2. 反模式 2

---

## 总结

本文核心要点：

1. **要点 1**：[简要总结]
2. **要点 2**：[简要总结]

### 延伸阅读

- [相关文章](链接)

---

## 参考资料

1. [参考文档](链接)
2. [相关博客](链接)

---

> 💡 **下期预告**：[下一篇文章主题]
EOF

echo -e "${GREEN}✅ 文章创建成功！${NC}"
echo -e "${BLUE}文件路径: ${FILEPATH}${NC}"
echo ""
echo -e "${YELLOW}下一步操作:${NC}"
echo "1. 编辑文章内容"
echo "2. 本地预览: hugo server -D"
echo "3. 完成后设置 draft = false"
echo ""
echo -e "${BLUE}打开编辑器:${NC}"
echo "code ${FILEPATH}  # VS Code"
echo "vim ${FILEPATH}   # Vim"
echo ""

# 自动更新 CONTENT_TRACKER.md
CURRENT_MONTH=$(date "+%Y年%m月")
echo -e "${BLUE}💡 别忘了更新 CONTENT_TRACKER.md 追踪进度${NC}"
EOF
