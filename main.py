# in & as LazyDeveloper
# Please Don't Remove Credit

from configs import Config
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio

# Bot Client for Inline Search
Bot = Client(
    "PrimeBotz",  
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

User = Client(
    "UserSession",  
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.USER_SESSION_STRING
)

# ডাটাবেজ (সেটিংস সংরক্ষণ করতে)
verified_groups = {}

LOG_CHANNEL_ID = -1002196408894  # লগ চ্যানেল আইডি
MAIN_DATABASE_CHANNEL = Config.CHANNEL_ID  # মূল ডাটাবেজ চ্যানেল

@Bot.on_message(filters.private & filters.command("start"))
async def start_handler(_, message: Message):
    await message.reply_photo(
        "https://telegra.ph/file/2b160d9765fe080c704d2.png",
        caption=Config.START_MSG.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔺 Donate us 🔺", url="https://p.paytm.me/xCTH/vo37hii9")],
            [InlineKeyboardButton("⚡️ LazyDeveloper ⚡️", url="https://t.me/LazyDeveloper")],
            [InlineKeyboardButton("🤒 Help", callback_data="Help_msg"),
             InlineKeyboardButton("🦋 About", callback_data="About_msg")]
        ])
    )

@Bot.on_message(filters.private & filters.command("help"))
async def help_handler(_, message: Message):
    await message.reply_text(
        Config.ABOUT_HELP_TEXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Updates", url="https://t.me/LazyDeveloper"),
             InlineKeyboardButton("Support Group", url="https://t.me/LazyPrincessSupport"), 
             InlineKeyboardButton("About", callback_data="About_msg")]
        ])
    )

# 🔹 গ্রুপ ভেরিফিকেশন কমান্ড
@Bot.on_message(filters.group & filters.command("verify_primebotz"))
async def verify_group(bot, message: Message):
    chat = message.chat
    user = message.from_user
    
    member = await bot.get_chat_member(chat.id, user.id)
    if member.status not in ["administrator", "creator"]:
        return await message.reply_text("❌ **শুধুমাত্র গ্রুপ এডমিন এই কমান্ড ব্যবহার করতে পারবেন!**")
    
    log_message = await bot.send_message(
        chat_id=LOG_CHANNEL_ID,
        text=f"**🔹 নতুন গ্রুপ ভেরিফিকেশন রিকোয়েস্ট**\n\n"
             f"👥 **গ্রুপের নাম:** {chat.title}\n"
             f"🆔 **গ্রুপ আইডি:** `{chat.id}`\n"
             f"👤 **রিকোয়েস্ট করেছেন:** {user.mention}\n\n"
             f"✅ একসেপ্ট করতে নিচের বাটন চাপুন।",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Accept", callback_data=f"accept_{chat.id}")],
            [InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{chat.id}")]
        ])
    )

    await message.reply_text("✅ **আপনার রিকোয়েস্ট পাঠানো হয়েছে! অ্যাডমিন অনুমোদনের পর আপনি চ্যানেল কানেক্ট করতে পারবেন।**")

# 🔹 একসেপ্ট এবং ক্যান্সেল হ্যান্ডলার
@Bot.on_callback_query(filters.regex(r"^(accept|cancel)_(\-?\d+)$"))
async def verification_callback(bot, callback: CallbackQuery):
    action, group_id = callback.data.split("_")
    group_id = int(group_id)
    
    if action == "accept":
        verified_groups[group_id] = None
        await bot.send_message(group_id, "✅ **আপনার গ্রুপ ভেরিফিকেশন একসেপ্ট করা হয়েছে! এখন আপনি চ্যানেল কানেক্ট করতে পারেন।**")
        await callback.message.edit_text("✅ **গ্রুপটি সফলভাবে ভেরিফাই করা হয়েছে!**")
    else:
        await bot.send_message(group_id, "❌ **আপনার ভেরিফিকেশন রিকোয়েস্ট বাতিল করা হয়েছে।**")
        await callback.message.edit_text("❌ **ভেরিফিকেশন বাতিল করা হয়েছে!**")

# 🔹 চ্যানেল কানেক্ট কমান্ড
@Bot.on_message(filters.group & filters.command("connect_prime"))
async def connect_channel(bot, message: Message):
    chat = message.chat
    args = message.text.split()

    if len(args) < 2:
        return await message.reply_text("❌ **ব্যবহার:** /connect_prime -1001234567890")

    channel_id = int(args[1])

    if chat.id not in verified_groups:
        return await message.reply_text("❌ **আপনার গ্রুপ এখনো ভেরিফাই করা হয়নি!**")

    try:
        chat_member = await bot.get_chat_member(channel_id, "me")
        if not chat_member.can_post_messages:
            return await message.reply_text("❌ **আমি চ্যানেলে এডমিন নই! প্রথমে আমাকে এডমিন করুন।**")
    except:
        return await message.reply_text("❌ **আমি চ্যানেলটি খুঁজে পাইনি! নিশ্চিত করুন যে চ্যানেল আইডি সঠিক।**")

    verified_groups[chat.id] = channel_id
    await message.reply_text(f"✅ **আপনার গ্রুপ এখন `{channel_id}` চ্যানেলের সাথে কানেক্ট করা হয়েছে!**")

# 🔹 রিসেট কমান্ড
@Bot.on_message(filters.group & filters.command("reset_prime"))
async def reset_group(bot, message: Message):
    chat = message.chat

    if chat.id in verified_groups:
        del verified_groups[chat.id]
        await message.reply_text("🔄 **সফলভাবে রিসেট করা হয়েছে! এখন মেইন ডাটাবেজ চ্যানেল ব্যবহার হবে।**")
    else:
        await message.reply_text("❌ **আপনার গ্রুপ ভেরিফাই করা হয়নি!**")

# 🔹 ফাইল সার্চ হ্যান্ডলার (চ্যানেল থেকে লিংক খুঁজে আনা)
@Bot.on_message(filters.text & filters.group)
async def search_handler(bot, message: Message):
    chat = message.chat
    search_query = message.text

    channel_id = verified_groups.get(chat.id, MAIN_DATABASE_CHANNEL)  # 🔹 যদি গ্রুপ ভেরিফাই না থাকে, তাহলে MAIN_DATABASE_CHANNEL ব্যবহার হবে।

    results = []
    async for msg in User.search_messages(chat_id=channel_id, limit=10, query=search_query):
        if msg.text:
            results.append(msg.text)

    if results:
        response_text = "\n\n".join(results[:5])
        await message.reply_text(f"🔍 **আপনার অনুসন্ধানের ফলাফল:**\n\n{response_text}")
    else:
        await message.reply_text("❌ **কোনো ফলাফল পাওয়া যায়নি!**")
	    
# Start Clients
Bot.start()
User.start()
idle()
Bot.stop()
User.stop()
