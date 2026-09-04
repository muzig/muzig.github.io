import { readFile, readdir } from 'node:fs/promises';
import { join, relative, resolve, sep } from 'node:path';
import legacyPosts from '../src/data/legacy-posts.json' with { type: 'json' };

const root = resolve(import.meta.dirname, '..');
const dist = join(root, 'dist');
let checks = 0;

function assert(condition, message) {
  if (!condition) throw new Error(message);
  checks += 1;
}

async function filesUnder(directory) {
  const result = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) result.push(...await filesUnder(path));
    else result.push(path);
  }
  return result;
}

const files = await filesUnder(dist);
const htmlFiles = files.filter((path) => path.endsWith('.html'));
const contentFiles = (await filesUnder(join(root, 'src', 'content', 'blog'))).filter((path) => /\.mdx?$/.test(path));
const generatedPosts = [];
const draftPaths = [];
for (const path of contentFiles) {
  const source = await readFile(path, 'utf8');
  const url = source.match(/^path:\s*(\S+)\s*$/m)?.[1];
  const draft = source.match(/^draft:\s*(true|false)\s*$/m)?.[1] === 'true';
  if (!url) throw new Error(`${relative(root, path)} 缺少 path`);
  (draft ? draftPaths : generatedPosts).push(url);
}
const expectedPostCount = legacyPosts.length + generatedPosts.length;
const decoder = new TextDecoder('utf-8', { fatal: true });
for (const path of htmlFiles) decoder.decode(await readFile(path));
assert(htmlFiles.length >= 160, `发布 HTML 数量异常：${htmlFiles.length}`);

const home = await readFile(join(dist, 'index.html'), 'utf8');
assert(home.includes('<!DOCTYPE html>') || home.includes('<!doctype html>'), '首页缺少 HTML5 doctype');
assert(home.includes('<html lang="zh-CN">'), '首页缺少 zh-CN lang');
assert(home.includes('<meta name="description"'), '首页缺少 description');
assert(home.includes('<link rel="canonical" href="https://muzig.github.io/">'), '首页 canonical 不正确');
assert((home.match(/class="story(?:\s|\")/g) ?? []).length === expectedPostCount, '首页文章卡片数量不正确');

for (const post of legacyPosts) {
  const output = join(dist, decodeURIComponent(post.url), 'index.html');
  assert(files.includes(output), `旧文章 URL 未保留：${post.url}`);
  assert(home.includes(`href="${post.url}"`), `首页缺少旧文章入口：${post.url}`);
}
for (const url of generatedPosts) {
  assert(files.includes(join(dist, url, 'index.html')), `Astro 文章未生成：${url}`);
  assert(home.includes(`href="${url}"`), `首页缺少 Astro 文章入口：${url}`);
}
for (const url of draftPaths) assert(!files.includes(join(dist, url, 'index.html')), `草稿被发布：${url}`);

const rss = await readFile(join(dist, 'index.xml'), 'utf8');
assert((rss.match(/<item>/g) ?? []).length === expectedPostCount, 'RSS 的已发布文章数量不正确');
const sitemap = await readFile(join(dist, 'sitemap.xml'), 'utf8');
assert((sitemap.match(/<url>/g) ?? []).length === expectedPostCount + 1, 'Sitemap 的 URL 数量不正确');
assert(sitemap.includes('https://muzig.github.io/'), 'Sitemap 缺少首页');
const robots = await readFile(join(dist, 'robots.txt'), 'utf8');
assert(robots.includes('Sitemap: https://muzig.github.io/sitemap.xml'), 'robots.txt 未指向正式 Sitemap');

const publicTextFiles = files.filter((path) => /\.(?:html|xml|txt)$/.test(path));
for (const path of publicTextFiles) {
  const source = await readFile(path, 'utf8');
  assert(!source.includes('muzig.io'), `${relative(dist, path)} 仍引用已弃用域名`);
}

assert(!files.includes(join(dist, 'posts', '_template', 'index.html')), '旧 HTML 模板被发布');

const redirectFiles = files.filter((path) => /^posts\/.+\/index\.html$/.test(relative(dist, path).split(sep).join('/')));
assert(redirectFiles.length === 13, `预期 13 个兼容重定向，实际 ${redirectFiles.length} 个`);
for (const path of redirectFiles) {
  const source = await readFile(path, 'utf8');
  assert(source.includes('http-equiv="refresh"') && source.includes('noindex,follow'), `${relative(dist, path)} 不是轻量重定向`);
}

console.log(`发布产物检查通过：${htmlFiles.length} 个 HTML 文件，${checks} 项断言。`);
