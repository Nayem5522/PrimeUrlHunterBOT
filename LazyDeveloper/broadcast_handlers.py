import asyncio
import datetime
import logging
import random
import string
import time
import traceback

import aiofiles
import aiofiles.os
from configs import BOT_OWNER  # Import BOT_OWNER from configs.py
from database import delete_user, get_all_users, total_users_count
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, PeerIdInvalid, UserIsBlocked
from pyrogram.types import Message

broadcast_ids = {}

# Broadcast Handler
@Bot.on_message(filters.private & filters.command("broadcast"))
async def broadcast_handler(bot, message: Message):
    if not m.reply_to_message:
        return await m.reply_text("⚠️ Please reply to a message to broadcast.")

    try:
        await main_broadcast_handler(m)
    except Exception as e:
        logging.error(f"❌ Broadcast failed: {e}", exc_info=True)
        await m.reply_text("❌ Unable to broadcast! Please check the logs.")


async def send_msg(user_id: int, message: Message):
    try:
        await message.copy(chat_id=user_id)  # Always send as copy
        return 200, None

    except FloodWait as e:
        logging.warning(f"⚠️ FloodWait: Waiting for {e.value} seconds...")
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)

    except InputUserDeactivated:
        return 400, f"{user_id} : ❌ User deactivated\n"

    except UserIsBlocked:
        return 400, f"{user_id} : 🚫 User blocked the bot\n"

    except PeerIdInvalid:
        return 400, f"{user_id} : ⚠️ Invalid user ID\n"

    except Exception as e:
        return 500, f"{user_id} : ❌ {traceback.format_exc()}\n"


async def main_broadcast_handler(m: Message):
    all_users = await get_all_users()
    broadcast_msg = m.reply_to_message

    broadcast_id = ''.join(random.choices(string.ascii_letters, k=5))
    total_users = await total_users_count()
    broadcast_ids[broadcast_id] = {"total": total_users, "done": 0, "success": 0, "failed": 0}

    out = await m.reply_text("📢 **Broadcast started... Please wait!**")

    start_time = time.time()
    failed_users = []

    async with aiofiles.open("broadcast_log.txt", "w") as log_file:
        async for user in all_users:
            user_id = int(user["user_id"])
            status, msg = await send_msg(user_id, broadcast_msg)

            if msg:
                await log_file.write(msg)

            if status == 200:
                broadcast_ids[broadcast_id]["success"] += 1
            else:
                broadcast_ids[broadcast_id]["failed"] += 1
                failed_users.append(user_id)
                if status == 400:
                    await delete_user(user_id)

            broadcast_ids[broadcast_id]["done"] += 1

    # Remove broadcast ID after completion
    broadcast_ids.pop(broadcast_id, None)

    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await out.delete()

    if not failed_users:
        await m.reply_text(
            f"✅ **Broadcast completed successfully!**\n\n"
            f"⏳ Time taken: `{completed_in}`\n"
            f"👥 Total users: `{total_users}`\n"
            f"✔️ Successful: `{broadcast_ids[broadcast_id]['success']}`\n"
            f"❌ Failed: `{broadcast_ids[broadcast_id]['failed']}`"
        )
    else:
        await m.reply_document(
            document="broadcast_log.txt",
            caption=(
                f"✅ **Broadcast completed!**\n\n"
                f"⏳ Time taken: `{completed_in}`\n"
                f"👥 Total users: `{total_users}`\n"
                f"✔️ Successful: `{broadcast_ids[broadcast_id]['success']}`\n"
                f"❌ Failed: `{broadcast_ids[broadcast_id]['failed']}`"
            )
        )

    # Delete the log file after sending
    await aiofiles.os.remove("broadcast_log.txt")
