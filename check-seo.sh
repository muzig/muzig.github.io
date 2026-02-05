#!/bin/bash

# SEO 配置检查脚本

echo "=== Hugo 博客 SEO 配置检查 ==="
echo ""

# 检查 Hugo 配置
HUGO_CONFIG="hugo.toml"

echo "📋 基础配置检查"
echo "------------------"

# 检查 baseURL
if grep -q "baseURL\s*=" "$HUGO_CONFIG"; then
  BASEURL=$(grep "baseURL\s*=" "$HUGO_CONFIG" | awk -F'=' '{print $2}' | tr -d "'\" ")
  echo "✅ baseURL: $BASEURL"
else
  echo "❌ baseURL 未配置"
fi

# 检查 languageCode
if grep -q "languageCode\s*=" "$HUGO_CONFIG"; then
  LANG=$(grep "languageCode\s*=" "$HUGO_CONFIG" | awk -F'=' '{print $2}' | tr -d "'\" ")
  echo "✅ languageCode: $LANG"
else
  echo "❌ languageCode 未配置"
fi

# 检查 title
if grep -q "title\s*=" "$HUGO_CONFIG"; then
  TITLE=$(grep "title\s*=" "$HUGO_CONFIG" | awk -F'=' '{print $2}' | tr -d "'\" ")
  echo "✅ title: $TITLE"
else
  echo "❌ title 未配置"
fi

# 检查 description
if grep -q "description\s*=" "$HUGO_CONFIG"; then
  DESC=$(grep "description\s*=" "$HUGO_CONFIG" | awk -F'=' '{print $2}' | tr -d "'\" ")
  echo "✅ description: $DESC"
  if [ ${#DESC} -gt 150 ]; then
    echo "⚠️  description 长度为 ${#DESC} 字符，建议不超过 150 字符"
  fi
else
  echo "❌ description 未配置"
fi

# 检查 keywords
if grep -q "keywords\s*=" "$HUGO_CONFIG"; then
  echo "✅ keywords 已配置"
else
  echo "❌ keywords 未配置"
fi

echo ""
echo "📁 文件检查"
echo "------------------"

# 检查 robots.txt
if [ -f "static/robots.txt" ]; then
  echo "✅ robots.txt 存在"
  if grep -q "Sitemap:" "static/robots.txt"; then
    echo "✅ robots.txt 包含 Sitemap 链接"
  else
    echo "⚠️  robots.txt 建议添加 Sitemap 链接"
  fi
else
  echo "❌ robots.txt 不存在"
fi

# 检查 sitemap 配置
if [ -f "config/sitemap.toml" ]; then
  echo "✅ sitemap.toml 配置文件存在"
else
  echo "⚠️  sitemap.toml 配置文件不存在"
fi

# 检查 Google 验证文件
if ls static/google*.html 1> /dev/null 2>&1; then
  echo "✅ Google 验证文件存在"
else
  echo "⚠️  Google 验证文件不存在，建议添加 Google Search Console 验证"
fi

echo ""
echo "🔧 功能检查"
echo "------------------"

# 检查 Hugo 版本
HUGO_VER=$(hugo version 2>/dev/null | awk '{print $2}')
if [ -n "$HUGO_VER" ]; then
  echo "✅ Hugo 版本: $HUGO_VER"
  if echo "$HUGO_VER" | grep -q "extended"; then
    echo "✅ 使用的是 Hugo Extended 版本"
  fi
else
  echo "❌ Hugo 未安装或不在 PATH 中"
fi

# 检查是否配置了 permalinks
if grep -q "permalinks" "$HUGO_CONFIG"; then
  echo "✅ permalinks 已配置"
else
  echo "⚠️  permalinks 未配置，建议优化 URL 结构"
fi

echo ""
echo "📊 内容检查"
echo "------------------"

# 统计文章数量
POST_COUNT=$(ls content/posts/*.md 2>/dev/null | wc -l)
echo "📝 文章总数: $POST_COUNT"

# 检查文章是否有合适的标题长度
if [ $POST_COUNT -gt 0 ]; then
  echo "📏 文章标题长度检查:"
  for file in content/posts/*.md; do
    if [ -f "$file" ]; then
      TITLE=$(grep -E "^title\s*=" "$file" | head -1 | awk -F'=' '{print $2}' | tr -d "'\" ")
      if [ -n "$TITLE" ]; then
        LENGTH=${#TITLE}
        if [ $LENGTH -lt 30 ]; then
          echo "⚠️  $file: 标题太短 ($LENGTH 字符)"
        elif [ $LENGTH -gt 70 ]; then
          echo "⚠️  $file: 标题太长 ($LENGTH 字符)"
        else
          echo "✅  $file: 标题长度合适 ($LENGTH 字符)"
        fi
      fi
    fi
  done
fi

echo ""
echo "🎯 SEO 建议"
echo "------------------"
echo "1. 注册 Google Search Console 并提交 sitemap"
echo "2. 配置 Google Analytics 跟踪网站流量"
echo "3. 确保所有文章都有适当的 meta 描述"
echo "4. 使用语义化的标题标签 (H1, H2, H3)"
echo "5. 为图片添加 ALT 文本"
echo "6. 优化网站加载速度"
echo "7. 定期更新内容，保持网站活跃度"
echo "8. 建立内部链接和外部链接"

echo ""
echo "=== 检查完成 ==="