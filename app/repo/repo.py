from sqlalchemy.orm import Session

from app.models import models
from .. import schema
from passlib.context import CryptContext
from app.settings.utility import hash_password



def create_user(user: schema.UserCreate, db: Session):
    password = hash_password(user.password)
    db_user = models.Users(email=user.email, hashed_password=password, lassra_id=user.lassra_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()

