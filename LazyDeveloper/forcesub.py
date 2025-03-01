import asyncio
from configs import Config
from pyrogram import Client, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

async def ForceSub(bot: Client, cmd: Message):
    try:
        user = await bot.get_chat_member(
            chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL),
            user_id=cmd.from_user.id
        )
        
        if user.status == "kicked":
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text="Hello hunter! I think you are **Banned** from using me.\n"
                     "Request unban to [LazyDeveloper](https://t.me/mRiderDM).",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_to_message_id=cmd.id
            )
            return 400

    except UserNotParticipant:
        try:
            invite_link = await bot.create_chat_invite_link(
                chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL)
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            invite_link = await bot.create_chat_invite_link(
                chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL)
            )
        except Exception as err:
            print(f"Unable to create invite link for {Config.UPDATES_CHANNEL}\n\nError: {err}")
            return 200

        await bot.send_photo(
            chat_id=cmd.from_user.id,
            photo="https://envs.sh/ifc.jpg",
            caption=(
                "ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜꜱᴇ ᴍᴇ, ʏᴏᴜ ᴍᴜꜱᴛ ꜰɪʀꜱᴛ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ.\n\n"
                "ᴄʟɪᴄᴋ ᴏɴ **'✇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ✇'** ʙᴜᴛᴛᴏɴ.\n"
                "ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ **'ʀᴇǫᴜᴇꜱᴛ ᴛᴏ ᴊᴏɪɴ'** ʙᴜᴛᴛᴏɴ.\n"
                "ᴀꜰᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴄʟɪᴄᴋ ᴏɴ **'🔄 Refresh'** ʙᴜᴛᴛᴏɴ."
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ✇", url=invite_link.invite_link)],
                [InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ 🔄", callback_data="refreshForceSub")]
            ]),
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_to_message_id=cmd.id
        )
        return 400

    except Exception as e:
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="⚠️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ᴛʜɪɴᴋ ʏᴏᴜ'ʀᴇ ǫᴜɪᴛᴇ sᴍᴀʀᴛ.  
ᴅᴏɴ'ᴛ ᴛʀʏ ᴛᴏ ᴀᴄᴛ ᴛᴏᴏ ᴄʟᴇᴠᴇʀ ᴡɪᴛʜ ᴍᴇ.😂.\n"
                 "»» ғɪʀsᴛ, ᴊᴏɪɴ ᴛʜᴇ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ, ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴛʜᴇ ʀᴇғʀᴇsʜ ʙᴜᴛᴛᴏɴ 🔄 .",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_to_message_id=cmd.id
        )
        return 400
    
    return 200
