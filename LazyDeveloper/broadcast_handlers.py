import asyncio
import datetime
import logging
import random
import string
import time
import traceback
import aiofiles
import aiofiles.os

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, PeerIdInvalid, UserIsBlocked
from pyrogram.types import Message

from config import BOT_OWNER
from database import delete_user, get_all_users, total_users_count

logging.basicConfig(level=logging.INFO)
broadcast_ids = {}

@Client.on_message(filters.command("broadcast") & filters.private & filters.user(BOT_OWNER))
async def broadcast_handler(c: Client, m: Message):
    """ Handles the broadcast command. """
    if not m.reply_to_message:
        return await m.reply_text("⚠️ **Please reply to a message to broadcast!**")
    
    try:
        await main_broadcast_handler(m)
    except Exception as e:
        logging.error("❌ **Broadcast failed:**", exc_info=True)
        await m.reply_text("❌ **Something went wrong! Check logs.**")

async def send_msg(user_id: int, message: Message):
    """ Sends a message to a user and handles exceptions. """
    try:
        await message.copy(chat_id=user_id)
        return 200, None  # Success
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : ❌ User Deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : ❌ Bot Blocked\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : ❌ Invalid User ID\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

async def main_broadcast_handler(m: Message):
    """ Manages the broadcasting process. """
    all_users = await get_all_users()
    total_users = await total_users_count()
    broadcast_msg = m.reply_to_message

    broadcast_id = ''.join(random.choices(string.ascii_letters, k=6))
    broadcast_ids[broadcast_id] = {"total": total_users, "current": 0, "failed": 0, "success": 0}

    start_time = time.time()
    msg_status = await m.reply_text("📢 **Broadcasting Started...**\n\n⏳ Please wait...")

    async with aiofiles.open('broadcast_log.txt', 'w') as log_file:
        async for user in all_users:
            user_id = int(user["user_id"])
            status, error_msg = await send_msg(user_id, broadcast_msg)

            if error_msg:
                await log_file.write(error_msg)

            if status == 200:
                broadcast_ids[broadcast_id]["success"] += 1
            else:
                broadcast_ids[broadcast_id]["failed"] += 1
                if status == 400:
                    await delete_user(user_id)

            broadcast_ids[broadcast_id]["current"] += 1

    elapsed_time = str(datetime.timedelta(seconds=int(time.time() - start_time)))
    await asyncio.sleep(2)
    await msg_status.delete()

    final_status = (
        f"✅ **Broadcast Completed!**\n\n"
        f"🕒 **Time Taken:** `{elapsed_time}`\n"
        f"👥 **Total Users:** `{total_users}`\n"
        f"📩 **Success:** `{broadcast_ids[broadcast_id]['success']}`\n"
        f"❌ **Failed:** `{broadcast_ids[broadcast_id]['failed']}`"
    )

    if broadcast_ids[broadcast_id]["failed"] == 0:
        await m.reply_text(final_status, quote=True)
    else:
        await m.reply_document("broadcast_log.txt", caption=final_status, quote=True)
    
    del broadcast_ids[broadcast_id]
    await aiofiles.os.remove("broadcast_log.txt")
    
