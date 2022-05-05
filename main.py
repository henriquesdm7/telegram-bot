import logging
import signal
from decouple import config
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
updater = Updater(token=config('TELEGRAM_BOT_TOKEN'))
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update:Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def debug_exit(update:Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Closing bot...")
    # signal.signal(signal.SIGINT, signal.SIG_DFL)
    updater.stop() # não funciona se dentro de um handler (aqui)

# Handlers
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
debug_exit_handler = CommandHandler('exit', debug_exit)


# Adds the handlers to the dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(debug_exit_handler)

# Start the bot
updater.start_polling()
updater.idle()