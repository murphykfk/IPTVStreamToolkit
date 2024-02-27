# IPTVStreamToolkit

这是一个用于高效管理和更新IPTV流的工具集合。此工具包旨在简化提取M3U播放列表和更新直播流链接的过程，确保您的IPTV体验流畅且保持最新。它非常适合IPTV爱好者和媒体服务器管理员使用。

## 特性

- 生成用户自己的，可访问的直播源文档和地址。
- 根据起止关键词，自动提取指定url文档内的直播源。
- 记录用户选择，在直播源失效时，一键更新（如果直播源提供者已更新）。
- 通过直播间链接获取直播源地址，加入到.m3u文件中（目前支持抖音、YY平台）。
- 设置定时任务，当直播间开启时，更新这些自媒体直播源。

## 开始使用

要使用此工具包，您可以通过以下命令下载并运行`IPTVAssistantSetup.sh`脚本：

```bash
curl -o IPTVAssistantSetup.sh https://raw.githubusercontent.com/murphykfk/IPTVStreamToolkit/main/IPTVAssistantSetup.sh && bash IPTVAssistantSetup.sh

## 配置
在自己的Debian系统中进行测试，未测试其他系统，作者对代码知识了解不多，可自行尝试。

## 贡献
如果您有任何建议或想要贡献代码，请随时提交 Pull Request 或创建 Issue。

## 致谢
特别感谢 ihmily 的 DouyinLiveRecorder 项目，自媒体直播源的提取代码来自于此项目。

## 许可
本项目采用MIT许可证。更多细节请查看 LICENSE 文件。