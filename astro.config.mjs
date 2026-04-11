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
      // 1. 语言锁定
      defaultLocale: 'zh-cn',
      locales: {
        root: {
          label: '简体中文',
          lang: 'zh-cn',
        },
      },
      // 2. 彻底移除所有按钮和链接
      pagination: false,    // 删掉底部的“下一页”
      lastUpdated: false,   // 删掉最后更新时间
      credits: false,       // 删掉页脚 Starlight 标志
      // 3. 社交链接也清空
      social: {},
      // 4. 侧边栏
      sidebar: [
        {
          label: '星体百科',
          autogenerate: { directory: 'planet' }, 
        },
      ],
    }),
  ],
});
