from sqlalchemy.dialects.mysql import DECIMAL
from store_app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, CheckConstraint, Enum, Text, Boolean
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import datetime


class StatusChoices(str, PyEnum):
    gold = 'gold'
    silver = 'silver'
    bronze = 'bronze'
    simple = 'simple'


class UserProfile(Base):
    __tablename__ = 'userprofile'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    username: Mapped[str]= mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow )
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.simple)
    user_product: Mapped[List['Product']] = relationship('Product', back_populates='owner',
                                                         cascade='all, delete-orphan')
    user_rating: Mapped[List['Rating']] = relationship('Rating', back_populates='user',
                                                       cascade='all, delete-orphan')



class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)
    category_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subcategories: Mapped[List['SubCategory']] = relationship(back_populates='category',
                                                              cascade='all, delete-orphan')


class SubCategory(Base):
    __tablename__ = 'subcategory'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    sub_category_name: Mapped[str] = mapped_column(String(32), unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(back_populates='subcategories')
    products: Mapped[List['Product']] = relationship(back_populates='sub_category',
                                                     cascade='all, delete-orphan')


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    sub_category_id: Mapped[int] = mapped_column(ForeignKey('subcategory.id'))
    sub_category: Mapped[SubCategory] = relationship(back_populates='products')
    product_name: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    article_number: Mapped[int] = mapped_column(Integer, CheckConstraint('article_number > 0'))
    description: Mapped[str] = mapped_column(Text)
    video: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    active: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    owner: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_product')
    product_rating: Mapped[List['Rating']] = relationship('Rating', back_populates='product',
                                                          cascade='all, delete-orphan')


class Rating(Base):
    __tablename__ = 'rating'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped[Product] = relationship(Product, back_populates='product_rating')

    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_rating')
    stars: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)