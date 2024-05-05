from Models.GameUser import get_balance_by_chat_id
class GetUserBalanceAction:
    def __init__(self, bot):
        self.bot = bot
    def get_user_balance(self, message):
        balance = get_balance_by_chat_id(message.chat.id)
        if balance is not None:
            self.bot.send_message(message.chat.id, 'Ваш баланс: ' + str(balance))
        else:
            self.bot.send_message(message.chat.id, 'Вашего счета не существует! Вы не зарегистрированы в игре.')
