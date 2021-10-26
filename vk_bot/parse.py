import datetime

from configs.vk_api.homework import SUBJECTS, DEFAULT_GROUP


# Парсит запрос превращая его в словарь
# Полное описание см в документации
def parse_request(request):

    try:
        request = str(request).lower()

        request.strip()
        request = request.split(" ")

        if request[0] == "команды":
            return parse_commands(request)
        if request[0] == "dz":
            return parse_new_homework(request)
        if request[0] == "дз":
            return parse_homework(request)
        if request[0] == "расписание":
            return parse_schedule(request)
        if request[0] == "преподаватели":
            return parse_teachers(request)
        if request[0] == "погода":
            return parse_weather(request)

    except Exception as ex:
        print("parse_request")
        print(ex)


def parse_commands(request):
    answer = {
        "Type": "commands"
    }
    return answer


def parse_new_homework(request):
    if len(request) < 4:
        answer = {
            "Type": "error",
            "Where": "vk_bot/parse/parse_new_homework",
            "Description": "Неправильный синтаксис"
        }
        return answer

    description = ""
    for i in range(2, len(request)-1):
        description += request[i] + " "

    answer = {
        "Type": "homework",
        "Subtype": "new_homework",
        "Subject": request[1],
        "Description": description,
        "DeadLine": request[-1]
    }
    return answer


def parse_homework(request):

    answer = {"Type": "homework"}

    if len(request) == 1:
        answer["Subtype"] = ""
        answer["Param"] = ""
        return answer

    if len(request) == 2:
        if request[1] in SUBJECTS:
            answer["Subtype"] = "filter"
            answer["Filter"] = request[1]
            answer["Param"] = ""
            return answer

        if request[1] == "вся":
            answer["Subtype"] = ""
            answer["Param"] = "all"
            return answer

        answer["Type"] = "error"
        answer["Where"] = "vk_bot/parse/parse_homework len = 2"
        answer["Description"] = "Неправильный синтаксис"
        answer["Received"] = request
        return answer

    if len(request) == 3:
        if request[1] in SUBJECTS and "вся" in request:
            answer["Subtype"] = "filter"
            answer["Filter"] = request[1]
            answer["Param"] = "all"
            return answer

        if request[1] == "готово":
            answer["Subtype"] = "change_status"
            answer["Param"] = request[2]
            return answer

        answer["Type"] = "error"
        answer["Where"] = "vk_bot/parse/parse_homework len = 3"
        answer["Description"] = "Неправильный синтаксис"
        answer["Received"] = request
        return answer


def parse_schedule(request):
    days = ["воскресенье", "понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
    today = int(datetime.datetime.now().strftime("%w"))
    answer = {"Type": "schedule"}

    if len(request) == 1:
        answer["Group"] = DEFAULT_GROUP
        answer["Day"] = days[today]
        return answer

    if len(request) == 2:
        if request[1] == "завтра":
            answer["Group"] = DEFAULT_GROUP
            answer["Day"] = days[today+1] if today < 6 else days[0]
            return answer
        if request[1] in days:
            answer["Group"] = DEFAULT_GROUP
            answer["Day"] = request[1]
            return answer
        answer["Group"] = request[1]
        answer["Day"] = days[today]
        return answer

    if len(request) == 3:
        if request[2] == "завтра":
            answer["Group"] = request[1]
            answer["Day"] = days[today + 1] if today < 6 else days[0]
            return answer
        if request[2] in days:
            answer["Group"] = request[1]
            answer["Day"] = request[2]
            return answer
        answer["Type"] = "error"
        answer["Where"] = "vk_bot/parse/parse_schedule"
        answer["Description"] = "Неправильный синтаксис"
        answer["Received"] = request
        return answer


def parse_teachers(request):
    return {"Type": "teachers"}


def parse_weather(request):
    return {"Type": "weather"}
