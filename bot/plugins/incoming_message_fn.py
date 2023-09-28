import datetime
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
import os, time, asyncio, json
from bot.localisation import Localisation
from bot import (
  DOWNLOAD_LOCATION, 
  AUTH_USERS,
  LOG_CHANNEL,
  UPDATES_CHANNEL,
  SESSION_NAME,
  data,
  app  
)
from bot.helper_funcs.ffmpeg import (
  convert_video,
  media_info,
  take_screen_shot
)
from bot.helper_funcs.display_progress import (
  progress_for_pyrogram,
  TimeFormatter,
  humanbytes
)

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

#from bot.helper_funcs.utils import(
#  delete_downloads
#)
os.system("wget https://telegra.ph/file/0e369e097843b0dc4b771.jpg -O thumb.jpg")

#LOGS_CHANNEL = -1001283278354
CURRENT_PROCESSES = {}
CHAT_FLOOD = {}
broadcast_ids = {}
bot = app        
async def incoming_start_message_f(bot, update):
    """/start command"""
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Localisation.START_TEXT,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('👨‍💻 Oᴡɴᴇʀ 👨‍💻', url='https://t.me/cmd_rulf')
                ]
            ]
        ),
        reply_to_message_id=update.message_id,
    )
    
async def incoming_compress_message_f(update):
  """/compress command"""
    
  isAuto = True
    #saved_file_path = video #DOWNLOAD_LOCATION + "/" + filename
    #LOGGER.info(saved_file_path)
  d_start = time.time()
  c_start = time.time()
  u_start = time.time()
  status = DOWNLOAD_LOCATION + "/status.json"
 # if not os.path.exists(status):
  sent_message = await bot.send_message(
  chat_id=update.chat.id,
  text=Localisation.DOWNLOAD_START,
  reply_to_message_id=update.message_id
              )
  chat_id = LOG_CHANNEL
  utc_now = datetime.datetime.utcnow()
  ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
  ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
  bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
  bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
  now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
  download_start = await bot.send_message(chat_id, f" **Bot Become Busy Now 🥵** ", parse_mode="markdown")
  try:
      d_start = time.time()
      status = DOWNLOAD_LOCATION + "/status.json"
      with open(status, 'w') as f:
        statusMsg = {
          'running': True,
          'message': sent_message.message_id
        }

        json.dump(statusMsg, f, indent=2)
      video = await bot.download_media(
        #message=update.reply_to_message,
        message=update,  
        #file_name=saved_file_path,
        progress=progress_for_pyrogram,
        progress_args=(
          bot,
          Localisation.DOWNLOAD_START,
          sent_message,
          d_start
        )
      )
      saved_file_path = video
      LOGGER.info(saved_file_path)  
      LOGGER.info(video)
      if( video is None ):
        try:
          await sent_message.edit_text(
            text="Dᴏᴡɴʟᴏᴀᴅ Sᴛᴏᴘᴘᴇᴅ 🛑"
          )
          chat_id = LOG_CHANNEL
          utc_now = datetime.datetime.utcnow()
          ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
          ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
          bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
          bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
          now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
          await bot.send_message(chat_id, f" **Download Stopped 🛑\nBot is Free Now.....✅** ", parse_mode="markdown")
          await download_start.delete()
        except:
          pass
       # delete_downloads()
        LOGGER.info("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴏᴘᴘᴇᴅ 🛑")
        return
  except (ValueError) as e:
      try:
        await sent_message.edit_text(
          text=str(e)
        )
      except:
          pass
      #delete_downloads()            
  try:
      await sent_message.edit_text(                
        text=Localisation.SAVED_RECVD_DOC_FILE                
      )
  except:
      pass     
  
  if os.path.exists(saved_file_path):
    downloaded_time = TimeFormatter((time.time() - d_start)*1000)
    duration, bitrate = await media_info(saved_file_path)
    if duration is None or bitrate is None:
      try:
        await sent_message.edit_text(                
          text="⚠️ Gᴇᴛᴛɪɴɢ Vɪᴅᴇᴏ Mᴇᴛᴀ Dᴀᴛᴀ Fᴀɪʟᴇᴅ ⚠️"                
        )
        chat_id = LOG_CHANNEL
        utc_now = datetime.datetime.utcnow()
        ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
        ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
        bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
        bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
        now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
        await bot.send_message(chat_id, f" **Download Failed ⚠️\nBot is Free Now.....✅** ", parse_mode="markdown")
        await download_start.delete()
      except:
          pass          
     # delete_downloads()
      return
    thumb_image_path = await take_screen_shot(
      saved_file_path,
      os.path.dirname(os.path.abspath(saved_file_path)),
      (duration / 2)
    )
    chat_id = LOG_CHANNEL
    utc_now = datetime.datetime.utcnow()
    ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
    ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
    bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
    bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
    now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
    await download_start.delete()
    compress_start = await bot.send_message(chat_id, f" **Compressing Video....🗜️** ", parse_mode="markdown")
    await sent_message.edit_text(                    
      text=Localisation.COMPRESS_START                    
    )
    c_start = time.time()
    o = await convert_video(
           video, 
           DOWNLOAD_LOCATION, 
           duration, 
           bot, 
           sent_message, 
           compress_start
         )
    compressed_time = TimeFormatter((time.time() - c_start)*1000)
    LOGGER.info(o)
    if o == 'stopped':
      return
    if o is not None:
      chat_id = LOG_CHANNEL
      utc_now = datetime.datetime.utcnow()
      ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
      ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
      bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
      bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
      now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
      await compress_start.delete()
      upload_start = await bot.send_message(chat_id, f" **Uploading Video to TG....📥** ", parse_mode="markdown")
      await sent_message.edit_text(                    
        text=Localisation.UPLOAD_START,                    
      )
      u_start = time.time()
      caption = Localisation.COMPRESS_SUCCESS.replace('{}', downloaded_time, 1).replace('{}', compressed_time, 1)
      upload = await bot.send_document(
        chat_id=update.chat.id,
        document=o,
        caption=caption,
        force_document=True,
        #duration=duration,
        thumb="thumb.jpg",
        reply_to_message_id=update.message_id,
        progress=progress_for_pyrogram,
        progress_args=(
          bot,
          Localisation.UPLOAD_START,
          sent_message,
          u_start
        )
      )
      if(upload is None):
        try:
          await sent_message.edit_text(
            text="Uᴘʟᴏᴀᴅ Sᴛᴏᴘᴘᴇᴅ 🛑" 
          )
          chat_id = LOG_CHANNEL
          utc_now = datetime.datetime.utcnow()
          ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
          ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
          bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
          bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
          now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
          await bot.send_message(chat_id, f" **Upload Stopped 🛑\nBot is Free Now.....✅** ", parse_mode="markdown")
          await upload_start.delete()
        except:
          pass
       # delete_downloads()
        return
      uploaded_time = TimeFormatter((time.time() - u_start)*1000)
      await sent_message.delete()
   #   delete_downloads()
      chat_id = LOG_CHANNEL
      utc_now = datetime.datetime.utcnow()
      ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
      ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
      bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
      bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
      now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
      await upload_start.delete()
      await bot.send_message(chat_id, f" **Upload Done.😎\nBot is Free Now.....✅** ", parse_mode="markdown")
      LOGGER.info(upload.caption);
      try:
        await upload.edit_caption(
          caption=upload.caption.replace('{}', uploaded_time)
        )
      except:
        pass
    else:
     # delete_downloads()
      try:
        await sent_message.edit_text(                    
          text="⚠️ Cᴏᴍᴘʀᴇꜱꜱɪᴏɴ Fᴀɪʟᴇᴅ ⚠️"               
        )
        chat_id = LOG_CHANNEL
        now = datetime.datetime.now()
        await bot.send_message(chat_id, f" **Compression Failed 🤧\nBot is Free Now.....✅** ", parse_mode="markdown")
        await download_start.delete()
      except:
        pass
      
  else:
  #  delete_downloads()
    try:
      await sent_message.edit_text(                    
        text="⚠️ Fᴀɪʟᴇᴅ Dᴏᴡɴʟᴏᴀᴅᴇᴅ Pᴀᴛʜ ɴᴏᴛ Exɪꜱᴛ ⚠️"               
      )
      chat_id = LOG_CHANNEL
      utc_now = datetime.datetime.utcnow()
      ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
      ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
      bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
      bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
      now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
      await bot.send_message(chat_id, f"** Download Error ❕\nBot is Free Now.....✅** ", parse_mode="markdown")
      await download_start.delete()
    except:
      pass
    
async def incoming_cancel_message_f(bot, update):
  """/cancel command"""
  #if update.from_user.id != 1391975600 or 888605132 or 1760568371:
  if update.from_user.id not in AUTH_USERS:      
        
    try:
      await update.message.delete()
    except:
      pass
    return

  status = DOWNLOAD_LOCATION + "/status.json"
  if os.path.exists(status):
    inline_keyboard = []
    ikeyboard = []
    ikeyboard.append(InlineKeyboardButton("Yᴇꜱ 🚫", callback_data=("fuckingdo").encode("UTF-8")))
    ikeyboard.append(InlineKeyboardButton("Nᴏ 🤗", callback_data=("fuckoff").encode("UTF-8")))
    inline_keyboard.append(ikeyboard)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await update.reply_text("Aʀᴇ ʏᴏᴜ Sᴜʀᴇ? 🚫 Tʜɪꜱ Wɪʟʟ Sᴛᴏᴘ Tʜᴇ Cᴏᴍᴘʀᴇꜱꜱɪᴏɴ!", reply_markup=reply_markup, quote=True)
  else:
   # delete_downloads()
    await bot.send_message(
      chat_id=update.chat.id,
      text="No active compression exists",
      reply_to_message_id=update.message_id
    )
