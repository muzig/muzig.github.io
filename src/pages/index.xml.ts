import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import legacyPosts from '../data/legacy-posts.json';

export async function GET(context: { site?: URL }) {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const items = [
    ...posts.map(({ data }) => ({
      title: data.title,
      description: data.description,
      pubDate: data.publishedAt,
      link: data.path,
      categories: [data.category, data.articleType, ...data.tags],
    })),
    ...legacyPosts.map((post) => ({
      title: post.title,
      description: post.description,
      pubDate: new Date(`${post.publishedAt}T10:00:00+08:00`),
      link: post.url,
      categories: [post.category, post.articleType],
    })),
  ].sort((a, b) => b.pubDate.getTime() - a.pubDate.getTime());

  return rss({
    title: 'Muzig 的技术博客',
    description: 'AI 工程、Agent 工具链、MCP、Go 工程、编程语言与 LLM 系统。',
    site: context.site ?? new URL('https://muzig.github.io'),
    items,
    customData: '<language>zh-CN</language>',
  });
}
