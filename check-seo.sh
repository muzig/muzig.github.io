#!/usr/bin/env bash
set -u

# 检查直接部署到 GitHub Pages 的单文件 HTML 站点。
# 用法：./check-seo.sh
# 自定义正式主域：SITE_ORIGIN="https://example.com" ./check-seo.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

SITE_ORIGIN="${SITE_ORIGIN:-https://muzig.io}"
SITE_ORIGIN="${SITE_ORIGIN%/}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[FAIL] 需要 python3 才能解析和检查 HTML"
  exit 1
fi

python3 - "$SITE_ORIGIN" <<'PY'
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path.cwd()
PUBLIC = ROOT / "public"
ORIGIN = sys.argv[1].rstrip("/")
ORIGIN_PARTS = urlsplit(ORIGIN)

passes = 0
warnings = 0
failures = 0


def passed(message: str) -> None:
    global passes
    passes += 1
    print(f"[PASS] {message}")


def warned(message: str) -> None:
    global warnings
    warnings += 1
    print(f"[WARN] {message}")


def failed(message: str) -> None:
    global failures
    failures += 1
    print(f"[FAIL] {message}")


class PageAnalyzer(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title_parts: list[str] = []
        self.in_title = False
        self.meta_name: dict[str, str] = {}
        self.meta_property: dict[str, str] = {}
        self.canonicals: list[str] = []
        self.hrefs: list[str] = []
        self.stylesheets: list[str] = []
        self.h1_count = 0
        self.main_count = 0
        self.article_count = 0
        self.style_count = 0
        self.images_without_alt = 0
        self.json_ld_parts: list[str] = []
        self.in_json_ld = False

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        values = {key.lower(): (value or "") for key, value in attrs}

        if tag == "html":
            self.lang = values.get("lang", "")
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            content = values.get("content", "").strip()
            name = values.get("name", "").lower()
            prop = values.get("property", "").lower()
            if name:
                self.meta_name[name] = content
            if prop:
                self.meta_property[prop] = content
        elif tag == "link":
            rel = {item.lower() for item in values.get("rel", "").split()}
            href = values.get("href", "").strip()
            if "canonical" in rel and href:
                self.canonicals.append(href)
            if "stylesheet" in rel and href:
                self.stylesheets.append(href)
        elif tag == "a":
            href = values.get("href", "").strip()
            if href:
                self.hrefs.append(href)
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "main":
            self.main_count += 1
        elif tag == "article":
            self.article_count += 1
        elif tag == "style":
            self.style_count += 1
        elif tag == "img" and "alt" not in values:
            self.images_without_alt += 1
        elif tag == "script" and values.get("type", "").lower() == "application/ld+json":
            self.in_json_ld = True

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag == "script":
            self.in_json_ld = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_json_ld:
            self.json_ld_parts.append(data)

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())


def analyze(path: Path) -> tuple[str, PageAnalyzer] | None:
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        failed(f"{path.relative_to(ROOT)} 无法按 UTF-8 读取：{exc}")
        return None

    parser = PageAnalyzer()
    try:
        parser.feed(source)
    except Exception as exc:
        failed(f"{path.relative_to(ROOT)} HTML 无法解析：{exc}")
        return None
    return source, parser


def display(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalized_url(url: str) -> tuple[str, str, str]:
    parts = urlsplit(url)
    path = unquote(parts.path or "/")
    if not path.endswith("/") and not Path(path).suffix:
        path += "/"
    return parts.scheme.lower(), parts.netloc.lower(), path


def href_path(href: str) -> str | None:
    if href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    parts = urlsplit(href)
    if parts.netloc and parts.netloc.lower() != ORIGIN_PARTS.netloc.lower():
        return None
    path = unquote(parts.path or "/")
    if not path.endswith("/") and not Path(path).suffix:
        path += "/"
    return path


def check_banned(source: str, label: str) -> None:
    banned = (
        (r"localhost(?::\d+)?", "localhost URL"),
        (r"livereload", "Hugo livereload"),
        (r"<meta[^>]+name=[\"']generator[\"'][^>]+Hugo", "Hugo generator"),
        (r"fonts\.(?:googleapis|gstatic)\.com", "Google Fonts 外链"),
        (r"(?:href|src|content)\s*=\s*[\"'][^\"']*(?:file://|/Users/)", "HTML 属性中的本地绝对路径"),
    )
    for pattern, description in banned:
        if re.search(pattern, source, flags=re.IGNORECASE):
            failed(f"{label} 含禁止提交的 {description}")


def check_json_ld(parser: PageAnalyzer, label: str) -> None:
    if not parser.json_ld_parts:
        warned(f"{label} 未提供 JSON-LD BlogPosting")
        return
    raw = "".join(parser.json_ld_parts).strip()
    try:
        json.loads(raw)
    except json.JSONDecodeError as exc:
        failed(f"{label} JSON-LD 不是合法 JSON：{exc.msg}")


def expected_article_url(article: Path) -> str:
    relative_dir = article.parent.relative_to(PUBLIC).as_posix()
    return f"{ORIGIN}/{relative_dir}/"


def check_page_core(path: Path, source: str, parser: PageAnalyzer, article: bool) -> bool:
    label = display(path)
    before = failures

    if not re.search(r"<!doctype\s+html", source, flags=re.IGNORECASE):
        failed(f"{label} 缺少 HTML5 doctype")
    if not parser.lang:
        failed(f"{label} 缺少 html lang")
    elif article and parser.lang.lower() not in {"zh-cn", "zh-hans", "zh"}:
        warned(f"{label} lang={parser.lang!r}，中文文章建议使用 zh-CN")
    if not re.search(r"<meta\s+[^>]*charset=[\"']?utf-8", source, flags=re.IGNORECASE):
        failed(f"{label} 缺少 UTF-8 charset")
    if "viewport" not in parser.meta_name:
        failed(f"{label} 缺少 viewport")
    if not parser.title:
        failed(f"{label} 缺少 title")
    description = parser.meta_name.get("description", "").strip()
    if not description:
        failed(f"{label} 缺少 meta description")
    elif len(description) < 24:
        warned(f"{label} description 较短（{len(description)} 字符）")
    elif len(description) > 180:
        warned(f"{label} description 过长（{len(description)} 字符）")
    if parser.h1_count != 1:
        failed(f"{label} 应有且仅有一个 h1，当前为 {parser.h1_count}")
    if article and parser.article_count == 0:
        failed(f"{label} 缺少 article 语义元素")
    if article and parser.main_count == 0:
        warned(f"{label} 缺少 main 语义元素")
    if parser.style_count == 0:
        warned(f"{label} 没有内联 style，确认页面专属样式未依赖旧主题")
    if parser.images_without_alt:
        warned(f"{label} 有 {parser.images_without_alt} 张图片缺少 alt 属性")
    if re.search(r"\{\{[^{}]+\}\}", source):
        failed(f"{label} 含未替换的模板占位符")

    check_banned(source, label)
    return failures == before


print("=== 单文件 HTML 博客检查 ===")
print(f"正式主域：{ORIGIN}")
print()

if ORIGIN_PARTS.scheme != "https" or not ORIGIN_PARTS.netloc:
    failed("SITE_ORIGIN 必须是包含主机名的 HTTPS URL")

if not PUBLIC.is_dir():
    failed("public/ 不存在，无法继续检查")
    print(f"\n结果：{passes} PASS / {warnings} WARN / {failures} FAIL")
    sys.exit(1)
passed("public/ 发布目录存在")

required_files = (
    PUBLIC / "index.html",
    PUBLIC / "posts" / "_template" / "index.html",
    PUBLIC / "robots.txt",
    PUBLIC / "sitemap.xml",
)
for required in required_files:
    if required.is_file():
        passed(f"{display(required)} 存在")
    else:
        failed(f"{display(required)} 不存在")

template_path = PUBLIC / "posts" / "_template" / "index.html"
if template_path.is_file():
    result = analyze(template_path)
    if result:
        template_source, template = result
        check_banned(template_source, display(template_path))
        if template.style_count == 0:
            failed("文章模板缺少内联 style")
        if "{{TITLE}}" not in template_source or "{{DESCRIPTION}}" not in template_source:
            failed("文章模板缺少 TITLE 或 DESCRIPTION 占位符")
        if not template.canonicals:
            warned("文章模板未提供 canonical 占位值；生成文章后必须手工补齐")
        if "og:url" not in template.meta_property:
            warned("文章模板未提供 og:url 占位值；生成文章后必须手工补齐")

article_pattern = re.compile(r"^\d{4}/\d{2}/\d{2}/.+/index\.html$")
articles = sorted(
    path for path in PUBLIC.rglob("index.html")
    if article_pattern.fullmatch(path.relative_to(PUBLIC).as_posix())
)

if not articles:
    failed("未找到 public/YYYY/MM/DD/slug/index.html 文章")
else:
    passed(f"发现 {len(articles)} 篇日期目录文章")

article_paths: set[str] = set()
article_core_passes = 0
published_articles = 0
for article_path in articles:
    result = analyze(article_path)
    if not result:
        continue
    source, page = result
    if check_page_core(article_path, source, page, article=True):
        article_core_passes += 1

    expected = expected_article_url(article_path)
    expected_normalized = normalized_url(expected)
    article_url_path = expected_normalized[2]
    is_noindex = "noindex" in page.meta_name.get("robots", "").lower()
    if not is_noindex:
        article_paths.add(article_url_path)
        published_articles += 1
    label = display(article_path)

    if len(page.canonicals) != 1:
        failed(f"{label} 应有且仅有一个 canonical，当前为 {len(page.canonicals)}")
    elif normalized_url(page.canonicals[0]) != expected_normalized:
        failed(f"{label} canonical 应为 {expected}")

    og_url = page.meta_property.get("og:url", "")
    if not og_url:
        failed(f"{label} 缺少 og:url")
    elif normalized_url(og_url) != expected_normalized:
        failed(f"{label} og:url 应为 {expected}")

    for key in ("og:type", "og:title", "og:description"):
        if not page.meta_property.get(key, "").strip():
            warned(f"{label} 缺少 {key}")
    if not page.meta_property.get("article:published_time", "").strip():
        warned(f"{label} 缺少 article:published_time")
    if not any(href_path(href) == "/" for href in page.hrefs):
        failed(f"{label} 缺少返回首页的链接")
    check_json_ld(page, label)

passed(f"{article_core_passes}/{len(articles)} 篇文章通过基础 HTML 结构检查")
passed(f"{published_articles} 篇正式文章，{len(articles) - published_articles} 篇 noindex 草稿")

home_path = PUBLIC / "index.html"
if home_path.is_file():
    result = analyze(home_path)
    if result:
        home_source, home = result
        check_page_core(home_path, home_source, home, article=False)
        home_paths = {path for href in home.hrefs if (path := href_path(href))}
        missing_from_home = sorted(article_paths - home_paths)
        if missing_from_home:
            preview = ", ".join(missing_from_home[:5])
            suffix = " …" if len(missing_from_home) > 5 else ""
            warned(f"首页未直接链接 {len(missing_from_home)} 篇日期文章：{preview}{suffix}")
        else:
            passed("首页包含全部日期文章入口")
        expected_home = normalized_url(f"{ORIGIN}/")
        if len(home.canonicals) != 1 or normalized_url(home.canonicals[0]) != expected_home:
            failed(f"public/index.html canonical 应为 {ORIGIN}/")
        home_og_url = home.meta_property.get("og:url", "")
        if not home_og_url or normalized_url(home_og_url) != expected_home:
            failed(f"public/index.html og:url 应为 {ORIGIN}/")

robots_path = PUBLIC / "robots.txt"
if robots_path.is_file():
    robots = robots_path.read_text(encoding="utf-8", errors="replace")
    expected_sitemap = f"Sitemap: {ORIGIN}/sitemap.xml"
    if expected_sitemap not in robots:
        failed(f"public/robots.txt 应包含：{expected_sitemap}")
    else:
        passed("robots.txt 指向正式 sitemap")
    check_banned(robots, display(robots_path))

sitemap_path = PUBLIC / "sitemap.xml"
if sitemap_path.is_file():
    sitemap_source = sitemap_path.read_text(encoding="utf-8", errors="replace")
    check_banned(sitemap_source, display(sitemap_path))
    try:
        sitemap_root = ET.fromstring(sitemap_source)
        sitemap_urls = [
            (node.text or "").strip()
            for node in sitemap_root.findall(".//{*}loc")
            if (node.text or "").strip()
        ]
    except ET.ParseError as exc:
        failed(f"public/sitemap.xml 不是合法 XML：{exc}")
        sitemap_urls = []

    sitemap_paths: set[str] = set()
    wrong_origins: list[str] = []
    for url in sitemap_urls:
        scheme, host, path = normalized_url(url)
        if scheme != ORIGIN_PARTS.scheme or host != ORIGIN_PARTS.netloc.lower():
            wrong_origins.append(url)
        else:
            sitemap_paths.add(path)
    if wrong_origins:
        failed(f"sitemap 有 {len(wrong_origins)} 个 URL 未使用正式主域 {ORIGIN}")
    missing_from_sitemap = sorted(article_paths - sitemap_paths)
    if missing_from_sitemap:
        warned(f"sitemap 缺少 {len(missing_from_sitemap)} 篇日期文章")
    elif articles:
        passed("sitemap 包含全部日期文章")

rss_path = PUBLIC / "index.xml"
if rss_path.is_file():
    rss_source = rss_path.read_text(encoding="utf-8", errors="replace")
    check_banned(rss_source, display(rss_path))
else:
    warned("public/index.xml 不存在；如果不再提供 RSS，请同时移除首页 RSS 入口")

verification_files = list(PUBLIC.glob("google*.html"))
if verification_files:
    passed("Google Search Console 验证文件位于 public/ 根目录")
else:
    warned("public/ 根目录没有 Google Search Console HTML 验证文件")

print()
print(f"结果：{passes} PASS / {warnings} WARN / {failures} FAIL")
if failures:
    print("发布前请修复全部 FAIL；WARN 需要人工确认。")
    sys.exit(1)
print("自动检查通过；仍需在浏览器检查内容、视觉、链接和移动端体验。")
PY
