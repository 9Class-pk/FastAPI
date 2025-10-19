from store_app.db.models import (UserProfile, Category, Product,
                                 SubCategory, Rating, RefreshToken,
                                 ProductImage, Cart, CartItem,
                                 FavouriteItem, Favourite)
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name, Category.category_image]


class SubCategoryAdmin(ModelView, model=SubCategory):
    column_list = [SubCategory.id ,SubCategory.sub_category_name, SubCategory.category]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.product_name, Product.sub_category]


class ProductImageAdmin(ModelView, model=ProductImage):
    column_list = [ProductImage.id, ProductImage.product_image]


class RatingAdmin(ModelView, model=Rating):
    column_list = [Rating.id, Rating.product, Rating.user,
                   Rating.stars, Rating.comment]


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [RefreshToken.id, RefreshToken.user, RefreshToken.token]


class CartAdmin(ModelView, model=Cart):
    column_list = [Cart.id, Cart.items]


class CartItemAdmin(ModelView, model=CartItem):
    column_list = [CartItem.cart, CartItem.product]


class FavouriteAdmin(ModelView, model=Favourite):
    column_list = [Favourite.favourite_items]


class FavouriteItemAdmin(ModelView, model=FavouriteItem):
    column_list = [FavouriteItem.product]


