import time
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.app.core.base import Base

class Users(Base):
    __tablename__ = "Users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(index=True, nullable=True)
    reg_date: Mapped[int] = mapped_column(BigInteger, default=lambda: int(time.time()))
    is_admin: Mapped[bool] = mapped_column(index=True, default=False)