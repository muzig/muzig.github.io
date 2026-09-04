import { getCollection } from 'astro:content';
import legacyPosts from '../data/legacy-posts.json';

const escapeXml = (value: string) => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&apos;');

export async function GET() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const pages = [
    { url: '/', modified: undefined },
    ...posts.map(({ data }) => ({ url: data.path, modified: data.updatedAt ?? data.publishedAt })),
    ...legacyPosts.map((post) => ({ url: post.url, modified: new Date(`${post.publishedAt}T10:00:00+08:00`) })),
  ];
  const body = pages.map(({ url, modified }) => {
    const loc = escapeXml(new URL(url, 'https://muzig.github.io').href);
    const lastmod = modified ? `<lastmod>${modified.toISOString()}</lastmod>` : '';
    return `  <url><loc>${loc}</loc>${lastmod}</url>`;
  }).join('\n');

  return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
}
