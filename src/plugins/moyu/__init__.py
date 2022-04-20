# Author: FrostN_0V0
# Date  : 2022/4/12 21:01
import requests
from pathlib import Path
import httpx
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.rule import to_me
from selenium.webdriver.chrome.options import Options
from nonebot.adapters import Bot, Event
from selenium import webdriver
import os
from .config import Config
from nonebot import require
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import nonebot
opt = Options()
opt.add_argument("--headless")
global_config = nonebot.get_driver().config
nonebot.logger.info("global_config:{}".format(global_config))
plugin_config = Config(**global_config.dict())
nonebot.logger.info("plugin_config:{}".format(plugin_config))
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler
chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver, chrome_options=opt)
moyu = on_command("moyu", aliases=set(['摸鱼', '摸鱼日历']), rule=to_me(), priority=1)


@moyu.handle()
async def handle(event: Event):
        img = Path('C:/sk/src/plugins/moyu/img/myrb.png')
        await moyu.send(MessageSegment.image(img))
@scheduler.scheduled_job('cron',hour=7,minute=30)
async def _():
    driver.get('http://d.jiek.top/vJfV')
    # 跳转到新页面
    imgurl = format(driver.current_url)
    driver.quit()
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
