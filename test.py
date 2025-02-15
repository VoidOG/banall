import asyncio
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

# Fixed API ID and API HASH
API_ID = 28561722  # Replace with your API ID
API_HASH = "a538ba07656f746def99bed7032121cc"  # Replace with your API HASH

# User Input for String Session
STRING_SESSION = input("Enter Your String Session: ")

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

# Ban rights (permanent ban)
RIGHTS = ChatBannedRights(
    until_date=None, view_messages=True, send_messages=True, send_media=True,
    send_stickers=True, send_gifs=True, send_games=True, send_polls=True,
    change_info=True, invite_users=True, pin_messages=True
)

@client.on(events.NewMessage(pattern="^/banall$"))
async def banall(event):
    """ Ban-All with Floodwait 0.1s """
    if not event.is_group:
        return await event.reply("Use this command in a group!")

    chat = await event.get_chat()
    admins = await client.get_participants(chat, filter=functions.channels.ChannelParticipantsAdmins)
    admin_ids = {admin.id for admin in admins}

    await event.reply(
        "**Aᴛᴛᴇɴᴛɪᴏɴ, ᴜɴᴅᴇʀʟɪɴɢs! Tʜᴇ ʙᴀɴ-ᴀʟʟ ᴅᴇᴄʀᴇᴇ ʜᴀs ʙᴇᴇɴ sᴇᴛ ɪɴᴛᴏ ᴍᴏᴛɪᴏɴ...**"
    )

    total, banned = 0, 0
    async for user in client.iter_participants(chat):
        total += 1
        if user.id not in admin_ids:
            try:
                await client(EditBannedRequest(chat.id, user.id, RIGHTS))
                banned += 1
                await asyncio.sleep(0.1)  # Floodwait 0.1s
            except Exception:
                pass

    await event.reply(
        f"**Tʜᴇ Bᴀɴ-ᴀʟʟ ᴘʀᴏᴄᴇss ʜᴀs ʙᴇᴇɴ ғɪɴɪsʜᴇᴅ !**\n"
        f"**Tʜɪs ɢᴄ ʜᴀs ʙᴇᴇɴ ᴇʀᴀᴅɪᴄᴀᴛᴇᴅ ʙʏ ᴛʜᴇ ᴍᴀssᴀᴄʀᴇs !**\n\n"
        f"**Tʜᴇ Fᴇᴡ Tʜᴇ Fᴇᴀʀʟᴇss. !**\n\n"
        f"**Banned Users:** `{banned}` \n **From Total Users:** `{total}`"
    )

client.start()
client.run_until_disconnected()
