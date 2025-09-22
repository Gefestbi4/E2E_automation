import sentry_sdk
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import time
import redis
from config import settings
from routers import router
from models import create_db_and_tables

# Инициализация Sentry, если DSN предоставлен
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[sentry_sdk.integrations.fastapi.FastAPIIntegration()],
    )

# Создаем клиент Redis
redis_client = redis.from_url(settings.REDIS_URL)

app = FastAPI(
    title="Offer Processing Service",
    description="Сервис для обработки офферов, сохранения в БД и отправки уведомлений.",
    version="1.0.0"
)

# Подключение CORS Middleware для разрешения запросов с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретный домен фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение метрик Prometheus
Instrumentator().instrument(app).expose(app)

# Подключение роутов
app.include_router(router, prefix="/api/v1", tags=["Offers"])


@app.on_event("startup")
def on_startup():
    # Создание таблиц в базе данных при старте приложения
    # В продакшене для миграций лучше использовать Alembic
    create_db_and_tables()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Offer Processing Service is running."}


# Rate limiting middleware с использованием Redis
RATE_LIMIT_DURATION = 60  # 60 секунд
RATE_LIMIT_REQUESTS = 20  # 20 запросов


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    key = f"rate_limit:{client_ip}"

    # Используем транзакцию Redis для атомарности операций
    pipe = redis_client.pipeline()
    # 1. Удаляем старые записи (которые вышли за пределы окна)
    pipe.zremrangebyscore(key, 0, now - RATE_LIMIT_DURATION)
    # 2. Добавляем текущий запрос
    pipe.zadd(key, {str(now): now})
    # 3. Получаем количество запросов в текущем окне
    pipe.zcard(key)
    # 4. Устанавливаем время жизни ключа, чтобы он автоматически удалился
    pipe.expire(key, RATE_LIMIT_DURATION)
    
    results = pipe.execute()
    request_count = results[2]

    if request_count > RATE_LIMIT_REQUESTS:
        return Response("Too Many Requests", status_code=429)

    response = await call_next(request)
    return response

# uvicorn app:app --reload
# Сервер будет доступен по адресу http://127.0.0.1:8000. Документация API (Swagger UI) будет по адресу http://127.0.0.1:8000/docs.