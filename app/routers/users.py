from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..auth import get_password_hash
from ..dependencies import get_db, get_current_admin

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserOut)
def create(user_in: schemas.UserCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    if db.query(models.User).filter(models.User.username == user_in.username).first():
        raise HTTPException(400, "Username exists")
    user = models.User(username=user_in.username, hashed_password=get_password_hash(user_in.password), role=user_in.role)
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.get("/", response_model=list[schemas.UserOut])
def all(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(models.User).all()
