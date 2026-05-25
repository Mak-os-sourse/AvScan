from typing import TypeVar
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

TModel = TypeVar("TModel", bound=Base)