from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import router  
from app.database import engine
from app.models import Base

app = FastAPI()
# enable cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all frontend requests (for development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables
Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/users", tags=["Users"])

@app.get("/")
def health_check():
    return {"status": "User Service is Running"}
