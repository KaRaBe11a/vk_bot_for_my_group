import datetime

from vk_api.longpoll import VkEventType
import vk_api
from vk_api.longpoll import VkLongPoll

from vk_bot.parse import parse_request
from vk_bot.logs import make_log
from vk_bot.request_processing import request_processing
from configs.vk_api import keyboards, token

vk_session = vk_api.VkApi(token=token.token)
longpoll = VkLongPoll(vk_session)


# Находит полученные сообщения
def found_some_message():

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:

                    message = str(event.text.lower())
                    request = parse_request(message)
                    user_id = event.user_id
                    time_now = datetime.datetime.now()

                    make_log(time_now, user_id, message)
                    answer = request_processing(request, user_id)
                    send_some_message(user_id, answer)

        except Exception as ex:
            print(request)
            print("found_some_message")
            print(ex)


def send_some_message(id, text):
    post = {
        "user_id": id,
        "message": text,
        "random_id": 0,
        "keyboard": keyboards.main_keyboard().get_keyboard()

    }

    vk_session.method("messages.send", post)