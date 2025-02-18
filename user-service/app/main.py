# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, crud  # ✅ Correct import
from app.database import SessionLocal, engine, Base  # ✅ Correct

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    return crud.create_user(db, username, email, password)
