from database.database import close_database_connection
from database.database import open_database_connection


def update_start_bonus_value(start_bonus_value):
    conn, cur = open_database_connection()
    cur.execute("UPDATE game_settings SET start_bonus_value = '%d' "
                "WHERE id = (SELECT MAX(id) FROM game_settings)" % int(start_bonus_value))
    conn.commit()
    close_database_connection(cur, conn)


def get_cheat_code():
    conn, cur = open_database_connection()
    cur.execute("SELECT cheat_code FROM game_settings")
    cheat_code = cur.fetchone()[0]
    close_database_connection(cur, conn)

    return cheat_code


def get_intro_info_message():
    conn, cur = open_database_connection()
    cur.execute("SELECT intro_info_message FROM game_settings")
    intro_info_message = cur.fetchone()[0]
    close_database_connection(cur, conn)

    return intro_info_message


def get_start_bonus_value():
    conn, cur = open_database_connection()
    cur.execute("SELECT start_bonus_value FROM game_settings")
    start_bonus_value = cur.fetchone()[0]
    close_database_connection(cur, conn)

    return start_bonus_value
