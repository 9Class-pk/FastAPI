from typing import Union
from fastapi import FastAPI

store_app = FastAPI() #application


@store_app.get("/") #URLS
def read_root(): #View
    return {"Hello": "World123"}



from typing import Optional
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))