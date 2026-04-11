// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://cxxy161.github.io',
  base: '/C17-Wiki/',
  trailingSlash: 'always', 
  integrations: [
    starlight({
      title: 'C17星区 Wiki',
      defaultLocale: 'zh-CN',
      locales: {
        root: {
          label: '简体中文',
          lang: 'zh-CN',
        },
      },
      // 1. 禁用上下页导航
      pagination: false,
      // 2. 移除最后更新时间
      lastUpdated: false,
      // 3. 彻底禁用编辑链接：不要写 editLink 属性，或者把整个对象删掉
      // 这里的配置如果不需要就直接注释掉或删除
      
      // 4. 禁用页脚
      credits: false,
      sidebar: [
        {
          label: '星体百科',
          autogenerate: { directory: 'planet' }, 
        },
      ],
    }),
  ],
});
