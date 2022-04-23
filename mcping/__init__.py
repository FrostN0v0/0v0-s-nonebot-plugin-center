# Author: FrostN_0V0
# Date  : 2022/4/22 22:01
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
mcp = on_command("mcp", aliases=set(['查询服务器', 'ping']), priority=1)
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
    a = status.favicon
    b = a.split(',')[1]
    img_data = base64.b64decode(b)
    # print(img_data)
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
                # print(result + "="+str(data))
                remix = ''
                for j in range(len(data)):
                    # print(data[j]['text'])
                    real_data = data[j]['text']
                    remix = remix + real_data
                # print(remix)
                # print(type(remix))
                ls.append(remix)
                # print(ls)
                return ls
    try:
        raw_dict = status.raw['description']['extra']
        data_return = analyze_date(raw_dict, result="motd")
        color_motd = f"服务器信息:\n{data_return[0]}"
        msg+= MessageSegment.text(color_motd)
        # print(raw_dict)
    except:
        motd = status.raw['description']['text']
        v_motd = f"服务器信息：\n{motd}"
        msg+= MessageSegment.text(v_motd)
        #print(v_motd)
    return msg