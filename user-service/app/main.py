from fastapi import FastAPI
from app.routes.user_routes import router  # ✅ FIXED IMPORT
from app.database import engine
from app.models import Base

app = FastAPI()

# Initialize database tables
Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/users", tags=["Users"])

@app.get("/")
def health_check():
    return {"status": "User Service is Running"}
