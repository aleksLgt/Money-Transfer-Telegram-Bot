from Models.GameSetting import get_start_bonus_value
from database.database import close_database_connection
from database.database import open_database_connection


def bind_user_with_game(game_id, user_id):
    conn, cur = open_database_connection()
    start_bonus_value = get_start_bonus_value()
    cur.execute("INSERT INTO game_user(game_id, user_id, balance) VALUES ('%d', '%d', '%d')" % (
        game_id, user_id, start_bonus_value))
    conn.commit()
    close_database_connection(cur, conn)

def debiting_funds_by_chat_id(chat_id, new_balance):
    conn, cur = open_database_connection()
    cur.execute("UPDATE game_user SET balance = ('%s') WHERE user_id = (select user_id from game_user, users WHERE "
                "game_user.user_id = users.id And users.chat_id = ('%s'))" % (new_balance, chat_id))
    conn.commit()
    close_database_connection(cur, conn)

def replenishment_funds_by_user_id(user_id, amount):
    conn, cur = open_database_connection()
    cur.execute("UPDATE game_user SET balance = balance + ('%s') WHERE user_id = ('%s')" % (amount, user_id))
    conn.commit()
    close_database_connection(cur, conn)

def balance_by_user_id(user_id):
    conn, cur = open_database_connection()
    cur.execute("SELECT balance from game_user WHERE game_id = ('%d') AND user_id = ('%d')" % (user_id))
    result = cur.fetchone()
    if result:
        balance = result[0]
    else:
        balance = None
    close_database_connection(cur, conn)

    return balance

def get_balance(game_id, user_id):
    conn, cur = open_database_connection()
    cur.execute("SELECT balance from game_user WHERE game_id = ('%d') AND user_id = ('%d')" % (
        game_id, user_id))
    result = cur.fetchone()
    if result:
        balance = result[0]
    else:
        balance = None
    close_database_connection(cur, conn)

    return balance

def get_balance_by_chat_id(chat_id):
    conn, cur = open_database_connection()
    cur.execute("SELECT balance from game_user, users WHERE game_user.user_id = users.id And users.chat_id = ('%s')"
                % chat_id)
    result = cur.fetchone()
    if result:
        balance = result[0]
    else:
        balance = None
    close_database_connection(cur, conn)

    return balance


def get_game_user_id_by_chat_id(chat_id):
    conn, cur = open_database_connection()
    cur.execute(
        "SELECT game_user.id from game_user, users WHERE game_user.user_id = users.id And users.chat_id = ('%s')"
        % chat_id)
    result = cur.fetchone()
    if result:
        game_user_id = result[0]
    else:
        game_user_id = None
    close_database_connection(cur, conn)

    return game_user_id


def get_game_user_id_by_user_id(user_id):
    conn, cur = open_database_connection()
    cur.execute("SELECT game_user.id from game_user, users WHERE game_user.user_id = users.id And users.id = ('%s')"
                % user_id)
    result = cur.fetchone()
    if result:
        game_user_id = result[0]
    else:
        game_user_id = None
    close_database_connection(cur, conn)

    return game_user_id


def user_in_game(chat_id):
    """Находится ли пользователь в игре"""
    conn, cur = open_database_connection()
    cur.execute("SELECT COUNT(*) FROM users, game_user  WHERE users.id = game_user.user_id AND users.chat_id = ('%s')"
                % chat_id)
    result = cur.fetchone()[0] != 0
    close_database_connection(cur, conn)

    return result


def user_in_game_by_username(username):
    conn, cur = open_database_connection()
    cur.execute("SELECT COUNT(*) FROM users, game_user  WHERE users.id = game_user.user_id AND users.username = ('%s')"
                % username)
    result = cur.fetchone()[0] != 0
    close_database_connection(cur, conn)

    return result


def get_user_id(chat_id):
    """Получение id пользователя по chat id"""
    conn, cur = open_database_connection()
    cur.execute("SELECT id FROM users WHERE chat_id = ('%d')" % chat_id)
    result = cur.fetchone()
    if result:
        user_id = result[0]
    else:
        user_id = None
    close_database_connection(cur, conn)

    return user_id


def disconnecting_user_from_game(user_id):
    """Удаление пользователя из игры"""
    conn, cur = open_database_connection()
    cur.execute("DELETE FROM game_user WHERE user_id = ('%d')" % user_id)
    conn.commit()
    close_database_connection(cur, conn)


def get_transaction_history(username, user_id):
    conn, cur = open_database_connection()
    cur.execute("SELECT ('%s') AS username, \"->\" AS curs, transfer_amount, usr.username AS username "
                "FROM transactions AS trns, game_user AS gu, users AS usr WHERE trns.sender_user_id = ('%s') AND "
                "trns.beneficiary_user_id = gu.id AND gu.user_id = usr.id UNION ALL "
                "SELECT ('%s'), \"<-\", transfer_amount, usr.username "
                "FROM transactions AS trns, game_user AS gu, users AS usr "
                "WHERE trns.beneficiary_user_id = ('%s') AND "
                "trns.sender_user_id = gu.id AND gu.user_id = usr.id" % (username, user_id, username, user_id))
    result = cur.fetchall()
    if result:
        table = result
    else:
        table = None
    close_database_connection(cur, conn)
    return table
