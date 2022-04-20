from nonebot import get_driver
from pathlib import Path
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.rule import to_me
from selenium.webdriver.chrome.options import Options
from nonebot.adapters import Bot, Event
from nonebot import require
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .config import Config
from selenium import webdriver
import nonebot
import os
global_config = nonebot.get_driver().config
nonebot.logger.info("global_config:{}".format(global_config))
plugin_config = Config(**global_config.dict())
nonebot.logger.info("plugin_config:{}".format(plugin_config))
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler

opt = Options()
opt.add_argument("--headless")
opt.add_argument('--disable-gpu')
chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver,options=opt)
today = on_command("fj", aliases=set(['番剧', '今日番剧']), priority=1)
tomorrow = on_command("mrfj",aliases=set(['明日番剧']),priority=1)
week = on_command("bzfj",aliases=set(['本周番剧']),priority=1)
@scheduler.scheduled_job('cron',hour=0,minute=30)
async def _():
    driver.set_window_size(1920, 7200)
    driver.get('https://mikanani.me/')
    today = driver.find_element_by_xpath('//*[@id="sk-body"]/div[1]')
    tomorrow = driver.find_element_by_xpath('//*[@id="sk-body"]/div[7]')
    week = driver.find_element_by_xpath('//*[@id="sk-body"]')
    today.screenshot('C:/sk/data/anime/today.png')
    tomorrow.screenshot('C:/sk/data/anime/tomorrow.png')
    week.screenshot('C:/sk/data/anime/week.png')
    driver.quit()
    print('download ok')
@today.handle()
async def handle(event: Event):
    td_img = Path('C:/sk/data/anime/today.png')
    await today.send(MessageSegment.image(td_img))
@tomorrow.handle()
async def handle(event: Event):
    tm_img = Path('C:/sk/data/anime/tomorrow.png')
    await tomorrow.send(MessageSegment.image(tm_img))
@week.handle()
async def handle(event: Event):
    wk_img = Path('C:/sk/data/anime/week.png')
    await tomorrow.send(MessageSegment.image(wk_img))
@scheduler.scheduled_job('cron',hour=8,minute=30)
async def __():
    for qq_group in plugin_config.anime_qq_groups:
        daily_img = Path('C:/sk/data/anime/today.png')
        msg = MessageSegment.text("今日番剧推送完成喵~\n")
        msg+= MessageSegment.image(daily_img)
        await nonebot.get_bot().send_group_msg(group_id=qq_group, message=msg)
    for qq in plugin_config.anime_qq_friends:
        await nonebot.get_bot().send_private_msg(user_id=qq, message=msg)
