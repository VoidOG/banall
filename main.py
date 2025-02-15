import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

# Fixed API ID & Hash
API_ID = 28561722  # Replace with your API ID
API_HASH = "a538ba07656f746def99bed7032121cc"

# User Input for String Session
STRING_SESSION = input("Enter Your String Session: ")

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

async def ban_all_members(chat_id):
    banned = 0
    async for user in app.get_chat_members(chat_id):
        try:
            if not user.user.is_bot:  # Don't ban bots
                await app.ban_chat_member(chat_id, user.user.id)
                banned += 1
                await asyncio.sleep(0.1)  # Prevent FloodWait
        except FloodWait as e:
            await asyncio.sleep(e.value)  # Auto-handle floodwait

    return banned

@app.on_message(filters.command("banall") & filters.user("me"))  # Only session owner
async def banall_handler(client, message):
    chat_id = message.chat.id
    await message.reply(
        "**Aᴛᴛᴇɴᴛɪᴏɴ, ᴜɴᴅᴇʀʟɪɴɢs! Tʜᴇ ʙᴀɴ-ᴀʟʟ ᴅᴇᴄʀᴇᴇ ʜᴀs ʙᴇᴇɴ sᴇᴛ ɪɴᴛᴏ ᴍᴏᴛɪᴏɴ,**\n"
        "**ᴘʀᴏᴘᴇʟʟᴇᴅ ʙʏ ᴛʜᴇ ɪᴍᴘᴀᴄᴛ ᴏғ Tʜᴇ ᴍᴀssᴀᴄʀᴇs.**\n"
        "**Pʀᴇᴘᴀʀᴇ ғᴏʀ ᴛʜᴇ ʀɪᴘᴘʟᴇ ᴇғғᴇᴄᴛ ᴏғ ᴏᴜʀ ᴍᴀʟᴇᴠᴏʟᴇɴᴛ ᴅᴇᴇᴅs...**"
    )

    banned = await ban_all_members(chat_id)
    total = len([m async for m in app.get_chat_members(chat_id)])

    await message.reply(
        f"**Tʜᴇ Bᴀɴ-ᴀʟʟ ᴘʀᴏᴄᴇss ʜᴀs ʙᴇᴇɴ ғɪɴɪsʜᴇᴅ!**\n"
        f"**Tʜɪs ɢᴄ ʜᴀs ʙᴇᴇɴ ᴇʀᴀᴅɪᴄᴀᴛᴇᴅ ʙʏ ᴛʜᴇ ᴍᴀssᴀᴄʀᴇs!**\n\n"
        f"**Tʜᴇ Fᴇᴡ. Tʜᴇ Fᴇᴀʀʟᴇss!**\n\n"
        f"**Banned Users:** `{banned}`\n"
        f"**From Total Users:** `{total}`"
    )

app.run()
