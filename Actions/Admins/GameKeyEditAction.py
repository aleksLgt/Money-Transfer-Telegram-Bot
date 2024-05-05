from Models.Game import update_key as update_game_key
from Views.MenuAdmin import get_menu_admin


class GameKeyEditAction:
    KEY_SIZE = 6

    def __init__(self, bot):
        self.bot = bot  # Объект бота

    def game_key_edit_step_one(self, message):
        self.bot.send_message(message.chat.id, 'Введите новый шестисимвольный ключ')
        self.bot.register_next_step_handler(message, self.game_key_edit_step_two)

    def game_key_edit_step_two(self, message):
        if message.text.isdigit() and len(message.text) == self.KEY_SIZE:
            update_game_key(message.text)
            self.bot.send_message(message.chat.id, 'Ключ был успешно изменен', reply_markup=get_menu_admin())
        else:
            self.bot.send_message(message.chat.id, 'Некорректный формат для ключа (6 символов)',
                                  reply_markup=get_menu_admin())
