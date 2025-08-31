import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "Rimetool",
  description: "医键通词库转换工具 - 一款强大的Rime输入法词库转换工具",
  base: '/rimetool/',
  lastUpdated: true,
  lang: 'zh-CN',
  
  head: [
    ['link', { rel: 'icon', href: '/rimetool/favicon.ico' }]
  ],

  themeConfig: {
    logo: '/logo.png',
    
    nav: [
      { text: '首页', link: '/' },
      { text: '安装', link: '/install' },
      { text: '快速上手', link: '/quickstart' },
      { text: 'Web 工具', link: '/web-tool' },
      { text: 'API 文档', link: '/api' }
    ],

    sidebar: [
      {
        text: '开始使用',
        items: [
          { text: '简介', link: '/' },
          { text: '安装', link: '/install' },
          { text: '快速上手', link: '/quickstart' }
        ]
      },
      {
        text: '功能特性',
        items: [
          { text: 'Web 在线工具', link: '/web-tool' },
          { text: '命令行工具', link: '/cli' },
          { text: 'API 接口', link: '/api' }
        ]
      },
      {
        text: '进阶使用',
        items: [
          { text: '支持的格式', link: '/formats' },
          { text: '自定义转换', link: '/custom' },
          { text: '开发指南', link: '/development' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/B-Beginner/rimetool' }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2024-present rimetool contributors'
    },

    editLink: {
      pattern: 'https://github.com/B-Beginner/rimetool/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页'
    },

    lastUpdatedText: '最后更新',
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },

    darkModeSwitchLabel: '外观',
    sidebarMenuLabel: '菜单',
    returnToTopLabel: '返回顶部',

    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: '搜索文档',
                buttonAriaLabel: '搜索文档'
              },
              modal: {
                noResultsText: '无法找到相关结果',
                resetButtonTitle: '清除查询条件',
                footer: {
                  selectText: '选择',
                  navigateText: '切换'
                }
              }
            }
          }
        }
      }
    }
  }
})