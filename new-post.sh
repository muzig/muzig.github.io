#!/usr/bin/env bash
set -euo pipefail

# 新文章创建脚本：生成可直接发布、可自由改造的单文件 HTML。
# 用法: ./new-post.sh "文章标题" [url-slug]

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [[ -z "${1:-}" ]]; then
  printf "%b用法: %s \"文章标题\" [url-slug]%b\n" "$YELLOW" "$0" "$NC"
  exit 1
fi

TITLE="$1"
SLUG="${2:-$(printf '%s' "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g; s/--*/-/g; s/^-//; s/-$//')}"
if [[ -z "$SLUG" ]]; then
  SLUG="note-$(date '+%H%M%S')"
fi

YEAR=$(date '+%Y')
MONTH=$(date '+%m')
DAY=$(date '+%d')
DATE_ISO=$(date '+%Y-%m-%dT%H:%M:%S+08:00')
DATE_LABEL=$(date '+%Y.%m.%d')
TARGET_DIR="public/${YEAR}/${MONTH}/${DAY}/${SLUG}"
FILEPATH="${TARGET_DIR}/index.html"
TEMPLATE="public/posts/_template/index.html"
CANONICAL_URL="https://muzig.io/${YEAR}/${MONTH}/${DAY}/${SLUG}/"

if [[ -e "$FILEPATH" ]]; then
  printf "%b文件已存在: %s%b\n" "$YELLOW" "$FILEPATH" "$NC"
  exit 1
fi
if [[ ! -f "$TEMPLATE" ]]; then
  printf "%b找不到模板: %s%b\n" "$YELLOW" "$TEMPLATE" "$NC"
  exit 1
fi

printf "%b文章主题（默认 AI Agent）: %b" "$BLUE" "$NC"
read -r TOPIC
TOPIC="${TOPIC:-AI Agent}"
printf "%b一句话摘要: %b" "$BLUE" "$NC"
read -r DESCRIPTION
DESCRIPTION="${DESCRIPTION:-在这里填写文章摘要}"

mkdir -p "$TARGET_DIR"
cp "$TEMPLATE" "$FILEPATH"

# 一次性替换模板元信息与页面占位值。
TITLE="$TITLE" TOPIC="$TOPIC" DESCRIPTION="$DESCRIPTION" DATE_ISO="$DATE_ISO" DATE_LABEL="$DATE_LABEL" CANONICAL_URL="$CANONICAL_URL" \
perl -0pi -e '
  s/\{\{TITLE\}\}/$ENV{TITLE}/g;
  s/\{\{TOPIC\}\}/$ENV{TOPIC}/g;
  s/\{\{DESCRIPTION\}\}/$ENV{DESCRIPTION}/g;
  s/\{\{DATE\}\}/$ENV{DATE_ISO}/g;
  s/\{\{DATE_LABEL\}\}/$ENV{DATE_LABEL}/g;
  s/\{\{CANONICAL_URL\}\}/$ENV{CANONICAL_URL}/g;
  s/\{\{READING_TIME\}\}/8/g;
' "$FILEPATH"

printf "%b✓ 单文件 HTML 已创建%b\n" "$GREEN" "$NC"
printf "  %s\n\n" "$FILEPATH"
printf "%b下一步：%b\n" "$BLUE" "$NC"
printf "  1. 编辑页面内容与内联样式\n"
printf "  2. 把文章链接添加到 public/index.html\n"
printf "  3. 本地预览: python3 -m http.server 8080 -d public\n"
