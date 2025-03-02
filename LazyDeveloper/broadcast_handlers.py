import asyncio
import datetime
import random
import string
import time
import traceback
import aiofiles
import aiofiles.os
import logging
from configs import Config
from database import db
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, PeerIdInvalid, UserIsBlocked
from pyrogram.types import Message

broadcast_ids = {}


@Client.on_message(filters.command("broadcast") & filters.user(Config.BOT_OWNER))
async def broadcast_handler(c: Client, m: Message):
    if not m.reply_to_message:
        return await m.reply_text("**দয়া করে এমন একটি মেসেজ রিপ্লাই করুন যা ব্রডকাস্ট করতে চান!**")

    broadcast_msg = m.reply_to_message

    broadcast_id = ''.join(random.choices(string.ascii_letters, k=3))
    broadcast_ids[broadcast_id] = {
        "total": await db.total_users_count(),
        "success": 0,
        "failed": 0,
        "current": 0
    }

    msg = await m.reply_text(f"📡 **ব্রডকাস্ট শুরু হচ্ছে...**\n\n👥 মোট ইউজার: {broadcast_ids[broadcast_id]['total']} জন")

    start_time = time.time()
    log_file = "broadcast_failed_users.txt"
    async with aiofiles.open(log_file, "w") as log:
        for user_id in await db.get_all_users():
            status, error = await send_msg(user_id, broadcast_msg)
            if error:
                await log.write(error)
            if status == 200:
                broadcast_ids[broadcast_id]["success"] += 1
            else:
                broadcast_ids[broadcast_id]["failed"] += 1
                if status == 400:
                    await db.delete_user(user_id)
            broadcast_ids[broadcast_id]["current"] += 1

    elapsed_time = str(datetime.timedelta(seconds=int(time.time() - start_time)))
    await msg.delete()

    if broadcast_ids[broadcast_id]["failed"] == 0:
        await m.reply_text(
            f"✅ **ব্রডকাস্ট সম্পন্ন হয়েছে!**\n\n⏳ সময়: `{elapsed_time}`\n👥 মোট ইউজার: `{broadcast_ids[broadcast_id]['total']}`\n✅ সফল: `{broadcast_ids[broadcast_id]['success']}`\n❌ ব্যর্থ: `{broadcast_ids[broadcast_id]['failed']}`"
        )
    else:
        await m.reply_document(
            document=log_file,
            caption=f"❗ **ব্রডকাস্ট আংশিক সফল হয়েছে!**\n\n⏳ সময়: `{elapsed_time}`\n👥 মোট ইউজার: `{broadcast_ids[broadcast_id]['total']}`\n✅ সফল: `{broadcast_ids[broadcast_id]['success']}`\n❌ ব্যর্থ: `{broadcast_ids[broadcast_id]['failed']}`"
        )
        await aiofiles.os.remove(log_file)


async def send_msg(user_id, message):
    try:
        if Config.BROADCAST_AS_COPY:
            await message.copy(chat_id=user_id)
        else:
            await message.forward(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid) as e:
        return 400, f"{user_id} : {str(e)}\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"
