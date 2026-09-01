import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';

const [title, slug] = process.argv.slice(2);
if (!title || !slug) {
  console.error('用法：./new-post.sh "文章标题" english-url-slug');
  process.exit(1);
}
if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) {
  console.error('URL slug 只能包含小写字母、数字和单个连字符。');
  process.exit(1);
}

const now = new Date();
const parts = new Intl.DateTimeFormat('en-CA', {
  timeZone: 'Asia/Shanghai',
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
}).formatToParts(now);
const get = (type) => parts.find((part) => part.type === type)?.value;
const date = `${get('year')}-${get('month')}-${get('day')}`;
const path = `/${date.replaceAll('-', '/')}/${slug}/`;
const root = resolve(import.meta.dirname, '..');
const output = resolve(root, `src/content/blog/${date}-${slug}.md`);
const source = `---
title: ${JSON.stringify(title)}
description: 请用一句完整的话说明文章解决的问题、适合的读者以及能够获得的核心价值。
publishedAt: ${date}T10:00:00+08:00
draft: true
category: AI工程
articleType: 深度解析
tags:
  - AI工程
design: standard
path: ${path}
legacyUrls: []
featured: false
---

这里开始写正文。
`;

await mkdir(dirname(output), { recursive: true });
try {
  await writeFile(output, source, { encoding: 'utf8', flag: 'wx' });
} catch (error) {
  if (error?.code === 'EEXIST') {
    console.error(`文件已存在：${output}`);
    process.exit(1);
  }
  throw error;
}
console.log(`已创建草稿：${output}`);
console.log(`发布路径：${path}`);
