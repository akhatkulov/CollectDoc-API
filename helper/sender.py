from telebot import TeleBot
import conf

bot = TeleBot(conf.BOT_TOKEN)

def zip_sender(x,p_caption):
    with open(x, 'rb') as file:
                bot.send_document(conf.CHANNEL_ID, file, caption=p_caption)
