from fastapi import HTTPException, Depends, APIRouter
from store_app.db.models import Product
from store_app.db.schema import ProductOutSchema, ProductCreateSchema
from store_app.db.database import  SessionLocal
from sqlalchemy.orm import Session
from typing import List



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


product_router = APIRouter(prefix='/product', tags=['Product'])


@product_router.post("/", response_model=ProductCreateSchema)
async def create_product(product: ProductCreateSchema, db:Session = Depends(get_db)):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get("/", response_model=List[ProductOutSchema])
async def list_product(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get("/{product_id}/", response_model=ProductCreateSchema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id==product_id).first()
    if product_db is None:
        raise HTTPException(status_code=404, detail='Нету такого продукат')
    return product_db


@product_router.put("/{product_id}/")
async def update_product(product: ProductCreateSchema, product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail="Product not found")

    for product_key, product_value in product.dict().items():
        setattr(product_db, product_key, product_value)

    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.delete("/{product_id}/")
async def delete_product(product_id: int, db:Session = Depends(get_db)):
    product_db = db.query(Product). filter(Product.id == product_id).first()
    if product_db is None:
        raise HTTPException(status_code=404, detail='Нету такой категории')
    db.delete(product_db)
    db.commit()
    return  {'message': 'Deleted'}


