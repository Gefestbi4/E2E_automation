from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main_routers import router as main_router
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
app.include_router(main_router)

# Подключение роутера уведомлений
from routers.notifications import router as notifications_router

app.include_router(notifications_router)

# Подключение роутера медиафайлов
from routers.media import router as media_router

app.include_router(media_router)

# Подключение роутера поиска
from routers.search import router as search_router

app.include_router(search_router)

# Подключение роутера настроек
from routers.settings import router as settings_router

app.include_router(settings_router)

# Подключение роутера AI
from routers.ai import router as ai_router

app.include_router(ai_router)

# Подключение роутера расширенной аналитики
from routers.advanced_analytics import router as advanced_analytics_router

app.include_router(advanced_analytics_router)

# Подключение роутера интеграций
from routers.integrations import router as integrations_router

app.include_router(integrations_router)

# Подключение роутера расширенных уведомлений
from routers.advanced_notifications import router as advanced_notifications_router

app.include_router(advanced_notifications_router)

# Подключение роутера ролей и разрешений
from routers.roles import router as roles_router

app.include_router(roles_router)

# Подключение роутера мониторинга
from routers.monitoring import router as monitoring_router

app.include_router(monitoring_router)

# Подключение роутера тестирования
from routers.testing import router as testing_router

app.include_router(testing_router)


@app.get("/")
def read_root():
    return {"message": "E2E Automation API is running"}
