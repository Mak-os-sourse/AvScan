import time
from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.core.base import Base

class Products(Base):
    __tablename__ = "Products"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_product: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[str] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(nullable=True)
    url_photo: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    task_id: Mapped[int] = mapped_column(nullable=True)
    create_date: Mapped[int] = mapped_column(BigInteger, default=lambda: int(time.time()))
    
    user: Mapped["Users"] = relationship(lazy="selectin")