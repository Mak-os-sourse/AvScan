import time
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.core.base import Base

class Tasks(Base):
    __tablename__ = "Tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    url: Mapped[str] = mapped_column(index=True)
    interval: Mapped[int] = mapped_column(index=True)
    last_views: Mapped[int] = mapped_column(index=True)
    scheduled_at: Mapped[int] = mapped_column(index=True)
    last_update: Mapped[int] = mapped_column(onupdate=int(time.time()), nullable=True)
    launches: Mapped[int] = mapped_column(index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), index=True)
    
    user: Mapped["Users"] = relationship(lazy="selectin", cascade="all, delete")