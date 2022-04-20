# Author: FrostN_0V0
# Date  : 2022/4/12 21:01
import requests
import httpx
import random
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
fox = on_command("fox", aliases=set(['来只狐娘', '嘤']), priority=1)


@fox.handle()
async def handle( event: Event):
    at_ = "[CQ:at,qq={}]".format(event.get_user_id())
    async with httpx.AsyncClient() as client:
        r = random.randint(1, 679)
        weburl = "https://www.adorable0v0.top/api/image/%s%s" % (r, '.jpg')
        cqimg = f"[CQ:image,file=1.{weburl.split('.')[1]},url={weburl}]"
        await fox.send(Message(cqimg))
