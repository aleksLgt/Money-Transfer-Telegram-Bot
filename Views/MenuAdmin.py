from telebot import types


def get_menu_admin():
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton('Изменить уникальный ключ игры', callback_data='gameKeyEdit')
    btn2 = types.InlineKeyboardButton('Пауза игры', callback_data='gamePause')
    btn3 = types.InlineKeyboardButton('Изменить величину изначального размера игровой валюты', callback_data='startBonusValueEdit')

    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)

    return markup
