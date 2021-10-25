import datetime

import requests

from configs.weather.config import *

#  Через API openwheather возвращает
#  погоду в питере на данный момент
def get_weather():

    code_to_smile = {

        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"

    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={KEY}&units=metric"
        )
        data = r.json()

        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно я неебу чё там"

        cur_humidity = data["main"]["humidity"]
        feels_like = data["main"]["feels_like"]
        wind_speed = data["wind"]["speed"]

        info = (f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в питере:\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {cur_humidity}% \nВетер: {wind_speed}м/c\n"
              f"Все это говно ощущается как {feels_like}С°")
        return info

    except Exception as ex:
        print(ex)
