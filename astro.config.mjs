import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://muzig.github.io',
  output: 'static',
  trailingSlash: 'always',
  integrations: [mdx()],
});
