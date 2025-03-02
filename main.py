from configs import Config  
from pyrogram import Client, filters, idle  
from pyrogram.enums import ParseMode  
from pyrogram.errors import UserNotParticipant  
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton  
import asyncio  
import urllib.parse  

AUTH_CHANNEL = Config.AUTH_CHANNEL

# Bot Client
Bot = Client("PrimeBotz", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)  

# User Client
User = Client("UserSession", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.USER_SESSION_STRING)  

async def is_subscribed(bot, user_id):
    """Check if the user is subscribed to the required channel(s)."""
    btn = []
    for channel in AUTH_CHANNEL:
        try:
            await bot.get_chat_member(int(channel), user_id)
        except UserNotParticipant:
            chat = await bot.get_chat(int(channel))
            btn.append([InlineKeyboardButton("✇ Join Updates Channel ✇", url=chat.invite_link)])
        except Exception as e:
            pass
    return btn

async def force_sub(bot, message):
    """Middleware function to check subscription before allowing any command or search."""
    btn = await is_subscribed(bot, message.from_user.id)
    if btn:
        await message.reply_photo(
            photo="https://envs.sh/KgA.jpg",  # Change this if needed
            caption="👋 Hello {message.from_user.mention},\n\n"
                    "You must join our updates channel before using the bot. "
                    "Click the 'Join Updates Channel' button below and then press 'Try Again'.",
            reply_markup=InlineKeyboardMarkup(btn + [[InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{(await bot.get_me()).username}?start=true")]])
        )
        return False
    return True

# Start Command
@Bot.on_message(filters.private & filters.command("start"))
async def start_handler(bot, message: Message):
    if not await force_sub(bot, message):
        return

    await message.reply_photo(
        "https://envs.sh/i1Y.jpg",
        caption=Config.START_MSG.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("☆ Add Me to Group ☆", url="https://t.me/Prime_Link_Search_FastBot?startgroup=true")],
            [InlineKeyboardButton("✪ Support Group ✪", url="https://t.me/Prime_Botz_Support"),
             InlineKeyboardButton("🎬 Movies Channel 🎬", url="https://t.me/Prime_Movies4U")],
            [InlineKeyboardButton("〄 Updates Channel 〄", url="https://t.me/Prime_Botz")],
            [InlineKeyboardButton("〆 About 〆", callback_data="About_msg"),
             InlineKeyboardButton("〆 Help 〆", callback_data="Help_msg")],
            [InlineKeyboardButton("✧ Creator ✧", url="https://t.me/Prime_Nayem")]
        ]),
        parse_mode=ParseMode.HTML    
    )  

# Help Command
@Bot.on_message(filters.private & filters.command("help"))
async def help_handler(bot, message: Message):
    if not await force_sub(bot, message):
        return

    await message.reply_text(
        Config.ABOUT_HELP_TEXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("〄 Updates Channel 〄", url="https://t.me/Prime_Botz"),
             InlineKeyboardButton("✪ Support Group ✪", url="https://t.me/Prime_Botz_support")],
            [InlineKeyboardButton("〆 About 〆", callback_data="About_msg")]
        ]),
        parse_mode=ParseMode.HTML
    )  

# Search Function
@Bot.on_message(filters.incoming & ~filters.channel)
async def inline_handlers(bot, message: Message):
    if not await force_sub(bot, message):
        return

    if message.text == '/start':
        return  

    sticker_msg = await message.reply_sticker("CAACAgUAAxkBAAIojGfEhpbbnjm9DDhCsYfT3ICbDQb5AAJMFgACJdWRVLSFBTAsBpJ5HgQ")  
    await asyncio.sleep(3)  
    await sticker_msg.delete()  

    answers = f'**📂 🔍 Here is your search 🔎 ➠ {message.text}**\n\n'  
    found = False  

    async for msg in User.search_messages(chat_id=Config.CHANNEL_ID, limit=50, query=message.text):  
        if msg.text:  
            found = True  
            f_text = msg.text.split("\n", 1)[0]  
            d_link = msg.text.split("\n", 2)[-1]  
            answers += f'''**▰▱▰▱▰▱▰▱▰▱▰▱▰▱  
📜 File Name: {f_text}  
🔗 Link: 👇  
{d_link}  
▰▱▰▱▰▱▰▱▰▱▰▱▰▱**\n\n'''  

    if found:
        answers += '''\n\n\n⋆★⋆━━━━━━★━━━━⋆★⋆\n❗️❗️❗️ Important Notice ❗️❗️❗️\n⚠️ Link will auto-delete in 3 minutes... ⏰\n⋆★⋆━━━━━━★━━━━⋆★⋆'''  
        msg = await message.reply_text(answers)  
    else:
        google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(message.text)}"  
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 Check on Google", url=google_search_url)],
            [InlineKeyboardButton("📩 Request to Admin", url="https://t.me/Prime_Admin_Support_ProBot")]
        ])  
        msg = await message.reply_photo(
            photo="https://envs.sh/iJJ.jpg",
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
