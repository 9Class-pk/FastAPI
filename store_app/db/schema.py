from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
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


class UserProfileLoginSchema(BaseModel):

    username: str
    password: str

    class Config:
        form_attributes = True


class CategorySchema(BaseModel):
    id: int
    category_name: str

    class Config:
        form_attributes = True


class CategoryImageSchema(BaseModel):
    id: int
    category_image: str


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


class ProductImageOutSchema(BaseModel):
    id: int
    product_id: int
    product_image: str

    class Config:
        form_attributes = True


class ProductImageCreateSchema(BaseModel):
    product_id: int
    image: str

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

class CartItemSchema(BaseModel):
    id: int
    cart_id: int
    product_id: int

    class Config:
        form_attributes = True


class CartSchema(BaseModel):
    user_id: int
    items: List[CartItemSchema] = []
    total_price: int

    class Config:
        from_attributes = True


class CartItemCreateSchema(BaseModel):
    product_id: int
    quantity: Optional[int] = 1

    class Config:
        from_attributes = True


class FavouriteItemSchema(BaseModel):
    id: int
    favourite_id: int
    product_id: int

    class Config:
        form_attributes = True


class FavouriteSchema(BaseModel):
    id: int
    user_id: int
    favourite_items: List[FavouriteItemSchema] = []

    class Config:
        form_attributes = True


class FavouriteItemCreateSchema(BaseModel):
    product_id: int

    class Config:
        from_attributes = True



class UploadImageResponse(BaseModel):
    id: int
    image: str
    product_id: Optional[int] = None
    category_id: Optional[int] = None

    class Config:
        from_attributes = True
