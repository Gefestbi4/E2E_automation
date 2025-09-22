
from fastapi import FastAPI
from .routers import user_router
from .models import create_db_and_tables

app = FastAPI(
    title="User Management Service",
    description="API for managing users.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user_router, prefix="/api/v1", tags=["Users"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "User Management Service is running."}

# To run this app:
# uvicorn back_end.user_api_app:app --reload
