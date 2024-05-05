from Models.Game import update_status as update_game_status, get_id_by_key as get_game_id_by_key, send_message_to_all_users
from Views.MenuAdmin import get_menu_admin


class GamePauseAction:
    def __init__(self, bot):
        self.bot = bot  # Объект бота

    def game_pause_step_one(self, message):
        self.bot.send_message(message.chat.id, 'Введите уникальный ключ игры')
        self.bot.register_next_step_handler(message, self.game_pause_step_two)

    def game_pause_step_two(self, message):
        game_id = get_game_id_by_key(message.text)
        if game_id:
            update_game_status(game_id)
            send_message_to_all_users(self.bot, game_id)
            self.bot.send_message(message.chat.id, 'Сообщение о приостановке игры было разослано всем игрокам', reply_markup=get_menu_admin())
        else:
            self.bot.send_message(message.chat.id, 'Игры с таким уникальным ключом не существует', reply_markup=get_menu_admin())


