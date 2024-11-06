from BotData.config import bot_token
from BotData.database_function import *
from App.states import *

import App.user_keyboard as kb
import App.globals as g

from aiogram import Router, Bot, F, types
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram import exceptions

bot = Bot(token=bot_token)
router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    user_in_db = chek_user(user_id)
    if user_in_db:
        await message.answer("Приветсвую!", reply_markup=kb.main_menu)
    else:
        await message.answer("Ваших данных нет в базе, поэтому зарегистрируйтесь")
        await message.answer("Введите ваше имя:")
        await state.set_state(Reg.name)


@router.message(Reg.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.surname)
    await message.reply("Введите вашу фамилию:")


@router.message(Reg.surname)
async def set_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(Reg.surname)
    data = await state.get_data()
    name = data.get('name')
    surname = data.get('surname')
    user = message.from_user
    user_id = user.id
    user_username = user.username
    chat_id = message.chat.id
    await user_to_db(user_id,user_username, name, surname, chat_id)
    await message.answer('Ваши данные добавлены!',reply_markup=kb.main_menu)
    await state.clear()

@router.message(F.text == "Записаться на лабу")
async def lab(message: Message, state: FSMContext):
    user_id = message.from_user.id
    day = g.current_day
    list_lab= g.calendar_labs[day]
    is_can_record = g.flag
    if len(user_by_tg_id(user_id)):
        if len(list_lab) and not(is_can_record):
            output_str = ''
            for i in range(len(list_lab)):
                output_str += str(list_lab[i][0][0] + ' - ' + list_lab[i][0][1]) + ' ' + str(list_lab[i][1]) + '\n'
            output_str += '\nЗапись будет доступна за 5 минут до начала'
            await message.answer(output_str)
        elif len(list_lab) and is_can_record and not(check_user_in_set(user_id)):
            await state.set_state(Record.priority)
            await message.answer('Укажите ваш приоритет: 0 - все равно, когда сдаваться, но было бы неплохо ближе к концу,  '
                                 '1 - хочу сдать чуть пораньше, но не срочно, 2 - ОЧЕНЬ НАДО ГОРИТ!')
        elif len(list_lab) and is_can_record and (check_user_in_set(user_id)):
            await message.answer('Вы уже находитесь в очереди!\nОжидайте результатов')
        else:
            await message.answer("Сегодня нет лаб!!!")
    else:
        await message.answer("Ваших данных нет в базе, поэтому зарегистрируйтесь")
        await message.answer("Введите ваше имя:")
        await state.set_state(Reg.name)
        

@router.message(Record.priority)
async def lab(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        user_priority = int(message.text)
        choose_variant_list = [0, 1, 2]
        if (user_priority not in choose_variant_list):
            raise ValueError()
        if not(check_user_in_set(user_id)):
            set_user_to_order(user_id, user_priority)
            await message.answer('Вы находитесь в очереди!')
        else:
            await message.answer('Вы уже в очереди!')
        await state.clear()
    except ValueError:
        await message.answer("Введите ваш приоритет в нормальном формате!!!")





