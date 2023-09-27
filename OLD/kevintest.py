import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Your bot token (replace 'YOUR_BOT_TOKEN' with your own token)
TOKEN = '6243320723:AAE6Bip1fb8ltmhUbFyWXE7tdrxdZ9GgDBo'

# Create an updater object
updater = Updater(token=TOKEN, use_context=True)

# Create a dispatcher
dispatcher = updater.dispatcher


def start(update, context):
    # Send multiple messages one after the other
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm your Telegram bot!")
    context.bot.send_message(chat_id=update.effective_chat.id, text="How can I assist you today?")


# Register the start command handler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def echo(update, context):
    # Echo the received message
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# Register the echo message handler
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


def main():
    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()