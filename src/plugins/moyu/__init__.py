# Author: FrostN_0V0
# Date  : 2022/4/27 10:01
import requests
from pathlib import Path
import json
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
from .config import Config
from nonebot import require
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import nonebot
global_config = nonebot.get_driver().config
nonebot.logger.info("global_config:{}".format(global_config))
plugin_config = Config(**global_config.dict())
nonebot.logger.info("plugin_config:{}".format(plugin_config))
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler
moyu = on_command("moyu", aliases=set(['摸鱼', '摸鱼日历']), rule=to_me(), priority=1)
update = on_command("update",aliases=set(['获取更新']),rule=to_me(),priority=1)


@moyu.handle()
async def handle(event: Event):
        img = Path('C:/sk/src/plugins/moyu/img/myrb.png')
        await moyu.send(MessageSegment.image(img))
@update.handle()
async def update(event: Event):
    req = requests
    url = "https://api.j4u.ink/proxy/remote/moyu.json"
    a = req.get(url).text
    imgurl = json.loads(a)['data']['moyu_url']
    r = requests.get(imgurl)
    with open('C:/sk/src/plugins/moyu/img/myrb.png', 'wb') as f:
        f.write(r.content)
    update_msg="download ok"
    print(update_msg)
@scheduler.scheduled_job('cron',hour=7,minute=30)
async def _():
    req = requests
    url = "https://api.j4u.ink/proxy/remote/moyu.json"
    a = req.get(url).text
    imgurl = json.loads(a)['data']['moyu_url']
    r = requests.get(imgurl)
    with open('C:/sk/src/plugins/moyu/img/myrb.png', 'wb') as f:
        f.write(r.content)
    print('download ok')
@scheduler.scheduled_job('cron',hour=8,minute=0)
async def a():
    for qq_group in plugin_config.read_qq_groups:
        img = Path('C:/sk/src/plugins/moyu/img/myrb.png')
        await nonebot.get_bot().send_group_msg(group_id=qq_group, message=MessageSegment.image(img))
    for qq in plugin_config.read_qq_friends:
        await nonebot.get_bot().send_private_msg(user_id=qq, message=MessageSegment.image(img))
