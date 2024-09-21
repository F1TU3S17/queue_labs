import sqlite3 as sq
from App.function import *
from aiogram.utils.chat_action import ChatActionSender
from aiogram import exceptions

db = sq.connect('BotData/database.db')
cur = db.cursor()


async def db_start():
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                username TEXT,
                name TEXT,
                surname TEXT,
                chat_id INTEGER)
                ''')
    cur.execute(f'''CREATE TABLE IF NOT EXISTS subjects (
                        subject TEXT,
                        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        day_even TEXT,
                        day_odd TEXT,
                        date_start_even TEXT,
                        date_start_2_even TEXT,
                        date_start_odd TEXT,
                        date_start_2_odd TEXT,
                        labs_counter INTEGER)
                       ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS admins(
            tg_id INTEGER PRIMARY KEY)
                ''')
    db.commit()






async def user_to_db(tg_id, username, name, surname, chat_id):
    cur.execute('SELECT COUNT(*) FROM users WHERE tg_id = ?', (tg_id,))
    exists = cur.fetchone()[0]
    if not exists:
        cur.execute('INSERT INTO users(tg_id, username, name, surname, chat_id) VALUES (?,?,?,?,?)',(tg_id,username,name,surname,chat_id))
        db.commit()


def get_chat_id(tg_id):
    chat_id = cur.execute('SELECT chat_id FROM users WHERE tg_id == ?',(tg_id,)).fetchone()
    if chat_id:
        return list(chat_id)
    return []

def chek_user(tg_id):
    exists = False
    user = cur.execute('SELECT * FROM users WHERE tg_id = ?',(tg_id, )).fetchone()
    if user:
        exists = True
    return exists


def check_admin(tg_id):
    admin = cur.execute('SELECT tg_id FROM admins WHERE tg_id = ?',(tg_id,)).fetchone()
    if admin:
        return True
    return False


async def set_subject(subject_name, labs_counter, max_in_brigade, day_even,
                      date_start_even, date_start_2_even, day_odd, date_start_odd, date_start_2_odd):

    cur.execute("SELECT * FROM subjects WHERE subject = ?", (subject_name,))
    result = cur.fetchone()

    if result:
        query = '''
            UPDATE subjects
            SET labs_counter = ?, max_in_brigade = ?, day_even = ?, date_start_even = ?, 
                date_start_2_even = ?, day_odd = ?, date_start_odd = ?, date_start_2_odd = ?
            WHERE subject = ?
            '''
        cur.execute(query, (labs_counter, max_in_brigade, day_even, date_start_even,
                            date_start_2_even, day_odd, date_start_odd, date_start_2_odd, subject_name))
    else:
        query = '''
            INSERT INTO subjects (subject, labs_counter, max_in_brigade, day_even, 
            date_start_even, date_start_2_even, day_odd, date_start_odd, date_start_2_odd)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
        cur.execute(query, (subject_name, labs_counter, max_in_brigade, day_even,
                            date_start_even, date_start_2_even, day_odd, date_start_odd, date_start_2_odd))

    db.commit()

def get_subject_name():
    query = '''
    SELECT subject FROM subjects 
    '''
    collection = cur.execute(query).fetchall()
    subject_list = [i[0] for i in collection]

    return subject_list



def get_subject(sbj_name):
    query = '''
    SELECT * FROM subjects WHERE subject == ?
    '''
    collection = cur.execute(query,(sbj_name,)).fetchone()
    subject_list = list(collection)

    return subject_list


def get_obj_name(sbj_id, obj_name):
    name = cur.execute(f"""
        SELECT {obj_name} FROM subjects WHERE subject_id== ?""",(sbj_id,)).fetchone()
    if name:
        return (name[0])
    return []


async def delete_subject_by_id(subject_id):
    query = '''
    DELETE FROM subjects WHERE subject_id = ?
    '''
    cur.execute(query, (subject_id,))

    db.commit()

def user_by_tg_id(tg_id):
    user = cur.execute("SELECT name, surname FROM users WHERE tg_id == ?",(tg_id,)).fetchone()
    if user:
        return list(user)
    return []
def get_lab_day():
    moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
    moscow_date = moscow_time.date()
    is_odd = is_odd_week(moscow_date)
    current_day_of_week = get_current_day_of_week()
    date_start_labs = []
    if is_odd:
        date_start_labs = (cur.execute('SELECT subject, date_start_odd, date_start_2_odd FROM subjects WHERE day_odd == ?',(current_day_of_week,)).fetchone())
    else:
        date_start_labs = (cur.execute('SELECT subject, date_start_even, date_start_2_even FROM subjects WHERE day_even == ?',(current_day_of_week,)).fetchone())
    if date_start_labs != None:
        return date_start_labs
    return []



async def users_list():
    users = cur.execute('SELECT tg_id FROM users').fetchall()
    user_list = [i[0] for i in users]
    return user_list


async def check_time(bot):
    """
    Назначение:
    Асинхронно проверяет текущее время каждую минуту и выполняет действия, если наступило нужное время.

    Возвращаемое значение:
    None.
    """
    while True:
        now = datetime.now(pytz.timezone('Europe/Moscow'))
        lab_day = get_lab_day()
        if len(lab_day):
            first_pair = lab_day[1].split(":")
            second_pair = lab_day[2].split(":")
            hour = now.hour
            if now.minute + 5 >= 60:
                hour = (now.hour + 1) % 24
            true_time = (((hour == int(first_pair[0])) and (((now.minute + 5) % 60 == int(first_pair[1]))))
                         or ((hour == int(second_pair[0])) and ((now.minute + 5) % 60 == int(second_pair[1]))))
            if true_time:
                set_flag(True)
                users = await users_list()
                for user in users:
                    await bot.send_message(user, text=f"Запись на лабу по {lab_day[0]} открыта!!!")
                await asyncio.sleep(300)
                final_queue = distribute_queue(list(g.set_order_id))
                order = ""
                for i, (id, priority) in enumerate(final_queue, 1):
                    user_info = user_by_tg_id(id)
                    order +=f"{i}){user_info[0]} {user_info[1]}\n"
                if not(len(order)):
                    order = "Очередь не была сформирована"
                for user in users:
                    try:
                        async with ChatActionSender.typing(bot=bot, chat_id=get_chat_id(user)[0]):
                            await bot.send_message(user, order)
                    except exceptions.TelegramAPIError:
                        print(user, 'Забанил бота(((')
                set_flag(False)
                g.set_order_id.clear()
        await asyncio.sleep(60)