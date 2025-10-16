from fastapi import HTTPException, Depends, APIRouter
from store_app.db.models import SubCategory
from store_app.db.schema import SubCategorySchema
from store_app.db.database import  SessionLocal
from sqlalchemy.orm import Session
from typing import List



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

subcategory_router = APIRouter(prefix='/subcategory', tags=['Subcategory'])



@subcategory_router.post("/")
async def create_subcategory(subcategory: SubCategorySchema, db: Session = Depends(get_db)):
    subcategory_db = SubCategory(sub_category_name=subcategory.sub_category_name, category_id=subcategory.category_id)
    db.add(subcategory_db)
    db.commit()
    db.refresh(subcategory_db)
    return subcategory_db



@subcategory_router.get("/", response_model=List[SubCategorySchema])
async def list_subcategory(db: Session = Depends(get_db)):
    return db.query(SubCategory).all()


@subcategory_router.get("/{subcategory_id}")
async def detail_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id==subcategory_id).first()
    if subcategory_db is None:
        raise HTTPException(status_code=404, detail='Нету такой категории')
    return subcategory_db


@subcategory_router.put("/{subcategory_id}/", response_model=dict)
async def update_subcategory(subcategory: SubCategorySchema, subcategory_id:int, db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if subcategory_db is None:
        raise HTTPException(status_code=404, detail='нету ')
    subcategory_db.sub_category_name = subcategory.sub_category_name
    db.add(subcategory_db)
    db.commit()
    db.refresh(subcategory_db)
    return {'message': 'Updated'}



@subcategory_router.delete("/{subcategory_id}/")
async def delete_subcategory(subcategory_id: int, db:Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory). filter(SubCategory.id == subcategory_id).first()
    if subcategory_db is None:
        raise HTTPException(status_code=404, detail='Нету такой категории')
    db.delete(subcategory_db)
    db.commit()
    return  {'message': 'Deleted'}