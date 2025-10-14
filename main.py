import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from store_app.db.models import  Product
from store_app.db.schema import ProductOutSchema, ProductCreateSchema
from store_app.db.database import  SessionLocal
from sqlalchemy.orm import Session
from typing import List
from store_app.api import category, subcategory, product, auth



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
store.include_router(auth.auth_router)



#Product/////////


if __name__ == '__main__':
    uvicorn.run(store, host='127.0.0.1', port=8080)


