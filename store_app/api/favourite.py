from store_app.db.models import Favourite, Product, UserProfile, CartItem, FavouriteItem
from store_app.db.schema import FavouriteItemSchema, FavouriteSchema, FavouriteItemCreateSchema
from store_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Security
from store_app.api.auth import get_current_user

favourite_router = APIRouter(prefix='/favourite', tags=['Favourite'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@favourite_router.get('/', response_model=FavouriteSchema)
async def get_favourite(user_id: int, db: Session = Depends(get_db),
                        current_user: dict = Security(get_current_user, scopes=["favourite:read"])):
    user_id = current_user["user_id"]

    favourite = db.query(Favourite).filter(Favourite.user_id == user_id).first()
    if not favourite:
        raise HTTPException(status_code=404, detail='Favourite not found')
    return favourite


# Добавить товар в избранное
@favourite_router.post('/item/', response_model=FavouriteItemSchema)
async def add_favourite_item(item_data: FavouriteItemCreateSchema, user_id: int, db: Session = Depends(get_db),
                             current_user: dict = Security(get_current_user, scopes=["favourite:write"])):
    user_id = current_user["user_id"]

    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    favourite = db.query(Favourite).filter(Favourite.user_id == user_id).first()
    if not favourite:
        favourite = Favourite(user_id=user_id)
        db.add(favourite)
        db.commit()
        db.refresh(favourite)

    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    # Проверка, есть ли уже товар в избранном
    fav_item = db.query(FavouriteItem).filter(
        FavouriteItem.favourite_id == favourite.id,
        FavouriteItem.product_id == item_data.product_id
    ).first()
    if fav_item:
        raise HTTPException(status_code=400, detail='Product already in favourite')

    fav_item = FavouriteItem(favourite_id=favourite.id, product_id=item_data.product_id)
    db.add(fav_item)
    db.commit()
    db.refresh(fav_item)
    return fav_item


# Удалить товар из избранного
@favourite_router.delete('/item/{product_id}/')
async def delete_favourite_item(product_id: int, user_id: int, db: Session = Depends(get_db),
                                current_user: dict = Security(get_current_user, scopes=["favourite:write"])):

    user_id = current_user["user_id"]
    favourite = db.query(Favourite).filter(Favourite.user_id == user_id).first()
    if not favourite:
        raise HTTPException(status_code=404, detail='Favourite not found')

    fav_item = db.query(FavouriteItem).filter(
        FavouriteItem.favourite_id == favourite.id,
        FavouriteItem.product_id == product_id
    ).first()
    if not fav_item:
        raise HTTPException(status_code=404, detail='Product not in favourite')

    db.delete(fav_item)
    db.commit()
    return {'message': 'Item deleted'}