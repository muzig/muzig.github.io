#!/usr/bin/env python3
"""Apply a distinct, self-contained visual system to every legacy article HTML."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BEGIN = "<!-- ARTICLE-DESIGN:BEGIN -->"
END = "<!-- ARTICLE-DESIGN:END -->"


@dataclass(frozen=True)
class Theme:
    match: str
    name: str
    family: str
    label: str
    bg: str
    ink: str
    accent: str
    soft: str
    display: str = '"Songti SC","STSong",Georgia,serif'
    body: str = '"Songti SC","STSong",Georgia,serif'


THEMES = [
    Theme("MCP（Model Context Protocol）", "protocol-slate", "editorial", "PROTOCOL / 001", "#ede9df", "#17211d", "#d64a32", "#cfd7cd"),
    Theme("深度解析：官方 Go", "go-blueprint", "blueprint", "GO TOOLCHAIN / MAP", "#153b55", "#edf6e9", "#f3b33d", "#27566f", 'Arvo,"Songti SC",serif'),
    Theme("编程语言设计组成解析", "language-construct", "construct", "LANGUAGE / KIT OF PARTS", "#f2d83f", "#181713", "#d63d2e", "#eee8d8", 'Arvo,"Heiti SC",sans-serif'),
    Theme("编程语言运行流程剖析", "runtime-signal", "signal", "SOURCE → MACHINE", "#171b18", "#f4e7c6", "#ef7b32", "#28312b", 'Arvo,"Songti SC",serif'),
    Theme("编程语言核心要素", "core-brutalist", "brutalist", "CORE / EVALUATION", "#f1eee4", "#11120f", "#4169a1", "#e0d85c", '"Heiti SC","PingFang SC",sans-serif'),
    Theme("Go 版本升级检查指南", "upgrade-ledger", "ledger", "RELEASE LEDGER", "#e9eddc", "#203126", "#b5422f", "#d6ddc6", 'Arvo,"Songti SC",serif'),
    Theme("Go 语言设计组成深度解析", "go-poster", "poster", "GO / ANATOMY", "#bfe7e2", "#17333a", "#e84a32", "#f2d76b", 'Arvo,"Heiti SC",sans-serif'),
    Theme("文章标题：简洁明确", "draft-blank", "draft", "DRAFT / NOT PUBLISHED", "#f4f1ea", "#54534d", "#b6aa98", "#e7e0d4"),
    Theme("Multi-Agent 系统", "agent-constellation", "constellation", "MULTI / AGENT", "#172338", "#f2e7ca", "#e3b553", "#243552", 'Arvo,"Songti SC",serif'),
    Theme("Clawdbot：", "clawdbot-dialogue", "messenger", "HUMAN ↔ MACHINE", "#f1e8de", "#302821", "#cf553a", "#c9ded7", '"Kaiti SC","STKaiti",serif'),
    Theme("MCP vs LangChain", "integration-split", "split", "THREE WAYS / ONE CHOICE", "#eee9df", "#161916", "#d24a36", "#cad8e6", 'Arvo,"Songti SC",serif'),
    Theme("OpenClaw：AI Agent", "openclaw-os", "terminal", "OPENCLAW / SYSTEM", "#151813", "#e9edcf", "#b8d34b", "#252b20", 'Arvo,ui-monospace,monospace'),
    Theme("Claude Code 团队使用技巧", "claude-cards", "cards", "10 NOTES FROM THE TEAM", "#efe7da", "#2e2822", "#c65a3c", "#d7c8ac", '"Kaiti SC","STKaiti",serif'),
    Theme("OpenClaw 工作区设计", "memory-archive", "archive", "MEMORY / ARCHIVE", "#e8dfcc", "#332b21", "#8f382b", "#cfc0a2", 'Arvo,"Songti SC",serif'),
    Theme("llama.cpp vs vLLM", "inference-duel", "duel", "EDGE ←→ CLOUD", "#ece9e1", "#171918", "#b83a32", "#9dbbc4", 'Arvo,"Heiti SC",sans-serif'),
    Theme("OpenClaw 架构揭秘", "claw-topology", "topology", "1 BRAIN / N HANDS", "#e5eadf", "#1d2c27", "#d75532", "#b8c9b7", 'Arvo,"Songti SC",serif'),
    Theme("OpenClaw Node 执行权限", "permission-docket", "security", "EXEC / APPROVAL", "#f0e9cf", "#171811", "#d6a700", "#27291f", 'Arvo,"Heiti SC",sans-serif'),
    Theme("QMD：", "semantic-library", "library", "LOCAL / SEMANTIC INDEX", "#eee8d8", "#24342d", "#a5402d", "#ccd5c2"),
    Theme("OpenClaw 多 Agent", "agent-orgchart", "orgchart", "TEAM / ORCHESTRATION", "#e9e5dc", "#242825", "#476b59", "#d4c26b", 'Arvo,"Songti SC",serif'),
    Theme("Unity 程序集系统", "unity-cad", "cad", "ASSEMBLY / DRAWING", "#173751", "#e8f1e7", "#e4a64a", "#2a526d", 'Arvo,"Heiti SC",sans-serif'),
    Theme("OpenClaw 修复 Python", "venv-incident", "incident", "INCIDENT / EBADF", "#f1eee8", "#232321", "#c7362f", "#e5d8cc", 'Arvo,"Songti SC",serif'),
    Theme("Agent-Orchestrated Development", "orchestration-score", "score", "HUMAN / CONDUCTOR", "#f1ecde", "#24241f", "#395f79", "#d9cda9"),
    Theme("编程，在过去两个月", "programming-zine", "zine", "THE BREAK / 60 DAYS", "#eee9dd", "#171714", "#e1432f", "#d8cfbd", '"Heiti SC","PingFang SC",sans-serif'),
    Theme("Augmented LLM 架构", "augmented-circuit", "circuit", "LLM + CONTEXT", "#18211b", "#e8edda", "#d7b94c", "#29362c", 'Arvo,"Songti SC",serif'),
    Theme("AI 编程进入第三阶段", "ai-factory", "industrial", "STAGE 03 / FACTORY", "#dedbd1", "#20211e", "#d39f24", "#343832", '"Heiti SC","PingFang SC",sans-serif'),
    Theme("当 Andrej Karpathy", "research-lab", "lab", "PROGRAMMING / A LAB", "#edf0ea", "#22302e", "#3d6c78", "#d8dfd6", 'Arvo,"Songti SC",serif'),
    Theme("Karpathy microGPT", "microgpt-notebook", "notebook", "200 LINES / ZERO MAGIC", "#f1eddc", "#27302a", "#b44837", "#cfd8cf", '"Kaiti SC","STKaiti",serif'),
    Theme("OpenClaw ACP Agents", "acp-patchbay", "patchbay", "ACP / PATCH BAY", "#f0dfc5", "#1e2b32", "#d45832", "#9db4ae", 'Arvo,"Heiti SC",sans-serif'),
    Theme("AI 不一定让打工人变惨", "economics-paper", "newspaper", "ECONOMY / LABOR", "#ece8dc", "#25241f", "#9b2f28", "#d5cbb7"),
    Theme("从 Vibe Coding", "evolution-timeline", "timeline", "DAY 01 → DAY 40", "#e7e9df", "#1d2825", "#ce5335", "#c8d1c4", 'Arvo,"Songti SC",serif'),
    Theme("OpenClaw 小白入门指南", "openclaw-fieldguide", "fieldguide", "FIELD GUIDE / 01", "#edf0dd", "#263529", "#cb5737", "#cbd7b8", '"Kaiti SC","STKaiti",serif'),
    Theme("6个反直觉的Agent工程原则", "agent-manifesto", "manifesto", "SIX / PRINCIPLES", "#ee583b", "#171713", "#f4eecf", "#d94831", '"Heiti SC","PingFang SC",sans-serif'),
]


BASE_CSS = r"""
@font-face{font-family:Arvo;src:url('/fonts/Arvo.woff2') format('woff2');font-display:swap}
:root,[data-theme=dark]{--page-bg:BG;--page-ink:INK;--page-accent:ACCENT;--page-soft:SOFT;--bg-color:BG;--text-color:INK;--link-color:INK;--secondary-text:INK;--code-bg:SOFT;--blockquote-color:INK;--blockquote-border:ACCENT}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0!important;background:var(--page-bg)!important;color:var(--page-ink)!important;font-family:BODY!important;-webkit-font-smoothing:antialiased;overflow-x:hidden}
body::selection{background:var(--page-accent);color:var(--page-bg)}a{color:inherit}.post{max-width:none!important;margin:0!important}.post>.row{display:block!important;margin:0!important}.post>.row>.col-xs-12{width:100%!important;max-width:none!important;padding:0!important;flex:none!important}.site-header{width:min(100% - 40px,1240px);margin:0 auto!important;padding:22px 0 15px;border-bottom:1px solid currentColor;position:relative;z-index:3}.site-header header{display:flex;align-items:baseline;gap:20px}.header-title{font:700 15px/1 Arvo,sans-serif!important;margin:0!important;letter-spacing:.08em}.header-title a::after{content:" / LABEL";font-weight:400;color:var(--page-accent)}.header-subtitle{font:11px/1.4 Arvo,sans-serif;color:inherit!important;opacity:.62}.header-items{position:absolute;right:0;top:17px;margin:0!important;font:11px Arvo,sans-serif}.header-item-left{display:none}.header-line{display:none}.site-header+.row{width:min(100% - 40px,1240px);margin:0 auto!important;padding-top:clamp(45px,7vw,90px);display:block!important}.site-header+.row br{display:none}.site-header+.row .col-xs-12{max-width:none!important;padding:0!important}.post-tags{display:inline-block!important;border:1px solid currentColor!important;border-radius:999px!important;padding:5px 10px!important;margin:0 5px 6px 0!important;font:10px Arvo,sans-serif!important;letter-spacing:.04em}.post-tags a{text-decoration:none!important}
.post-header{width:min(100% - 40px,1240px);margin:0 auto!important;padding:clamp(22px,4vw,55px) 0 clamp(55px,8vw,110px);position:relative}.post-title{font-family:DISPLAY!important;font-size:clamp(46px,8vw,116px)!important;line-height:.98!important;letter-spacing:-.055em!important;font-weight:500!important;margin:0!important;max-width:1120px}.post-desc{margin:34px 0 0!important;font:11px Arvo,sans-serif!important;letter-spacing:.08em;text-transform:uppercase}.post-desc .col-xs-6{padding:0!important}.post-date{font-style:normal!important;font-weight:400!important}.post-content{width:min(100% - 40px,760px);margin:0 auto clamp(80px,10vw,150px)!important;font-family:BODY!important;font-size:clamp(17px,1.35vw,20px)!important;line-height:1.9!important;position:relative}.post-content p{line-height:1.9!important;margin:0 0 1.45em!important}.post-content h2,.post-content h3,.post-content h4{font-family:DISPLAY!important;line-height:1.2;scroll-margin-top:30px}.post-content h2{font-size:clamp(32px,4vw,54px);letter-spacing:-.035em;font-weight:500;margin:2.4em 0 .7em}.post-content h2::before{content:attr(data-section);display:block;color:var(--page-accent);font:10px Arvo,sans-serif;letter-spacing:.15em;margin-bottom:10px}.post-content h3{font-size:clamp(23px,2.3vw,31px);font-weight:600;margin:2em 0 .65em}.post-content blockquote{margin:2.2em 0!important;padding:1em 0 1em clamp(20px,4vw,42px)!important;border:0!important;border-left:5px solid var(--page-accent)!important;color:inherit!important;font-size:1.18em}.post-content pre{padding:24px!important;overflow:auto;border-radius:0!important;background:var(--page-ink)!important;color:var(--page-bg)!important;border:1px solid var(--page-accent);font:13px/1.65 ui-monospace,SFMono-Regular,Consolas,monospace}.post-content code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}.post-content :not(pre)>code{background:var(--page-soft)!important;color:var(--page-ink);border-radius:0!important;padding:.15em .35em}.post-content table{display:block;width:100%;overflow:auto;border-collapse:collapse;margin:2em 0;font-size:.88em}.post-content th,.post-content td{padding:12px 14px;border:1px solid color-mix(in srgb,var(--page-ink) 35%,transparent);text-align:left}.post-content th{background:var(--page-soft)}.post-content img{max-width:100%;height:auto;filter:saturate(.88)}.post-content hr{border:0;border-top:1px solid currentColor;opacity:.35;margin:4em 0}.post-content a{text-decoration-color:var(--page-accent)!important;text-decoration-thickness:2px!important}.related-content{width:min(100% - 40px,900px);margin:0 auto 80px!important;border:1px solid currentColor!important;padding:28px!important}.related-content h3{font:500 26px DISPLAY;margin-top:0}.related-content li{margin:10px 0!important}.post-comments,.site-footer{width:min(100% - 40px,900px);margin:0 auto}.design-progress{position:fixed;left:0;top:0;width:100%;height:4px;transform:scaleX(0);transform-origin:left;background:var(--page-accent);z-index:20}.design-toc{position:fixed;right:clamp(12px,3vw,48px);top:50%;transform:translateY(-50%);width:170px;z-index:5;font:9px/1.4 Arvo,sans-serif;letter-spacing:.04em}.design-toc strong{display:block;color:var(--page-accent);letter-spacing:.16em;margin-bottom:10px}.design-toc a{display:block;text-decoration:none;padding:5px 0;opacity:.48;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.design-toc a:hover{opacity:1}.design-home{position:fixed;left:18px;bottom:18px;width:44px;height:44px;display:grid;place-items:center;background:var(--page-ink);color:var(--page-bg);border:1px solid var(--page-accent);border-radius:50%;text-decoration:none;z-index:8;font:18px Arvo,sans-serif;transition:transform .25s}.design-home:hover{transform:translateY(-4px)}
@media(max-width:1120px){.design-toc{display:none}}@media(max-width:700px){.header-subtitle{display:none}.site-header{padding-top:18px}.site-header+.row{padding-top:45px}.post-title{font-size:clamp(42px,13vw,72px)!important}.post-content{width:min(100% - 34px,760px)}.post-content h2{margin-top:2em}.related-content{width:calc(100% - 34px)}.design-home{width:38px;height:38px;left:10px;bottom:10px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.design-home{transition:none}}
.design-toc{opacity:0;pointer-events:none;transition:opacity .25s ease}.design-toc.is-visible{opacity:1;pointer-events:auto}
"""


FAMILY_CSS = {
    "editorial": "body{background-image:linear-gradient(90deg,var(--page-accent) 0 9px,transparent 9px)}.post-header{border-bottom:1px solid currentColor}.post-content>p:first-of-type:first-letter{float:left;font:80px/.76 DISPLAY;color:var(--page-accent);padding:10px 10px 0 0}.post-content h2{border-top:1px solid currentColor;padding-top:18px}",
    "blueprint": "body{background-image:linear-gradient(color-mix(in srgb,var(--page-ink) 9%,transparent) 1px,transparent 1px),linear-gradient(90deg,color-mix(in srgb,var(--page-ink) 9%,transparent) 1px,transparent 1px);background-size:32px 32px!important}.site-header,.post-header{border-color:color-mix(in srgb,var(--page-ink) 55%,transparent)}.post-header{border:1px solid currentColor;margin-top:35px!important;padding-left:clamp(20px,4vw,55px);padding-right:clamp(20px,4vw,55px)}.post-content h2{border:1px solid currentColor;padding:18px}.post-content pre{background:#0d293b!important}",
    "construct": "body{background-image:linear-gradient(135deg,transparent 0 82%,var(--page-accent) 82% 86%,transparent 86%)}.post-header::after{content:'A / Z';position:absolute;right:0;bottom:30px;font:700 clamp(60px,12vw,160px) Arvo,sans-serif;color:var(--page-accent);opacity:.2;z-index:-1}.post-title{text-transform:uppercase}.post-content h2{background:var(--page-accent);color:var(--page-bg);padding:12px 18px;transform:translateX(-20px) rotate(-.6deg)}",
    "signal": "body{background-image:repeating-linear-gradient(0deg,transparent 0 31px,color-mix(in srgb,var(--page-accent) 9%,transparent) 32px)}.post-title{text-shadow:3px 3px 0 var(--page-accent)}.post-header{border-bottom:2px solid var(--page-accent)}.post-content h2::after{content:'  ─────────';color:var(--page-accent);font-family:monospace;white-space:nowrap}.post-content blockquote{background:var(--page-soft);padding:22px!important}",
    "brutalist": ".site-header{border:3px solid currentColor;margin-top:16px!important;padding:15px}.post-header{border:4px solid currentColor;margin-top:28px!important;padding:35px!important;box-shadow:12px 12px 0 var(--page-accent)}.post-title{text-transform:uppercase!important}.post-content h2{border:3px solid currentColor;padding:15px;box-shadow:6px 6px 0 var(--page-soft)}.post-tags{border-width:2px!important}.related-content{border-width:3px!important}",
    "ledger": "body{background-image:linear-gradient(90deg,transparent 0 9%,color-mix(in srgb,var(--page-accent) 38%,transparent) 9% calc(9% + 1px),transparent calc(9% + 1px))}.post-header{border-bottom:3px double currentColor}.post-content{background-image:repeating-linear-gradient(transparent 0 37px,color-mix(in srgb,var(--page-ink) 12%,transparent) 38px)}.post-content h2{background:var(--page-bg);border-bottom:3px double currentColor;padding-bottom:10px}.post-content p{background:color-mix(in srgb,var(--page-bg) 88%,transparent)}",
    "poster": ".post-header{min-height:62vh;display:flex;flex-direction:column;justify-content:end}.post-title{font-size:clamp(58px,11vw,160px)!important}.post-header::before{content:'G';position:absolute;right:-.05em;top:-.3em;font:700 clamp(260px,45vw,700px)/1 Arvo,sans-serif;color:var(--page-accent);opacity:.12;z-index:-1}.post-content h2{border-left:18px solid var(--page-accent);padding-left:18px}.post-content strong{background:var(--page-soft)}",
    "draft": "body{background-image:repeating-linear-gradient(135deg,transparent 0 18px,color-mix(in srgb,var(--page-ink) 4%,transparent) 18px 19px)}.post-header{opacity:.7}.post-title{text-decoration:line-through;text-decoration-color:var(--page-accent)}.post-header::after{content:'DRAFT';position:absolute;right:0;top:10px;border:3px solid currentColor;padding:8px 12px;transform:rotate(8deg);font:700 18px Arvo,sans-serif}",
    "constellation": "body{background-image:radial-gradient(circle at 12% 18%,var(--page-accent) 0 1px,transparent 2px),radial-gradient(circle at 78% 32%,var(--page-ink) 0 1px,transparent 2px),radial-gradient(circle at 44% 73%,var(--page-accent) 0 1px,transparent 2px);background-size:180px 180px,230px 230px,310px 310px!important}.post-header{min-height:58vh;display:flex;align-items:end;border-bottom:1px solid var(--page-accent)}.post-content h2{padding-left:35px;position:relative}.post-content h2::after{content:'';position:absolute;left:0;top:.25em;width:18px;height:18px;border:1px solid var(--page-accent);border-radius:50%;box-shadow:0 0 0 6px var(--page-soft)}",
    "messenger": ".post-header{text-align:center;max-width:980px}.post-title{margin:auto!important}.post-content blockquote{max-width:88%;margin-left:auto!important;border:0!important;background:var(--page-soft);padding:22px 28px!important;border-radius:26px 26px 4px 26px!important}.post-content p:nth-of-type(4n){margin-right:8% !important}.post-content h2{text-align:center}.post-content h2::after{content:' ·';color:var(--page-accent)}",
    "split": "body{background-image:linear-gradient(90deg,var(--page-bg) 0 50%,var(--page-soft) 50%)}.post-header{display:grid;grid-template-columns:1fr 1fr;gap:40px;border-bottom:8px solid var(--page-accent)}.post-title{grid-column:1/-1}.post-content h2:nth-of-type(odd){transform:translateX(-8vw)}.post-content h2:nth-of-type(even){transform:translateX(8vw);text-align:right}.post-content table{background:var(--page-bg)}",
    "terminal": "body{background-image:linear-gradient(color-mix(in srgb,var(--page-accent) 5%,transparent) 1px,transparent 1px);background-size:100% 4px!important}.site-header{font-family:ui-monospace,monospace}.post-header::before{content:'muzig@openclaw:~$ read';display:block;color:var(--page-accent);font:14px ui-monospace,monospace;margin-bottom:25px}.post-title{font-family:ui-monospace,monospace!important;letter-spacing:-.04em!important}.post-content h2::before{content:'$ section_' attr(data-section);display:inline;margin-right:12px}.post-content h2{font-family:ui-monospace,monospace}.post-content a{color:var(--page-accent)}",
    "cards": ".post-header{border-bottom:1px solid currentColor}.post-content>ol{list-style:none;counter-reset:tips;padding:0}.post-content>ol>li{counter-increment:tips;margin:32px 0;padding:28px;background:var(--page-soft);border:1px solid currentColor;transform:rotate(-.35deg)}.post-content>ol>li:nth-child(even){transform:rotate(.45deg);background:var(--page-bg)}.post-content>ol>li::before{content:counter(tips,decimal-leading-zero);float:right;color:var(--page-accent);font:700 38px Arvo,sans-serif}.post-content h2{font-style:italic}",
    "archive": "body{background-image:radial-gradient(color-mix(in srgb,var(--page-ink) 13%,transparent) .7px,transparent .7px);background-size:5px 5px!important}.post-header{border:1px solid currentColor;padding-left:35px;padding-right:35px}.post-header::after{content:'ARCHIVED';position:absolute;right:30px;bottom:25px;border:2px solid var(--page-accent);color:var(--page-accent);padding:8px 12px;transform:rotate(-6deg);font:700 12px Arvo,sans-serif;letter-spacing:.15em}.post-content h2{border-bottom:1px dashed currentColor;padding-bottom:12px}.post-content blockquote{border:1px solid currentColor!important;padding:24px!important}",
    "duel": "body{background:linear-gradient(90deg,var(--page-soft) 0 11px,var(--page-bg) 11px calc(100% - 11px),var(--page-accent) calc(100% - 11px))!important}.post-title em{color:var(--page-accent)}.post-content h2{padding:18px}.post-content h2:nth-of-type(odd){border-left:8px solid var(--page-accent);background:var(--page-soft)}.post-content h2:nth-of-type(even){border-right:8px solid var(--page-ink);text-align:right}.post-content table{border-top:8px solid var(--page-accent)}",
    "topology": ".post-header{border-bottom:1px solid currentColor}.post-content::before{content:'';position:absolute;left:-55px;top:0;bottom:0;border-left:1px dashed var(--page-accent)}.post-content h2{position:relative}.post-content h2::after{content:'';position:absolute;left:-64px;top:.35em;width:17px;height:17px;background:var(--page-bg);border:3px solid var(--page-accent);border-radius:50%}.post-content blockquote{background:var(--page-soft);clip-path:polygon(0 0,96% 0,100% 50%,96% 100%,0 100%)}",
    "security": "body{background-image:repeating-linear-gradient(135deg,transparent 0 28px,color-mix(in srgb,var(--page-accent) 8%,transparent) 28px 42px)}.post-header{border-top:14px repeating-linear-gradient(45deg,var(--page-accent));border-bottom:12px solid var(--page-ink)}.post-header::before{content:'AUTHORIZED PERSONNEL ONLY';display:inline-block;background:var(--page-accent);color:var(--page-ink);padding:8px 12px;font:700 11px Arvo,sans-serif;letter-spacing:.12em;margin-bottom:22px}.post-content h2{background:var(--page-ink);color:var(--page-bg);padding:14px 18px}.post-content strong{background:var(--page-accent);color:var(--page-ink)}",
    "library": ".post-header{border-bottom:5px double currentColor}.post-title{font-style:italic}.post-content h2{border-top:12px solid var(--page-soft);padding-top:16px}.post-content h2::after{content:'INDEX';float:right;font:9px Arvo,sans-serif;color:var(--page-accent);letter-spacing:.15em}.post-content blockquote{border-left:0!important;border-top:1px solid currentColor!important;border-bottom:1px solid currentColor!important;padding:22px 0!important}.related-content{background:var(--page-soft)}",
    "orgchart": ".post-header{text-align:center}.post-title{margin:auto!important}.post-content h2{text-align:center;border:1px solid currentColor;padding:18px;position:relative}.post-content h2::before{content:attr(data-section);position:absolute;left:50%;top:-29px;transform:translateX(-50%);background:var(--page-bg);border:1px solid currentColor;padding:4px 8px}.post-content h2::after{content:'';position:absolute;left:50%;top:-18px;height:17px;border-left:1px solid currentColor}.post-content h3{border-left:1px solid currentColor;padding-left:25px}",
    "cad": "body{background-image:linear-gradient(color-mix(in srgb,var(--page-ink) 8%,transparent) 1px,transparent 1px),linear-gradient(90deg,color-mix(in srgb,var(--page-ink) 8%,transparent) 1px,transparent 1px);background-size:20px 20px!important}.post-header{border:1px solid currentColor;margin-top:32px!important;padding:28px}.post-header::before{content:'DRAWING № ASM-2026';font:10px Arvo,sans-serif;color:var(--page-accent);letter-spacing:.14em}.post-title{margin-top:25px!important}.post-content h2{border:1px solid currentColor;padding:15px}.post-content h2::after{content:' ◇';color:var(--page-accent)}",
    "incident": ".post-header{border-top:12px solid var(--page-accent);border-bottom:1px solid currentColor}.post-header::before{content:'STATUS: RESOLVED';display:inline-block;border:2px solid var(--page-accent);color:var(--page-accent);padding:6px 10px;font:700 11px Arvo,sans-serif;letter-spacing:.13em;margin-bottom:25px}.post-content h2{counter-increment:incident;border-bottom:1px solid currentColor;padding-bottom:12px}.post-content pre{border-left:9px solid var(--page-accent)}.post-content blockquote{background:var(--page-soft)}",
    "score": "body{background-image:repeating-linear-gradient(0deg,transparent 0 12px,color-mix(in srgb,var(--page-ink) 8%,transparent) 13px,transparent 14px 25px)}.post-header{min-height:52vh;display:flex;align-items:end}.post-content{background:var(--page-bg);padding:0 24px}.post-content h2::after{content:' 𝄞';color:var(--page-accent)}.post-content h2{font-style:italic;border-bottom:1px solid currentColor}.post-content blockquote{text-align:center;border:0!important;font-size:1.4em}",
    "zine": "body{background-image:radial-gradient(color-mix(in srgb,var(--page-ink) 9%,transparent) .8px,transparent .8px);background-size:4px 4px!important}.post-header{border:4px solid currentColor;padding:30px;transform:rotate(-.45deg);box-shadow:13px 13px 0 var(--page-accent)}.post-title{text-transform:uppercase}.post-content h2{display:table;background:var(--page-ink);color:var(--page-bg);padding:9px 15px;transform:rotate(-1deg)}.post-content h2:nth-of-type(even){transform:rotate(1deg);margin-left:auto}.post-content blockquote{border:4px solid currentColor!important;padding:22px!important;transform:rotate(.5deg)}",
    "circuit": "body{background-image:linear-gradient(90deg,color-mix(in srgb,var(--page-accent) 7%,transparent) 1px,transparent 1px),linear-gradient(color-mix(in srgb,var(--page-accent) 7%,transparent) 1px,transparent 1px);background-size:48px 48px!important}.post-header{border-bottom:1px solid var(--page-accent)}.post-content h2{padding-left:32px;position:relative}.post-content h2::before{content:attr(data-section);display:grid;place-items:center;position:absolute;left:-25px;top:.1em;width:38px;height:38px;border:1px solid var(--page-accent);border-radius:50%;background:var(--page-bg)}.post-content h2::after{content:'';position:absolute;left:-6px;top:38px;height:45px;border-left:1px solid var(--page-accent)}",
    "industrial": "body{background-image:repeating-linear-gradient(135deg,transparent 0 36px,color-mix(in srgb,var(--page-ink) 4%,transparent) 36px 38px)}.site-header{border-bottom:8px solid var(--page-accent)}.post-header{min-height:58vh;display:flex;align-items:end}.post-header::after{content:'03';position:absolute;right:0;top:0;font:700 clamp(180px,32vw,500px)/.8 Arvo,sans-serif;color:var(--page-accent);opacity:.3;z-index:-1}.post-content h2{border-left:14px solid var(--page-accent);padding-left:18px;text-transform:uppercase}.post-content pre{box-shadow:8px 8px 0 var(--page-accent)}",
    "lab": ".post-header{border-bottom:1px solid currentColor}.post-header::before{content:'OBSERVATION / HYPOTHESIS / ITERATION';display:block;color:var(--page-accent);font:10px Arvo,sans-serif;letter-spacing:.14em;margin-bottom:28px}.post-content{border-left:1px solid var(--page-soft);padding-left:35px}.post-content h2{position:relative}.post-content h2::before{position:absolute;right:calc(100% + 48px);top:12px}.post-content h2::after{content:'+';position:absolute;left:-44px;top:.15em;color:var(--page-accent);font:24px Arvo}.post-content blockquote{background:var(--page-soft)}",
    "notebook": "body{background-image:linear-gradient(90deg,transparent 0 12%,color-mix(in srgb,var(--page-accent) 35%,transparent) 12% calc(12% + 1px),transparent calc(12% + 1px)),repeating-linear-gradient(0deg,transparent 0 35px,color-mix(in srgb,var(--page-ink) 10%,transparent) 36px)}.post-title{transform:rotate(-1deg)}.post-content h2{transform:rotate(-.7deg);text-decoration:underline;text-decoration-color:var(--page-accent);text-decoration-thickness:3px}.post-content pre{transform:rotate(.3deg)}.post-content blockquote{border:0!important;background:color-mix(in srgb,var(--page-soft) 78%,transparent);transform:rotate(.5deg)}",
    "patchbay": ".post-header{border:2px solid currentColor;padding:32px}.post-header::after{content:'●  ○  ●  ○  ●';display:block;color:var(--page-accent);font:35px Arvo,sans-serif;letter-spacing:.3em;margin-top:30px}.post-content h2{border-bottom:3px solid currentColor;padding-bottom:12px}.post-content h2::before{display:inline-block;border:2px solid var(--page-accent);border-radius:50%;width:36px;height:36px;line-height:32px;text-align:center;margin-right:12px}.post-content a{color:var(--page-accent)}.post-content pre{border-top:10px solid var(--page-soft)}",
    "newspaper": ".site-header{border-top:5px double currentColor;border-bottom:5px double currentColor;margin-top:16px!important}.post-header{text-align:center;border-bottom:5px double currentColor}.post-title{margin:auto!important;font-size:clamp(50px,8.5vw,122px)!important}.post-header::before{content:'THE WORKING ENGINEER';display:block;font:700 12px Arvo,sans-serif;letter-spacing:.25em;margin-bottom:30px}.post-content>p:first-of-type{font-size:1.25em;font-weight:600}.post-content>p:first-of-type:first-letter{float:left;font:90px/.8 DISPLAY;padding:8px 10px 0 0;color:var(--page-accent)}.post-content h2{border-top:3px double currentColor;border-bottom:1px solid currentColor;padding:15px 0}",
    "timeline": ".post-header{min-height:55vh;display:flex;align-items:end}.post-content{border-left:3px solid var(--page-accent);padding-left:clamp(25px,5vw,60px)}.post-content h2{position:relative}.post-content h2::before{position:absolute;right:calc(100% + clamp(34px,5vw,69px));top:.4em;background:var(--page-bg);padding:5px 0}.post-content h2::after{content:'';position:absolute;right:calc(100% + clamp(19px,5vw,54px));top:.4em;width:13px;height:13px;background:var(--page-accent);border-radius:50%}.post-content blockquote{background:var(--page-soft)}",
    "fieldguide": "body{background-image:radial-gradient(ellipse at top right,color-mix(in srgb,var(--page-soft) 75%,transparent),transparent 38%)}.post-header{border-bottom:1px solid currentColor}.post-header::after{content:'✣';position:absolute;right:0;bottom:30px;color:var(--page-accent);font-size:90px}.post-content h2{color:var(--page-ink);border-bottom:1px solid var(--page-accent);padding-bottom:12px}.post-content h2::after{content:'  ✦';color:var(--page-accent);font-size:.45em}.post-content blockquote{border:0!important;background:var(--page-soft);padding:24px!important}.post-content strong{color:color-mix(in srgb,var(--page-accent) 85%,var(--page-ink))}",
    "manifesto": ".site-header{border-color:var(--page-ink)}.header-title a::after{color:var(--page-ink)}.post-header{min-height:72vh;display:flex;align-items:end;border-bottom:8px solid var(--page-ink)}.post-title{font-size:clamp(64px,12vw,180px)!important;text-transform:uppercase!important}.post-content{font-family:'Heiti SC','PingFang SC',sans-serif!important;font-weight:600}.post-content ol{counter-reset:rule;list-style:none;padding:0}.post-content ol>li{counter-increment:rule;border-top:5px solid var(--page-ink);padding:30px 0;font-size:1.18em}.post-content ol>li::before{content:counter(rule,decimal-leading-zero);display:block;font:700 64px Arvo,sans-serif;color:var(--page-accent);-webkit-text-stroke:1px var(--page-ink)}.post-content h2{font-size:clamp(46px,7vw,86px);text-transform:uppercase;border-top:7px solid currentColor;padding-top:18px}.post-content blockquote{border-color:var(--page-ink)!important;font-size:1.4em}",
}


SCRIPT = r"""
<script>
document.addEventListener('DOMContentLoaded',()=>{
  document.body.dataset.articleDesign='NAME';
  const content=document.querySelector('.post-content');
  if(!content)return;
  const progress=document.createElement('div');progress.className='design-progress';progress.setAttribute('aria-hidden','true');document.body.append(progress);
  const home=document.createElement('a');home.className='design-home';home.href='/';home.textContent='←';home.setAttribute('aria-label','返回文章首页');document.body.append(home);
  const headings=[...content.querySelectorAll('h2')];
  headings.forEach((heading,index)=>{heading.dataset.section=String(index+1).padStart(2,'0');if(!heading.id)heading.id='section-'+(index+1)});
  let toc=null;if(headings.length>2){toc=document.createElement('aside');toc.className='design-toc';toc.setAttribute('aria-label','文章目录');toc.innerHTML='<strong>ON THIS PAGE</strong>'+headings.map(h=>`<a href="#${h.id}">${h.textContent}</a>`).join('');document.body.append(toc)}
  const date=document.querySelector('.post-date');if(date){const chars=content.textContent.replace(/\s/g,'').length;date.append(document.createTextNode(` · ${Math.max(1,Math.ceil(chars/500))} MIN READ`))}
  const update=()=>{const max=document.documentElement.scrollHeight-innerHeight;progress.style.transform=`scaleX(${max>0?scrollY/max:0})`;if(toc)toc.classList.toggle('is-visible',content.getBoundingClientRect().top<innerHeight*.72)};update();addEventListener('scroll',update,{passive:true});addEventListener('resize',update);
});
</script>
"""


def title_of(source: str) -> str:
    match = re.search(r"<title>(.*?)</title>", source, re.S | re.I)
    return html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip() if match else ""


def theme_for(title: str) -> Theme | None:
    prefixes = [theme for theme in THEMES if title.startswith(theme.match)]
    if prefixes:
        return max(prefixes, key=lambda theme: len(theme.match))
    matches = [theme for theme in THEMES if theme.match in title]
    return max(matches, key=lambda theme: len(theme.match)) if matches else None


def clean_legacy_build(source: str) -> str:
    """Remove development-only Hugo residue while preserving article content."""
    source = source.replace('<html lang="en">', '<html lang="zh-CN">')
    source = re.sub(r'("inLanguage"\s*:\s*)"en-US"', r'\1"zh-CN"', source)
    source = re.sub(r'<script src="/livereload\.js[^>]*></script>\s*', "", source)
    source = re.sub(r'\s*<meta name="generator" content="Hugo [^"]+">', "", source)
    source = re.sub(r'\s*<link rel="preconnect" href="https://fonts\.gstatic\.com"\s*/>', "", source)
    source = re.sub(
        r'\s*<link\s+href="https://fonts\.googleapis\.com[^"]+"\s+rel="stylesheet"\s*/>',
        "",
        source,
    )
    source = source.replace("http://localhost:1313", "https://muzig.io")
    source = source.replace(r"http:\/\/localhost:1313", r"https:\/\/muzig.io")
    # A legacy article used H1 for every body section. Keep one page H1 and
    # normalize identified body headings so the generated TOC remains complete.
    source = re.sub(r'<h1(\s+id="[^"]+"[^>]*)>(.*?)</h1>', r'<h2\1>\2</h2>', source, flags=re.S)
    source = re.sub(
        r'<div class="post-content markdown-body">(.*?)\n\s*</div>\n\s*\n\s*<div class="row">',
        r'<main class="post-content markdown-body">\1\n        </main>\n\n        <div class="row">',
        source,
        count=1,
        flags=re.S,
    )
    if 'property="article:published_time"' not in source:
        published = re.search(r'<time class="post-date" datetime="\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})', source)
        if published:
            iso_date = f"{published.group(1)}T{published.group(2)}+08:00"
            source = source.replace("</head>", f'  <meta property="article:published_time" content="{iso_date}">\n</head>', 1)
    def concise_description(match: re.Match[str]) -> str:
        plain = " ".join(html.unescape(match.group(2)).split())
        if len(plain) > 160:
            plain = plain[:157].rstrip("，。；：、,. ;:") + "…"
        return match.group(1) + html.escape(plain, quote=True) + match.group(3)

    source = re.sub(
        r'(<meta\s+(?:name|property)="(?:description|og:description|twitter:description)"\s+content=")(.*?)("\s*/?>)',
        concise_description,
        source,
        flags=re.S | re.I,
    )
    source = re.sub(
        r'(<script type="application/ld\+json">)(.*?)(</script>)',
        lambda match: match.group(1) + re.sub(r",(\s*[}\]])", r"\1", match.group(2)) + match.group(3),
        source,
        flags=re.S,
    )
    return source


def render(theme: Theme) -> str:
    css = BASE_CSS
    replacements = {
        "BG": theme.bg,
        "INK": theme.ink,
        "ACCENT": theme.accent,
        "SOFT": theme.soft,
        "DISPLAY": theme.display,
        "BODY": theme.body,
        "LABEL": theme.label,
    }
    for key, value in replacements.items():
        css = css.replace(key, value)
    css += "\n" + FAMILY_CSS[theme.family]
    script = SCRIPT.replace("NAME", theme.name)
    robots = (
        '\n<meta name="robots" content="noindex,nofollow">'
        if theme.name in {"draft-blank", "augmented-circuit"}
        else ""
    )
    return f'{BEGIN}\n<meta name="article-design" content="{theme.name}">{robots}\n<style id="article-design">\n{css}\n</style>\n{script}\n{END}'


def article_files() -> list[Path]:
    dated = list((ROOT / "public/2025").rglob("index.html")) + list((ROOT / "public/2026").rglob("index.html"))
    aliases = [path for path in (ROOT / "public/posts").glob("*/index.html") if path.parent.name != "_template"]
    return sorted(dated + aliases)


def canonical_of(source: str) -> str | None:
    match = re.search(r'<link rel="canonical" href="([^"]+)"', source)
    return match.group(1) if match else None


def main() -> None:
    changed = 0
    missing: list[tuple[Path, str]] = []
    dated_files = list((ROOT / "public/2025").rglob("index.html")) + list((ROOT / "public/2026").rglob("index.html"))
    canonical_by_title = {
        title_of(path.read_text(encoding="utf-8")): canonical_of(path.read_text(encoding="utf-8"))
        for path in dated_files
    }
    for path in article_files():
        source = clean_legacy_build(path.read_text(encoding="utf-8"))
        title = title_of(source)
        theme = theme_for(title)
        if not theme:
            missing.append((path, title))
            continue
        if path.is_relative_to(ROOT / "public/posts"):
            old_canonical = canonical_of(source)
            new_canonical = canonical_by_title.get(title)
            if old_canonical and new_canonical and old_canonical != new_canonical:
                source = source.replace(old_canonical, new_canonical)
                source = source.replace(old_canonical.replace("/", r"\/"), new_canonical.replace("/", r"\/"))
        injection = render(theme)
        if BEGIN in source:
            source = re.sub(
                re.escape(BEGIN) + r".*?" + re.escape(END),
                lambda _match: injection,
                source,
                flags=re.S,
            )
        else:
            source = source.replace("</head>", injection + "\n</head>", 1)
        path.write_text(source, encoding="utf-8")
        changed += 1
        print(f"{theme.name:24} {path.relative_to(ROOT)}")
    if missing:
        for path, title in missing:
            print(f"NO THEME: {path.relative_to(ROOT)} :: {title}")
        raise SystemExit(f"{len(missing)} article pages have no theme")
    print(f"Updated {changed} HTML pages with {len(THEMES)} distinct article themes.")


if __name__ == "__main__":
    main()
