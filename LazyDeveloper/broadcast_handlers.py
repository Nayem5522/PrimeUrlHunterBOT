
import asyncio
import datetime
import logging
import random
import string
import time
import traceback
import aiofiles
import aiofiles.os

from config import Config
from database import delete_user, get_all_users, total_users_count
from pyrogram import Client, filters
from pyrogram.errors import (
    FloodWait, InputUserDeactivated, PeerIdInvalid, UserIsBlocked
)
from pyrogram.types import Message

broadcast_ids = {}

@Client.on_message(filters.command("broadcast") & filters.private & filters.user(Config.OWNER_ID))
async def broadcast_handler(c: Client, m: Message):
    if m.reply_to_message:
        try:
            await main_broadcast_handler(m)
        except Exception:
            logging.error("Error during broadcast", exc_info=True)
    else:
        await m.reply_text("Please reply to a message to broadcast.")

async def send_msg(user_id, message):
    try:
        if Config.BROADCAST_AS_COPY:
            await message.copy(chat_id=user_id)
        else:
            await message.forward(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.value)  # Wait for the required time
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : invalid user id\n"
    except Exception:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

async def main_broadcast_handler(m: Message):
    all_users = await get_all_users()
    broadcast_msg = m.reply_to_message

    broadcast_id = ''.join(random.choices(string.ascii_letters, k=3))
    while broadcast_id in broadcast_ids:
        broadcast_id = ''.join(random.choices(string.ascii_letters, k=3))

    out = await m.reply_text("Broadcasting started...")

    start_time = time.time()
    total_users = await total_users_count()
    done, failed, success = 0, 0, 0

    broadcast_ids[broadcast_id] = {"total": total_users, "current": done, "failed": failed, "success": success}

    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id=int(user['user_id']), message=broadcast_msg)
            if msg:
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
            broadcast_ids[broadcast_id].update({"current": done, "failed": failed, "success": success})

    broadcast_ids.pop(broadcast_id, None)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()

    report_text = f"Broadcast completed in `{completed_in}`\n\nTotal users: {total_users}.\nProcessed: {done}, Success: {success}, Failed: {failed}."
    
    if failed == 0:
        await m.reply_text(report_text, quote=True)
    else:
        await m.reply_document(document='broadcast.txt', caption=report_text, quote=True)

    await aiofiles.os.remove('broadcast.txt')
  
