from typing import Literal
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base

class Tasks(Base):
    __tablename__ = "Tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    url: Mapped[str] = mapped_column(index=True)
    interval: Mapped[int] = mapped_column(nullable=True, index=True)
    last_views: Mapped[int] = mapped_column(index=True)
    scheduled_at: Mapped[int] = mapped_column(index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), index=True)
    launches: Mapped[int] = mapped_column(index=True)
    mode: Mapped[Literal["Interval", "Every"]] = mapped_column(index=True)
    
    user: Mapped["Users"] = relationship(lazy="selectin")