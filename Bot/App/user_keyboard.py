from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardButton,InlineKeyboardMarkup)
from Bot.BotData.database_function import *


main_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Записаться на лабу")]],
                                resize_keyboard=True)


verfiy_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Подтвердить")],
                                            [KeyboardButton(text="Отменить")]],resize_keyboard=True)

