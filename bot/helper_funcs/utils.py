
# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import os, asyncio, pyrogram, psutil, platform, time
from speedtest import Speedtest
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
    message = await e.reply_text(f"<u><b>SYSTEM STATS 🧮</b></u>\n\n"
                                 f"<b>💾 Total Disk Space:</b> {psutil._common.bytes2human(disk.total)}B\n"
                                 f"<b>Used:</b> {psutil._common.bytes2human(disk.used)}B | <b>Free:</b> {psutil._common.bytes2human(disk.free)}B\n\n"
                                 f"<b>🔺 Total Upload:</b> {psutil._common.bytes2human(ul_size)}B\n"
                                 f"<b>🔻 Total Download:</b> {psutil._common.bytes2human(dl_size)}B\n\n"
                                 f"<b>🎮 Total Ram Space:</b> {psutil._common.bytes2human(ram_stats.total)}B\n"
                                 f"<b>Used:</b>{psutil._common.bytes2human(ram_stats.used)}B | <b>Free:</b> {psutil._common.bytes2human(ram_stats.available)}B\n\n"
                                 f"<b>🖥 CPU:</b> {cpuUsage}%\n"
                                 f"<b>🎮 RAM:</b> {int(ram_stats.percent)}%\n"
                                 f"<b>💿 DISK:</b> {int(disk.percent)}%")

def speed_convert(size, byte=True):
    """Hi human, you can't read bytes?"""
    if not byte: size = size / 8 # byte or bit ?
    power = 2 ** 10
    zero = 0
    units = {0: "B/s", 1: "KB/s", 2: "MB/s", 3: "GB/s", 4: "TB/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

async def speedtest(update, context):
    speed = sendMessage("Running Speed Test. Wait about 20 secs.", context.bot, update.message)
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
 message = await e.reply_text(f"<b>Server</b>"
                              f"<b>Name:</b> <code>{result['server']['name']}</code>"
                              f"<b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>"
                              f"<b>Sponsor:</b> <code>{result['server']['sponsor']}</code>"
                              f"<b>ISP:</b> <code>{result['client']['isp']}</code>"

                              f"<b>SpeedTest Results</b>"
                              f"<b>Upload:</b> <code>{speed_convert(result['upload'], False)}</code>"
                              f"<b>Download:</b>  <code>{speed_convert(result['download'], False)}</code>"
                              f"<b>ISP Rating:</b> <code>{result['client']['isprating']}</code>")

    
