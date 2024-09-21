import sqlite3 as sq
from App.function import *
from aiogram.utils.chat_action import ChatActionSender

db = sq.connect('BotData')
cur = db.cursor()