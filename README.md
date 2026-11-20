# Evp Remote 官网

面向 Windows 客户端用户的中文 VitePress 站点。使用 Node.js 22.13 或以上版本和 npm。

```sh
npm ci
npm run dev
npm run build
npm run preview
```

构建输出在 `docs/.vitepress/dist/`，可部署到静态站点根路径。项目仓库固定为 `https://github.com/Evanpatchouli/evp-remote`。

根目录 `.env` 提供官方 Windows 安装包地址。在 `.env.local` 设置 `VITE_CLIENT_DOWNLOAD_URL` 可覆盖默认值，也可在构建环境设置同名变量。必须是完整的 HTTP(S) 下载地址，不能放密钥。修改后重启开发服务或重新构建。地址为空或无效时，页面显示未配置提示，不会生成空链接。

Windows 原生客户端 0.3.1 及其构建源码按 GPL-3.0-or-later 授权，可商用和转售。第三方组件各自遵循其许可证。未纳入此次授权的其他软件、官网代码、文档与素材继续适用原条款。授权范围见[版权页](docs/copyright.md)，纯文本入口为 [license.txt](docs/public/license.txt)。

教程截图取自原生客户端；首页屏幕内的冰蓝纹理是装饰图，并非客户端界面。

## GitHub Actions CI

本站仓库发布 Release（`release.published`）时会运行 **Site CI**。也可在 **Actions → Site CI → Run workflow** 选择分支并手动运行（`workflow_dispatch`）。这是工作流的全部触发条件。

在仓库 **Settings → Pages → Build and deployment** 中将 Source 设为 **GitHub Actions**。工作流在 Ubuntu 24.04 上使用 Node.js 24 构建和检查站点，然后发布到 GitHub Pages。构建时根据 Pages 地址设置站点基础路径；也可在运行记录的 **Artifacts** 区域下载 `evp-remote-site`。环境 `github-pages` 的保护规则须允许所选分支或 Release 标签部署。
