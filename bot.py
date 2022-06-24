from telegram import Update
from telegram.ext import Filters, Updater
from telegram.ext import CommandHandler, CallbackContext, MessageHandler


states_db = {}


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text = 'Приветствую'
    )
    return 'ECHO'


def echo(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=update.message.text
    )
    return


def handle_user_reply(update: Update, context: CallbackContext):
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id

    else:
        return
    
    if user_reply == '/start':
        user_state = 'START'
    elif user_reply != '/start':
        update.message.reply_text(
            text='Для начала работы с ботом, напишите /start'
        )
    else:
        user_state = states_db.get(chat_id)
    
    states_functions = {
        'START': start,
        'ECHO': echo
    }
    
    state_handler = states_functions[user_state]
    next_state = state_handler(update, context)
    states_db.update({chat_id: next_state})
    

def main():
    # token = 
    updater = Updater('5431788933:AAH2H7NBFbhRZki4r6-mn2diy4asvJLUtgI')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', handle_user_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_user_reply ))
    updater.start_polling()


if __name__ == "__main__":
    main()