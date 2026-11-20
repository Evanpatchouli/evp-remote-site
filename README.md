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

版权页的 `docs/public/license.txt` 是主项目 `LICENSE` 的副本；主仓条款变化时应同步。教程截图取自原生客户端；首页屏幕内的冰蓝纹理是装饰图，并非客户端界面。

## GitHub Actions CI

本站仓库发布 Release（`release.published`）时会运行 **Site CI**。也可在 **Actions → Site CI → Run workflow** 选择分支并手动运行（`workflow_dispatch`）。这是工作流的全部触发条件。

工作流在 Ubuntu 24.04 上使用 Node.js 24，依次执行 `npm ci` 和 `npm run build`。随后检查首页、版权页和指南页面，以及页面引用的本地脚本、样式表、图片和站点所需的品牌图、纹理与许可文件。检查通过后，可在该次运行的 **Artifacts** 区域下载 `evp-remote-site`，解压即为静态站点根目录。工作流到上传产物为止。
