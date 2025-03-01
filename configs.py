

import os


class Config(object):
    API_ID = int(os.environ.get("API_ID", 12345))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    BOT_SESSION_NAME = os.environ.get("BOT_SESSION_NAME", "MdiskSearchBot")
    USER_SESSION_STRING = os.environ.get("USER_SESSION_STRING", "")
    CHANNEL_ID = int(os.environ.get("CHANNEL_ID", -100))
    BOT_USERNAME = os.environ.get("BOT_USERNAME")
    BOT_OWNER = int(os.environ.get("BOT_OWNER"))
    DATABASE_URL = os.environ.get("DATABASE_URL")
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", None)
    ABOUT_BOT_TEXT = """<b><blockquote>⍟───[  <a href='https://t.me/Prime_Botz'>📌 ᴍʏ ᴅᴇᴛᴀɪʟꜱ ʙʏ ᴘʀɪᴍᴇ ʙᴏᴛᴢ 🤖</a ]───⍟</blockquote>
    
‣ ᴍʏ ɴᴀᴍᴇ : <a href='https://t.me/Prime_Link_Search_FastBot'>🔍 ᴘʀɪᴍᴇ ʟɪɴᴋ sᴇᴀʀᴄʜ ғᴀsᴛʙᴏᴛ 🚀</a>
‣ ᴍʏ ʙᴇsᴛ ғʀɪᴇɴᴅ : <a href='tg://settings'>ᴛʜɪs ᴘᴇʀsᴏɴ</a> 
‣ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href='https://t.me/Prime_Nayem'>ᴍʀ.ᴘʀɪᴍᴇ</a> 
‣ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ : <a href='https://t.me/Prime_Botz'>ᴘʀɪᴍᴇ ʙᴏᴛᴢ</a> 
‣ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ : <a href='https://t.me/Prime_Movies4U'>ᴘʀɪᴍᴇ ᴍᴏᴠɪᴇs</a> 
‣ ѕᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ : <a href='https://t.me/Prime_Botz_Support'>ᴘʀɪᴍᴇ ʙᴏᴛᴢ ѕᴜᴘᴘᴏʀᴛ</a> 
‣ ᴅᴀᴛᴀ ʙᴀsᴇ : <a href='https://www.mongodb.com/'>ᴍᴏɴɢᴏ ᴅʙ</a> 
‣ ʙᴏᴛ sᴇʀᴠᴇʀ : <a href='https://heroku.com'>ʜᴇʀᴏᴋᴜ</a> 
‣ ʙᴜɪʟᴅ sᴛᴀᴛᴜs : ᴠ2.7.1 [sᴛᴀʙʟᴇ]></b>"""

    ABOUT_HELP_TEXT = """<b>✅ ɪᴛ'ꜱ ɴᴏᴛ ᴀ ᴅɪꜰꜰɪᴄᴜʟᴛ ᴘʀᴏᴄᴇꜱꜱ, ᴊᴜꜱᴛ ᴛʏᴘᴇ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ʜᴇʀᴇ ᴀɴᴅ ᴛʜᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄ ʟɪɴᴋ ᴡɪʟʟ ᴄᴏᴍᴇ.  

🔍 ɪꜰ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ ꜱᴘᴇʟʟɪɴɢ, ʏᴏᴜ ᴄᴀɴ ᴄʜᴇᴄᴋ ɪᴛ ꜰʀᴏᴍ ɢᴏᴏɢʟᴇ.  

➕ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴀᴅᴅ ᴛʜɪꜱ ᴛᴏ ᴀɴʏ ᴏꜰ ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ, ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ɪᴛ, ᴀɴᴅ ɪ ᴡɪʟʟ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴡɪᴛʜ ʟɪɴᴋꜱ ᴛᴏ ᴀʟʟ ᴛʜᴏꜱᴇ ɢʀᴏᴜᴘꜱ.  

❗ ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍꜱ, ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ᴏᴘᴛɪᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ꜱᴜᴘᴘᴏʀᴛ ꜰʀᴏᴍ ᴜꜱ. ❗
    

🤖 ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ʏᴏᴜʀ ᴏᴡɴ ʙᴏᴛ ʟɪᴋᴇ ᴛʜɪꜱ, ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ \nᴄᴏɴᴛᴀᴄᴛ ᴏᴜʀ ᴅᴇᴠᴇʟᴏᴘᴇʀ 👉 <a href='https://t.me/prime_Nayem'>ᴍʀ.ᴘʀɪᴍᴇ</a></b>
"""

    HOME_TEXT = """
<b>👋 ʜᴇʟʟᴏ ʙᴜᴅᴅʏ! {}🥰,

🤖 ɪ ᴀᴍ ᴀ ꜱɪᴍᴘʟᴇ ʙᴜᴛ ᴘᴏᴡᴇʀꜰᴜʟ ᴀɴᴅ ᴀᴅᴠᴀɴᴄᴇᴅ ʟɪɴᴋ ꜱᴇᴀʀᴄʜ ʙᴏᴛ.  
ʏᴏᴜ ᴄᴀɴ ᴄᴀʟʟ ᴍᴇ ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ᴀᴜᴛᴏꜰɪʟᴛᴇʀ, ʟɪɴᴋ ꜱᴇᴀʀᴄʜ, ᴏʀ ᴜʀʟ ꜱᴇᴀʀᴄʜ ʙᴏᴛ—ᴡʜɪᴄʜᴇᴠᴇʀ ʏᴏᴜ ᴘʀᴇꜰᴇʀ!  

📌 ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ, ɪ ᴡɪʟʟ ɢɪᴠᴇ ᴍᴏᴠɪᴇꜱ ᴏʀ ꜱᴇʀɪᴇꜱ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴘᴍ!!  

⚡ ɪᴛ ɪꜱ ᴇᴀꜱʏ ᴛᴏ ᴜꜱᴇ ᴍᴇ, ᴊᴜꜱᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀɴ ᴀᴅᴍɪɴ.

<blockquote> 🌿 ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ  <a href='https://t.me/Prime_Botz'>ᴘʀɪᴍᴇ ʙᴏᴛz</a></blockquote>
"""


    START_MSG = """
<b>👋 ʜᴇʟʟᴏ ʙᴜᴅᴅʏ! {}🥰,

🤖 ɪ ᴀᴍ ᴀ ꜱɪᴍᴘʟᴇ ʙᴜᴛ ᴘᴏᴡᴇʀꜰᴜʟ ᴀɴᴅ ᴀᴅᴠᴀɴᴄᴇᴅ ʟɪɴᴋ ꜱᴇᴀʀᴄʜ ʙᴏᴛ.  
ʏᴏᴜ ᴄᴀɴ ᴄᴀʟʟ ᴍᴇ ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ᴀᴜᴛᴏꜰɪʟᴛᴇʀ, ʟɪɴᴋ ꜱᴇᴀʀᴄʜ, ᴏʀ ᴜʀʟ ꜱᴇᴀʀᴄʜ ʙᴏᴛ—ᴡʜɪᴄʜᴇᴠᴇʀ ʏᴏᴜ ᴘʀᴇꜰᴇʀ!  

📌 ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ, ɪ ᴡɪʟʟ ɢɪᴠᴇ ᴍᴏᴠɪᴇꜱ ᴏʀ ꜱᴇʀɪᴇꜱ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴘᴍ!!  

⚡ ɪᴛ ɪꜱ ᴇᴀꜱʏ ᴛᴏ ᴜꜱᴇ ᴍᴇ, ᴊᴜꜱᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀɴ ᴀᴅᴍɪɴ.

<blockquote> 🌿 ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ  <a href='https://t.me/Prime_Botz'>ᴘʀɪᴍᴇ ʙᴏᴛz</a></blockquote>
"""

