from database.database import close_database_connection
from database.database import open_database_connection


def create(username, chat_id):
    conn, cur = open_database_connection()
    cur.execute("INSERT INTO users(username, chat_id) VALUES ('%s', '%d')" % (username, chat_id))
    conn.commit()
    close_database_connection(cur, conn)


def set_is_admin(username):
    conn, cur = open_database_connection()
    cur.execute("UPDATE users SET is_admin = True WHERE username = ('%s')" % username)
    conn.commit()
    close_database_connection(cur, conn)


def is_user_already_exist(username):
    conn, cur = open_database_connection()
    cur.execute("SELECT COUNT(*) FROM users WHERE username = ('%s')" % username)
    result = cur.fetchone()[0] != 0
    close_database_connection(cur, conn)

    return result


def get_id(username):
    conn, cur = open_database_connection()
    cur.execute("SELECT id FROM users WHERE username = ('%s')" % username)

    result = cur.fetchone()
    if result and result[0] != 0:
        user_id = result[0]
    else:
        user_id = None
    close_database_connection(cur, conn)

    return user_id


def is_admin(chat_id):
    conn, cur = open_database_connection()
    cur.execute("SELECT is_admin FROM users WHERE chat_id = ('%s')" % chat_id)

    result = cur.fetchone()
    if result:
        response = result[0]
    else:
        response = False
    close_database_connection(cur, conn)

    return response

def get_chat_id(username):
    conn, cur = open_database_connection()
    cur.execute("SELECT chat_id FROM users WHERE username = ('%s')" % username)

    result = cur.fetchone()
    if result:
        chat_id = result[0]
    else:
        chat_id = None
    close_database_connection(cur, conn)

    return chat_id

def get_username(chat_id):
    conn, cur = open_database_connection()
    cur.execute("SELECT username FROM users WHERE chat_id = ('%s')" % chat_id)

    result = cur.fetchone()
    if result:
        username = result[0]
    else:
        username = None
    close_database_connection(cur, conn)

    return username
