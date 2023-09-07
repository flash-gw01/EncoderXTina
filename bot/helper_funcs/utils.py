
# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import os, asyncio, pyrogram, psutil, platform, time
from bot import data
from bot.plugins.incoming_message_fn import incoming_compress_message_f
from pyrogram.types import Message
from psutil import disk_usage, cpu_percent, virtual_memory, Process as psprocess


def checkKey(dict, key):
  if key in dict.keys():
    return True
  else:
    return False

def hbs(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

async def on_task_complete():
    del data[0]
    if len(data) > 0:
      await add_task(data[0])

async def add_task(message: Message):
    try:
        os.system('rm -rf /app/downloads/*')
        await incoming_compress_message_f(message)
    except Exception as e:
        LOGGER.info(e)  
    await on_task_complete()

async def sysinfo(e):
    cpuUsage = psutil.cpu_percent(interval=0.5)
    ram_stats = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    dl_size = psutil.net_io_counters().bytes_recv
    ul_size = psutil.net_io_counters().bytes_sent
    message = await e.reply_text(f"<b>╭「 💠 BOT STATISTICS 」</b>\n"
                                 f"<b>│</b>\n"
                                 f"<b>├💾 Total Disk Space : {psutil._common.bytes2human(disk.total)}</b>\n"
                                 f"<b>├📀 Total Used Space : {psutil._common.bytes2human(disk.used)}</b>\n"
                                 f"<b>├💿 Total Free Space : {psutil._common.bytes2human(disk.free)}</b>\n"
                                 f"<b>├🔺 Total Upload : {psutil._common.bytes2human(ul_size)}</b>\n"
                                 f"<b>├🔻 Total Download : {psutil._common.bytes2human(dl_size)}</b>\n"
                                 f"<b>├🖥 CPU : {cpuUsage}%</b>\n"
                                 f"<b>├⚙️ RAM : {int(ram_stats.percent)}%</b>\n"
                                 f"<b>╰💿 DISK : {int(disk.percent)}%</b>")
    
