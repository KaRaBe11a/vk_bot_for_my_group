from homework import homework_back


def AddHomework(request):
    try:
        connection = homework_back.make_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO `homeworks` (subject, description, deadline) VALUES (%s, %s, %s)",
                           (request['Subject'], request['Description'], request['DeadLine']))

        id_homework = cursor.lastrowid
        cursor.execute("SELECT id FROM `all_users`")
        users_id = cursor.fetchall()

        for id in users_id:
            cursor.execute("INSERT INTO `users` (id, id_homework, status) VALUES (%s, %s, %s)",
                           (id['id'], id_homework, "Нужно сделать"))
        connection.commit()
        return "complete"
    finally:
        connection.close()


def change_status_homework(vk_id, homework_id):
    connection = homework_back.make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE `users` SET status=%s WHERE id=%s AND id_homework=%s",
                           ("Сделанно", int(homework_back.get_user_id_by_vk_id(vk_id)), homework_id))
            connection.commit()
        return "Молодец"
    finally:
        connection.close()


def get_all_homeworks_by_vk_id(vk_id):
    connection = homework_back.make_connection()
    try:
        with connection.cursor() as cursor:
            user_id = homework_back.get_user_id_by_vk_id(vk_id)

            id_homeworks = homework_back.get_homeworks_id_by_user_id(user_id)
            homeworks_result = []
            homeworks = []
            for id_h in id_homeworks:
                cursor.execute("SELECT * FROM `homeworks` WHERE id=%s", (id_h['id_homework']))
                homeworks.append(cursor.fetchall())
                homeworks_result.append({
                    "id": homeworks[-1][0]['id'],
                    "subject": homeworks[-1][0]['subject'],
                    "description": homeworks[-1][0]['description'],
                    "deadline": homeworks[-1][0]['deadline'],
                    "status": id_h['status']
                })
            return homeworks_result
    finally:
        connection.close()


def get_all_homework_with_param_to_str(param, id):
    try:
        homeworks = get_all_homeworks_by_vk_id(id)
        result = ""
        if param == "вся":
            for homework in homeworks:
                result += "\nНомер: " + str(homework['id']) +"\n Предмет: " + homework['subject'] + "\n Описание: \n" + str(homework['description']) + "\n Дедлайн: " + homework['deadline'] + "\n Статус: " + str(homework['status']) + "\n"
        else:
            for homework in homeworks:
                if homework['status'] == "Нужно сделать":
                    result += "\nНомер: " + str(homework['id']) +"\n Предмет: " + homework['subject'] + "\n Описание: \n" + str(homework['description']) + "\n Дедлайн: " + homework['deadline'] + "\n Статус: " + str(homework['status']) + "\n"

        return result
    except Exception as ex:
        print("get_all_homework_with_param_to_str")
        print(ex)


def insert_into_base(vk_id):
    connection = homework_back.make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO `all_users` (`id_vk`, name) VALUES (%s, %s)", (vk_id, "Незаданно"))
            id_user = cursor.lastrowid
            cursor.execute("SELECT id FROM `homeworks`")
            homeworks_id = cursor.fetchall()

            for homework_id in homeworks_id:
                cursor.execute("INSERT INTO `users` (id, id_homework, status) VALUES (%s, %s, %s)",
                               (str(id_user), str(homework_id['id']), "Нужно сделать"))

            connection.commit()
    finally:
        connection.close()

def get_homeworks_by_vk_id_with_filter(request, id):
    homeworks = get_all_homeworks_by_vk_id(id)
    result = ""
    if request['Param'] == "вся":
        for homework in homeworks:
            if homework['subject'] == request['Filter']:
                result += "\nНомер: " + str(homework['id']) + "\n Предмет: " + homework[
                    'subject'] + "\n Описание: \n\n" + str(homework['description']) + "\n\n Дедлайн: " + homework[
                              'deadline'] + "\n Статус: " + str(homework['status']) + "\n============================\n"
    else:
        for homework in homeworks:
            if homework['subject'] == request['Filter'] and homework['status'] == "Нужно сделать":
                result += "\nНомер: " + str(homework['id']) + "\n Предмет: " + homework[
                    'subject'] + "\n Описание: \n\n" + str(homework['description']) + "\n\n Дедлайн: " + homework[
                              'deadline'] + "\n Статус: " + str(homework['status']) + "\n============================\n"

    return result

def id_in_base(vk_id):
    try:
        connection = homework_back.make_connection()
        try:
            with connection.cursor() as cursor:

                cursor.execute("SELECT * FROM `all_users` WHERE id_vk=%s", (vk_id))
                id = cursor.fetchall()
                if id == ():
                    return False
                else:
                    return True
        finally:
            connection.close()

    except Exception as ex:
        print("Id in Base")
        print(ex)