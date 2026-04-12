import json
import re
import time

import requests
from bs4 import BeautifulSoup

from loguru import logger
from utils.dy_utils import trans_cookies, generate_requests, generate_html_headers, generate_request_headers


class TiktokAPI:
    tiktok_url = 'https://www.tiktok.com'

    def get_user_posted(self, secUid, cursor, cookies_str):
        cookies = trans_cookies(cookies_str)
        url = self.tiktok_url + "/api/post/item_list/"
        params = {
           "WebIdLastTime": "1737115998",
           "aid": "1988",
           "app_language": "zh-Hans",
           "app_name": "tiktok_web",
           "browser_language": "zh-CN",
           "browser_name": "Mozilla",
           "browser_online": "true",
           "browser_platform": "Win32",
           "browser_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
           "channel": "tiktok_web",
           "cookie_enabled": "true",
           "count": "16",
           "coverFormat": "2",
           "cursor": cursor,
           "data_collection_enabled": "false",
           "device_id": "7460856262408259088",
           "device_platform": "web_pc",
           "focus_state": "true",
           "from_page": "user",
           "history_len": "2",
           "is_fullscreen": "false",
           "is_page_visible": "true",
           "language": "zh-Hans",
           "needPinnedItemIds": "true",
           "odinId": re.findall(r'multi_sids=(.*?)%3A', cookies_str)[0],
           "os": "windows",
           "post_item_list_request_type": "0",
           "priority_region": "",
           "referer": "",
           "region": "JP",
           "root_referer": "https://www.tiktok.com/@gunvw",
           "screen_height": "1440",
           "screen_width": "2560",
           "secUid": secUid,
           "tz_name": "Asia/Shanghai",
           "user_is_login": "false",
           "verifyFp": cookies["s_v_web_id"],
           "webcast_language": "zh-Hans",
           "msToken": cookies["msToken"],
        }
        url, headers = generate_requests(url, params, cookies_str)
        response = requests.get(url, headers=headers)
        res_json = response.json()
        return res_json

    def get_live_room_info(self, live_url, cookies_str):
        if 'vt.tiktok.com' in live_url:
            logger.info("redirect short live url")
            res = requests.get(live_url, allow_redirects=False)
            live_url = res.headers['Location']
            logger.info(f"閲嶅畾鍚戝悗鐨勭洿鎾棿閾炬帴: {live_url}")
        headers = generate_html_headers(live_url)
        cookies = trans_cookies(cookies_str)
        response = requests.get(live_url, headers=headers, cookies=cookies)
        res_text = response.text
        soup = BeautifulSoup(res_text, 'html.parser')
        script = soup.find_all('script', attrs={'id': 'SIGI_STATE'})[0]
        script_text = script.text
        script_text = script_text.replace('false', 'False').replace('true', 'True').replace('null', 'None').replace('undefined', 'None')
        ans = eval(script_text)
        try:
            user = ans['LiveRoom']['liveRoomUserInfo']['user']
            user_id, secUid, uniqueId, room_id, status = user['id'], user['secUid'], user['uniqueId'], user['roomId'], user['status']
            return user_id, secUid, uniqueId, room_id, status, live_url
        except Exception as e:
            return None

        # ans = re.findall(r'"id":"(.*?)","nickname":".*?","secUid":"(.*?)","secret":.*?,"uniqueId":"(.*?)","verified":.*?,"roomId":"(.*?)",', res_text)
        # user_id, secUid, uniqueId, room_id = ans[0]
        # return user_id, secUid, uniqueId, room_id


    def get_webcast_rank_list(self, referer, anchor_id, room_id, cookies_str):
        cookies = trans_cookies(cookies_str)
        url = "https://webcast.tiktok.com/webcast/ranklist/online_audience/"
        params = {
            "aid": "1988",
            "anchor_id": anchor_id,
            "app_language": "zh-Hans",
            "app_name": "tiktok_web",
            "browser_language": "zh-CN",
            "browser_name": "Mozilla",
            "browser_online": "true",
            "browser_platform": "Win32",
            "browser_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "channel": "tiktok_web",
            "cookie_enabled": "true",
            "data_collection_enabled": "true",
            "device_id": "7460856262408259088",
            "device_platform": "web_pc",
            "focus_state": "true",
            "from_page": "user",
            "history_len": "4",
            "is_fullscreen": "false",
            "is_page_visible": "true",
            "os": "windows",
            "priority_region": "",
            "referer": referer,
            "region": "JP",
            "room_id": room_id,
            "root_referer": "https://www.tiktok.com/@gunvw",
            "screen_height": "1440",
            "screen_width": "2560",
            "tz_name": "Asia/Shanghai",
            "user_is_login": "true",
            "verifyFp": cookies["s_v_web_id"],
            "webcast_language": "zh-Hans",
            "msToken": cookies["msToken"],
        }
        url, headers = generate_requests(url, params, cookies_str)
        response = requests.get(url, headers=headers)
        res_json = response.json()
        return res_json

    def get_user_info(self, user_url, cookies_str):
        cookies = trans_cookies(cookies_str)
        headers = generate_html_headers(user_url)
        response = requests.get(user_url, headers=headers, cookies=cookies)
        res_text = response.text
        user_info = re.findall(r'"webapp\.user-detail":(.*?),"webapp\.a-b"', res_text)[0]
        user_info = user_info.replace('false', 'False').replace('true', 'True').replace('null', 'None').replace('undefined', 'None')
        user_info = eval(user_info)
        return user_info

    def get_user_live_info(self, user_url, cookies_str, proxies=None):
        live_url = user_url + '/live'
        cookies = trans_cookies(cookies_str)
        headers = generate_html_headers(user_url)

        response = requests.get(live_url, headers=headers, cookies=cookies, proxies=proxies)
        res_text = response.text
        soup = BeautifulSoup(res_text, 'html.parser')
        script = soup.find_all('script', attrs={'id': 'SIGI_STATE'})[0]
        script_text = script.text
        user_live_info = json.loads(script_text)
        return user_live_info

    def get_user_info_and_text(self, user_url, cookies_str, proxies=None):
        cookies = trans_cookies(cookies_str)
        headers = generate_html_headers(user_url)

        response = requests.get(user_url, headers=headers, cookies=cookies, proxies=proxies)
        res_text = response.text
        user_info = re.findall(r'"webapp\.user-detail":(.*?),"webapp\.a-b"', res_text)[0]
        user_info = user_info.replace('false', 'False').replace('true', 'True').replace('null', 'None').replace('undefined', 'None')
        user_info = eval(user_info)
        return user_info, res_text

    def get_simple_user_info(self, user_id, cookies_str):
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.tiktok.com/messages?lang=zh-Hans",
            "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }
        url = "https://www.tiktok.com/tiktok/v1/im/user/profile/"
        cookies = trans_cookies(cookies_str)
        params = {
            "aid": "1988",
            "user_ids": f"[\"{user_id}\"]"
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        res_json = response.json()
        return res_json


    def get_webcast_user_info(self, target_uid, room_id, cookies_str):
        cookies = trans_cookies(cookies_str)
        url = "https://webcast.tiktok.com/webcast/user/"
        params = {
            "aid": "1988",
            "app_language": "zh-Hans",
            "app_name": "tiktok_web",
            "browser_language": "zh-CN",
            "browser_name": "Mozilla",
            "browser_online": "true",
            "browser_platform": "Win32",
            "browser_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "channel": "tiktok_web",
            "cookie_enabled": "true",
            "current_room_id": room_id,
            "data_collection_enabled": "true",
            "device_id": "7460856262408259088",
            "device_platform": "web_pc",
            "focus_state": "true",
            "from_page": "user",
            "history_len": "3",
            "is_fullscreen": "false",
            "is_page_visible": "true",
            "os": "windows",
            "owner_user_id": re.findall(r'multi_sids=(.*?)%3A', cookies_str)[0],
            "priority_region": "",
            "referer": "",
            "region": "JP",
            "screen_height": "1440",
            "screen_width": "2560",
            "target_uid": target_uid,
            "tz_name": "Asia/Shanghai",
            "user_is_login": "true",
            "verifyFp": cookies["s_v_web_id"],
            "webcast_language": "zh-Hans",
            "msToken": cookies["msToken"],
        }
        url, headers = generate_requests(url, params, cookies_str)
        response = requests.get(url, headers=headers)
        res_json = response.json()
        return res_json

    def get_wid(self, cookies_str):
        cookies = trans_cookies(cookies_str)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.tiktok.com/messages?lang=zh-Hans',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'x-pns-referrer': 'https://www.tiktok.com/messages',
            'x-web-privacy-sdk-ver': '1.0.1',
        }
        params = {
            'locale': 'zh-Hans',
            'appId': '1988',
            'theme': 'default',
            'tea': '1',
        }

        response = requests.get('https://www.tiktok.com/api/v1/web-cookie-privacy/config', params=params, cookies=cookies, headers=headers)
        res_json = response.json()
        wid = res_json['body']['consent']['wid']
        return wid
    def search_live_room(self, keyword, offset, cookies_str):
        headers = generate_request_headers(cookies_str)
        cookies = trans_cookies(cookies_str)
        url = "https://www.tiktok.com/api/search/live/full/"
        params = {
            "WebIdLastTime": "1737115998",
            "aid": "1988",
            "app_language": "zh-Hans",
            "app_name": "tiktok_web",
            "browser_language": "zh-CN",
            "browser_name": "Mozilla",
            "browser_online": "true",
            "browser_platform": "Win32",
            "browser_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "channel": "tiktok_web",
            "cookie_enabled": "true",
            "count": "20",
            "data_collection_enabled": "true",
            "device_id": "7460856262408259088",
            "device_platform": "web_pc",
            "device_type": "web_h264",
            "focus_state": "true",
            "from_page": "search",
            "history_len": "15",
            "is_fullscreen": "false",
            "is_page_visible": "true",
            "keyword": keyword,
            "odinId": re.findall(r'multi_sids=(.*?)%3A', cookies_str)[0],
            "offset": str(offset),
            "os": "windows",
            "priority_region": "",
            "referer": "https://www.tiktok.com/live",
            "region": "JP",
            "root_referer": "https://www.tiktok.com/@gunvw",
            "screen_height": "1440",
            "screen_width": "2560",
            "tz_name": "Asia/Shanghai",
            "user_is_login": "true",
            "verifyFp": cookies["s_v_web_id"],
            "web_search_code": "{\"tiktok\":{\"client_params_x\":{\"search_engine\":{\"ies_mt_user_live_video_card_use_libra\":1,\"mt_search_general_user_live_card\":1}},\"search_server\":{}}}",
            "webcast_language": "zh-Hans"
        }
        response = requests.get(url, headers=headers, params=params)
        res_json = response.json()
        return res_json

    def spider_some_comment(self, aweme_id, cookies_str):
        cookies = trans_cookies(cookies_str)
        url = "https://www.tiktok.com/api/comment/list/"
        params = {
            "WebIdLastTime": str(int(time.time())),
            "aid": "1988",
            "app_language": "ja-JP",
            "app_name": "tiktok_web",
            "aweme_id": aweme_id,
            "browser_language": "zh-CN",
            "browser_name": "Mozilla",
            "browser_online": "true",
            "browser_platform": "Win32",
            "browser_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "channel": "tiktok_web",
            "cookie_enabled": "true",
            "count": "20",
            "current_region": "JP",
            "cursor": "0",
            "data_collection_enabled": "false",
            "device_id": "7473127097071519239",
            "device_platform": "web_pc",
            "enter_from": "tiktok_web",
            "focus_state": "false",
            "fromWeb": "1",
            "from_page": "video",
            "history_len": "5",
            "is_fullscreen": "false",
            "is_non_personalized": "false",
            "is_page_visible": "true",
            "odinId": re.findall(r'multi_sids=(.*?)%3A', cookies_str)[0],
            "os": "windows",
            "priority_region": "",
            "referer": "",
            "region": "RU",
            "screen_height": "1440",
            "screen_width": "2560",
            "tz_name": "Asia/Shanghai",
            "user_is_login": "false",
            "webcast_language": "zh-Hans",
            "msToken": cookies["msToken"],
        }
        url, headers = generate_requests(url, params, cookies_str)
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        print(response.text)
        res_json = response.json()
        return res_json

