import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const sourcePath = `${root}/legacy-pages/index.html`;
const outputPath = `${root}/src/data/legacy-posts.json`;
const source = await readFile(sourcePath, 'utf8');

const clean = (value) =>
  value
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, ' ')
    .trim();

const cards = [...source.matchAll(/<a class="story\s*([^"]*)" data-topic="([^"]+)" href="([^"]+)">(.*?)<\/a>/gs)];
const posts = cards.map((match, index) => {
  const [, cardClasses, topic, url, body] = match;
  const top = body.match(/<div class="story-top">(.*?)<\/div>/s)?.[1] ?? '';
  const topSpans = [...top.matchAll(/<span[^>]*>(.*?)<\/span>/gs)].map((item) => clean(item[1]));
  const title = clean(body.match(/<h3>(.*?)<\/h3>/s)?.[1] ?? '');
  const foot = body.match(/<div class="story-foot">(.*?)<\/div>/s)?.[1] ?? '';
  const summary = clean(foot.match(/<span>(.*?)<\/span>/s)?.[1] ?? '');
  const date = topSpans[1]?.match(/(\d{4}\.\d{2}\.\d{2})/)?.[1]?.replaceAll('.', '-') ?? '';

  if (!title || !date || !url) {
    throw new Error(`无法解析第 ${index + 1} 张旧文章卡片`);
  }

  return {
    title,
    description: summary,
    publishedAt: date,
    category: topic,
    articleType: summary,
    url,
    featured: cardClasses.split(/\s+/).includes('featured'),
    legacy: true,
  };
});

if (posts.length !== 30) {
  throw new Error(`预期提取 30 篇旧文章，实际得到 ${posts.length} 篇`);
}

await writeFile(outputPath, `${JSON.stringify(posts, null, 2)}\n`, 'utf8');
console.log(`已写入 ${posts.length} 篇旧文章元数据：${outputPath}`);
