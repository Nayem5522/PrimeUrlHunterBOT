# in & as LazyDeveloper
# Please Don't Remove Credit

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
    ABOUT_BOT_TEXT = """<b> <a href='https://t.me/LazyUrlHunterrBOT'>Lazy Url Hunterr</a> is an open source project.

    Devs: 
        <a href='https://t.me/mRiderDM'>❤️ LazyDeveloper ❤️</a>
    
    
🤖 My Name: <a href='https://t.me/Official_Movies_Group'>Mdisk Search Robot</a>

📝 Language: <a href='https://www.python.org'>Python V3</a>

📚 Library: <a href='https://docs.pyrogram.org'>Pyrogram</a>

📡 Server: <a href='https://heroku.com'>Heroku</a>

📡 Server 2: <a href='https://heroku.com'>koyeb</a> <i>comming soon</i>

👨‍💻 Developer Channel: <a href='https://t.me/LazyDeveloper'>LazyDeveloper</a></b>
"""

    ABOUT_HELP_TEXT = """<b>✅ ɪᴛ'ꜱ ɴᴏᴛ ᴀ ᴅɪꜰꜰɪᴄᴜʟᴛ ᴘʀᴏᴄᴇꜱꜱ, ᴊᴜꜱᴛ ᴛʏᴘᴇ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ʜᴇʀᴇ ᴀɴᴅ ᴛʜᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄ ʟɪɴᴋ ᴡɪʟʟ ᴄᴏᴍᴇ.  

🔍 ɪꜰ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ ꜱᴘᴇʟʟɪɴɢ, ʏᴏᴜ ᴄᴀɴ ᴄʜᴇᴄᴋ ɪᴛ ꜰʀᴏᴍ ɢᴏᴏɢʟᴇ.  

➕ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴀᴅᴅ ᴛʜɪꜱ ᴛᴏ ᴀɴʏ ᴏꜰ ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ, ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ɪᴛ, ᴀɴᴅ ɪ ᴡɪʟʟ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴡɪᴛʜ ʟɪɴᴋꜱ ᴛᴏ ᴀʟʟ ᴛʜᴏꜱᴇ ɢʀᴏᴜᴘꜱ.  

❗ ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍꜱ, ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ᴏᴘᴛɪᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ꜱᴜᴘᴘᴏʀᴛ ꜰʀᴏᴍ ᴜꜱ. ❗
    

🤖 ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ʏᴏᴜʀ ᴏᴡɴ ʙᴏᴛ ʟɪᴋᴇ ᴛʜɪꜱ, ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ \nᴄᴏɴᴛᴀᴄᴛ ᴏᴜʀ ᴅᴇᴠᴇʟᴏᴘᴇʀ 👉 <a href='https://t.me/prime_Nayem'>ᴍʀ.ᴘʀɪᴍᴇ</a></b>
"""

    HOME_TEXT = """
<b>Hello Baby ! {}😅,

I'm the one and only fastest URL finder BOT. Add me to any Group and Give me Hunting rights !!

I will be only yours if you will restrict adding me to other groups.
Go to @BotFather to change settings.

Don't be sad ! Your all urls are in safe Hand.

»»» <b>Happy Hunting</b> «««

🔺Thank You <a href='https://t.me/LazyDeveloper'>LazyDeveloper</a>🔺 </b>
"""


    START_MSG = """
<b>Hello Baby ! {}😅,

I'm the one and only fastest URL & post finder BOT. Add me to any Group and Give me Hunting rights !!

Don't be sad ! Your all urls are in safe Hand.</b>

   »»»» <b>Happy Hunting</b> ««««

💸<b>Donate us to Keep service Alive.💸</b>
»» A small amount of ₹5 - ₹20 - ₹50 - ₹100 will be great help !
🔺 Thank You 🔺 
"""

