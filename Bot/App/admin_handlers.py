from BotData.config import bot_token, admin_id
from BotData.database_function import *
from App.states import *
from aiogram.utils.chat_action import ChatActionSender

from .function import *
import App.user_keyboard as kb
import App.admin_keyboard as ad_kb
from aiogram import Router, Bot, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.utils import chat_action
from aiogram import exceptions
from aiogram.exceptions import TelegramAPIError

bot = Bot(token=bot_token)
router_admin = Router()


#Рудимент!!! Она по-факту не нужна!!!
@router_admin.message(Command('admin'))
async def admin(message:Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    admin_in_db = check_admin(user_id)
    if user_id == admin_id or admin_in_db:
        await message.answer('Вы действительно администратор!', reply_markup=ad_kb.admin_main_kb)
        await state.set_state(Admin.authorized)
    else:
        await message.answer('Вы не являетесь администратором')

@router_admin.message(F.text == "Добавить предмет", Admin.authorized)
async def add_subject(message:Message, state: FSMContext):
    await message.answer("Введите название предмета")
    await state.set_state(Subject.subject_name)


@router_admin.message(Subject.subject_name)
async def add_subject(message:Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(subject_name=user_msg)
    await message.answer("Введите количество лаб по предмету")
    await state.set_state(Subject.labs_counter)


@router_admin.message(Subject.labs_counter)
async def add_subject(message:Message, state: FSMContext):
    user_msg = message.text
    try:
        int(user_msg)
        await state.update_data(labs_counter=user_msg)
        await message.answer("Введите максимально число участников в \"бригадах\"")
        await state.set_state(Subject.max_in_brigade)
    except ValueError:
        await message.answer("Введите число!!!")


@router_admin.message(Subject.max_in_brigade)
async def add_subject(message:Message, state: FSMContext):
    user_msg = message.text
    try:
        int(user_msg)
        await state.update_data(max_in_brigade=user_msg)
        await message.answer("Напишите день недели в который есть пара на нечетной неделе")
        await state.set_state(Subject.day_odd)
    except ValueError:
        await message.answer("Введите число!!!")


@router_admin.message(Subject.day_odd)
async def add_subject(message:Message, state: FSMContext):
    user_msg = message.text
    if check_day(user_msg):
        await state.update_data(day_odd=user_msg)
        await message.answer("Введите время начала первой лабы в формате ЧЧ:ММ")
        await state.set_state(Subject.date_start_odd)
    else:
        await message.answer('Некорректный день недели!!!')


@router_admin.message(Subject.date_start_odd)
async def add_subject(message:Message, state: FSMContext):
    user_msg = message.text
    if check_time_format(user_msg):
        await state.update_data(date_start_odd=user_msg)
        await message.answer("Введите время начала второй лабы в формате ЧЧ:ММ")
        await state.set_state(Subject.date_start_2_odd)
    else:
        await message.answer("Введено некорректное время!")


@router_admin.message(Subject.date_start_2_odd)
async def add_subject(message:Message, state: FSMContext):
    user_msg = message.text
    if check_time_format(user_msg):
        await state.update_data(date_start_2_odd=user_msg)
        await message.answer("Напишите день недели в который есть пара на четной неделе")
        await state.set_state(Subject.day_even)
    else:
        await message.answer("Введено некорректное время!")


@router_admin.message(Subject.day_even)
async def add_subject(message: Message, state: FSMContext):
    user_msg = message.text
    if check_day(user_msg):
        await state.update_data(day_even=user_msg)
        await message.answer("Введите время начала пары первой лабы в формате ЧЧ:ММ")
        await state.set_state(Subject.date_start_even)
    else:
        await message.answer('Некорректный день недели!!!')


@router_admin.message(Subject.date_start_even)
async def add_subject(message: Message, state: FSMContext):
    user_msg = message.text
    if check_time_format(user_msg):
        await state.update_data(date_start_even=user_msg)
        await message.answer("Введите время начала второй лабы в формате ЧЧ:ММ")
        await state.set_state(Subject.date_start_2_even)
    else:
        await message.answer("Введено некорректное время!")


@router_admin.message(Subject.date_start_2_even)
async def add_subject(message: Message, state: FSMContext):
    user_msg = message.text
    if check_time_format(user_msg):
        await state.update_data(date_start_2_even=user_msg)
        await message.answer('Подтвердите добавление предмета', reply_markup=kb.verfiy_menu)
        await state.set_state(Subject.finish)
    else:
        await message.answer("Введено некорректное время!")


@router_admin.message(Subject.finish)
async def add_subject(message: Message, state: FSMContext):
    user_msg = message.text
    if user_msg == "Подтвердить":
        data = await state.get_data()
        subject_name = data.get('subject_name')
        labs_counter = data.get('labs_counter')
        max_in_brigade = data.get('max_in_brigade')
        day_even = data.get('day_even')
        date_start_even = data.get('date_start_even')
        date_start_2_even = data.get('date_start_2_even')
        day_odd = data.get('day_odd')
        date_start_odd = data.get('date_start_odd')
        date_start_2_odd = data.get('date_start_2_odd')
        await set_subject(subject_name, labs_counter, max_in_brigade, day_even,
                          date_start_even, date_start_2_even, day_odd, date_start_odd, date_start_2_odd)
        await message.answer("Предмет добавлен!!!")
        await state.clear()
        await state.set_state(Admin.authorized)
    else:
        await state.clear()
        await message.answer("Хорошо!\n Не добавляем")
        await state.set_state(Admin.authorized)



@router_admin.message(F.text == "Настроить предметы", Admin.authorized)
async def add_subject(message:Message, state: FSMContext):
    await message.answer("Вот список предметов", reply_markup=ad_kb.admin_settings_subj())


@router_admin.callback_query(lambda c: c.data.startswith("subj"))
async def edit_subj(callback_query: CallbackQuery, state: FSMContext):
    data = (callback_query.data.split(":"))
    if data[0] == "subj":
        subj = get_subject(data[1])
        subj_id = subj[1]
        await callback_query.message.answer(f"Название предмета: {subj[0]}\nДень пары на начетной неделе: {subj[2]}\n"
                                            f"День начала пары на четной неделе: {subj[3]}\n"
                                            f"Время начала первой пары на нечетной неделе: {subj[4]}\n"
                                            f"Время начала второй пары на нечетной неделе: {subj[5]}\n"
                                            f"Время начала первой пары на четной неделе: {subj[6]}\n"
                                            f"Время начала второй пары на четной неделе: {subj[7]}\n"
                                            f"Кол-во лаб:{subj[9]}\n"
                                            f"Кол-во людей в бригаде: {subj[10]}", reply_markup=ad_kb.sbj_edit_all(subj_id)
                                            )

    elif data[0] == "subj_edit":
        name = get_obj_name(data[1], "subject")
        await state.set_state(Subject.labs_counter)
        await state.update_data(name=name)
        await callback_query.message.answer("Введите кол-во лаб по предмету")

    elif data[0] == "subj_del":
        await callback_query.message.delete()
        subj_id = data[1]
        print(subj_id)
        await delete_subject_by_id(subj_id)
        await callback_query.message.answer("Удаление завершено!", reply_markup=ad_kb.admin_main_kb)


@router_admin.message(F.text == 'Устроить рассылку', Admin.authorized)
async def start_mailing(message: Message, state: FSMContext):
    await message.answer('Хорошо, давайте создадим рассылку.\nДля этого отправьте сообщение, которое хотите разослать',
                         reply_markup=ad_kb.admin_main_kb)
    await state.set_state(Admin.message)

@router_admin.message(Admin.message)
async def get_message_mailing(message: Message, state: FSMContext):
    await state.update_data(message=message.text)
    await message.answer('Что дальше?', reply_markup=ad_kb.send)
    await state.set_state(Admin.mailing)

@router_admin.message(Admin.mailing)
async def go_mailing(message: Message, state: FSMContext):
    await state.update_data(mailing=message.text)
    data = await state.get_data()
    mailing = data.get('mailing')
    if mailing == 'Отправить':
        data_message = str(data.get('message'))
        users = await users_list()
        await message.answer('***Выполняем рассылку***⏳', parse_mode='Markdown')
        counter = 0
        for i in users:
            try:
                chat_id = get_chat_id(i)[0]
                async with ChatActionSender.typing(bot=bot, chat_id=chat_id):
                    await bot.send_message(i, data_message)
                counter += 1
            except exceptions.TelegramForbiddenError:
                print(i, 'Забанил бота(((')
            except Exception as e:
                print(f'Ошибка для пользователя {i}: {e}')
            await message.answer(f'***Сообщение доставлено всем*** ___"{counter}"___ ***пользователям***📧',
                                 parse_mode='Markdown', reply_markup=ad_kb.admin_main_kb)
    else:
        await message.answer('Как вам угодно😊', reply_markup=ad_kb.admin_main_kb)
    await state.clear()
    await state.set_state(Admin.authorized)
