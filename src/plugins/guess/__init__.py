# Author: FrostN_0V0
# Date  : 2022/4/25 19:44
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message,MessageSegment,GroupMessageEvent
from selenium.webdriver.chrome.options import Options
from nonebot.params import Arg, CommandArg, ArgPlainText
from selenium import webdriver
import os,time
from pathlib import Path
from nonebot import require
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import nonebot
opt = Options()
#opt.add_argument('--headless')
#opt.add_argument('--disable-gpu')
#opt.add_argument('--window-size=1366,768')
global_config = nonebot.get_driver().config
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler
chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver


guess_operator = on_command("guess_operator",aliases=set(['猜干员']),priority=1)
guess = on_command("guess", aliases=set(['猜']),priority=1)
again = on_command("again",aliases=set(['再试一次']),priority=1)
shut = on_command("stop", aliases=set(['关闭进程']), priority=1)

@guess_operator.handle()
async def csh(event:GroupMessageEvent):
    browser = webdriver.Chrome(chromedriver, chrome_options=opt)
    browser.get("http://akg.saki.cc")
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="modal233"]/div[1]').click()
    csh_msg = "进程已经启动，如果发现多进程并行的情况，请执行[关闭进程]指令。\n输入[猜+干员名]进行猜干员\n有8次机会，输入[再试一次]进行下一轮猜干员"
    await guess_operator.send(message=csh_msg)
    @guess.handle()
    async def handle(event:GroupMessageEvent):
        get_msg = event.get_plaintext()
        msg_list = get_msg.split(" ")
        if len(msg_list) > 1:
            operator = msg_list[-1]
        else:
            operator = get_msg[1:]
        input = browser.find_element_by_id('guess')
        input.send_keys(operator)
        browser.find_element_by_xpath('//*[@id="magic-wrapper"]/div/div/form/button').click()
        browser.find_element_by_xpath('//*[@id="magic-wrapper"]/div/div/div[5]').screenshot('C:/sk/src/plugins/guess/guess.png')
        pic = Path('C:/sk/src/plugins/guess/guess.png')

        await guess.send(MessageSegment.image((pic)))
    @again.handle()
    async def handle(event:GroupMessageEvent):
        browser.find_element_by_xpath('//*[@id="magic-wrapper"]/div/div/a').click()
        again_msg = "已进行重置操作，如果仍未结束，请完成本轮猜干员，再次执行此命令"
        await again.send(message=again_msg)
    @shut.handle()
    async def stop(event: GroupMessageEvent):
        browser.quit()
        shut_msg = "进程已关闭。"
        await guess_operator.send(message=shut_msg)