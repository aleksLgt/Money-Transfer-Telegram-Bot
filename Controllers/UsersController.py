from Actions.Users.RegAction import RegUserAction
from Actions.Users.DeRegAction import DeRegUserAction
from Actions.Users.MoneyTransferAction import MoneyTransferAction
from Actions.Users.GetBalanceAction import GetUserBalanceAction
from Actions.Users.GetTransactionHistoryAction import GetTransactionHistoryAction

KEY_SIZE = 6


def init_user_methods(bot):
    @bot.message_handler(commands=['reg'])
    def main(message):
        action = RegUserAction(bot)
        action.reg_step_one(message)

    @bot.message_handler(commands=['dereg'])
    def main(message):
        action = DeRegUserAction(bot)
        action.dereg(message)

    @bot.message_handler(commands=['transfer'])
    def main(message):
        action = MoneyTransferAction(bot)
        action.moneyTransfer_step_one(message)

    @bot.message_handler(commands=['balance'])
    def main(message):
        action = GetUserBalanceAction(bot)
        action.get_user_balance(message)

    @bot.message_handler(commands=['transactionHistory'])
    def main(message):
        action = GetTransactionHistoryAction(bot)
        action.get_transaction_history_action(message)