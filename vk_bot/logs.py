def make_log(time, user_id, message):
    with open(f"vk_bot/logs/{time.year}.{time.month}.{time.day}.txt", "a", encoding="UTF-8") as file:
        file.write(f"Время: {time.hour}:{time.minute}:{time.second}"
                   f" Id Беседы: {user_id} Получено сообщение: {message}\n")
