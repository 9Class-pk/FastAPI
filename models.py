from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime
from typing import Optional
from datetime import datetime

class UserProfile(Base):
    __tablename__ = 'userprofile'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    username: Mapped[str]= mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow )



class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)