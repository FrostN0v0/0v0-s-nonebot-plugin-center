# Author: FrostN_0V0
# Date  : 2022/4/27 10:45
import json,requests
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message,MessageSegment,GroupMessageEvent
from nonebot import require
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import nonebot
global_config = nonebot.get_driver().config
nonebot.logger.info("global_config:{}".format(global_config))
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler
gpbt = on_command("gpbt", aliases=set(['狗屁不通']), priority=1)
@gpbt.handle()
async def _(event:GroupMessageEvent):
    get_msg = event.get_plaintext()
    msg_list = get_msg.split(" ")
    msg=msg_list[1]
    num=msg_list[2]
    url = f"https://api.iyk0.com/gpbt/?msg={msg}&num={num}"
    req = requests
    txt = req.get(url).text
    send = json.loads(txt)["data"]
    await gpbt.send(MessageSegment.text(send))
