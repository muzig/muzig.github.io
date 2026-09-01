import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const categories = [
  'AI工程',
  'Agent工具链',
  'MCP',
  'Go工程',
  '编程语言',
  'LLM系统',
  '软件架构',
] as const;

const articleTypes = [
  '深度解析',
  '实战教程',
  '入门指南',
  '架构拆解',
  '对比分析',
  '方法论',
  '观点评论',
  '故障排查',
] as const;

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string().min(1),
    description: z.string().min(24).max(180),
    publishedAt: z.coerce.date(),
    updatedAt: z.coerce.date().optional(),
    draft: z.boolean().default(false),
    category: z.enum(categories),
    series: z.string().optional(),
    articleType: z.enum(articleTypes),
    tags: z.array(z.string()).default([]),
    design: z.enum(['standard', 'editorial', 'manifesto']).default('standard'),
    path: z.string().regex(/^\/\d{4}\/\d{2}\/\d{2}\/[a-z0-9][a-z0-9-]*\/$/),
    canonical: z.url().optional(),
    legacyUrls: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
  }),
});

export const collections = { blog };
