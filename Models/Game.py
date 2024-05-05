from database.database import close_database_connection
from database.database import open_database_connection
from enums.GameStatus import GameStatus


def update_key(key):
    conn, cur = open_database_connection()
    cur.execute("UPDATE games SET key = '%s' WHERE id = (SELECT MAX(id) FROM games)" % key)
    conn.commit()
    close_database_connection(cur, conn)


def update_status(game_id):
    conn, cur = open_database_connection()
    cur.execute("UPDATE games SET status = '%d' WHERE id = ('%d')" % (GameStatus.PAUSED.value, game_id))
    conn.commit()
    close_database_connection(cur, conn)

def get_status(chat_id):
    conn, cur = open_database_connection()
    cur.execute("SELECT status FROM games, game_user, users  WHERE "
                "games.id = game_user.game_id AND users.id = game_user.user_id AND users.chat_id = ('%d')" % chat_id)
    result = cur.fetchone()
    if result and result[0] != 0:
        game_status = result[0]
    else:
        game_status = None
    close_database_connection(cur, conn)
    return game_status

def get_game_id_by_chat_id(chat_id):
    conn, cur = open_database_connection()
    cur.execute("SELECT games.id FROM games, game_user, users  WHERE "
                "games.id = game_user.game_id AND users.id = game_user.user_id AND users.chat_id = ('%d')" % chat_id)
    result = cur.fetchone()
    if result and result[0] != 0:
        game_id = result[0]
    else:
        game_id = None
    close_database_connection(cur, conn)
    return game_id

def get_id_by_key(key, status=None):
    conn, cur = open_database_connection()
    if status:
        query = "SELECT id FROM games WHERE key = ('%s') AND status IS NOT ('%d')" % (key, status)
    else:
        query = "SELECT id FROM games WHERE key = ('%s')" % key
    cur.execute(query)
    result = cur.fetchone()
    if result and result[0] != 0:
        game_id = result[0]
    else:
        game_id = None
    close_database_connection(cur, conn)

    return game_id


def is_game_already_exist(key):
    conn, cur = open_database_connection()
    cur.execute(
        "SELECT COUNT(*) FROM games WHERE key = ('%s') AND status IS NOT ('%d')" % (key, GameStatus.STOPPED.value))
    result = cur.fetchone()[0] != 0
    close_database_connection(cur, conn)

    return result


def send_message_to_all_users(bot, game_id):
    conn, cur = open_database_connection()
    cur.execute("SELECT users.chat_id FROM users INNER JOIN game_user ON users.id = game_user.user_id WHERE "
                "game_user.game_id = ('%d')" % game_id)
    chat_ids = [chat_id[0] for chat_id in cur.fetchall()]
    for chat_id in chat_ids:
        try:
            bot.send_message(chat_id,
                             'Игра была приостановлена. Переводы игровой валюты между игроками недоступны.')
        except Exception as e:
            print(f"Ошибка при отправке сообщения на chat_id {chat_id}: {str(e)}")

    close_database_connection(cur, conn)

def commit_transaction(game_id, sender_user_id, beneficiary_user_id, transfer_amount):
    conn, cur = open_database_connection()
    cur.execute("INSERT INTO transactions(game_id, sender_user_id, beneficiary_user_id, "
                "transfer_amount) VALUES (('%s'), ('%s'), ('%s'), ('%s'))" %
                (game_id, sender_user_id, beneficiary_user_id, transfer_amount))
    conn.commit()
    close_database_connection(cur, conn)

