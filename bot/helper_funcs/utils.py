
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

async def test(event):
    try:
        zylern = "speedtest --simple"
        fetch = await asyncrunapp(
            zylern,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await fetch.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())
        await message.reply_text("**" + result + "**")
    except FileNotFoundError:
        await message.reply_text("**Install speedtest-cli**")

async def sysinfo(e):
    cpuUsage = psutil.cpu_percent(interval=0.5)
    ram_stats = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    dl_size = psutil.net_io_counters().bytes_recv
    ul_size = psutil.net_io_counters().bytes_sent
    message = await e.reply_text(f"<u><b>SYSTEM STATS 🧮</b></u>\n\n"
                                 f"<b>💾 Total Disk Space:</b> {psutil._common.bytes2human(disk.total)}B\n"
                                 f"<b>Used:</b> {psutil._common.bytes2human(disk.used)}B | <b>Free:</b> {psutil._common.bytes2human(disk.free)}B\n\n"
                                 f"<b>🔺 Total Upload:</b> {psutil._common.bytes2human(ul_size)}B\n"
                                 f"<b>🔻 Total Download:</b> {psutil._common.bytes2human(dl_size)}B\n\n"
                                 f"<b>🎮 Total Ram Space:</b> {psutil._common.bytes2human(ram_stats.total)}B\n"
                                 f"<b>Used:</b>{psutil._common.bytes2human(ram_stats.total)}B | <b>Free:</b> {psutil._common.bytes2human(ram_stats.available)}B\n\n"
                                 f"<b>🖥 CPU:</b> {cpuUsage}%\n"
                                 f"<b>🎮 RAM:</b> {int(ram_stats.percent)}%\n"
                                 f"<b>💿 DISK:</b> {int(disk.percent)}%")
    
