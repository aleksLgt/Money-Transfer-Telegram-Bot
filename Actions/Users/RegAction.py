from Models.Game import is_game_already_exist, get_id_by_key as get_game_id_by_key
from Models.GameSetting import get_cheat_code, get_intro_info_message
from Models.GameUser import bind_user_with_game as bind_user_with_game, get_balance
from Models.User import create as create_user, set_is_admin, is_user_already_exist, get_id as get_user_id
from Views.MenuAdmin import get_menu_admin
from enums.GameStatus import GameStatus


class RegUserAction:
    def __init__(self, bot):
        self.bot = bot  # Объект бота

    def reg_step_one(self, message):
        self.bot.send_message(message.chat.id, 'Введите ваш username')
        self.bot.register_next_step_handler(message, self.reg_step_two)

    def reg_step_two(self, message):
        username = message.text

        def reg_step_three(message):
            words = message.text.split()
            cheat_code = get_cheat_code()

            if len(words) >= 2 and words[1] == cheat_code:
                if not is_user_already_exist(username):
                    create_user(username, message.chat.id)
                set_is_admin(username)

                self.bot.send_message(message.chat.id, 'Вы перешли в режим администратора', reply_markup=get_menu_admin())

            else:
                if not is_game_already_exist(message.text):
                    self.bot.send_message(message.chat.id, 'Игры с таким ключом не существует')
                else:
                    if not is_user_already_exist(username):
                        create_user(username, message.chat.id)

                    user_id = get_user_id(username)
                    game_id = get_game_id_by_key(message.text, GameStatus.STOPPED.value)

                    bind_user_with_game(game_id, user_id)
                    balance = get_balance(game_id, user_id)
                    intro_info_message = get_intro_info_message()
                    self.bot.send_message(message.chat.id, f'Вы успешно зарегистрированы в игре! \n'
                                                           f'{intro_info_message} \n'
                                                           f'Ваш баланс: {balance}')
        self.bot.send_message(message.chat.id, 'Введите уникальный ключ игры')
        self.bot.register_next_step_handler(message, reg_step_three)
