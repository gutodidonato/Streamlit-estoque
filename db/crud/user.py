from ..models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db import get_db_auth
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(username: str, password: str, email: str) -> object | None:
    db = get_db_auth()
    try:
        hashed_password = pwd_context.hash(password)
        db_user = User(username=username, password=hashed_password, email=email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        return None
    finally:
        db.close()

def get_user_auth(username: str, password: str) -> object | None:
    db = get_db_auth()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and pwd_context.verify(password, user.password):
            return user
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()

def get_user(user_id: int) -> object:
    db = get_db_auth()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()

def get_user_by_email(email: str) -> object:
    db = get_db_auth()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()

def get_users(skip: int = 0, limit: int = 100) -> list:
    db = get_db_auth()
    try:
        return db.query(User).offset(skip).limit(limit).all()
    finally:
        db.close()

def update_user(user_id: int, username: str = None, password: str = None, email: str = None) -> object | None:
    db = get_db_auth()
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            if username:
                db_user.username = username
            if password:
                db_user.password = pwd_context.hash(password)
            if email:
                db_user.email = email
            db.commit()
            db.refresh(db_user)
        return db_user
    finally:
        db.close()

def delete_user(user_id: int) -> bool:
    db = get_db_auth()
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False
    finally:
        db.close()