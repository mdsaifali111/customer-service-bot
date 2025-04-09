import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json

# Load the environment variables
TOKEN = os.getenv('TELEGRAM_API_TOKEN')  # Fetching Telegram bot token from environment variables
RENDER_URL = os.getenv('RENDER_URL')     # Fetching the Render URL if needed for webhook or any other use

# Predefined FAQs
faq_data = {
    "help": "How can I help you?",
    "hours": "We are available from 9 AM to 6 PM."
}

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Command for /start
def start(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.first_name
    message = f"Hello {user_name}, welcome to our support bot! Join our official channel: [link]. How can we assist you today?"
    update.message.reply_text(message)

# Command for /help
def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("You can ask for help here, or type 'FAQ' to see common questions.")

# Handle messages
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()
    
    # Check if the message matches FAQ
    if user_message in faq_data:
        response = faq_data[user_message]
    else:
        # Save user query if no FAQ match found
        response = "Please wait, our team will respond shortly."
        with open('user_data.json', 'a') as f:
            json.dump({'user': update.message.from_user.id, 'message': update.message.text}, f)
        # Notify admin
        # Here, you can forward the message to admin (if needed)
        notify_admin(update.message.text)
    
    update.message.reply_text(response)

def notify_admin(user_message):
    # Logic to notify admin (optional)
    admin_chat_id = 'YOUR_ADMIN_CHAT_ID'  # Replace with admin's chat ID
    bot.send_message(chat_id=admin_chat_id, text=f"User query: {user_message}")

# Main function to start the bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    # Add message handler to capture user input
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
