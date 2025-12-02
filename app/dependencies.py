from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from .database import SessionLocal
from . import models, schemas
from .auth import SECRET_KEY, ALGORITHM, oauth2_scheme

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_user_by_username(db, username):
    return db.query(models.User).filter(models.User.username == username).first()

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    cred_exc = HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None: raise cred_exc
    except JWTError:
        raise cred_exc
    user = get_user_by_username(db, username)
    if not user or not user.is_active: raise cred_exc
    return user

async def get_current_admin(user: models.User = Depends(get_current_user)):
    if user.role != models.RoleEnum.admin:
        raise HTTPException(403, "Admin privileges required")
    return user

async def get_current_employee(user: models.User = Depends(get_current_user)):
    if user.role != models.RoleEnum.employee:
        raise HTTPException(403, "Employee privileges required")
    return user
