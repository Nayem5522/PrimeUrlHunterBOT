from configs import Config  
from pyrogram import Client, filters, idle  
from pyrogram.enums import ParseMode  
from pyrogram.errors import QueryIdInvalid  
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery  
from LazyDeveloper.forcesub import ForceSub  
from pyrogram.client import Client as User  
import asyncio  
import urllib.parse  

# Bot Client
Bot = Client("PrimeBotz", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)  

# User Client
User = Client("UserSession", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.USER_SESSION_STRING)  

PRIME_BOTZ_STIK = "CAACAgUAAxkBAAI9pmfCrCQ2pNi_3CtnMCUPrty_RQ82AAJIFwAC1BkYVqY09g5jKSm5HgQ"  
PRIME_BOTZ_NO = "https://envs.sh/iJJ.jpg"  

# Start Command
@Bot.on_message(filters.private & filters.command("start"))
async def start_handler(bot, message: Message):
    await message.reply_photo(
        "https://envs.sh/i1Y.jpg",
        caption=Config.START_MSG.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("☆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ☆", url="https://t.me/Prime_Link_Search_FastBot?startgroup=true")],
            [InlineKeyboardButton("✪ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ✪", url="https://t.me/Prime_Botz_Support"),
             InlineKeyboardButton("🎬 ᴍᴏᴠɪᴇꜱ ᴄʜᴀɴɴᴇʟ 🎬", url="https://t.me/Prime_Movies4U")],
            [InlineKeyboardButton("〄 ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ 〄", url="https://t.me/Prime_Botz")],
            [InlineKeyboardButton("〆 ᴀʙᴏᴜᴛ 〆", callback_data="About_msg"),
             InlineKeyboardButton("〆 ʜᴇʟᴘ 〆", callback_data="Help_msg")],
            [InlineKeyboardButton("✧ ᴄʀᴇᴀᴛᴏʀ ✧", url="https://t.me/Prime_Nayem")]
        ]),
        parse_mode=ParseMode.HTML    
    )  

# Help Command
@Bot.on_message(filters.private & filters.command("help"))
async def help_handler(bot, message: Message):
    await message.reply_text(
        Config.ABOUT_HELP_TEXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("〄 ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ 〄", url="https://t.me/Prime_Botz"),
             InlineKeyboardButton("✪ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ✪", url="https://t.me/Prime_Botz_support")],
            [InlineKeyboardButton("〆 ᴀʙᴏᴜᴛ 〆", callback_data="About_msg")]
        ]),
        parse_mode=ParseMode.HTML
    )  

@Bot.on_message(filters.incoming & ~filters.channel)
async def inline_handlers(bot, message: Message):
    if message.text == '/start': return  

    sticker_msg = await message.reply_sticker(PRIME_BOTZ_STIK)  
    await asyncio.sleep(3)  
    await sticker_msg.delete()  

    answers = f'**📂 🔍 ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ꜱᴇᴀʀᴄʜ 🔎 ➠ {message.text}**\n\n'  
    found = False  

    async for msg in User.search_messages(chat_id=Config.CHANNEL_ID, limit=50, query=message.text):  
        if msg.text:  
            found = True  
            f_text = msg.text.split("\n", 1)[0]  
            d_link = msg.text.split("\n", 2)[-1]  
            answers += f'''**▰▱▰▱▰▱▰▱▰▱▰▱▰▱  
📜 𝗙𝗶𝗹𝗲 𝗡𝗮𝗺𝗲: {f_text}  
🔗 𝗟𝗶𝗻𝗸: 👇  
{d_link}  
▰▱▰▱▰▱▰▱▰▱▰▱▰▱**\n\n'''  

    if found:
        answers += '''\n\n\n⋆★⋆━━━━━━★━━━━⋆★⋆\n❗️❗️❗️ ɪᴍᴘᴏʀᴛᴀɴᴛ ɴᴏᴛɪᴄᴇ ❗️❗️❗️\n⚠️ Link will auto-delete in 3 minutes... ⏰\n⋆★⋆━━━━━━★━━━━⋆★⋆'''  
        msg = await message.reply_text(answers)  
    else:
        google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(message.text)}"  
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 Check on Google", url=google_search_url)],
            [InlineKeyboardButton("📩 Request to Admin", url="https://t.me/Prime_Admin_Support_ProBot")]
        ])  
        msg = await message.reply_photo(
            photo=PRIME_BOTZ_NO,
            caption=f"**❌ No results found for ➠ {message.text}\n\n⚡ Try searching with correct spelling or add the release year.**",
            reply_markup=keyboard
        )  

    try:
        await asyncio.sleep(180)  
        await msg.delete()  
        await message.delete()  
    except:
        print(f"[{Config.BOT_SESSION_NAME}] - Failed to delete message for {message.from_user.first_name}")  

# Callback Query Handler
@Bot.on_callback_query()
async def button(bot, cmd: CallbackQuery):
    cb_data = cmd.data  
    if "About_msg" in cb_data:
        await cmd.message.edit(
            text=Config.ABOUT_BOT_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("〄 ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ 〄", url="https://t.me/Prime_Botz")],
                [InlineKeyboardButton("✧ ᴀᴅᴍɪɴ ꜱᴜᴘᴘᴏʀᴛ ✧", url="https://t.me/Prime_Nayem"),
                 InlineKeyboardButton("🏠 ʜᴏᴍᴇ 🏠", callback_data="gohome")]
            ]),
            parse_mode=ParseMode.HTML
        )  

    elif "Help_msg" in cb_data:
        await cmd.message.edit(
            text=Config.ABOUT_HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✪ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ✪", url="https://t.me/Prime_Botz_support"),
                 InlineKeyboardButton("〄 ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ 〄", url="https://t.me/Prime_Botz")],
                [InlineKeyboardButton("🏠 ʜᴏᴍᴇ 🏠", callback_data="gohome")]
            ]),
            parse_mode=ParseMode.HTML
        )  

    elif "gohome" in cb_data:  # এখানে ইন্ডেন্ট ঠিক করা হয়েছে
        await cmd.message.edit(
            text=Config.START_MSG.format(cmd.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("☆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ☆", url="https://t.me/Prime_Link_Search_FastBot?startgroup=true")],
                [InlineKeyboardButton("✪ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ✪", url="https://t.me/Prime_Botz_Support"),
                 InlineKeyboardButton("🎬 ᴍᴏᴠɪᴇꜱ ᴄʜᴀɴɴᴇʟ 🎬", url="https://t.me/Prime_Movies4U")],
                [InlineKeyboardButton("〄 ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ 〄", url="https://t.me/Prime_Botz")],
                [InlineKeyboardButton("〆 ʜᴇʟᴘ 〆", callback_data="Help_msg"),
                 InlineKeyboardButton("〆 ᴀʙᴏᴜᴛ 〆", callback_data="About_msg")],
                [InlineKeyboardButton("✧ ᴄʀᴇᴀᴛᴏʀ ✧", url="https://t.me/Prime_Nayem")]
            ]),
            parse_mode=ParseMode.HTML
        )

# Start Clients
Bot.start()  
User.start()  
idle()  
Bot.stop()  
User.stop()
