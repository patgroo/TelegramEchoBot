import logging

import Message_saver_to_json
import API
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Welcome.. {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
    Message_saver_to_json.create_json_file()
    print(f"{update.message}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def read_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""

    user = update.effective_user
    print(f"{user.name} requested to read the chat history...")
    history = []
    history = Message_saver_to_json.read_user_file(user.name)
    await update.message.reply_text("Sending Chat History...")
    await update.message.reply_text(history)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # Extract the text message from the update
    message_text = update.message.text
    user = update.effective_user
    # Print the incoming message to the console
    
    print(f"{message_text}, {user.name}")
    Message_saver_to_json.update_user_file(username=user.name, text=message_text)

    # Reply to the user with the same message
    
    API.send_post_request(user, message_text)
    await update.message.reply_text(user)
    await update.message.reply_text(f"Message transfered to API, this was the message: '{message_text}'")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    #
    application = Application.builder().token("6484111519:AAEspSsyiW7Tbxri6bsWRwdJRUl5zHkQNtA").build()

    # on different commands - answer in Telegram
    #
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("read_chat", read_chat_command))

    # on non command i.e message - echo the message on Telegram
    #
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    #
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
