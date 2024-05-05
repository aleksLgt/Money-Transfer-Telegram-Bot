from Models.GameUser import user_in_game, disconnecting_user_from_game, get_user_id

class DeRegUserAction:
    """Описание дерегистрации пользователя"""
    def __init__(self, bot):
        self.bot = bot

    def dereg(self, message):
        """Проверка на участие в игре"""
        is_in_game = user_in_game(message.chat.id)
        if is_in_game:
            user_id = get_user_id(message.chat.id)
            disconnecting_user_from_game(user_id)
            self.bot.send_message(message.chat.id, 'Вы успешно покинули игру!')
        else:
            self.bot.send_message(message.chat.id, 'Не возможно удалить Вас из игры, так ка вы не зарегистрированы!')