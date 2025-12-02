from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db, get_current_admin, get_current_employee, get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.TaskOut)
def create(task_in: schemas.TaskCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    owner = db.query(models.User).filter(models.User.id == task_in.owner_id).first()
    if not owner: raise HTTPException(404, "Owner not found")
    if owner.role != models.RoleEnum.employee: raise HTTPException(400, "Assign only to employees")
    task = models.Task(title=task_in.title, description=task_in.description, status=task_in.status, owner_id=task_in.owner_id)
    db.add(task); db.commit(); db.refresh(task)
    return task

@router.get("/", response_model=list[schemas.TaskOut])
def all(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(models.Task).all()

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    t = db.query(models.Task).filter(models.Task.id == id).first()
    if not t: raise HTTPException(404, "Not found")
    db.delete(t); db.commit()
    return {"deleted": id}

@router.get("/me", response_model=list[schemas.TaskOut])
def my_tasks(db: Session = Depends(get_db), emp=Depends(get_current_employee)):
    return db.query(models.Task).filter(models.Task.owner_id == emp.id).all()

@router.patch("/{id}/status", response_model=schemas.TaskOut)
def update_status(id: int, status_in: schemas.TaskUpdateStatus, db: Session = Depends(get_db), user=Depends(get_current_user)):
    t = db.query(models.Task).filter(models.Task.id == id).first()
    if not t: raise HTTPException(404, "Not found")
    if user.role == models.RoleEnum.employee and t.owner_id != user.id:
        raise HTTPException(403, "Not your task")
    t.status = status_in.status
    db.commit(); db.refresh(t)
    return t
