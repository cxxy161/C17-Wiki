// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://cxxy161.github.io',
  base: '/C17-Wiki/', // 重点 1：确保末尾有斜杠
  integrations: [
    starlight({
      title: 'C17星区 Wiki',
      // 重点 2：对于单语言项目，去掉 locales 和 defaultLocale 配置
      // Starlight 会默认使用 root，手动写出来有时会干扰路径计算
      sidebar: [
        {
          label: '星体百科',
          autogenerate: { directory: 'planet' }, 
        },
      ],
      // 重点 3：在这里统一设置语言
      defaultLocale: 'zh-cn', 
    }),
  ],
});
