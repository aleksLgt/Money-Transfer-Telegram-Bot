from Models.GameSetting import update_start_bonus_value
from Views.MenuAdmin import get_menu_admin


class StartBonusValueEditAction:
    def __init__(self, bot):
        self.bot = bot  # Объект бота

    def start_bonus_value_edit_step_one(self, message):
        self.bot.send_message(message.chat.id, 'Введите новое значение величины изначального размера игровой валюты '
                                               'для игрока')
        self.bot.register_next_step_handler(message, self.start_bonus_value_edit_step_two)

    def start_bonus_value_edit_step_two(self, message):
        if message.text.isdigit():
            update_start_bonus_value(message.text)
            self.bot.send_message(message.chat.id, 'Изначальный размер игровой валюты для игрока был успешно изменен', reply_markup=get_menu_admin())
        else:
            self.bot.send_message(message.chat.id, 'Значение не является числом', reply_markup=get_menu_admin())
