import requests
from bs4 import BeautifulSoup
import datetime
import json
import os

class Para(object):

    def __init__(self, day, time, audition, para, prepod):
        self.day = day
        self.time = time
        self.auditon = audition
        self.para = para
        self.prepod = prepod


    def show(self):
        print(f"День: {self.day}  Время: {self.time}  Аудитория: {self.auditon}  Предмет: {self.para}  Преподаватель: {self.prepod}")

    def to_string(self):
        return f"День: {self.day}\n  Время: {self.time}\n  Аудитория: {self.auditon}\n  Предмет: {self.para}\n  Преподаватель: {self.prepod}\n\n"




days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
def get_data(group):
    url = f"https://www.smtu.ru/ru/viewschedule/{group}/"
    r = requests.get(url=url)

    with open("internet_parsers/index.html", "w", encoding="UTF-8")as file:
        file.write(r.text)

    with open("internet_parsers/index.html", encoding="UTF-8")as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    result1 = soup.find("table").find_all("thead")

    days = []
    for lol in result1:
        days.append(str(lol.text).replace('\n', ""))
    days.remove("ВремяАудиторияПредметПреподаватель")

    result1 = soup.find("table").find_all("tbody")
    result1 = result1[1::]
    info = []
    Pars = []
    j = 0
    for resu in result1:
        res = str(resu.text).replace('\t', "")
        while res[0] == '\n':
            res = res[1::]
        while len(res) != 0:
            number = res.find('\n')
            if number != 0:
                info.append(res[:number:])
            res = res[number + 1::]

        while len(info) != 0:
            day_ = days[j]
            time_ = info[0]
            auditory_ = info[1]
            predmet_ = str(info[2])

            index = predmet_.find("Лекция")
            if index != -1:
                predmet_ = predmet_[:index] + " " + predmet_[index:]

            index = predmet_.find("Лабораторное занятие")
            if index != -1:
                predmet_ = predmet_[:index] + " " + predmet_[index:]

            index = predmet_.find("Практическое занятие")
            if index != -1:
                predmet_ = predmet_[:index] + " " + predmet_[index:]

            try:
                prepod_ = info[3]
            except:
                pass
            if prepod_[0].isdigit():
                Pars.append(Para(day=day_, time=time_, audition=auditory_, para=predmet_, prepod=""))
                info = info[3::]
            else:
                Pars.append(Para(day=day_, time=time_, audition=auditory_, para=predmet_, prepod=prepod_))
                info = info[4::]

        j += 1
        text = ""
        for para in Pars:
            text = text + para.to_string()

    result = make_slovar(text)
    with open(f"data_base/schedules/smtu/{group}.txt", "w", encoding="windows-1251")as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    return 1



def make_slovar(info):

 #with open("info.txt", "r", encoding="UTF-8")as file:
     # info = file.read()

  count = info.count("День")
  double_periods = []
  for i in range(0, count):
      #Берём День
      number = info.find(":")
      number2 = info.find("\n")
      day = info[number+2:number2:]
      info = info[number2::].lstrip()

      #Берём Время
      number = info.find(":")
      number2 = info.find("\n")
      time = info[number + 2:number2:]
      info = info[number2::].lstrip()

      # Берём Аудиторию
      number = info.find(":")
      number2 = info.find("\n")
      audition = info[number + 2:number2:]
      info = info[number2::].lstrip()

      # Берём Предмет
      number = info.find(":")
      number2 = info.find("\n")
      predmet = info[number + 2:number2:]
      info = info[number2::].lstrip()

      # Берём Преподавателя
      number = info.find(":")
      number2 = info.find("\n")
      prepod = info[number + 2:number2:]
      info = info[number2::].lstrip()

      if time.count("Верхняя") == 1:
        week = "Верхняя"
        number = time.find("Верхняя")
        time = time[:number:]
      elif time.count("Нижняя") == 1:
        week = "Нижняя"
        number = time.find("Нижняя")
        time = time[:number:]
      else:
        week = "Всегда"

      double_period = {
        'Day': day,
        'Week': week,
        'Time': time,
        'Auditory': audition,
        'Predmet': predmet,
        'Prepod': prepod
      }
      double_periods.append(double_period)

  return double_periods

def give_data(group, day):
    days = ["воскресенье", "понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
    if os.path.isfile(f"rasp{group}.txt"):
        pass
    else:
        get_data(group)

    with open(f"data_base/schedules/smtu/{group}.txt", "r", encoding="windows-1251")as file:
        rasp = json.load(file)

    now = datetime.datetime.now()
    week = int(now.strftime("%U"))



    need = days.index(day)
    today = int(now.strftime("%w"))


    if need<today:
        week += 1

    if week % 2 == 0:
        week = "Нижняя"
    else:
        week = "Верхняя"

    day = day.title()


    Answer = []
    for para in rasp:
        if (para['Week'] == week or para['Week'] == "Всегда") and para['Day'] == day:
            Answer.append(para)

    result = ""
    for para in Answer:
       result = result + para['Time'] + " " + para['Week'] + '\n'
       result = result + para['Auditory'] + '\n'
       result = result + para['Predmet'] + '\n'
       result = result + para['Prepod'] + '\n\n'

    return result