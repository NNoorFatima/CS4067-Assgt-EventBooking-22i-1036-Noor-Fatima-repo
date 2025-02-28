# crud.py
from sqlalchemy.orm import Session
from app.models import User  # ✅ Correct

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

#create a new user
def create_user(db: Session, username: str, email: str, password: str):
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
