from internet_parsers import schedule_smtu
from weather import get_weather
from homework import homework_front
from configs.vk_api import admins


def request_processing(request, vk_id):
    if request["Type"] == "homework":
        return request_processing_homework(request, vk_id)
    if request["Type"] == "schedule":
        return request_processing_schedule(request)
    if request["Type"] == "teachers":
        return request_processing_teachers(request)
    if request["Type"] == "weather":
        return request_processing_weather(request)
    if request["Type"] == "error":
        return request_processing_error(request)
    if request["Type"] == "commands":
        return request_processing_commands(request)


def request_processing_schedule(request):
    answer = schedule_smtu.give_data(request["Group"], request["Day"])
    if answer == "":
        answer = "Выходной либо ошибка (проверь)"
    return answer


def request_processing_teachers(request):
    with open("configs/messages/Teachers.txt", "r", encoding="UTF-8") as file:
        answer = file.read()
    return answer


def request_processing_weather(request):
    return get_weather.get_weather()


def request_processing_commands(request):
    with open("configs/messages/Commands.txt", "r", encoding="UTF-8") as file:
        answer = file.read()
    return answer


def request_processing_error(request):
    return "Произошла ошибка((("


def request_processing_homework(request, vk_id):
    if homework_front.id_in_base(vk_id):
        if request["Subtype"] == "":
            return homework_front.get_all_homework_with_param_to_str(request["Param"], vk_id)
        if request["Subtype"] == "filter":
            return homework_front.get_homeworks_by_vk_id_with_filter(request, vk_id)
        if request["Subtype"] == "change_status":
            return homework_front.change_status_homework(vk_id, request["Param"])
        if request["Subtype"] == "new_homework":
            if vk_id in admins.admins:
                return homework_front.AddHomework(request)
            else:
                return "только админы могут добавлять дз"
    else:
        homework_front.insert_into_base(vk_id)
        return "Вы добавленны в базу пожалуйста повторите запрос"
