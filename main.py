from pyrogram import Client
from pyrogram.errors import RPCError

# Replace with your Pyrogram string session
STRING_SESSION = "BQGFRPwAtsFV0LWtFbEad6FWm_Z0RONbO2lPgDQYuznA1W6Rz4Boqk202IHdFuaf8BfOJdbqoJIZKPLCx6GFQTLRR3m3779z9ObbmuKz_j6VNDRxJTmisfEcWeOhLmxp_IhdsS_nb1VB5BSl3OQ5ewImP379in6WpuFAnpX_FlA62ilDhxa_1T-cI9fiNgaSqElYJPYdoDw49Xf-dHhKVIplLwoOf4mLN8w2j524uv158Jlob1heelBi49oRBKugvymCG-Mr1hWFkvSgweFzvgDMO02kY7rj0Lydcd6AMP77BemJV_2TJxZDNiwd8St-kENuqLUZWpxJopiJjkOkbkDaNXst3wAAAAGIyZUZAA"

app = Client("my_account", session_string=STRING_SESSION)

async def delete_all_stickers(chat_id):
    """Fetch and delete all sticker messages in the group."""
    deleted_count = 0

    try:
        # Fetch and iterate through messages containing stickers
        async for message in app.search_messages(chat_id, filter="stickers"):
            try:
                await app.delete_messages(chat_id, message.message_id)
                deleted_count += 1
            except RPCError as e:
                print(f"Error deleting message {message.message_id}: {e}")

        print(f"Deleted {deleted_count} stickers from the group.")
    except Exception as e:
        print(f"Error fetching or deleting messages: {e}")

@app.on_message()
async def main(client, message):
    """Main entry point to delete stickers."""
    # Replace `CHAT_ID` with your target group's chat ID or username
    CHAT_ID = -1001994840446  # e.g., -1001234567890 for private groups

    print("Deleting all stickers from the group...")
    await delete_all_stickers(CHAT_ID)

if __name__ == "__main__":
    app.run()  # This automatically calls the `main` handler when a message is received.
