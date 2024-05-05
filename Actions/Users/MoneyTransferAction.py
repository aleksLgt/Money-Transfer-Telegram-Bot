from Models.GameUser import (user_in_game_by_username, get_balance_by_chat_id, debiting_funds_by_chat_id,
                             replenishment_funds_by_user_id, get_game_user_id_by_chat_id,
                             get_game_user_id_by_user_id)
from Models.Game import get_status, get_game_id_by_chat_id, commit_transaction
from Models.User import get_id, get_chat_id, get_username
class MoneyTransferAction:
    def __init__(self, bot):
        self.bot = bot

    def moneyTransfer_step_one(self, message):
        # Проверка статуса игры
        status_game = get_status(message.chat.id)
        if status_game == 1:
            self.bot.send_message(message.chat.id, 'Введите username игрока, которому желаете перевести средства')
            self.bot.register_next_step_handler(message, self.moneyTransfer_step_two)
        else:
            self.bot.send_message(message.chat.id, 'Невозможно перевести средства! Игра на паузе или ее не существует.')

    def moneyTransfer_step_two(self, message):
        # Проверка на участие в игре
        username = message.text
        is_in_game = user_in_game_by_username(username)
        if is_in_game:
            self.bot.send_message(message.chat.id, 'Введите сумму средств для перевода игроку с именем: ' + username)
            self.bot.register_next_step_handler(message, self.moneyTransfer_step_three, username)
        else:
            self.bot.send_message(message.chat.id, 'Игрок не найден! Уточните имя игрока и попробуйте еще раз.')

    def moneyTransfer_step_three(self, message, username):
        # Проверка на наличие средств
        amount = message.text
        balance = get_balance_by_chat_id(message.chat.id)
        difference = balance - int(amount)
        if difference >= 0:
            # Обновляем баланс отправителя
            debiting_funds_by_chat_id(message.chat.id,  difference)
            # Обновляем баланс получателя
            user_id = get_id(username)
            replenishment_funds_by_user_id(user_id, amount)
            # Фиксируем тразакцию
            commit_transaction(get_game_id_by_chat_id(message.chat.id), get_game_user_id_by_chat_id(message.chat.id),
                                get_game_user_id_by_user_id(user_id), amount)
            self.bot.send_message(message.chat.id, 'Вы успешно перевели средства игроку ' + username + ', на сумму: ' +
                                  str(amount) + '\n' + 'Ваш баланс: ' + str(get_balance_by_chat_id(message.chat.id)))

            self.bot.send_message(get_chat_id(username), 'Вам перевел средства игрок ' + get_username(message.chat.id) +
                                  ', в размере ' + str(amount) + '\n' + 'Ваш баланс: ' + str(get_balance_by_chat_id(
                                    get_chat_id(username))))
        else:
            self.bot.send_message(message.chat.id, 'Игрок не найден! Уточните имя игрока и попробуйте еще раз.')
