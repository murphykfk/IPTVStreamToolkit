#!/bin/bash

# 首先检查并安装 sudo 如果需要
if ! command -v sudo &> /dev/null; then
    echo "sudo could not be found, attempting to install..."
    apt-get update && apt-get install -y sudo
    if [ $? -ne 0 ]; then
        echo "Failed to install sudo, exiting."
        exit 1
    fi
    echo "sudo has been successfully installed."
else
    echo "sudo is already installed."
fi

# 首先检查并安装python3-pip如果需要
if ! command -v pip3 &> /dev/null; then
    echo "pip3 could not be found, attempting to install python3-pip..."
    apt update && apt install -y python3-pip
    if [ $? -ne 0 ]; then
        echo "Failed to install python3-pip, exiting."
        exit 1
    fi
fi

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
CRON_JOB="*/5 * * * * python3 $TARGET_DIR/update_live_streams.py"

# 检查Cron任务是否已存在
if ! crontab -l | grep -Fq "$CRON_JOB"; then
  (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
fi


# 将别名添加到.bashrc，使其永久有效
ALIAS_CMD="alias iptv='python3 $TARGET_DIR/m3u_extractor.py'"

# 检查别名是否已存在
if ! grep -Fxq "$ALIAS_CMD" ~/.bashrc; then
  echo "$ALIAS_CMD" >> ~/.bashrc
fi

# 重新加载.bashrc以立即应用更改
source ~/.bashrc

# 提示用户
echo "别名 'iptv' 已设置。请重启shell会话，并在会话中通过输入 'iptv' 来执行直播源管理脚本。"
