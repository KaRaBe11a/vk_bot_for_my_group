import pymysql

from configs.MYSQL import config


def make_connection():
    connection = pymysql.Connection(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        database=config.db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


def get_user_id_by_vk_id(vk_id):
    try:
        connection = make_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM `all_users` WHERE id_vk=%s", (vk_id))
                id = cursor.fetchall()
                return id[0]['id']
        finally:
            connection.close()

    except Exception as ex:
        print("get_id_by_vk_id")
        print(ex)


def get_homeworks_id_by_user_id(id):
    try:
        connection = make_connection()
        try:

            with connection.cursor() as cursor:

                cursor.execute("SELECT id_homework, status FROM `users` WHERE id=%s", id)
                id_homeworks = cursor.fetchall()
            return id_homeworks
        finally:
            connection.close()
    except Exception as ex:
        print("get_homeworks_id_by_user_id")
        print(ex)