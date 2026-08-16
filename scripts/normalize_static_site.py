#!/usr/bin/env python3
"""Normalize checked-in static output after the Hugo-to-HTML migration."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
TEXT_SUFFIXES = {".html", ".xml", ".txt"}


def normalize(source: str, suffix: str) -> str:
    source = source.replace("http://localhost:1313", "https://muzig.io")
    source = source.replace(r"http:\/\/localhost:1313", r"https:\/\/muzig.io")
    if suffix == ".html":
        source = source.replace('<html lang="en">', '<html lang="zh-CN">')
        source = re.sub(r'<script src="/livereload\.js[^>]*></script>\s*', "", source)
        source = re.sub(r'\s*<meta name="generator" content="Hugo [^"]+">', "", source)
        source = re.sub(r'("inLanguage"\s*:\s*)"en-US"', r'\1"zh-CN"', source)
        source = re.sub(
            r'(<script type="application/ld\+json">)(.*?)(</script>)',
            lambda match: match.group(1)
            + re.sub(r",(\s*[}\]])", r"\1", match.group(2))
            + match.group(3),
            source,
            flags=re.S,
        )
    return source


def main() -> None:
    changed = 0
    for path in sorted(PUBLIC.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        source = path.read_text(encoding="utf-8")
        updated = normalize(source, path.suffix)
        if updated != source:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Normalized {changed} static files in public/.")


if __name__ == "__main__":
    main()
