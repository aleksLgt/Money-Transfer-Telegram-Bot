from Actions.Admins.GameKeyEditAction import GameKeyEditAction
from Actions.Admins.GamePauseAction import GamePauseAction
from Actions.Admins.StartBonusValueEditAction import StartBonusValueEditAction
from Models.User import is_admin


def init_admin_methods(bot):
    @bot.message_handler(commands=['gameKeyEdit'])
    def main(message):
        if is_admin(message.chat.id):
            action = GameKeyEditAction(bot)
            action.game_key_edit_step_one(message)

    @bot.message_handler(commands=['startBonusValueEdit'])
    def main(message):
        if is_admin(message.chat.id):
            action = StartBonusValueEditAction(bot)
            action.start_bonus_value_edit_step_one(message)

    @bot.message_handler(commands=['gamePause'])
    def main(message):
        if is_admin(message.chat.id):
            action = GamePauseAction(bot)
            action.game_pause_step_one(message)

    @bot.callback_query_handler(func=lambda callback: True)
    def handle_callback_query(callback):
        if not is_admin(callback.message.chat.id):
            return
        if callback.data == 'gameKeyEdit':
            action = GameKeyEditAction(bot)
            action.game_key_edit_step_one(callback.message)
        elif callback.data == 'startBonusValueEdit':
            action = StartBonusValueEditAction(bot)
            action.start_bonus_value_edit_step_one(callback.message)
        elif callback.data == 'gamePause':
            action = GamePauseAction(bot)
            action.game_pause_step_one(callback.message)
