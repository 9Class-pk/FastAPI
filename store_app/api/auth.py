from datetime import timedelta, datetime
from fastapi import HTTPException, Depends, APIRouter, Security
from starlette import status
from store_app.db.models import UserProfile, RefreshToken
from store_app.db.schema import UserProfileSchema, UserProfileLoginSchema
from store_app.db.database import  SessionLocal
from sqlalchemy.orm import Session
from typing import List, Optional
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from store_app.config import (ALGORITHM, SECRET_KEY,
                                ACCESS_TOKEN_LIFETIME,
                              REFRESH_TOKEN_LIFETIME)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

#refresh token
def create_access_token(data:dict, scopes: List[str], expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({'exp': expire, 'scopes': scopes})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#refresh token
def create_refresh_token(data:dict):
    return create_access_token(data, scopes=[], expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))


@auth_router.post('/register', response_model=dict)
async def register(user: UserProfileSchema, db: Session = Depends(get_db)):
    user_name = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    user_email = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if user_name:
        raise HTTPException(status_code=400, detail='Username is have')
    elif user_email:
        raise HTTPException(status_code=400, detail='User email is have')
    new_hash_pass = get_password_hash(user.password)
    new_user = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        age=user.age,
        phone_number=user.phone_number,
        status=user.status,
        password=new_hash_pass
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'Registered'}


@auth_router.post('/login', response_model=None)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Маалымат туура эмес")

    user_scopes = [
        "cart:read", "cart:write",
        "favourite:read", "favourite:write",
        "product:read", "product:write",
        "category:read", "category:write",
        "subcategory:read", "subcategory:write"
    ]

    access_token = create_access_token({"sub": user.username}, scopes=user_scopes)
    refresh_token = create_refresh_token({"sub": user.username})


    new_token = RefreshToken(user_id=user.id, token=refresh_token)
    db.add(new_token)
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@auth_router.post('/logout')
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Маалымат туура эмес")
    db.delete(stored_token)
    db.commit()
    return {"message": "вышли"}


@auth_router.post('/refresh')
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Маалымат туура эмес")
    access_token = create_access_token({"sub": stored_token.id})
    return {"access_token": access_token, "token_type": "bearer"}



#scope --> permissions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login",
        scopes={
        "cart:read": "Просмотр корзины",
        "cart:write": "Добавление/удаление товаров в корзине",
        "favourite:read": "Просмотр избранного",
        "favourite:write": "Добавление/удаление товаров в избранное",
        "product:read": "Просмотр продуктов",
        "product:write": "Создание/редактирование продуктов",
        "category:read": "Просмотр категорий",
        "category:write": "Создание/редактирование категорий",
        "subcategory:read": "Просмотр подкатегорий",
        "subcategory:write": "Создание/редактирование подкатегорий",
    }

)

def decode_token_scopes(token: str) -> List[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("scopes", [])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def decode_token_user_id(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        db = SessionLocal()
        user = db.query(UserProfile).filter(UserProfile.username == username).first()
        db.close()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user.id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(security_scopes: SecurityScopes, token: str = Security(oauth2_scheme)):
    token_scopes = decode_token_scopes(token)
    user_id = decode_token_user_id(token)

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(status_code=403, detail="Not enough permissions")

    return {"user_id": user_id, "scopes": token_scopes}