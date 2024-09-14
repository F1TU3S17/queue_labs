from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup


class Reg(StatesGroup):
    name = State()
    surname = State()

class Admin(StatesGroup):
    authorized = State()
    message = State()
    mailing = State()

class Subject(StatesGroup):
    subject_name = State()
    labs_counter = State()
    max_in_brigade = State()
    day_even = State()
    date_start_even = State()
    date_start_2_even = State()
    day_odd = State()
    date_start_odd = State()
    date_start_2_odd = State()
    finish = State()

class Record(StatesGroup):
    priority = State()
