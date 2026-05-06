from aiogram.fsm.state import State, StatesGroup

class Parsing(StatesGroup):
    url = State()
    
class IntervalParsing(StatesGroup):
    url = State()
    time = State()

class EverylParsing(StatesGroup):
    url = State()
    time = State()