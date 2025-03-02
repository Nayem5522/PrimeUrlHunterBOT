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

# ✅ শুধুমাত্র এই OWNER ID ব্রডকাস্ট করতে পারবে
BOT_OWNER_ID = 6761157656

# ✅ LOGGING সেটআপ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("broadcast.log"), logging.StreamHandler()]
)

broadcast_ids = {}

@Client.on_message(filters.command("broadcast"))
async def broadcast_handler(c: Client, m: Message):
    user_id = m.from_user.id

    # ✅ শুধুমাত্র OWNER পারবে, অন্য কেউ পারবে না
    if user_id != BOT_OWNER_ID:
        logging.warning(f"❌ অনুমতি নেই! {user_id} চেষ্টা করেছিল।")
        return await m.reply_text("❌ **আপনার এই কমান্ড চালানোর অনুমতি নেই!**\n\nশুধুমাত্র বটের মালিক এটি ব্যবহার করতে পারবেন।")

    if not m.reply_to_message:
        logging.info(f"⚠️ {user_id} ব্রডকাস্ট করতে চেয়েছিল কিন্তু কোনো মেসেজ রিপ্লাই করেনি।")
        return await m.reply_text("**দয়া করে এমন একটি মেসেজ রিপ্লাই করুন যা ব্রডকাস্ট করতে চান!**")

    broadcast_msg = m.reply_to_message
    logging.info(f"📡 {user_id} ব্রডকাস্ট শুরু করেছে...")

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
                logging.error(f"❌ ব্যর্থ: {error.strip()}")
            if status == 200:
                broadcast_ids[broadcast_id]["success"] += 1
                logging.info(f"✅ সফল: {user_id}")
            else:
                broadcast_ids[broadcast_id]["failed"] += 1
                if status == 400:
                    await db.delete_user(user_id)
                    logging.warning(f"🗑️ ইউজার রিমুভ করা হলো: {user_id}")
            broadcast_ids[broadcast_id]["current"] += 1

    elapsed_time = str(datetime.timedelta(seconds=int(time.time() - start_time)))
    await msg.delete()

    if broadcast_ids[broadcast_id]["failed"] == 0:
        logging.info(f"✅ ব্রডকাস্ট সফলভাবে সম্পন্ন হয়েছে!\nসময়: {elapsed_time}")
        await m.reply_text(
            f"✅ **ব্রডকাস্ট সম্পন্ন হয়েছে!**\n\n⏳ সময়: `{elapsed_time}`\n👥 মোট ইউজার: `{broadcast_ids[broadcast_id]['total']}`\n✅ সফল: `{broadcast_ids[broadcast_id]['success']}`\n❌ ব্যর্থ: `{broadcast_ids[broadcast_id]['failed']}`"
        )
    else:
        logging.warning(f"⚠️ কিছু ইউজার ব্রডকাস্ট পায়নি, লগ ফাইল সংযুক্ত করা হলো।")
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
        logging.warning(f"⏳ FloodWait: {e.value} সেকেন্ড অপেক্ষা...")
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid) as e:
        return 400, f"{user_id} : {str(e)}\n"
    except Exception as e:
        logging.error(f"❌ Unknown Error: {traceback.format_exc()}")
        return 500, f"{user_id} : {traceback.format_exc()}\n"
        
