from datetime import datetime, timedelta

import pytz

def check_lab_time(list_day_lessons, current_time): 
    for lesson in list_day_lessons:
        start_time = lesson[0][0]
        end_time = lesson[0][1]
        # Преобразуем время начала занятия и текущее время в объекты datetime
        lesson_time = datetime.strptime(start_time, '%H:%M')
        current_time_obj = datetime.strptime(current_time, '%H:%M')
         # Вычисляем разницу между временем урока и текущим временем
        time_difference = abs(lesson_time - current_time_obj)

        # Проверяем, что разница не превышает 5 минут
        if (lesson_time.time() > current_time_obj.time()) and time_difference <= timedelta(minutes=5):
            return True
    return False

def get_current_time():
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    return now.strftime('%H:%M')

list_less = [[['13:45', '15:20'], 'лаб.Объектно-ориентированное программирование- 1 п/г Лутай В. Н. Г-425'], [['18:45', '17:25'], 'лаб.Объектно-ориентированное программирование- 2 п/г Лутай В. Н. Г-425']]

print(check_lab_time(list_less, get_current_time()))

output_str = ''
for i in range(len(list_less)):
    output_str += str(list_less[i][0][0] + ' - ' + list_less[i][0][1]) + ' ' + str(list_less[i][1]) + '\n'

print(output_str)