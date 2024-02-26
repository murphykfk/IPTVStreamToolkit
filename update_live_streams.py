from typing import Dict, Any, Union
import json
import urllib.request
import os
LAST_UPDATES_FILE = '/root/iptv/last_updates.json'
from datetime import datetime, timedelta

# 假设 m3u_extractor 包含必要的函数
from m3u_extractor import get_douyin_stream_data, get_yy_stream_data, update_imported_urls, delete_duplicated_streams

M3U_FILE_PATH = '/var/www/html/live.m3u'

def load_last_updates():
    """从JSON文件加载最后更新的时间信息"""
    if os.path.exists(LAST_UPDATES_FILE):
        with open(LAST_UPDATES_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_last_updates(last_updates):
    """将最后更新的时间信息保存到JSON文件"""
    with open(LAST_UPDATES_FILE, 'w') as file:
        json.dump(last_updates, file, indent=4, default=str)

def should_update(url: str, last_updates) -> bool:
    """检查自上次更新以来是否已经过去了2小时"""
    now = datetime.now()
    if url in last_updates:
        last_update = datetime.fromisoformat(last_updates[url])
        if now - last_update < timedelta(hours=2):
            return False
    return True

def check_and_update_live_status():
    urls = parse_m3u_file(M3U_FILE_PATH)
    last_updates = load_last_updates()
    urls_to_update = []  # 新增列表以收集需要更新的URLs

    for url in urls:
        if should_update(url, last_updates):
            live_status = get_live_status(url)
            if live_status.get('is_live'):
                urls_to_update.append(url)  # 将符合条件的URL添加到列表中
                last_updates[url] = datetime.now().isoformat()

    if urls_to_update:  # 如果有URL需要更新，则调用update_imported_urls函数
        update_imported_urls(M3U_FILE_PATH, urls_to_update)
        delete_duplicated_streams(M3U_FILE_PATH)
        save_last_updates(last_updates)  # 保存最后更新的时间信息

    if not urls_to_update:
        print("没有直播源需要更新。")
    else:
        print(f"更新了 {len(urls_to_update)} 个直播源。")


def get_live_status(url: str, cookies: Union[str, None] = None) -> Dict[str, Any]:
    """根据URL判断直播状态，区分抖音或YY的直播间"""
    if "douyin" in url:
        data = get_douyin_stream_data(url, cookies)
        status = data.get("status", 4)  # 直播状态 2 是正在直播、4 是未开播
        return {"is_live": status == 2, "anchor_name": data.get("anchor_name", "")}
    elif "yy" in url:
        data = get_yy_stream_data(url, cookies)
        is_live = 'avp_info_res' in data and 'stream_line_addr' in data['avp_info_res'] and list(data['avp_info_res']['stream_line_addr'].values())[0]
        return {"is_live": is_live, "anchor_name": data.get("anchor_name", "")}
    else:
        return {"is_live": False}

def parse_m3u_file(file_path):
    """解析.m3u文件来获取直播间的URLs"""
    urls = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith("# Link:"):
                url = stripped_line.replace("# Link: ", "")
                urls.append(url)
    except Exception as e:
        print(f"Error parsing .m3u file: {e}")
    return urls

if __name__ == "__main__":
    check_and_update_live_status()
