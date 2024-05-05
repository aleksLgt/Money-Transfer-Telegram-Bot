from os import getenv

import telebot
from database.database import init_database
from Controllers.AdminsController import init_admin_methods
from Controllers.UsersController import init_user_methods
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
telegram_bot_token = getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(telegram_bot_token)


@bot.message_handler(commands=['start'])
def main(message):
    init_database()

    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')


init_user_methods(bot)
init_admin_methods(bot)

bot.infinity_polling()
