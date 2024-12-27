from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)
import pymongo

# MongoDB Configuration
MONGO_URI = "mongodb+srv://Cenzo:Cenzo123@cenzo.azbk1.mongodb.net/"
client = pymongo.MongoClient(MONGO_URI)
db = client['telegram_bot']

# Bot Configuration
BOT_TOKEN = "6973619618:AAERC40Khl5U8UM3wKOJoDbCnK7yUEvCl88"
OWNER_ID = 6663845789


# --- Functions --- #

# Check bot aliveness
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot is alive and ready! 🟢")

# Add authorized user
def sauth(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return update.message.reply_text("Unauthorized!")
    if len(context.args) != 1:
        return update.message.reply_text("Usage: /sauth <user_id>")
    
    user_id = int(context.args[0])
    if db.auth_users.find_one({"_id": user_id}):
        update.message.reply_text("User already authorized.")
    else:
        db.auth_users.insert_one({"_id": user_id})
        update.message.reply_text(f"User {user_id} authorized.")

# Remove authorized user
def sunauth(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return update.message.reply_text("Unauthorized!")
    if len(context.args) != 1:
        return update.message.reply_text("Usage: /sunauth <user_id>")
    
    user_id = int(context.args[0])
    result = db.auth_users.delete_one({"_id": user_id})
    if result.deleted_count > 0:
        update.message.reply_text(f"User {user_id} unauthorized.")
    else:
        update.message.reply_text("User not found.")

# List authorized users
def sauthusers(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return update.message.reply_text("Unauthorized!")
    
    users = db.auth_users.find({})
    if users.count_documents({}) > 0:
        user_list = "\n".join([str(user["_id"]) for user in users])
        update.message.reply_text(f"Authorized Users:\n{user_list}")
    else:
        update.message.reply_text("No authorized users.")

# Delete media
def delmedia(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_authorized(update.effective_user.id):
        return update.message.reply_text("Unauthorized!")

    context.bot.delete_message(chat_id, update.message.message_id)

# Delete stickers
def delsticker(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_authorized(update.effective_user.id):
        return update.message.reply_text("Unauthorized!")

    if update.message.sticker:
        context.bot.delete_message(chat_id, update.message.message_id)

# Delete GIFs
def delgif(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_authorized(update.effective_user.id):
        return update.message.reply_text("Unauthorized!")

    if update.message.animation:
        context.bot.delete_message(chat_id, update.message.message_id)

# Help command
def help_command(update: Update, context: CallbackContext):
    help_text = """
/start - Check if the bot is alive.
/sauth <user_id> - Authorize a user. (Owner only)
/sunauth <user_id> - Unauthorize a user. (Owner only)
/sauthusers - List all authorized users. (Owner only)
/delmedia - Delete all media.
/delsticker - Delete all stickers.
/delgif - Delete all GIFs.
    """
    update.message.reply_text(help_text)

# Check if user is authorized
def is_authorized(user_id):
    return db.auth_users.find_one({"_id": user_id}) is not None

# Error handler
def error_handler(update: Update, context: CallbackContext):
    print(f"Error: {context.error}")


# --- Main Function --- #

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Command Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("sauth", sauth))
    dispatcher.add_handler(CommandHandler("sunauth", sunauth))
    dispatcher.add_handler(CommandHandler("sauthusers", sauthusers))
    dispatcher.add_handler(CommandHandler("delmedia", delmedia))
    dispatcher.add_handler(CommandHandler("delsticker", delsticker))
    dispatcher.add_handler(CommandHandler("delgif", delgif))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Error Handler
    dispatcher.add_error_handler(error_handler)

    # Start Bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
