import sqlite3
from enums.GameStatus import GameStatus


def init_database():
    conn, cur = open_database_connection()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username varchar(50) NOT NULL,'
                'chat_id varchar(100) NOT NULL, is_admin BOOLEAN DEFAULT FALSE)')
    cur.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY AUTOINCREMENT, key varchar(6) UNIQUE NOT "
                "NULL, status INTEGER NOT NULL DEFAULT ('%d'))" % GameStatus.CREATED.value)
    cur.execute('CREATE TABLE IF NOT EXISTS game_settings (id INTEGER PRIMARY KEY AUTOINCREMENT, start_bonus_value '
                'INTEGER NOT NULL, cheat_code VARCHAR(50) NOT NULL, intro_info_message TEXT)')
    cur.execute("SELECT COUNT(*) FROM game_settings")
    result = cur.fetchone()[0]
    if result == 0:
        cur.execute("INSERT INTO game_settings(start_bonus_value, cheat_code) VALUES ('%d', '%s')" % (100, 'AEZAKMI'))
    cur.execute("CREATE TABLE IF NOT EXISTS game_user (id INTEGER PRIMARY KEY AUTOINCREMENT, game_id INTEGER NOT "
                "NULL, user_id INTEGER NOT NULL, balance INTEGER NOT NULL, FOREIGN KEY (game_id) REFERENCES games ("
                "id), FOREIGN KEY (user_id) REFERENCES users (id))")
    # Таблица для хранения транзакций
    cur.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "game_id INTEGER NOT NULL, sender_user_id INTEGER NOT NULL, "
                "beneficiary_user_id INTEGER NOT NULL, transfer_amount INTEGER NOT NULL, "
                "FOREIGN KEY (game_id) REFERENCES games (id), FOREIGN KEY (sender_user_id) REFERENCES game_user (id))")
    conn.commit()
    close_database_connection(cur, conn)


def open_database_connection():
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()

    return conn, cur


def close_database_connection(cur, conn):
    cur.close()
    conn.close()
