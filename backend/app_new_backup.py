"""
Главное приложение FastAPI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from core.config import settings
from core.database import create_tables
from api.auth import router as auth_router

# Создание приложения
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Полноценное веб-приложение для обучения автоматизаторов",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]  # В продакшене указать конкретные хосты
)

# Подключение роутеров
app.include_router(auth_router)

# TODO: Добавить остальные роутеры
# app.include_router(ecommerce_router, prefix="/api")
# app.include_router(social_router, prefix="/api")
# app.include_router(tasks_router, prefix="/api")
# app.include_router(content_router, prefix="/api")
# app.include_router(analytics_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """События при запуске приложения"""
    # Создаем таблицы в БД
    create_tables()


@app.on_event("shutdown")
async def shutdown_event():
    """События при остановке приложения"""
    pass


@app.get("/")
async def root():
    """Главная страница API"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Обработчик 404 ошибок"""
    return JSONResponse(status_code=404, content={"detail": "Endpoint not found"})


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Обработчик 500 ошибок"""
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


if __name__ == "__main__":
    uvicorn.run("app_new:app", host="0.0.0.0", port=5000, reload=settings.DEBUG)
