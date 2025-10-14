from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from store_app.db.models import StatusChoices
from datetime import datetime


class UserProfileSchema(BaseModel):

    first_name: str
    last_name: str
    username: str
    email: EmailStr
    age: int | None # Optional -> пустой
    phone_number: Optional[int]
    status: StatusChoices
    created_date: datetime
    password: str

    class Config:
        form_attributes = True


class CategorySchema(BaseModel):
    id: int
    category_name: str

    class Config:
        form_attributes = True


class SubCategorySchema(BaseModel):
    id: int
    sub_category_name: str
    category_id: int

    class Config:
        form_attributes = True


class ProductOutSchema(BaseModel):
    id: int
    product_name: str
    sub_category_id: int
    price: float
    description: str
    active: bool
    article_number: int
    video: str
    owner_id: int

    class Config:
        form_attributes = True


class ProductCreateSchema(BaseModel):
    product_name: str
    sub_category_id: int
    price: float
    description: str
    active: bool
    article_number: int
    video: str
    owner_id: int

    class Config:
        form_attributes = True


class RatingSchema(BaseModel):
    id: int
    product_id: int
    user_id: int
    stars: int = Field(None, gt=0, lt=6)
    comment: str

    class Config:
        form_attributes = True