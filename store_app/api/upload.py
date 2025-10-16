from fastapi import APIRouter, UploadFile, File
import os
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from store_app.db.database import SessionLocal
from store_app.db.models import ProductImage
from store_app.db.schema import ProductImageOutSchema, ProductImageCreateSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


upload_router = APIRouter(prefix="/upload", tags=['ProductImage'])


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "product_images")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@upload_router.post("/upload-image", response_model=ProductImageOutSchema)
async def upload_image(product_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Проверка типа файла
    if not file.content_type.startswith("image/"):
        return {"error": "Можно загружать только изображения"}

    # Путь сохранения
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Сохраняем в базу
    product_image = ProductImage(product_id=product_id, image=file.filename)
    db.add(product_image)
    db.commit()
    db.refresh(product_image)

    return product_image
