#!/bin/bash

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ -z "${1:-}" ]; then
  echo -e "${YELLOW}用法: $0 \"文章标题\"${NC}"
  echo -e "${YELLOW}示例: $0 \"Go 内存管理深度剖析\"${NC}"
  exit 1
fi

TITLE="$1"
DATE_PREFIX=$(date "+%Y-%m-%d")
DATETIME=$(date "+%Y-%m-%dT%H:%M:%S+08:00")

trim() {
  printf "%s" "$1" | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//'
}

slugify() {
  printf "%s" "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[[:space:]]+/-/g; s/[^a-z0-9-]//g; s/-+/-/g; s/^-+//; s/-+$//'
}

dedupe_csv() {
  awk -F',' '
    {
      for (i = 1; i <= NF; i++) {
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", $i)
        if ($i != "" && !seen[$i]++) items[++count] = $i
      }
    }
    END {
      for (i = 1; i <= count; i++) {
        printf "%s%s", items[i], (i < count ? "," : "")
      }
    }
  '
}

escape_toml() {
  printf "%s" "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

to_toml_array() {
  local csv="$1"
  local result=""
  IFS=',' read -r -a parts <<< "$csv"
  for raw in "${parts[@]}"; do
    local item
    item=$(trim "$raw")
    if [ -n "$item" ]; then
      if [ -n "$result" ]; then
        result="${result}, "
      fi
      result="${result}\"$(escape_toml "$item")\""
    fi
  done
  printf "[%s]" "$result"
}

choose_from_menu() {
  local prompt="$1"
  local default="$2"
  shift 2
  local options=("$@")

  echo -e "${BLUE}${prompt}${NC}"
  local i=1
  for option in "${options[@]}"; do
    echo "${i}) ${option}"
    i=$((i + 1))
  done

  local choice=""
  read -p "请选择 (默认 ${default}): " choice
  if [ -z "$choice" ]; then
    choice="$default"
  fi

  if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt "${#options[@]}" ]; then
    echo -e "${YELLOW}输入无效，使用默认值 ${default}${NC}"
    choice="$default"
  fi

  printf "%s" "${options[$((choice - 1))]}"
}

SLUG=$(slugify "$TITLE")
if [ -z "$SLUG" ]; then
  while [ -z "$SLUG" ]; do
    read -p "标题包含中文，请输入英文 slug（只允许小写字母、数字、连字符）: " MANUAL_SLUG
    MANUAL_SLUG=$(slugify "$MANUAL_SLUG")
    SLUG="$MANUAL_SLUG"
  done
fi

FILEPATH="content/posts/${DATE_PREFIX}-${SLUG}.md"

if [ -f "$FILEPATH" ]; then
  echo -e "${YELLOW}⚠️  文件已存在: ${FILEPATH}${NC}"
  read -p "是否覆盖? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}取消创建${NC}"
    exit 0
  fi
fi

CATEGORY=$(choose_from_menu "选择主题分类:" 2 \
  "AI工程" "Agent工具链" "MCP" "Go工程" "编程语言" "LLM系统" "软件架构")

echo
ARTICLE_TYPE=$(choose_from_menu "选择文章形式:" 1 \
  "深度解析" "实战教程" "入门指南" "架构拆解" "对比分析" "方法论" "观点评论" "故障排查")

echo
SERIES_CHOICE=$(choose_from_menu "选择所属系列:" 9 \
  "AI 工程观察" "Claude Code 实战" "OpenClaw 深度系列" "MCP 技术系列" \
  "Go 工程实践" "编程语言原理" "LLM 系统拆解" "架构拆解" "无")

DEFAULT_TAGS=""
case "$CATEGORY" in
  "AI工程")
    DEFAULT_TAGS="AI 工程,Agent"
    ;;
  "Agent工具链")
    DEFAULT_TAGS="Agent,AI 工具"
    ;;
  "MCP")
    DEFAULT_TAGS="MCP"
    ;;
  "Go工程")
    DEFAULT_TAGS="Go"
    ;;
  "编程语言")
    DEFAULT_TAGS="编程语言"
    ;;
  "LLM系统")
    DEFAULT_TAGS="LLM"
    ;;
  "软件架构")
    DEFAULT_TAGS="架构设计"
    ;;
esac

case "$SERIES_CHOICE" in
  "Claude Code 实战")
    DEFAULT_TAGS="${DEFAULT_TAGS},Claude Code"
    ;;
  "OpenClaw 深度系列")
    DEFAULT_TAGS="${DEFAULT_TAGS},OpenClaw"
    ;;
  "MCP 技术系列")
    DEFAULT_TAGS="${DEFAULT_TAGS},MCP"
    ;;
  "Go 工程实践")
    DEFAULT_TAGS="${DEFAULT_TAGS},Go"
    ;;
  "编程语言原理")
    DEFAULT_TAGS="${DEFAULT_TAGS},编程语言"
    ;;
  "LLM 系统拆解")
    DEFAULT_TAGS="${DEFAULT_TAGS},LLM"
    ;;
  "架构拆解")
    DEFAULT_TAGS="${DEFAULT_TAGS},架构设计"
    ;;
esac

DEFAULT_TAGS=$(printf "%s" "$DEFAULT_TAGS" | dedupe_csv)
echo
read -p "补充标签（逗号分隔，可留空）: " CUSTOM_TAGS
ALL_TAGS=$(printf "%s,%s" "$DEFAULT_TAGS" "$CUSTOM_TAGS" | dedupe_csv)
TAGS_TOML=$(to_toml_array "$ALL_TAGS")

DESCRIPTION=""
echo
read -p "一句话描述（可留空，建议补上）: " DESCRIPTION

SERIES_LINE='# series = ["系列名"]'
if [ "$SERIES_CHOICE" != "无" ]; then
  SERIES_LINE="series = [\"$(escape_toml "$SERIES_CHOICE")\"]"
fi

cat > "$FILEPATH" <<EOF
+++
date = '${DATETIME}'
draft = true
title = "$(escape_toml "$TITLE")"
description = "$(escape_toml "$DESCRIPTION")"
categories = ["$(escape_toml "$CATEGORY")"]
${SERIES_LINE}
articleType = "$(escape_toml "$ARTICLE_TYPE")"
tags = ${TAGS_TOML}
+++

## 文章背景

[在这里说明为什么写这篇文章，以及它解决什么问题]

---

## 核心内容

### 核心概念

[解释关键概念、上下文和边界]

\`\`\`go
// 代码示例
package main

func main() {
    // TODO: 添加示例代码
}
\`\`\`

---

## 实战案例

### 场景描述

[描述使用场景]

### 完整实现

\`\`\`go
package main

import "fmt"

func main() {
    fmt.Println("example")
}
\`\`\`

---

## 总结

本文核心要点：

1. **要点 1**：[简要总结]
2. **要点 2**：[简要总结]

---

## 参考资料

1. [参考文档](链接)
2. [相关博客](链接)
EOF

echo -e "${GREEN}✅ 文章创建成功！${NC}"
echo -e "${BLUE}文件路径: ${FILEPATH}${NC}"
echo -e "${BLUE}默认标签: ${ALL_TAGS}${NC}"
echo
echo -e "${YELLOW}下一步操作:${NC}"
echo "1. 按 CONTENT_SCHEMA.md 校验分类、系列和标签"
echo "2. 编辑文章内容"
echo "3. 本地预览: hugo server -D"
echo "4. 完成后设置 draft = false"
