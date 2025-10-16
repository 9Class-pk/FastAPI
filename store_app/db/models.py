from sqlalchemy.dialects.mysql import DECIMAL
from store_app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (String, Integer, DateTime, ForeignKey,
                        CheckConstraint, Enum, Text, Boolean)
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
    #OptionalCart-->OnetoOne
    cart: Mapped[Optional['Cart']] = relationship('Cart', back_populates='user', uselist=False)
    favourites: Mapped[Optional['Favourite']] = relationship('Favourite', back_populates='user', uselist=False)
    user_token: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.first_name}, {self.last_name}'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_token')
    token: Mapped[str] = mapped_column(String, nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)
    category_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subcategories: Mapped[List['SubCategory']] = relationship(back_populates='category',
                                                              cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.category_name}'



class SubCategory(Base):
    __tablename__ = 'subcategory'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    sub_category_name: Mapped[str] = mapped_column(String(32), unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(back_populates='subcategories')
    products: Mapped[List['Product']] = relationship(back_populates='sub_category',
                                                     cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.sub_category_name}'


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
    product_images: Mapped[List['ProductImage']] = relationship('ProductImage', back_populates='product',
                                                                cascade='all, delete-orphan')
    cart_product: Mapped[List['CartItem']] = relationship('CartItem', back_populates='product')
    products: Mapped[List['FavouriteItem']] = relationship('FavouriteItem', back_populates='product')


    def __repr__(self):
        return f'{self.product_name}'


class ProductImage(Base):
    __tablename__ = 'product_image'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped[Product] = relationship(back_populates='product_images')
    image: Mapped[str] = mapped_column(String, nullable=False)


class Rating(Base):
    __tablename__ = 'rating'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped[Product] = relationship(Product, back_populates='product_rating')
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_rating')
    stars: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self):
        return f'{self.user}, {self.stars}'


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='cart',)
    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart',
                                                   cascade='all, delete-orphan')


class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    cart: Mapped[Cart] = relationship(Cart, back_populates='items')
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped['Product'] = relationship('Product', back_populates='cart_product')
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)


class Favourite(Base):
    __tablename__ = 'favourite'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='favourites')
    favourite_items: Mapped[List['FavouriteItem']] = relationship('FavouriteItem', back_populates='favourite',
                                                                  cascade='all, delete-orphan')


class FavouriteItem(Base):
    __tablename__ = 'favourite_item'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    favourite_id: Mapped[int] = mapped_column(ForeignKey('favourite.id'))
    favourite: Mapped['Favourite'] = relationship('Favourite', back_populates='favourite_items')
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped['Product'] = relationship('Product', back_populates='products')

