import re
import sys
import time
import json
import random
import base64
import urllib
import uuid
from os import path
import static.Tiktok_Request_pb2 as Tiktok_Request
import requests
requests.packages.urllib3.disable_warnings()
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs

if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS
else:
    basedir = path.dirname(__file__)


try:
    node_modules = path.join(basedir, 'static', 'node_modules')
    tiktok_path = path.join(basedir, 'static', 'tiktok.js')
    tiktok_js = execjs.compile(open(tiktok_path, 'r', encoding='gb18030').read(), cwd=node_modules)
except:
    node_modules = path.join(basedir, '..', 'static', 'node_modules')
    tiktok_path = path.join(basedir, '..', 'static', 'tiktok.js')
    tiktok_js = execjs.compile(open(tiktok_path, 'r', encoding='gb18030').read(), cwd=node_modules)


def trans_cookies(cookies_str):
    cookies = {
        # "douyin.com": "",
    }
    for i in cookies_str.split("; "):
        try:
            cookies[i.split('=')[0]] = '='.join(i.split('=')[1:])
        except:
            continue
    # cookies = {i.split('=')[0]: '='.join(i.split('=')[1:]) for i in cookies_str.split('; ')}
    return cookies


def generate_Xbogus(query):
    Xbogus = tiktok_js.call('getXBogus', query)
    return Xbogus


def generate_signature():
    signature = tiktok_js.call()
    return signature

def splice_params(params):
    splice_url = ''
    for key, value in params.items():
        splice_url += f"{key}={urllib.parse.quote(value, safe='?&=+$')}&"
    return splice_url[:-1]

def generate_request_headers(cookies_str):
    return {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': cookies_str,
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.tiktok.com/@gunvw',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

def generate_html_headers(referer):
    return {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": referer,
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
def generate_requests(url, params, cookies_str):
    splice_params_str = splice_params(params)
    params['X-Bogus'] = generate_Xbogus(splice_params_str)
    params['_signature'] = ''
    splice_params_str = splice_params(params)
    url = url + '?' + splice_params_str
    return url, generate_request_headers(cookies_str)


def send_live_room_message(self, myid, toid, message):
    uuid_ = uuid.uuid4()
    seq_id = random.randint(10100, 10300)
    request = Tiktok_Request.Request()
    request.cmd = 100
    request.sequence_id = seq_id
    request.sdk_version = "1.2.3"
    request.token = ""
    request.refer = 3
    request.inbox_type = 0
    request.build_number = "831c301:master"
    request.body.send_message_body.conversation_id = f"0:1:{toid}:{myid}"
    request.body.send_message_body.conversation_type = 1
    request.body.send_message_body.conversation_short_id = 7471574364992045000
    request.body.send_message_body.content = message

    ext = request.body.send_message_body.ext.add()
    ext.key = "s:mentioned_users"
    ext.value = ""
    ext = request.body.send_message_body.ext.add()
    ext.key = "s:client_message_id"
    ext.value = str(uuid_)

    request.body.send_message_body.message_type = 1021
    request.body.send_message_body.ticket = "deprecated"
    request.body.send_message_body.client_message_id = str(uuid_)
    request.device_id = "7460856262408259088"
    request.device_platform = "web"
    request.headers.append(
        Tiktok_Request.ExtValue(key='aid', value="1988")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='app_name', value="tiktok_web")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='channel', value="web")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='device_platform', value="web_pc")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='device_id', value="7460856262408259088")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='region', value="JP")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='priority_region', value="US")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='os', value="windows")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='referer', value="https://www.tiktok.com/messages?lang=zh-Hans")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='root_referer', value="")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='cookie_enabled', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='screen_width', value="2560")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='screen_height', value="1440")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_language', value="zh-CN")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_platform', value="Win32")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_name', value="Mozilla")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_version', value="5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_online', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='verifyFp', value=self.verifyFp)
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='app_language', value="zh-Hans")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='webcast_language', value="zh-Hans")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='tz_name', value="Asia/Shanghai")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='is_page_visible', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='focus_state', value="false")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='is_fullscreen', value="false")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='history_len', value="9")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='user_is_login', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='data_collection_enabled', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='from_appID', value="1988")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='user_agent', value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='Web-Sdk-Ms-Token', value=self.msToken)
    )
    request.auth_type = 1
    frame = Tiktok_Request.Frame()
    frame.seqid = seq_id
    frame.logid = int(time.time() * 1000)
    frame.service = 5
    frame.method = 1
    frame.headers.append(
        Tiktok_Request.ExtValue(key='X-Bogus', value="RK3+A9FfXHV0yral")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='aid', value="1988")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='app_name', value="tiktok_web")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='channel', value="web")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='device_platform', value="web_pc")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='device_id', value="7460856262408259088")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='region', value="JP")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='priority_region', value="US")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='os', value="windows")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='referer', value="https://www.tiktok.com/messages?lang=zh-Hans")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='root_referer', value="")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='cookie_enabled', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='screen_width', value="2560")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='screen_height', value="1440")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_language', value="zh-CN")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_platform', value="Win32")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_name', value="Mozilla")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_version', value="5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_online', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='verifyFp', value=self.verifyFp)
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='app_language', value="zh-Hans")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='webcast_language', value="zh-Hans")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='tz_name', value="Asia/Shanghai")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='is_page_visible', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='focus_state', value="false")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='is_fullscreen', value="false")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='history_len', value="9")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='user_is_login', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='data_collection_enabled', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='from_appID', value="1988")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='user_agent', value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='Web-Sdk-Ms-Token', value=self.msToken)
    )

    frame.payload_type = 'pb'
    frame.payload = request.SerializeToString()
    self.ws.send(frame.SerializeToString(), opcode=0x2)


def send_common_message(self, myid, toid, message):
    uuid_ = uuid.uuid4()
    seq_id = random.randint(10100, 10300)
    request = Tiktok_Request.Request()
    request.cmd = 100
    request.sequence_id = seq_id
    request.sdk_version = "1.2.3"
    request.token = ""
    request.refer = 3
    request.inbox_type = 0
    request.build_number = "831c301:master"
    request.body.send_message_body.conversation_id = f"0:1:{toid}:{myid}"
    request.body.send_message_body.conversation_type = 1
    request.body.send_message_body.conversation_short_id = 7471574364992045000
    request.body.send_message_body.content = "{\"aweType\":0,\"text\":\"%s\"}" % message

    ext = request.body.send_message_body.ext.add()
    ext.key = "s:mentioned_users"
    ext.value = ""
    ext = request.body.send_message_body.ext.add()
    ext.key = "s:client_message_id"
    ext.value = str(uuid_)

    request.body.send_message_body.message_type = 7
    request.body.send_message_body.ticket = "deprecated"
    request.body.send_message_body.client_message_id = str(uuid_)
    request.device_id = "7460856262408259088"
    request.device_platform = "web"
    request.headers.append(
        Tiktok_Request.ExtValue(key='aid', value="1988")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='app_name', value="tiktok_web")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='channel', value="web")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='device_platform', value="web_pc")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='device_id', value="7460856262408259088")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='region', value="JP")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='priority_region', value="US")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='os', value="windows")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='referer', value="https://www.tiktok.com/messages?lang=zh-Hans")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='root_referer', value="")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='cookie_enabled', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='screen_width', value="2560")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='screen_height', value="1440")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_language', value="zh-CN")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_platform', value="Win32")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_name', value="Mozilla")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_version', value="5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_online', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='verifyFp', value=self.verifyFp)
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='app_language', value="zh-Hans")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='webcast_language', value="zh-Hans")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='tz_name', value="Asia/Shanghai")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='is_page_visible', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='focus_state', value="false")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='is_fullscreen', value="false")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='history_len', value="9")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='user_is_login', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='data_collection_enabled', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='from_appID', value="1988")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='user_agent', value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='Web-Sdk-Ms-Token', value=self.msToken)
    )
    request.auth_type = 1
    frame = Tiktok_Request.Frame()
    frame.seqid = seq_id
    frame.logid = int(time.time() * 1000)
    frame.service = 5
    frame.method = 1

    frame.headers.append(
        Tiktok_Request.ExtValue(key='X-Bogus', value="RK3+A9FfXHV0yral")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='aid', value="1988")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='app_name', value="tiktok_web")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='channel', value="web")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='device_platform', value="web_pc")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='device_id', value="7460856262408259088")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='region', value="JP")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='priority_region', value="US")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='os', value="windows")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='referer', value="https://www.tiktok.com/messages?lang=zh-Hans")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='root_referer', value="")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='cookie_enabled', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='screen_width', value="2560")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='screen_height', value="1440")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_language', value="zh-CN")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_platform', value="Win32")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_name', value="Mozilla")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_version', value="5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_online', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='verifyFp', value=self.verifyFp)
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='app_language', value="zh-Hans")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='webcast_language', value="zh-Hans")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='tz_name', value="Asia/Shanghai")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='is_page_visible', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='focus_state', value="false")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='is_fullscreen', value="false")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='history_len', value="9")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='user_is_login', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='data_collection_enabled', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='from_appID', value="1988")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='user_agent', value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='Web-Sdk-Ms-Token', value=self.msToken)
    )

    frame.payload_type = 'pb'
    frame.payload = request.SerializeToString()
    self.ws.send(frame.SerializeToString(), opcode=0x2)

def send_strangerconversation_msg(self):
    seq_id = random.randint(10100, 10300)
    request = Tiktok_Request.Request()
    request.cmd = 1001
    request.sequence_id = seq_id
    request.sdk_version = "1.2.3"
    request.token = ""
    request.refer = 3
    request.inbox_type = 0
    request.build_number = "831c301:master"
    request.body.get_stranger_conversation_list_body.cursor = 0
    request.body.get_stranger_conversation_list_body.count = 1
    request.body.get_stranger_conversation_list_body.show_total_unread = True

    request.device_id = "7460856262408259088"
    request.device_platform = "web"
    request.headers.append(
        Tiktok_Request.ExtValue(key='aid', value="1988")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='app_name', value="tiktok_web")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='channel', value="web")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='device_platform', value="web_pc")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='device_id', value="7460856262408259088")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='region', value="JP")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='priority_region', value="US")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='os', value="windows")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='referer', value="https://www.tiktok.com/messages?lang=zh-Hans")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='root_referer', value="")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='cookie_enabled', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='screen_width', value="2560")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='screen_height', value="1440")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_language', value="zh-CN")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_platform', value="Win32")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_name', value="Mozilla")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_version', value="5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='browser_online', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='verifyFp', value=self.verifyFp)
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='app_language', value="zh-Hans")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='webcast_language', value="zh-Hans")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='tz_name', value="Asia/Shanghai")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='is_page_visible', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='focus_state', value="false")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='is_fullscreen', value="false")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='history_len', value="9")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='user_is_login', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='data_collection_enabled', value="true")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='from_appID', value="1988")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='user_agent', value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    )
    request.headers.append(
        Tiktok_Request.ExtValue(key='Web-Sdk-Ms-Token', value=self.msToken)
    )
    request.auth_type = 1
    frame = Tiktok_Request.Frame()
    frame.seqid = seq_id
    frame.logid = int(time.time() * 1000)
    frame.service = 5
    frame.method = 1
    frame.headers.append(
        Tiktok_Request.ExtValue(key='aid', value="1988")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='app_name', value="tiktok_web")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='channel', value="web")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='device_platform', value="web_pc")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='device_id', value="7460856262408259088")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='region', value="JP")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='priority_region', value="US")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='os', value="windows")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='referer', value="https://www.tiktok.com/messages?lang=zh-Hans")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='root_referer', value="")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='cookie_enabled', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='screen_width', value="2560")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='screen_height', value="1440")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_language', value="zh-CN")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_platform', value="Win32")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_name', value="Mozilla")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_version', value="5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='browser_online', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='verifyFp', value=self.verifyFp)
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='app_language', value="zh-Hans")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='webcast_language', value="zh-Hans")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='tz_name', value="Asia/Shanghai")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='is_page_visible', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='focus_state', value="false")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='is_fullscreen', value="false")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='history_len', value="9")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='user_is_login', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='data_collection_enabled', value="true")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='from_appID', value="1988")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='user_agent', value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    )
    frame.headers.append(
        Tiktok_Request.ExtValue(key='Web-Sdk-Ms-Token', value=self.msToken)
    )

    frame.payload_type = 'pb'
    frame.payload = request.SerializeToString()
    self.ws.send(frame.SerializeToString(), opcode=0x2)
