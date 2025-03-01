from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth import hash_password, verify_password, create_access_token
from pydantic import BaseModel
from datetime import timedelta
from typing import List  
import httpx  # Add this import at the top of the file


router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models






def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first() #chekc if user exist
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(user.password) #store hashed pass
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw) #new user obj
    db.add(new_user) #save to db
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # check if user exists in the database
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    # verify password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    #generate JWT token
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

EVENT_SERVICE_URL = "http://localhost:8080/api/events"
# Fetch events from Event Service
@router.get("/events")
async def get_events():
    async with httpx.AsyncClient() as client:
        response = await client.get(EVENT_SERVICE_URL)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch events")

        return response.json()

@router.get("/", response_model=List[UserResponse])  #  Use Pydantic Model Instead
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users  # FastAPI will convert SQLAlchemy objects to Pydantic automatically


# This creates a /users endpoint.
# It fetches all users from the database.
# It returns them as a JSON response.
