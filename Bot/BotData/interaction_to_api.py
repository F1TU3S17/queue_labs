import App.globals as g
import urllib.request
import urllib.parse
import json

def fetch_schedule(query):
    # Исходный URL
    url = f'https://webictis.sfedu.ru/schedule-api/?query={query}'

    # Кодирование URL
    encoded_url = urllib.parse.quote(url, safe=':/?=&')

    # Отправка запроса
    response = urllib.request.urlopen(encoded_url)

    # Проверка статуса ответа
    if response.status == 200:
        data = response.read().decode()

        # Преобразуем JSON-строку в объект Python
        data_dict = json.loads(data)

        # Извлекаем таблицу расписания
        schedule_table = data_dict['table']['table']

        # Создаем словарь для хранения расписания по дням недели
        schedule_by_day = {}

        # Список списков вида [Время начала пары, время конца пары], Индекс - день недели
        schedule_lessons_time = []

        for j in range(1, 7):
            schedule_lessons_time.append(schedule_table[1][j].split('-'))

        # Проходим по строкам таблицы, начиная с третьей строки (индекс 2)
        for row in schedule_table[2:]:
            day_of_week = row[0]  # Первый элемент строки - день недели
            lessons = row[1:]  # Остальные элементы строки - пары
            schedule_by_day[day_of_week] = lessons

        day_of_weeks = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        i = 0
        lesson_number = 0

        # Выводим расписание по дням недели
        for day, lessons in schedule_by_day.items():
            current_day = schedule_by_day[day]
            true_name_day = day_of_weeks[i]
            for lesson in current_day:
                if lesson.startswith('лаб.'):
                    # Если лаба, то добавляем в список список вида: День недели, список вида: Номер пары,
                    (g.calendar_labs[true_name_day]).append([schedule_lessons_time[lesson_number], lesson])
                lesson_number += 1
            lesson_number = 0
            i += 1
    else:
        print('Ошибка:', response.status, response.reason)

