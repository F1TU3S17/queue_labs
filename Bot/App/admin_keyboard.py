from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardButton,InlineKeyboardMarkup, ReplyKeyboardRemove)
from BotData.database_function import *

admin_main_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Добавить предмет"),
                                               KeyboardButton(text="Настроить предметы"),
                                               KeyboardButton(text="Устроить рассылку")]],
                                    resize_keyboard=True)


def admin_settings_subj():
    keyboard = []
    list_subj = get_subject_name()
    for i in range(len(list_subj)):
        keyboard.append([InlineKeyboardButton(text=list_subj[i], callback_data=f"subj:{list_subj[i]}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)




def sbj_edit_all(sbj_id):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Изменить все", callback_data=f"subj_edit:{sbj_id}")],
                                                 [InlineKeyboardButton(text="Удалить предмет", callback_data=f"subj_del:{sbj_id}")],
                                                 [InlineKeyboardButton(text="Бригады", callback_data=f"subj_brig:{sbj_id}")]])


def current_name_obj(sbj_id, obj_name):
    name = get_obj_name(sbj_id, obj_name)
    if name:
        return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=f"{name}")]])
    return ReplyKeyboardRemove()

send = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить')], [KeyboardButton(text='Отменить')]],resize_keyboard=True)



