from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db import get_db
from backend.app.models.models import User
from backend.app.schemas import UserSchema, UserCreateSchema, UserUpdateSchema
from datetime import datetime

router = APIRouter()


# -------------------------------------------------------
# Create User
# -------------------------------------------------------
@router.post("/", response_model=UserSchema)
def create_user(payload: UserCreateSchema, db: Session = Depends(get_db)):
    new_user = User(
        name=payload.name,
        phone=payload.phone,
        default_location=payload.default_location,
        years_of_experience=payload.years_of_experience,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -------------------------------------------------------
# Get User by ID
# -------------------------------------------------------
@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -------------------------------------------------------
# Get ALL Users
# -------------------------------------------------------
@router.get("/", response_model=list[UserSchema])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# -------------------------------------------------------
# Update User
# -------------------------------------------------------
@router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: int, payload: UserUpdateSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(user, field, value)

    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


# -------------------------------------------------------
# Delete User
# -------------------------------------------------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
