import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vitepress'

export default defineConfig({
  base: process.env.SITE_BASE || '/',
  lang: 'zh-CN', title: 'Evp Remote', description: 'Windows 远程桌面客户端：临时协助与个人设备远控。',
  vite: { envDir: fileURLToPath(new URL('../../', import.meta.url)) },
  head: [['link', { rel: 'icon', href: `${process.env.SITE_BASE || '/'}brand.png` }]],
  themeConfig: {
    logo: '/brand.png',
    nav: [{ text: '使用指南', link: '/guide/start', activeMatch: '/guide/' }, { text: '版权说明', link: '/copyright' }],
    socialLinks: [{ icon: 'github', link: 'https://github.com/Evanpatchouli/evp-remote' }],
    sidebar: { '/guide/': [
      { text: '开始使用', items: [{ text: '下载与首次设置', link: '/guide/start' }] },
      { text: '临时协助', items: [{ text: '共享这台电脑', link: '/guide/share' }, { text: '用邀请码连接', link: '/guide/join' }, { text: '操作与结束会话', link: '/guide/session' }] },
      { text: '我的设备', items: [{ text: '配对两台电脑', link: '/guide/pair' }, { text: '连接已配对的电脑', link: '/guide/devices' }, { text: '关闭远控与移除配对', link: '/guide/revoke' }] },
      { text: '客户端维护', items: [{ text: '检查与安装更新', link: '/guide/update' }] }
    ] },
    search: { provider: 'local', options: { translations: { button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' }, modal: { noResultsText: '没有找到相关内容', resetButtonTitle: '清除搜索', footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' } } } } },
    outline: { label: '本页内容', level: [2, 3] }, docFooter: { prev: '上一篇', next: '下一篇' },
    sidebarMenuLabel: '文档目录', returnToTopLabel: '回到顶部', darkModeSwitchLabel: '外观', skipToContentLabel: '跳到正文',
    footer: { message: `Windows 原生客户端 0.3.1 可商用、可转售 · <a href="${process.env.SITE_BASE || '/'}copyright.html">版权与许可</a>` }
  }
})
