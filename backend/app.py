from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router
from models import create_db_and_tables

app = FastAPI(
    title="E2E Automation API",
    description="API для фреймворка автоматизации тестирования",
    version="1.0.0",
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутов
app.include_router(router)


@app.on_event("startup")
def on_startup():
    """Создание таблиц в БД при старте"""
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "E2E Automation API is running"}
