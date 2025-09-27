from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router
from models import create_db_and_tables
from middleware import SecurityMiddleware, RequestLoggingMiddleware
from monitoring import MetricsCollector, PrometheusMetrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (если нужно)


app = FastAPI(
    title="E2E Automation API",
    description="API для фреймворка автоматизации тестирования",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware для мониторинга
metrics_collector = MetricsCollector()
app.add_middleware(PrometheusMetrics, metrics_collector=metrics_collector)

# Middleware для безопасности
app.add_middleware(SecurityMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost",
        "http://127.0.0.1:3000",
        "http://frontend:80",
        "http://frontend",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутов
app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "E2E Automation API is running"}
