#!/bin/bash

# 指定下载目录
TARGET_DIR="/root/iptv"

# 检查目录是否存在，如果不存在，则创建
if [ ! -d "$TARGET_DIR" ]; then
  mkdir -p "$TARGET_DIR"
fi

# 切换到目标目录
cd "$TARGET_DIR"

# 下载脚本到指定目录
curl -s -O https://raw.githubusercontent.com/murphykfk/IPTVStreamToolkit/main/m3u_extractor.py
curl -s -O https://raw.githubusercontent.com/murphykfk/IPTVStreamToolkit/main/update_live_streams.py

# 安装Python模块execjs，如果尚未安装
pip3 install PyExecJS

# 设置Cron任务以每5分钟执行update_live_streams.py脚本
(crontab -l 2>/dev/null; echo "*/5 * * * * python3 $TARGET_DIR/update_live_streams.py") | crontab -

# 将别名添加到.bashrc，使其永久有效
echo "alias iptv='python3 $TARGET_DIR/m3u_extractor.py'" >> ~/.bashrc

# 重新加载.bashrc以立即应用更改
source ~/.bashrc

# 提示用户
echo "别名 'iptv' 已设置。请重启shell会话，并在会话中通过输入 'iptv' 来执行直播源管理脚本。"
