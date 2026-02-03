from passlib.context import CryptContext
from jose import jwt, JWTError
from environs import Env
from datetime import timedelta, datetime

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
env = Env()
env.read_env(".env")
secret_key = env('SECRET_KEY')
algorithm = env('ALGORITHM')

async def get_password_hash(password):
    return pwd_context.hash(password)

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

async def decode_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        return None