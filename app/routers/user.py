from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.models.user import User
from app.core.dependencies import get_db

from app.core.security import hash_password

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import UserCreate, UserLogin

from app.core.security import hash_password, verify_password

from app.core.auth import create_access_token

from app.core.auth import get_current_user
router = APIRouter()


@router.post("/register",status_code=201,summary="Register a new organization")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    new_user = User(
        organization_name=user.organization_name,
        contact_person=user.contact_person,
        email=user.email,
        password=hash_password(user.password),
        contact_number=user.contact_number,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }

@router.post("/login",summary="Authenticate user and return JWT")
def login(user: UserLogin, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):

    return {
        "organization_name": current_user.organization_name,
        "contact_person": current_user.contact_person,
        "email": current_user.email,
        "role": current_user.role
    }