import hashlib
import time
import urllib.parse
from typing import Union, Dict, Any
import requests
import re
import json
import execjs
import urllib.request
import random
import os
import sys
import urllib.parse
import urllib.request
import configparser
import subprocess
import threading
import logging
import datetime
import time
import json
import re
import shutil
import signal

no_proxy_handler = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(no_proxy_handler)


def get_douyin_stream_data(url: str, cookies: Union[str, None] = None) -> Dict[str, Any]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'https://live.douyin.com/',
        'Cookie': 'ttwid=1%7CB1qls3GdnZhUov9o2NxOMxxYS2ff6OSvEWbv0ytbES4%7C1680522049%7C280d802d6d478e3e78d0c807f7c487e7ffec0ae4e5fdd6a0fe74c3c6af149511; my_rd=1; passport_csrf_token=3ab34460fa656183fccfb904b16ff742; passport_csrf_token_default=3ab34460fa656183fccfb904b16ff742; d_ticket=9f562383ac0547d0b561904513229d76c9c21; n_mh=hvnJEQ4Q5eiH74-84kTFUyv4VK8xtSrpRZG1AhCeFNI; store-region=cn-fj; store-region-src=uid; LOGIN_STATUS=1; __security_server_data_status=1; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; pwa2=%223%7C0%7C3%7C0%22; download_guide=%223%2F20230729%2F0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.6%7D; strategyABtestKey=%221690824679.923%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A150%7D%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1691443863751%2C%22type%22%3Anull%7D; home_can_add_dy_2_desktop=%221%22; __live_version__=%221.1.1.2169%22; device_web_cpu_core=8; device_web_memory_size=8; xgplayer_user_id=346045893336; csrf_session_id=2e00356b5cd8544d17a0e66484946f28; odin_tt=724eb4dd23bc6ffaed9a1571ac4c757ef597768a70c75fef695b95845b7ffcd8b1524278c2ac31c2587996d058e03414595f0a4e856c53bd0d5e5f56dc6d82e24004dc77773e6b83ced6f80f1bb70627; __ac_nonce=064caded4009deafd8b89; __ac_signature=_02B4Z6wo00f01HLUuwwAAIDBh6tRkVLvBQBy9L-AAHiHf7; ttcid=2e9619ebbb8449eaa3d5a42d8ce88ec835; webcast_leading_last_show_time=1691016922379; webcast_leading_total_show_times=1; webcast_local_quality=sd; live_can_add_dy_2_desktop=%221%22; msToken=1JDHnVPw_9yTvzIrwb7cQj8dCMNOoesXbA_IooV8cezcOdpe4pzusZE7NB7tZn9TBXPr0ylxmv-KMs5rqbNUBHP4P7VBFUu0ZAht_BEylqrLpzgt3y5ne_38hXDOX8o=; msToken=jV_yeN1IQKUd9PlNtpL7k5vthGKcHo0dEh_QPUQhr8G3cuYv-Jbb4NnIxGDmhVOkZOCSihNpA2kvYtHiTW25XNNX_yrsv5FN8O6zm3qmCIXcEe0LywLn7oBO2gITEeg=; tt_scid=mYfqpfbDjqXrIGJuQ7q-DlQJfUSG51qG.KUdzztuGP83OjuVLXnQHjsz-BRHRJu4e986'
    }
    if cookies:
        headers['Cookie'] = cookies

    try:
        # 使用更底层的urllib内置库，防止开启代理时导致的抖音录制SSL 443报错
        req = urllib.request.Request(url, headers=headers)
        response = opener.open(req, timeout=15)
        html_str = response.read().decode('utf-8')
        match_json_str = re.search(r'(\{\\"state\\":.*?)]\\n"]\)', html_str)
        if not match_json_str:
            match_json_str = re.search(r'(\{\\"common\\":.*?)]\\n"]\)</script><div hidden', html_str)
        json_str = match_json_str.group(1)
        cleaned_string = json_str.replace('\\', '').replace(r'u0026', r'&')
        room_store = re.search('"roomStore":(.*?),"linkmicStore"', cleaned_string, re.S).group(1)
        anchor_name = re.search('"nickname":"(.*?)","avatar_thumb', room_store, re.S).group(1)
        room_store = room_store.split(',"has_commerce_goods"')[0] + '}}}'
        json_data = json.loads(room_store)['roomInfo']['room']
        json_data['anchor_name'] = anchor_name
        return json_data

    except Exception as e:
        print(f'失败地址：{url} 准备切换解析方法{e}')
        web_rid = re.match('https://live.douyin.com/(\d+)', url).group(1)
        headers['Cookie'] = 'sessionid=73d300f837f261eaa8ffc69d50162700'
        url2 = f'https://live.douyin.com/webcast/room/web/enter/?aid=6383&app_name=douyin_web&live_id=1&web_rid={web_rid}'
        req = urllib.request.Request(url2, headers=headers)
        response = opener.open(req, timeout=15)
        json_str = response.read().decode('utf-8')
        json_data = json.loads(json_str)['data']
        room_data = json_data['data'][0]
        room_data['anchor_name'] = json_data['user']['nickname']
        return room_data


def get_yy_stream_data(url: str, cookies: Union[str, None] = None) -> Dict[str, Any]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'https://www.yy.com/',
        'Cookie': 'hd_newui=0.2103068903976506; hdjs_session_id=0.4929014850884579; hdjs_session_time=1694004002636; hiido_ui=0.923076230899782'
    }
    if cookies:
        headers['Cookie'] = cookies

    req = urllib.request.Request(url, headers=headers)
    response = opener.open(req, timeout=15)
    html_str = response.read().decode('utf-8')
    anchor_name = re.search('nick: "(.*?)",\n\s+logo', html_str).group(1)
    cid = re.search('sid : "(.*?)",\n\s+ssid', html_str, re.S).group(1)

    data = '{"head":{"seq":1701869217590,"appidstr":"0","bidstr":"121","cidstr":"' + cid + '","sidstr":"' + cid + '","uid64":0,"client_type":108,"client_ver":"5.17.0","stream_sys_ver":1,"app":"yylive_web","playersdk_ver":"5.17.0","thundersdk_ver":"0","streamsdk_ver":"5.17.0"},"client_attribute":{"client":"web","model":"web0","cpu":"","graphics_card":"","os":"chrome","osversion":"0","vsdk_version":"","app_identify":"","app_version":"","business":"","width":"1920","height":"1080","scale":"","client_type":8,"h265":0},"avp_parameter":{"version":1,"client_type":8,"service_type":0,"imsi":0,"send_time":1701869217,"line_seq":-1,"gear":4,"ssl":1,"stream_format":0}}'
    data_bytes = data.encode('utf-8')
    url2 = f'https://stream-manager.yy.com/v3/channel/streams?uid=0&cid={cid}&sid={cid}&appid=0&sequence=1701869217590&encode=json'
    req = urllib.request.Request(url2, data=data_bytes, headers=headers)
    response = opener.open(req, timeout=15)
    json_str = response.read().decode('utf-8')
    json_data = json.loads(json_str)
    json_data['anchor_name'] = anchor_name
    return json_data


def get_douyin_stream_url(json_data: dict, video_quality: str) -> dict:
    # TODO: 获取抖音直播源地址

    anchor_name = json_data.get('anchor_name', None)

    result = {
        "anchor_name": anchor_name,
        "is_live": False,
    }

    status = json_data.get("status", 4)  # 直播状态 2 是正在直播、4 是未开播

    if status == 2:
        stream_url = json_data['stream_url']
        flv_url_list = stream_url['flv_pull_url']
        m3u8_url_list = stream_url['hls_pull_url_map']

        # video_qualities = {
        #     "原画": "FULL_HD1",
        #     "蓝光": "FULL_HD1",
        #     "超清": "HD1",
        #     "高清": "SD1",
        #     "标清": "SD2",
        # }

        quality_list: list = list(m3u8_url_list.keys())
        while len(quality_list) < 4:
            quality_list.append(quality_list[-1])
        video_qualities = {"原画": 0, "蓝光": 0, "超清": 1, "高清": 2, "标清": 3}
        quality_index = video_qualities.get(video_quality)
        quality_key = quality_list[quality_index]
        m3u8_url = m3u8_url_list.get(quality_key)
        flv_url = flv_url_list.get(quality_key)

        result['m3u8_url'] = m3u8_url
        result['flv_url'] = flv_url
        result['is_live'] = True
        result['record_url'] = m3u8_url  # 使用 m3u8 链接进行录制

    return result


def get_yy_stream_url(json_data: dict) -> dict:
    anchor_name = json_data.get('anchor_name', '')
    result = {
        "anchor_name": anchor_name,
        "is_live": False,
    }
    
    if 'avp_info_res' in json_data:
        stream_line_addr = json_data['avp_info_res']['stream_line_addr']
        
        # 获取最后一个键的值
        cdn_info = list(stream_line_addr.values())[0]
        
        flv_url = cdn_info['cdn_info']['url']  # 清晰度暂时默认高清
        result['flv_url'] = flv_url
        result['is_live'] = True
        result['record_url'] = flv_url
    
    return result


def extract_original_urls(m3u_file_path):
    original_urls = []
    with open(m3u_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(" # Link:"):
                url = line.strip().split(' ', 2)[2]
                original_urls.append(url)
    return original_urls

def update_stream_info(url):
    # 伪代码，需要根据实际情况实现
    stream_info = None
    if "yy.com" in url:
        stream_data = get_yy_stream_data(url)
        stream_info = get_yy_stream_url(stream_data)  
    elif "douyin.com" in url:
        stream_data = get_douyin_stream_data(url)
        stream_info = get_douyin_stream_url(stream_data, "原画")  
    else:
        print("不支持的平台")
    return stream_info


def replace_old_addresses(m3u_file_path):
    original_urls = extract_original_urls(m3u_file_path)
    updated_streams = []
    for url in original_urls:
        try:
            stream_info = update_stream_info(url)
            if stream_info:
                # 确保直播源信息格式正确，并附加 # Link: 注释行，同时移除末尾可能的多余换行符
                formatted_stream_info = format_stream_info_to_m3u(stream_info).rstrip() + '\n # Link: ' + url + '\n'
                updated_streams.append(formatted_stream_info)
        except Exception as e:
            print(f"当前直播间关闭中或提取错误，已跳过更新，URL: {url}, 错误信息: {e}")
            continue  # 发生异常时跳过当前直播源，继续处理下一个
    
    with open(m3u_file_path, 'r', encoding='utf-8') as file:
        original_content = file.readlines()
    
    if original_content and original_content[-1].strip() == '':
        original_content.pop()
    if original_content and not original_content[-1].endswith('\n'):
        original_content.append('\n')

    updated_content = original_content + updated_streams
    
    with open(m3u_file_path, 'w', encoding='utf-8') as file:
        file.writelines(updated_content)

    print("直播源更新完成。")


def delete_duplicated_streams(m3u_file_path):
    with open(m3u_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    blocks = []
    current_block = []
    for i, line in enumerate(lines):
        line = line.rstrip('\n')  # 移除行尾的换行符以统一处理
        if line.startswith('#EXTINF:'):
            if current_block:  # 开始新的信息块前，保存当前信息块
                blocks.append(current_block)
                current_block = []
        current_block.append((i, line))
        if line.startswith(' # Link:'):
            current_block.append((i, line))
            blocks.append(current_block)  # 结束当前信息块，准备开始新的信息块
            current_block = []

    if current_block:  # 添加最后一个信息块（如果存在）
        blocks.append(current_block)

    link_dict = {}
    lines_to_delete = set()
    for block in blocks:
        link_line = [line for i, line in block if line.startswith(' # Link:')]
        if link_line:
            link = link_line[-1]  # 取最后一个 # Link: 以处理可能的重复
            if link in link_dict:
                # 如果找到重复的 # Link:，标记旧的信息块的所有行为删除
                lines_to_delete.update(i for i, _ in link_dict[link])
            # 无论是否找到重复，都更新字典为当前信息块
            link_dict[link] = block

    updated_lines = [line for i, line in enumerate(lines) if i not in lines_to_delete]

    # 写入更新后的内容
    with open(m3u_file_path, 'w', encoding='utf-8') as file:
        for line in updated_lines:
        # 移除行首尾的空白字符后检查是否为空字符串
            if line.strip():
                file.write(line.rstrip() + '\n')  # 使用rstrip()移除尾随空白字符，然后添加换行符

    print("删除操作完成。更新后的直播源信息已写入。")


def update_imported_urls(m3u_file_path, urls_to_update):
    original_urls = extract_original_urls(m3u_file_path)
    updated_streams = []
    for url in original_urls:
        if url not in urls_to_update:
            continue  # 如果 URL 不在需要更新的列表中，则跳过
        try:
            stream_info = update_stream_info(url)
            if stream_info:
                formatted_stream_info = format_stream_info_to_m3u(stream_info).rstrip() + '\n # Link: ' + url + '\n'
                updated_streams.append(formatted_stream_info)
        except Exception as e:
            print(f"当前直播间关闭中或提取错误，已跳过更新，URL: {url}, 错误信息: {e}")
            continue
    
    # 更新文件内容的逻辑保持不变
    with open(m3u_file_path, 'r', encoding='utf-8') as file:
        original_content = file.readlines()
    
    if original_content and original_content[-1].strip() == '':
        original_content.pop()
    if original_content and not original_content[-1].endswith('\n'):
        original_content.append('\n')

    updated_content = original_content + updated_streams
    
    with open(m3u_file_path, 'w', encoding='utf-8') as file:
        file.writelines(updated_content)

    print("直播源更新完成。")



def extract_streams(m3u_url, start_keyword, end_keyword):
    try:
        response = requests.get(m3u_url)
        response.raise_for_status()

        lines = response.text.split('\n')
        extracted_lines = []
        extract = False

        for line in lines:
            if start_keyword in line:
                extract = True
            if extract:
                extracted_lines.append(line)
            if end_keyword in line and extract:
                # Add the line containing end_keyword and the next line (URL)
                if lines.index(line) + 1 < len(lines):
                    extracted_lines.append(lines[lines.index(line) + 1])
                break

        return extracted_lines
    except requests.RequestException as e:
        print(f"获取 M3U 文件出错: {e}")
        return []



def save_to_m3u_file(lines, output_path, mode='a'):
    def add_extm3u_if_needed(file_content):
        if not file_content.startswith('#EXTM3U'):
            return '#EXTM3U\n' + file_content
        return file_content

    file_content = ''
    # 如果是追加模式，先读取现有内容
    if mode == 'a' and os.path.exists(output_path):
        with open(output_path, 'r') as file:
            file_content = file.read()

    # 检查并添加#EXTM3U头部（如果需要）
    file_content = add_extm3u_if_needed(file_content)

    # 确保在追加新行之前文件内容（如果有的话）以换行符结束
    if file_content and not file_content.endswith('\n'):
        file_content += '\n'

    # 追加新行到文件内容
    new_content = '\n'.join(lines)
    if new_content and not new_content.endswith('\n'):
        new_content += '\n'  # 确保新内容以换行符结束
    file_content += new_content

    # 重写文件
    with open(output_path, 'w') as file:
        file.write(file_content)

    print(f"文件已保存为 {output_path}")







def save_user_choices(output_path, new_urls_and_keyword_pairs, operation_type):
    file_path = '/root/iptv/user_choices.json'  # 使用绝对路径
    existing_choices = load_user_choices() or {'urls_and_keywords': []}

    existing_urls_and_keywords = existing_choices.get('urls_and_keywords', [])
    updated_urls_and_keywords = existing_urls_and_keywords + new_urls_and_keyword_pairs

    existing_choices['urls_and_keywords'] = updated_urls_and_keywords

    with open(file_path, 'w') as file:
        json.dump(existing_choices, file, ensure_ascii=False, indent=4)


def load_user_choices():
    file_path = '/root/iptv/user_choices.json'  # 使用绝对路径
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read().strip()
                if not content:  # 文件为空
                    return {'urls_and_keywords': []}  # 返回一个包含空列表的默认字典
                return json.loads(content)  # 解析并返回 JSON 数据
        else:
            return {'urls_and_keywords': []}  # 文件不存在，返回默认字典
    except json.JSONDecodeError:
        print("无法解析 user_choices.json 文件。")
        return {'urls_and_keywords': []}  # 解析错误时返回默认字典


def compare_and_update(existing_lines, new_lines):
    # 去除空行和首行的 #EXTM3U
    existing_lines = [line.strip() for line in existing_lines if line.strip() and line.strip() != "#EXTM3U"]
    new_lines = [line.strip() for line in new_lines if line.strip()]

    # 创建映射，键为流的描述，值为URL
    def create_stream_map(lines):
        stream_map = {}
        for i in range(0, len(lines), 2):
            if i+1 < len(lines):
                stream_map[lines[i]] = lines[i+1]
        return stream_map

    existing_map = create_stream_map(existing_lines)
    new_map = create_stream_map(new_lines)

    # 检测更新
    updated = False
    for desc, url in new_map.items():
        if desc not in existing_map or existing_map[desc] != url:
            updated = True
            # print(f"新增或变更的流: {desc} -> {url}")

    for desc, url in existing_map.items():
        if desc not in new_map:
            updated = True
            # print(f"已移除的流: {desc} -> {url}")

    if updated:
        print("检测到更新。")
        return True
    else:
        print("没有检测到更新。")
        return False


def remove_user_streams_from_m3u(m3u_path, urls_and_keyword_pairs):
    # 读取.m3u文件的所有行
    with open(m3u_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 需要保留的行初始化为空列表
    lines_to_keep = []

    # 当前是否在删除区间内
    in_deletion_range = False

    # 对每一行进行迭代
    i = 0
    while i < len(lines):
        line = lines[i]

        # 检查是否为开始删除的标识符
        if any(start_keyword in line for _, keywords in urls_and_keyword_pairs for start_keyword, _ in keywords):
            in_deletion_range = True  # 开始删除区间
        
        # 如果不在删除区间，则将行添加到保留列表
        if not in_deletion_range:
            lines_to_keep.append(line)
        
        # 检查是否为结束删除的标识符
        if in_deletion_range and any(end_keyword in line for _, keywords in urls_and_keyword_pairs for _, end_keyword in keywords):
            in_deletion_range = False  # 结束删除区间，跳过此行和下一行（URL行）
            i += 1  # 额外增加索引以跳过URL行
        
        i += 1  # 常规索引增加

    # 将需要保留的内容写回.m3u文件
    with open(m3u_path, 'w', encoding='utf-8') as file:
        file.writelines(lines_to_keep)


def update_streams(m3u_file_path):
    user_choices = load_user_choices()
    urls_and_keyword_pairs = user_choices.get('urls_and_keywords', [])

    # 首先，从M3U文件中删除用户之前选择的流信息
    remove_user_streams_from_m3u(m3u_file_path, urls_and_keyword_pairs)

    # 初始化一个列表来存储所有重新提取的流信息
    all_extracted_streams = []

    # 遍历每个URL和关键词对，提取数据流信息
    for url, keywords in urls_and_keyword_pairs:
        for start_keyword, end_keyword in keywords:
            extracted_streams = extract_streams(url, start_keyword, end_keyword)
            all_extracted_streams.extend(extracted_streams)
    
    # 将更新后的流信息追加到M3U文件
    save_to_m3u_file(all_extracted_streams, m3u_file_path, 'a')
    print("关键字添加的直播源已更新。")


def format_stream_info_to_m3u(stream_info):
    anchor_name = stream_info.get('anchor_name', 'Unknown')
    # 尝试获取M3U8 URL，如果不存在，则尝试获取FLV URL
    stream_url = stream_info.get('m3u8_url') or stream_info.get('flv_url', '')
    
    if stream_url:  # 确保 stream_url 存在，否则可能返回空字符串或错误信息
        # 加入group-title="自媒体"
        m3u_entry = f"#EXTINF:-1 group-title=\"自媒体\", {anchor_name}\n{stream_url}\n"
        return m3u_entry
    else:
        return ""  # 如果没有有效的stream_url，则返回空字符串


def user_input_for_url_and_keywords():
    urls_and_keyword_pairs = []
    while True:
        m3u_url = input("请输入 M3U 文件的 URL: ")
        keyword_pairs = []
        while True:
            start_keyword = input("请输入起始关键词: ")
            end_keyword = input("请输入结束关键词: ")
            keyword_pairs.append((start_keyword, end_keyword))

            more_keywords = input("是否继续输入关键词范围？(1. 是  2. 否): ")
            if more_keywords != '1':
                break

        urls_and_keyword_pairs.append((m3u_url, keyword_pairs))

        more_urls = input("是否输入另一个直播源地址？(1. 是  2. 否): ")
        if more_urls != '1':
            break

    return urls_and_keyword_pairs

def install_nginx():
    """安装 Nginx 并设置监听端口为8008"""
    try:
        print("正在安装 Nginx...")
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "nginx"], check=True)
        print("Nginx 安装成功。")
        
        # 修改Nginx配置文件以监听端口8008
        print("正在设置Nginx监听端口为8008...")
        with open("/etc/nginx/sites-available/default", "r") as file:
            config = file.read()
        
        # 假设默认配置使用80端口，我们将其替换为8008
        config = config.replace("listen 80;", "listen 8008;")
        
        with open("/etc/nginx/sites-available/default", "w") as file:
            file.write(config)
        
        # 重启Nginx以应用配置更改
        subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
        print("Nginx已更新至监听端口8008。")
        
    except Exception as e:
        print(f"安装或配置Nginx时出错: {e}")

def create_empty_m3u_file(m3u_file_path):
    try:
        with open(m3u_file_path, "w") as file:
            pass  # 创建一个空文件
        print(f".m3u 文件已创建在 {m3u_file_path}")
    except Exception as e:
        print(f"创建 .m3u 文件时出错: {e}")


def configure_nginx_for_m3u():
    nginx_config = """
server {
    listen 80;
    server_name _;

    location /live.m3u {
        alias /var/www/html/live.m3u;
    }
}
"""
    try:
        with open("/etc/nginx/sites-available/default", "w") as file:
            file.write(nginx_config)
        subprocess.run(["sudo", "nginx", "-t"], check=True)
        subprocess.run(["sudo", "systemctl", "reload", "nginx"], check=True)
        print("Nginx 配置已更新，.m3u 文件可通过以下地址访问: http://您的服务器IP或域名/live.m3u")
    except subprocess.CalledProcessError as e:
        print(f"Nginx 配置测试失败，请检查错误: {e}")
    except Exception as e:
        print(f"写入 Nginx 配置时发生错误: {e}")


M3U_FILE_PATH = "/var/www/html/live.m3u"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def main():
    while True:
        print(f"{YELLOW}\nM3U 直播源提取器{RESET}")
        print(f"{GREEN}0. 退出{RESET}")
        print(f"{GREEN}1. 生成直播源文件及可访链接{RESET}")
        print(f"{GREEN}2. 为直播源文件添加新直播源{RESET}")
        print(f"{GREEN}3. 检查更新关键词所获直播源{RESET}")
        print(f"{GREEN}4. 从自媒体平台获取新直播源{RESET}")
        print(f"{RED}抖音url示例：https://live.douyin.com/745964462470{RESET}")
        print(f"{RED}YY url示例：https://www.yy.com/22490906/22490906{RESET}")



        choice = input(f"{YELLOW}请选择操作 (输入数字，0退出): {RESET}")

        if choice == '0':
            print(f"{RED}退出程序。{RESET}")
            break
        elif choice == '1':
            install_nginx()
            create_empty_m3u_file(M3U_FILE_PATH)  # 使用常量路径创建文件
            configure_nginx_for_m3u()
            server_ip_or_name = input("请输入您的服务器IP或域名，用于生成直播源链接: ")
            print(f"{GREEN}直播源链接地址已生成。地址为: http://{server_ip_or_name}:8008/live.m3u{RESET}")


        elif choice == '2':
            urls_and_keyword_pairs = user_input_for_url_and_keywords()
            all_extracted_streams = []
            for url, keywords in urls_and_keyword_pairs:
                for start_keyword, end_keyword in keywords:
                    extracted_streams = extract_streams(url, start_keyword, end_keyword)
                    all_extracted_streams.extend(extracted_streams)
            save_to_m3u_file(all_extracted_streams, M3U_FILE_PATH, 'a')
            save_user_choices(M3U_FILE_PATH, urls_and_keyword_pairs, 'add')
            print(f"{GREEN}新直播源已添加。{RESET}")

        elif choice == '3':
            update_streams(M3U_FILE_PATH)
            print(f"{GREEN}关键字添加直播源已更新{RESET}")
        elif choice == '4':
            url = input("请输入直播平台的URL: ")
            stream_info = None

            if "yy.com" in url:
                stream_data = get_yy_stream_data(url)
                stream_info = get_yy_stream_url(stream_data)  
            elif "douyin.com" in url:
                stream_data = get_douyin_stream_data(url)
                stream_info = get_douyin_stream_url(stream_data, "原画")  
            else:
                print("不支持的平台")


            if stream_info:
                # 成功获取到直播源后，保存用户输入的链接到文件
                formatted_stream_info = format_stream_info_to_m3u(stream_info) + f' # Link: {url}'
                stream_info_lines = formatted_stream_info.splitlines()  # 拆分为行的列表
                save_to_m3u_file(stream_info_lines, M3U_FILE_PATH, mode='a')
                print(f"{GREEN}自媒体平台直播源已更新。{RESET}")
            else:
                print(f"{RED}未能获取直播源信息。{RESET}")


# ...之前的函数定义...

if __name__ == "__main__":
    main()

