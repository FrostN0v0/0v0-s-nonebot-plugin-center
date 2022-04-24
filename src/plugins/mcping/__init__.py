# Author: FrostN_0V0
# Date  : 2022/4/24 22:01
import base64
from pathlib import Path
from nonebot import on_command
from mcstatus import JavaServer
from nonebot.adapters.onebot.v11 import Message,MessageSegment,GroupMessageEvent
from nonebot import require
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import nonebot
global_config = nonebot.get_driver().config
nonebot.logger.info("global_config:{}".format(global_config))
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler
mcp = on_command("mc", aliases=set(['查询服务器', '#mc']), priority=1)
@mcp.handle()
async def ser(event:GroupMessageEvent):
    get_msg = event.get_plaintext()
    msg_list = get_msg.split(" ")
    if len(msg_list) > 1:
        ip = msg_list[-1]
    else:
        ip =get_msg[:-2]
    msg = await get_info(ip)
    await mcp.finish(msg)
async def get_info(ip:str)->MessageSegment:
    server = JavaServer.lookup(ip)
    status = server.status()
    #获取并处理服务器图标，缓存到本地发送
    a = status.favicon
    b = a.split(',')[1]
    img_data = base64.b64decode(b)
    with open('C:/sk/data/mcicon/icon.png', 'wb+') as f:
        f.write(img_data)
    max = status.raw['players']['max']
    min = status.raw['players']['online']
    version = status.version.name
    ping_data = status.latency.real
    ping = round(ping_data,2)
    player = f"服务器在线玩家：{min}/{max}\n"
    vs = f"服务器版本：{version}\n"
    ping_msg = f"Ping:{ping}MS\n"
    server_icon = Path('C:/sk/data/mcicon/icon.png')
    msg = MessageSegment.image(server_icon)
    msg+= MessageSegment.text(player)
    msg+= MessageSegment.text(vs)
    msg+= MessageSegment.text(ping_msg)
    #获取并处理MOTD
    def analyze_date(data, result, ls=[]):
        if isinstance(data, dict):
            for k, v in data.items():
                analyze_date(v, result + ".get(\"%s\")" % str(k))
        elif isinstance(data, list):
            for i in range(len(data)):
                analyze_date(data[i], result + "[%s]" % i)
            else:
                remix = ''
                for j in range(len(data)):
                    real_data = data[j]['text']
                    remix = remix + real_data
                ls.append(remix)
                return ls
    try:
        raw_dict = status.raw['description']['extra']
        data_return = analyze_date(raw_dict, result="motd")
        color_motd = f"服务器信息:\n{data_return[0]}\n"
        msg+= MessageSegment.text(color_motd)
    except:
        motd = status.raw['description']['text']
        v_motd = f"服务器信息：\n{motd}\n"
        msg+= MessageSegment.text(v_motd)
    #获取在线玩家列表
    try:
        try:
            query=server.query()
            query_name = query.players.names
            pln = ''
            for n in range(len(query_name)):
                pln += f'{query_name[n]}\n'
                pln_list = f"在线玩家：\n{pln}"
            msg+=MessageSegment.text(pln_list)
        except:
            if status.players.sample is not None:
                player_name = sorted([player.name for player in status.players.sample])
            else:
                player_name = []
            pln = ''
            for n in range(len(player_name)):
                pln += f'{player_name[n]}\n'
                pln_list = f"在线玩家：\n{pln}"
            msg+=MessageSegment.text(pln_list)
    except:
            error="获取玩家列表失败"
            print(error)
    return msg