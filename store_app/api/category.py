from fastapi import FastAPI, HTTPException, Depends, APIRouter
from store_app.db.models import Category
from store_app.db.schema import CategorySchema
from store_app.db.database import  SessionLocal
from sqlalchemy.orm import Session
from typing import List



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

category_router = APIRouter(prefix='/category', tags=['Category'])



@category_router.post("/", response_model=CategorySchema)
async def create_category(category: CategorySchema, db: Session = Depends(get_db)):
    category_db = Category(category_name=category.category_name)
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.get("/", response_model=List[CategorySchema])
async def list_category(db: Session = Depends(get_db)):
    return db.query(Category).all()


@category_router.get("/{category_id}/")
async def detail_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id==category_id).first()
    if category_db is None:
        raise HTTPException(status_code=404, detail='Нету такой категории')
    return category_db


@category_router.put("/{category_id}/", response_model=dict)
async def update_category(category: CategorySchema, category_id:int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=404, detail='нету ')
    category_db.category_name = category.category_name
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return {'message': 'Updated'}



@category_router.delete("/{category_id}/")
async def delete_category(category_id: int, db:Session = Depends(get_db)):
    category_db = db.query(Category). filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=404, detail='Нету такой категории')
    db.delete(category_db)
    db.commit()
    return  {'message': 'Deleted'}
