from aiogram.fsm.state import State, StatesGroup

class Start(StatesGroup):
    user = State()

class Parsing(StatesGroup):
    user = State()
    url = State()
    
class IntervalParsing(StatesGroup):
    user = State()
    url = State()
    time = State()
