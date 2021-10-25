from vk_api.keyboard import VkKeyboard

def main_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button("Расписание")
    keyboard.add_button("Дз")
    keyboard.add_line()
    keyboard.add_button("Расписание завтра")
    keyboard.add_button("Дз вся")
    keyboard.add_line()
    keyboard.add_button("Преподаватели")
    keyboard.add_button("Погода")
    keyboard.add_line()
    keyboard.add_button("Команды")
    return keyboard