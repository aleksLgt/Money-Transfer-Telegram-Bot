from Models.GameUser import get_transaction_history, get_game_user_id_by_chat_id
from Models.User import get_username
class GetTransactionHistoryAction:
    def __init__(self, bot):
        self.bot = bot

    def get_transaction_history_action(self, message):
        game_user_id = get_game_user_id_by_chat_id(message.chat.id)
        if game_user_id is not None:
            username = get_username(message.chat.id)
            table_history = get_transaction_history(username, game_user_id)
            if table_history is not None:
                self.bot.send_message(message.chat.id, 'История операций с Вашем счетом: ')
                str_table_history = " "
                for row in table_history:
                    for elem in row:
                        str_table_history += " " + str(elem)
                    str_table_history += "\n"
                self.bot.send_message(message.chat.id, str_table_history)

            else:
                self.bot.send_message(message.chat.id,
                                      'История операций не найдена. Зарегистрируйтесь в игре.')
        else:
            self.bot.send_message(message.chat.id, 'Вы не зарегистрированны! Зарегистрируйтесь и повторите операцию.')
