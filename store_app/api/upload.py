from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from store_app.db.database import SessionLocal
from store_app.db.models import ProductImage, CategoryImage
from store_app.db.schema import UploadImageResponse
import os
from datetime import date

upload_router = APIRouter(prefix="/upload", tags=['ImageUpload'])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "static",)
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@upload_router.post("/upload-image", response_model=UploadImageResponse)
async def upload_image(
    product_id: int | None = None,
    category_id: int | None = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not product_id and not category_id:
        raise HTTPException(status_code=400, detail="Нужно указать product_id или category_id")

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Можно загружать только изображения")

    # Тип папки и дата
    folder_type = "product_images" if product_id else "category_images"
    today = date.today().isoformat()  # '2025-10-20'

    # Создаем папку
    upload_dir = os.path.join(BASE_DIR, "static", folder_type, today)
    os.makedirs(upload_dir, exist_ok=True)

    # Генерация уникального имени файла
    import uuid
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_location = os.path.join(upload_dir, filename)

    # Сохраняем файл
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Создаем объект для базы
    if product_id:
        image_obj = ProductImage(product_id=product_id, image=filename)
    else:
        image_obj = CategoryImage(category_id=category_id, category_image=filename)

    db.add(image_obj)
    db.commit()
    db.refresh(image_obj)

    return UploadImageResponse(
        id=image_obj.id,
        image=filename,
        product_id=product_id,
        category_id=category_id
    )
