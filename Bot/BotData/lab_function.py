from datetime import timedelta
from App.function import *
from aiogram.utils.chat_action import ChatActionSender
from aiogram import exceptions
from BotData.database_function import user_by_tg_id, get_chat_id, users_list
from App.function import *
from BotData.interaction_to_api import fetch_schedule



# Функция для проверки, наступило ли время записи на лабу
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

async def send_messages(bot, users, lab_name):
    for user in users:
        try:
            print("Рассылка записи!")
            async with ChatActionSender.typing(bot=bot, chat_id=get_chat_id(user)[0]):
                await bot.send_message(user, text=f"Запись на лабу:{lab_name} открыта!!!")
        except exceptions.TelegramForbiddenError:
            print(user, 'Забанил бота(((')
        except Exception as e:  # Обрабатываем все другие возможные ошибки
            print(f'Ошибка для пользователя {user}: {e}')


async def distribute_and_send(bot, users):
    final_queue = distribute_queue(list(g.set_order_id))
    order = ""
    for i, (id, priority) in enumerate(final_queue, 1):
        user_info = user_by_tg_id(id)
        if len(user_info):
            order += f"{i}){user_info[0]} {user_info[1]}, приоритет: {priority}\n"
    if not (len(order)):
        order = "Очередь не была сформирована"
    print(order)
    for user in users:
        try:
            async with ChatActionSender.typing(bot=bot, chat_id=get_chat_id(user)[0]):
                await bot.send_message(user, order)
        except exceptions.TelegramForbiddenError:
            print(user, 'Забанил бота(((')
        except Exception as e:
            print(f'Ошибка для пользователя {user}: {e}')

async def check_time(bot):
    """
    Назначение:
    Асинхронно проверяет текущее время каждую минуту и выполняет действия, если наступило нужное время.
    Возвращаемое значение:
    None.
    """
    while True:
        now = datetime.now(pytz.timezone('Europe/Moscow'))
        day = get_current_day_of_week()
        if day != g.current_day:
            g.current_day = day
            fetch_schedule('КТбо2-8')

        #print(g.current_day)
        #print(g.calendar_labs)
        if (day != 'Неизвестный день'):
            list_day_lessons = g.calendar_labs[day]
            #print(list_day_lessons)

            true_time = False
            if len(list_day_lessons):  
                current_time = get_current_time()
                true_time = check_lab_time(list_day_lessons, current_time)
        
            if true_time:
                lab_name = ''
                set_flag(True)
                users = await users_list()
                await send_messages(bot, users, lab_name)
                await asyncio.sleep(300)
                await distribute_and_send(bot, users)
                set_flag(False)
                g.set_order_id.clear()
        await asyncio.sleep(60)