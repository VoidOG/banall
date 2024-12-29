from pyrogram import Client
from pyrogram.errors import RPCError

# Replace with your Pyrogram string session
STRING_SESSION = "BQE8lCYAIILy1bqWn_JZB00JGpSlqGV6QCtBdwFBc17rsbGqcBeHrNBUKz0nugHOnMnhVhIUdKilAMr0V5IVjUnUooko1TYo2ps8LbgNhtEJYzU8IXlpUuxEKasB7kmcmn2Z5xXGChzRMkS7-2v6PuPdKGN-az8L_Rp4nVYO8G7eiY7gS6hbxmg3omM6Yq80RKmng27RvAW-wEd5ZHvVm6pbFZRhCmGtlpVV_LMfg5b5kUrT_mylLxUI6h2JC1YK4pnaUDka-LV2G_P2EmuvdDHN6ZdoRs8yG4v98X2Q0jUOTatLWP1vXcCGyQdzYfEVuZ59mS15QZ7emBCOBHCsCY_KqsoAAAAAGIyZUZAA"

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
async def main(client):
    """Main entry point to delete stickers."""
    # Replace `CHAT_ID` with your target group's chat ID or username
    CHAT_ID = "-1001994840446"  # e.g., -1001234567890 for private groups

    print("Deleting all stickers from the group...")
    await delete_all_stickers(CHAT_ID)

if __name__ == "__main__":
    app.run(main())
