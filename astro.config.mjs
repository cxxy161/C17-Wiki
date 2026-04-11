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
      // 1. 禁用所有“书籍感”的导航
      pagination: false,
      // 2. 移除所有页面元数据（最后更新时间、编辑链接等）
      lastUpdated: false,
      editLink: {
        baseUrl: null,
      },
      // 3. 禁用侧边栏的“收起”功能，让它像 Wiki 目录一样直观（可选）
      sidebar: [
        {
          label: '星体百科',
          autogenerate: { directory: 'planet' }, 
        },
      ],
      // 4. 彻底移除页脚（Credits 等）
      credits: false,
    }),
  ],
});
