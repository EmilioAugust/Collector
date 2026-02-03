import uuid, redis
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.database import Users, get_db
from app.models.models import CreateUser
from app.services.services import get_password_hash, verify_password, create_access_token, decode_token
from datetime import timedelta
from app.core.redis import r

auth_router = APIRouter(prefix='/auth', tags=['auth'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
REFRESH_TOKEN_TTL = 60 * 60 * 24 * 30  # 30 days

async def get_current_user(token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)):
    payload = await decode_token(token)
    user_id = payload.get('id')
    existing_user = db.query(Users).filter(Users.id == user_id).first()
    if payload is None:
        raise HTTPException(status_code=401, detail='Wrong token')
    if not existing_user:
        raise HTTPException(status_code=401, detail='User not found')
    return existing_user

@auth_router.post('/register')
async def register_user(user: CreateUser, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(Users).filter(Users.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists.")
        hashed_password = await get_password_hash(user.password)
        new_user = Users(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {'message': 'User registered!'}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists.")

@auth_router.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == form_data.username).first()
    if not user or not await verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Wrong username or password')
    access_token = await create_access_token(data={'id': user.id}, expires_delta=timedelta(days=30))
    return {'access_token': access_token, 'token_type': 'bearer'}

@auth_router.get('/protected')
async def protected_route(current_user: Users = Depends(get_current_user)):
    return current_user