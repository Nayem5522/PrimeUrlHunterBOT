# in & as LazyDeveloper
# Please Don't Remove Credit

import asyncio
import datetime
import logging
import random
import string
import time
import traceback
import aiofiles
import aiofiles.os

from config import BOT_OWNER  # Ensure BOT_OWNER is defined in config
from database import delete_user, get_all_users, total_users_count
from pyrogram import Client, filters
from pyrogram.errors import (FloodWait, InputUserDeactivated, PeerIdInvalid,
                             UserIsBlocked)
from pyrogram.types import Message

broadcast_ids = {}

@Client.on_message(filters.command("broadcast") & filters.private & filters.user(BOT_OWNER) & filters.reply)
async def broadcast_handler(c: Client, m: Message):
    try:
        await main_broadcast_handler(m)
    except Exception as e:
        logging.error("Something went wrong. Unable to broadcast!", exc_info=True)
        await m.reply_text("❌ ব্রডকাস্ট করতে সমস্যা হয়েছে! লগ চেক করুন।")

async def send_msg(user_id, message):
    try:
        if Config.BROADCAST_AS_COPY:  # Use Config for better settings management
            await message.copy(chat_id=user_id)
        else:
            await message.forward(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : ❌ Account Deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : ❌ Blocked the Bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : ❌ Invalid User ID\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

async def main_broadcast_handler(m: Message):
    all_users = await get_all_users()
    broadcast_msg = m.reply_to_message

    # Unique broadcast ID
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for _ in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break

    out = await m.reply_text("🔄 **ব্রডকাস্ট শুরু হয়েছে...**")
    start_time = time.time()
    total_users = await total_users_count()
    done, failed, success = 0, 0, 0
    broadcast_ids[broadcast_id] = dict(total=total_users, current=done, failed=failed, success=success)

    async with aiofiles.open('broadcast_log.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id=int(user['user_id']), message=broadcast_msg)
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await delete_user(user['user_id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(dict(current=done, failed=failed, success=success))

    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    
    await asyncio.sleep(3)
    await out.delete()
    
    if failed == 0:
        await m.reply_text(f"✅ **ব্রডকাস্ট সম্পন্ন হয়েছে!**\n\n⏳ সময় লেগেছে: `{completed_in}`\n👥 মোট ইউজার: `{total_users}`\n📤 সফল: `{success}`\n❌ ব্যর্থ: `{failed}`")
    else:
        await m.reply_document(document='broadcast_log.txt', caption=f"✅ **ব্রডকাস্ট সম্পন্ন হয়েছে!**\n\n⏳ সময় লেগেছে: `{completed_in}`\n👥 মোট ইউজার: `{total_users}`\n📤 সফল: `{success}`\n❌ ব্যর্থ: `{failed}`")
    
    await aiofiles.os.remove('broadcast_log.txt')
