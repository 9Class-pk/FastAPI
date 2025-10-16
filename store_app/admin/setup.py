from .views import (UserProfileAdmin, CategoryAdmin,
                    SubCategoryAdmin, ProductAdmin,
                    RatingAdmin, RefreshTokenAdmin,
                    ProductImageAdmin, CartAdmin,
                    CartItemAdmin, FavouriteAdmin, FavouriteItemAdmin)

from fastapi import FastAPI
from sqladmin import Admin
from store_app.db.database import engine

def setup_admin(store_app: FastAPI):
    admin = Admin(store_app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(SubCategoryAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ProductImageAdmin)
    admin.add_view(RatingAdmin)
    admin.add_view(CartAdmin)
    admin.add_view(CartItemAdmin)
    admin.add_view(FavouriteAdmin)
    admin.add_view(FavouriteItemAdmin)
    admin.add_view(RefreshTokenAdmin)


