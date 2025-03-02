
from configs import Config
from handlers.database import db
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import asyncio


async def AddUserToDatabase(bot: Client, cmd: Message):
    user_id = cmd.from_user.id
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)

        if Config.LOG_CHANNEL:
            try:
                await bot.send_message(
                    int(Config.LOG_CHANNEL),
                    f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={user_id}) started @{Config.BOT_USERNAME} !!"
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as err:
                print(f"LOG_CHANNEL Error: {err}")
