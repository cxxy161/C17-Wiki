// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'C17星区 Wiki',
      defaultLocale: 'root',
      locales: {
        root: {
          label: '简体中文',
          lang: 'zh-CN',
        },
      },
      sidebar: [
        {
          label: '星体百科',
          // 重点：尝试去掉 directory 里的所有前缀，甚至可以试着写成 './planet'
          autogenerate: { directory: 'planet' }, 
        },
      ],
    }),
  ],
});
