from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlmodel import Field

from app.config import settings
from app.db.session import get_db
from app.Models.user_model import User

auth_router = APIRouter(tags=['Auth'])


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')


class createUserRequest(BaseModel):
    first_name: str = Field(alias='First Name')
    last_name: str = Field(alias='Last Name')
    username: str = Field(alias='User Name')
    password: str = Field(min_length=5, max_length=20, unique=True, alias='Password')
    email: EmailStr = Field(alias='Email')


class CreateAuthToken(BaseModel):
    access_token: str
    token_type: str


@auth_router.post("/create")
def create_user(create_user: createUserRequest, db: Session = Depends(get_db)):
    password = create_user.password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12, prefix=b"2b")
    hashed_password = bcrypt.hashpw(password=password, salt=salt).decode("utf-8")
    new_user = User(
        email=create_user.email,
        username=create_user.username,
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    return Response('User Created Successfully', status_code=201)


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()  # type: ignore
    if not user:
        return False
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return False
    return user


@auth_router.post('/token', response_model=CreateAuthToken)
def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        return False
    access_token = create_access_token(username=user.username, id=user.id, expiry=timedelta(days=7))
    return {'access_token': access_token, 'token_type': 'bearer'}


def create_access_token(username: str, id: int, expiry: timedelta):
    expire = datetime.utcnow() + expiry
    encode = {'user': username, 'id': id}
    encode.update({'exp': int(expire.timestamp())})
    token = jwt.encode(encode, settings.secret_key, settings.algorithm)
    return token


def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, settings.secret_key, settings.algorithm)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail='User not authorised')
