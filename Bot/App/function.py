import asyncio
import string
from datetime import datetime, date
import pytz
import random
import re
import App.globals as g

def check_time_format(time_str):
    time_pattern = r'^[0-2]\d:[0-5]\d$'
    return bool(re.match(time_pattern, time_str))


def is_english(text):
    english_chars = set(string.ascii_letters + ' ')
    return all(char in english_chars for char in text)



# Функция для получения текущего времени
def get_current_time():
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    return now.strftime('%H:%M')

def get_current_day_of_week():
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz)
    day_of_week = moscow_time.strftime("%A")
    days_of_week = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }
    return days_of_week.get(day_of_week, 'Неизвестный день')


def check_day_of_week(day_of_week):
    days_of_week = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }
    if days_of_week.get(day_of_week, 'Неизвестный день') == 'Неизвестный день':
        return False
    return True


def check_day(day: str):
    day = day.lower()
    list_days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    if day in list_days:
        return True
    return False


def is_odd_week(date_now: datetime.date) -> bool:
    """
    Возвращаемое значение:
    - True, если неделя нечетная, False, если неделя четная.
    """
    start_date = date(date_now.year, 9, 2)
    days_difference = (date_now - start_date).days
    week_number = days_difference // 7 + 1

    return week_number % 2 != 0


def set_flag(flag):
    g.flag = flag


def check_user_in_set(user_id):
    # bool: True, если элемент с таким user_id найден, иначе False.
    user_set = g.set_order_id
    user_id = str(user_id)
    if ((user_id, 0) in user_set) or ((user_id, 1) in user_set) or ((user_id, 2) in user_set):
        return True
    return False


def set_user_to_order(tg_id, priority):
    g.set_order_id.add((str(tg_id), int(priority)))



def distribute_queue(people):
    priority_0 = [person for person in people if person[1] == 0]
    priority_1 = [person for person in people if person[1] == 1]
    priority_2 = [person for person in people if person[1] == 2]

    random.shuffle(priority_0)
    random.shuffle(priority_1)
    random.shuffle(priority_2)

    final_queue = priority_2 + priority_1 + priority_0

    return final_queue

def time_to_seconds(hour, minute):
    return hour * 3600 + minute * 60


def clear_calendar_labs():
    g.calendar_labs = {
        'Понедельник': [],
        'Вторник': [],
        'Среда': [],
        'Четверг': [],
        'Пятница': [],
        'Суббота': []
    }