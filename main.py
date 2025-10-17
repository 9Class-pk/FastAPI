import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from store_app.db.models import  Product
from store_app.db.schema import ProductOutSchema, ProductCreateSchema
from store_app.db.database import  SessionLocal
from sqlalchemy.orm import Session
from typing import List
from store_app.api import (category, subcategory, product, auth,
                           upload, cart, favourite, social_auth)
from store_app.admin.setup import setup_admin
import os
from fastapi.staticfiles import StaticFiles
from store_app import static
from starlette.middleware.sessions import SessionMiddleware


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





store = FastAPI()
store.include_router(category.category_router)
store.include_router(subcategory.subcategory_router)
store.include_router(product.product_router)
store.include_router(cart.cart_router)
store.include_router(favourite.favourite_router)
store.include_router(upload.upload_router)
store.include_router(auth.auth_router)
store.include_router(social_auth.social_router)

setup_admin(store)

#oauth middleware
store.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")








#StaticFiles for images////////////
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "store_app", "static")

store.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
#Product/////////


if __name__ == '__main__':
    uvicorn.run(store, host='127.0.0.1', port=8080)


