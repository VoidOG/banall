from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Token
BOT_TOKEN = "7636888289:AAHbbR1Ku2D9kiiUheLk2yarduG8N1o_WbY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message."""
    await update.message.reply_text("I'm a sticker deletion bot. Use /dStick to delete all stickers in this group.")

async def delete_all_stickers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete all stickers in the group chat and report the count."""
    if update.effective_chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command can only be used in groups!")
        return

    # Check if the bot has delete permissions
    bot_member = await update.effective_chat.get_member(context.bot.id)
    if not bot_member.can_delete_messages:
        await update.message.reply_text("I need delete permissions to remove stickers!")
        return

    # Notify the user that the process has started
    notify_msg = await update.message.reply_text("Deleting all stickers in this group. This might take a while...")

    sticker_count = 0
    last_message_id = None

    try:
        while True:
            # Fetch messages in batches (100 max per call)
            messages = await context.bot.get_chat_history(
                chat_id=update.effective_chat.id,
                limit=100,
                offset_id=last_message_id
            )

            if not messages:  # No more messages to fetch
                break

            for message in messages:
                if message.sticker:
                    try:
                        await context.bot.delete_message(
                            chat_id=update.effective_chat.id,
                            message_id=message.message_id
                        )
                        sticker_count += 1
                    except Exception as e:
                        logger.error(f"Failed to delete sticker: {e}")

            # Update the offset to fetch older messages
            last_message_id = messages[-1].message_id

        # Edit the initial message to show the final count
        await notify_msg.edit_text(f"Deleted {sticker_count} sticker(s) from this group.")
    except Exception as e:
        logger.error(f"Error while fetching or deleting messages: {e}")
        if notify_msg:
            await notify_msg.edit_text("An error occurred while trying to delete stickers.")

def main():
    # Create the application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dStick", delete_all_stickers))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
