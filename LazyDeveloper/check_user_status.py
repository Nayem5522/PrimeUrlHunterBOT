# in & as LazyDeveloper
# Please Don't Remove Credit

import datetime
from configs import Config
from handlers.database import db
from pyrogram.errors import FloodWait
import asyncio


async def handle_user_status(bot, cmd):
    user_id = cmd.from_user.id

    # নতুন ইউজার হলে ডাটাবেজে যোগ করো
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)
        if Config.LOG_CHANNEL:
            try:
                await bot.send_message(
                    Config.LOG_CHANNEL,
                    f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={user_id}) started @{Config.BOT_USERNAME} !!"
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as err:
                print(f"LOG_CHANNEL Error: {err}")

    # ব্যান স্ট্যাটাস চেক করা হচ্ছে
    ban_status = await db.get_ban_status(user_id)
    
    if ban_status.get("is_banned", False):
        banned_on = datetime.date.fromisoformat(ban_status.get("banned_on", "9999-12-31"))
        ban_duration = ban_status.get("ban_duration", 0)
        days_banned = (datetime.date.today() - banned_on).days

        if days_banned > ban_duration:
            await db.remove_ban(user_id)
        else:
            await cmd.reply_text("🚫 আপনি ব্যান আছেন! দয়া করে এডমিনের সাথে যোগাযোগ করুন।", quote=True)
            return

    await cmd.continue_propagation()
