import { cp, mkdir, readFile, readdir, writeFile } from 'node:fs/promises';
import { dirname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const sourceRoot = resolve(root, 'legacy-pages');
const outputRoot = resolve(root, 'dist');
const generatedRootFiles = new Set(['index.html', 'index.xml', 'robots.txt', 'sitemap.xml']);
let copied = 0;
let redirected = 0;
let skipped = 0;

async function exists(path) {
  try {
    await readFile(path);
    return true;
  } catch (error) {
    if (error?.code === 'EISDIR') return true;
    if (error?.code === 'ENOENT') return false;
    throw error;
  }
}

function isNoindex(source) {
  return /<meta[^>]+(?:name=["']robots["'][^>]+content=["'][^"']*noindex|content=["'][^"']*noindex[^>]+name=["']robots["'])[^>]*>/i.test(source);
}

function redirectDocument(target) {
  const safeTarget = target.replaceAll('&', '&amp;').replaceAll('"', '&quot;');
  return `<!doctype html>\n<html lang="zh-CN">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <meta name="robots" content="noindex,follow">\n  <meta http-equiv="refresh" content="0; url=${safeTarget}">\n  <link rel="canonical" href="${safeTarget}">\n  <title>文章已迁移 · Muzig</title>\n</head>\n<body>\n  <p>文章已迁移，正在前往<a href="${safeTarget}">正式地址</a>。</p>\n</body>\n</html>\n`;
}

async function copyEntry(sourcePath) {
  const relativePath = relative(sourceRoot, sourcePath);
  const normalized = relativePath.split(sep).join('/');

  if (generatedRootFiles.has(normalized) || normalized === 'posts/_template/index.html') {
    skipped += 1;
    return;
  }

  const entries = await readdir(sourcePath, { withFileTypes: true }).catch((error) => {
    if (error?.code === 'ENOTDIR') return null;
    throw error;
  });
  if (entries) {
    for (const entry of entries) await copyEntry(join(sourcePath, entry.name));
    return;
  }

  const outputPath = join(outputRoot, relativePath);
  if (normalized.endsWith('.html')) {
    const source = await readFile(sourcePath, 'utf8');
    if (isNoindex(source)) {
      skipped += 1;
      return;
    }
    if (/^posts\/[^/]+\/index\.html$/.test(normalized)) {
      const canonical = source.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i)?.[1]
        ?? source.match(/<link[^>]+href=["']([^"']+)["'][^>]+rel=["']canonical["']/i)?.[1];
      if (!canonical || canonical.includes('{{')) throw new Error(`${normalized} 缺少可用 canonical`);
      await mkdir(dirname(outputPath), { recursive: true });
      await writeFile(outputPath, redirectDocument(canonical), 'utf8');
      redirected += 1;
      return;
    }
  }

  if (await exists(outputPath)) {
    throw new Error(`旧页面与 Astro 生成结果冲突：${normalized}`);
  }
  await mkdir(dirname(outputPath), { recursive: true });
  await cp(sourcePath, outputPath);
  copied += 1;
}

await copyEntry(sourceRoot);
console.log(`旧站兼容层：复制 ${copied} 个文件，生成 ${redirected} 个重定向，跳过 ${skipped} 个发布冲突或草稿。`);
