import logging
from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters
from pymongo import MongoClient
import time

# Constants
BOT_TOKEN = "6973619618:AAERC40Khl5U8UM3wKOJoDbCnK7yUEvCl88"
OWNER_ID = 6663845789  # Replace with your Telegram user ID
MONGO_URI = "mongodb+srv://Cenzo:Cenzo123@cenzo.azbk1.mongodb.net/"

# Initialize MongoDB
client = MongoClient(MONGO_URI)
db = client['telegram_bot']
authorized_users_collection = db['authorized_users']

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Helper functions
def is_authorized(user_id: int) -> bool:
    """Check if a user is authorized."""
    return authorized_users_collection.find_one({'user_id': user_id}) is not None

def get_chat_history(context: CallbackContext, chat_id: int):
    """Fetch the chat history."""
    return context.bot.get_chat(chat_id).get_history(limit=100)

# Command Handlers
def start(update: Update, context: CallbackContext) -> None:
    """Check bot aliveness with a ping."""
    start_time = time.time()
    update.message.reply_text("Pong!")
    end_time = time.time()
    logger.info(f"Ping response time: {end_time - start_time:.3f} seconds")

def sauth(update: Update, context: CallbackContext) -> None:
    """Authorize a user (Owner only)."""
    if update.effective_user.id == OWNER_ID:
        if context.args:
            try:
                user_id = int(context.args[0])
                if not is_authorized(user_id):
                    authorized_users_collection.insert_one({'user_id': user_id})
                    update.message.reply_text(f"User {user_id} authorized.")
                else:
                    update.message.reply_text(f"User {user_id} is already authorized.")
            except ValueError:
                update.message.reply_text("Invalid user ID format.")
        else:
            update.message.reply_text("Usage: /sauth <user_id>")
    else:
        update.message.reply_text("You are not authorized to use this command.")

def sunauth(update: Update, context: CallbackContext) -> None:
    """Unauthorize a user (Owner only)."""
    if update.effective_user.id == OWNER_ID:
        if context.args:
            try:
                user_id = int(context.args[0])
                if is_authorized(user_id):
                    authorized_users_collection.delete_one({'user_id': user_id})
                    update.message.reply_text(f"User {user_id} unauthorized.")
                else:
                    update.message.reply_text(f"User {user_id} is not authorized.")
            except ValueError:
                update.message.reply_text("Invalid user ID format.")
        else:
            update.message.reply_text("Usage: /sunauth <user_id>")
    else:
        update.message.reply_text("You are not authorized to use this command.")

def sauthusers(update: Update, context: CallbackContext) -> None:
    """List all authorized users (Owner only)."""
    if update.effective_user.id == OWNER_ID:
        users = authorized_users_collection.find()
        if users.count() > 0:
            user_list = '\n'.join([str(user['user_id']) for user in users])
            update.message.reply_text(f"Authorized users:\n{user_list}")
        else:
            update.message.reply_text("No authorized users.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

def delmedia(update: Update, context: CallbackContext) -> None:
    """Delete all media messages in the chat."""
    if is_authorized(update.effective_user.id):
        chat_id = update.effective_chat.id
        messages = get_chat_history(context, chat_id)
        for message in messages:
            if message.photo or message.video or message.document:
                context.bot.delete_message(chat_id, message.message_id)
        update.message.reply_text("All media deleted.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

def delsticker(update: Update, context: CallbackContext) -> None:
    """Delete all sticker messages in the chat."""
    if is_authorized(update.effective_user.id):
        chat_id = update.effective_chat.id
        messages = get_chat_history(context, chat_id)
        for message in messages:
            if message.sticker:
                context.bot.delete_message(chat_id, message.message_id)
        update.message.reply_text("All stickers deleted.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

def delgif(update: Update, context: CallbackContext) -> None:
    """Delete all GIF messages in the chat."""
    if is_authorized(update.effective_user.id):
        chat_id = update.effective_chat.id
        messages = get_chat_history(context, chat_id)
        for message in messages:
            if message.animation:
                context.bot.delete_message(chat_id, message.message_id)
        update.message.reply_text("All GIFs deleted.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

def help_command(update: Update, context: CallbackContext) -> None:
    """Display the help message."""
    help_text = (
        "/start - Check if the bot is alive\n"
        "/delmedia - Delete all media messages\n"
        "/delsticker - Delete all sticker messages\n"
        "/delgif - Delete all GIF messages\n"
        "/sauth <user_id> - Authorize a user (Owner only)\n"
        "/sunauth <user_id> - Unauthorize a user (Owner only)\n"
        "/sauthusers - List authorized users (Owner only)\n"
        "/help - Show this help message"
    )
    update.message.reply_text(help_text)

# Main Function
def main() -> None:
    """Run the bot."""
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("sauth", sauth))
    dispatcher.add_handler(CommandHandler("sunauth", sunauth))
    dispatcher.add_handler(CommandHandler("sauthusers", sauthusers))
    dispatcher.add_handler(CommandHandler("delmedia", delmedia))
    dispatcher.add_handler(CommandHandler("delsticker", delsticker))
    dispatcher.add_handler(CommandHandler("delgif", delgif))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
