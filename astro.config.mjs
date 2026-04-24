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
      // 1. 语言配置
      defaultLocale: 'zh-cn',
      locales: {
        root: {
          label: '简体中文',
          lang: 'zh-cn',
        },
      },
      // 2. 移除所有多余功能（Wiki 化）
      pagination: false,    // 禁用上下页
      lastUpdated: false,   // 禁用更新时间
      credits: false,       // 禁用页脚标志
      // 3. 修正后的社交链接语法（必须是空数组）
      social: [], 
      // 4. 侧边栏
            sidebar: [
        {
          label: '企业/集团',
          autogenerate: { directory: 'company' },
        },
        {
          label: '种族/文明',
          autogenerate: { directory: 'ethnicity' },
        },
        {
          label: '历史/战役',
          autogenerate: { directory: 'history' },
        },
        {
          label: '国家/政体',
          autogenerate: { directory: 'nation' },
        },
        {
          label: '物理',
          autogenerate: { directory: 'physics' },
        },
        {
          label: '星球',
          autogenerate: { directory: 'planet' },
        },
        {
          label: '舰船',
          autogenerate: { directory: 'ship' },
        },
      ],
    }),
  ],
});
