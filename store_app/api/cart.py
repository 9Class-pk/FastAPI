from fastapi import HTTPException, Depends, APIRouter
from store_app.db.models import Product, Cart, CartItem, UserProfile
from store_app.db.schema import CartSchema, CartItemSchema, CartItemCreateSchema
from store_app.db.database import  SessionLocal
from sqlalchemy.orm import Session



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


cart_router = APIRouter(prefix='/cart', tags=['Cart'])


@cart_router.get('/', response_model=CartSchema)
async def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail='Cart not found')
    return cart


# Добавить товар в корзину или обновить количество
@cart_router.post('/item/', response_model=CartItemSchema)
async def add_or_update_cart_item(item_data: CartItemCreateSchema, user_id: int, db: Session = Depends(get_db)):
    # Проверяем пользователя
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    # Проверяем корзину
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Проверяем продукт
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    # Проверяем, есть ли уже такой товар в корзине
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_data.product_id
    ).first()

    if cart_item:
        cart_item.quantity += item_data.quantity or 1
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=item_data.product_id,
                             quantity=item_data.quantity or 1)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item


# Удалить товар из корзины
@cart_router.delete('/item/{product_id}/')
async def delete_cart_item(product_id: int, user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail='Cart not found')

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail='Product not in cart')

    db.delete(cart_item)
    db.commit()
    return {'message': 'Item deleted'}