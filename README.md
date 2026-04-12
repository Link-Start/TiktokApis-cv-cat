# TikTok Reverse API

一个精简后的 TikTok Web 逆向接口项目，只保留 `api` 和 `ws` 相关能力。

## 功能概览

- TikTok Web 接口签名
  - `X-Bogus` 生成
- 用户与主页接口
  - 用户主页信息
  - 用户主页原始 HTML
  - 用户公开视频列表
- 直播相关接口
  - 直播间基础信息
  - 直播间在线观众榜
  - 直播间用户信息
  - 直播搜索
- 评论接口
  - 指定作品评论列表
- 私信 WebSocket
  - 建立 TikTok IM WebSocket 连接
  - 接收私信事件
  - 发送普通私信
  - 发送直播间分享消息

## 当前保留目录

```text
.
├─api
│  ├─tiktok.py
│  └─tiktok_chat.py
├─static
│  ├─tiktok.js
│  ├─Tiktok_Request.proto
│  ├─Tiktok_Request_pb2.py
│  ├─package.json
│  └─package-lock.json
├─utils
│  └─dy_utils.py
└─README.md
```

## 环境要求

- Python 3.9+
- Node.js 18+

## 安装

先安装 Python 依赖：

```bash
pip install requests beautifulsoup4 loguru websocket-client protobuf protobuf3_to_dict blackboxprotobuf PyExecJS
```

再安装 JS 运行依赖：

```bash
cd static
npm install
```

## Cookie 说明

本项目依赖你自己浏览器登录后的 TikTok Cookie。

建议至少确保 Cookie 中包含这些关键字段：

- `msToken`
- `s_v_web_id`
- `ttwid`
- `multi_sids` 或当前账号相关会话字段
- `sessionid` / `sid_tt`

不同接口对 Cookie 完整度要求不同，私信 WebSocket 对登录态要求更高。

## API 用法

### 1. 基础接口

```python
from api.tiktok import TiktokAPI

cookies_str = "你的完整 cookie"
api = TiktokAPI()

user_info = api.get_user_info("https://www.tiktok.com/@username", cookies_str)
print(user_info)

live_info = api.get_live_room_info("https://www.tiktok.com/@username/live", cookies_str)
print(live_info)

search_res = api.search_live_room("game", 0, cookies_str)
print(search_res)
```

### 2. 直播间观众榜

```python
from api.tiktok import TiktokAPI

cookies_str = "你的完整 cookie"
api = TiktokAPI()

user_id, sec_uid, unique_id, room_id, status, live_url = api.get_live_room_info(
    "https://www.tiktok.com/@username/live",
    cookies_str,
)

rank_list = api.get_webcast_rank_list(live_url, user_id, room_id, cookies_str)
print(rank_list)
```

### 3. 私信 WebSocket

```python
import threading
from api.tiktok_chat import TiktokSendMsgWs

cookies_str = "你的完整 cookie"
client = TiktokSendMsgWs(cookies_str)

threading.Thread(target=client.start_ws, daemon=True).start()
```

发送私信示例：

```python
from api.tiktok_chat import TiktokSendMsgWs

cookies_str = "你的完整 cookie"
client = TiktokSendMsgWs(cookies_str)

toid = "目标用户 id"
client.send_message(toid, "hello")
```

发送直播分享消息示例：

```python
from api.tiktok_chat import TiktokSendMsgWs

cookies_str = "你的完整 cookie"
client = TiktokSendMsgWs(cookies_str)

toid = "目标用户 id"
client.send_live_message(toid, "https://www.tiktok.com/@anchor/live")
```

## 主要文件说明

### `api/tiktok.py`

封装 TikTok Web 侧 HTTP 接口，包括：

- 用户主页信息
- 直播间信息
- 直播榜单
- 评论列表
- 直播搜索
- Web IM 所需的部分辅助接口

### `api/tiktok_chat.py`

封装 TikTok 私信 WebSocket 连接与消息收发逻辑，包括：

- 建链参数生成
- 心跳维持
- 私信事件解析
- 普通消息发送
- 直播分享消息发送


## 免责声明

本项目仅用于学习、研究和接口分析。请遵守目标平台服务条款与当地法律法规，不要用于违法违规用途。
