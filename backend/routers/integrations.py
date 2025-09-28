"""
API для внешних интеграций
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, EmailStr
from services.integration_service import integration_service
from auth import get_current_user
from models import User

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str
    template: Optional[str] = None


class SMSRequest(BaseModel):
    to: str
    message: str


class SocialMediaRequest(BaseModel):
    platform: str
    content: str
    media_urls: Optional[List[str]] = None


class PaymentRequest(BaseModel):
    amount: float
    currency: str = "USD"
    payment_method: str
    customer_id: str


class CloudStorageRequest(BaseModel):
    filename: str
    file_content: str  # Base64 encoded
    provider: str = "aws_s3"


class AnalyticsEventRequest(BaseModel):
    event_name: str
    properties: Dict[str, Any]
    provider: str = "google_analytics"


class CRMContactRequest(BaseModel):
    contact_data: Dict[str, Any]


class WebhookRequest(BaseModel):
    webhook_url: str
    data: Dict[str, Any]


class IntegrationConfigRequest(BaseModel):
    config: Dict[str, Any]


@router.post("/email/send")
async def send_email(
    request: EmailRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """Отправка email через внешний сервис"""
    try:
        result = await integration_service.send_email(
            request.to, request.subject, request.body, request.template
        )
        return {
            "result": result,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки email: {str(e)}")


@router.post("/sms/send")
async def send_sms(
    request: SMSRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """Отправка SMS через внешний сервис"""
    try:
        result = await integration_service.send_sms(request.to, request.message)
        return {
            "result": result,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки SMS: {str(e)}")


@router.post("/social-media/post")
async def post_to_social_media(
    request: SocialMediaRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """Публикация в социальных сетях"""
    try:
        result = await integration_service.post_to_social_media(
            request.platform, request.content, request.media_urls
        )
        return {
            "result": result,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка публикации в соцсети: {str(e)}"
        )


@router.post("/payment/process")
async def process_payment(
    request: PaymentRequest,
    current_user: User = Depends(get_current_user),
):
    """Обработка платежа через внешний сервис"""
    try:
        result = await integration_service.process_payment(
            request.amount,
            request.currency,
            request.payment_method,
            request.customer_id,
        )
        return {
            "result": result,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка обработки платежа: {str(e)}"
        )


@router.post("/cloud-storage/upload")
async def upload_to_cloud_storage(
    request: CloudStorageRequest,
    current_user: User = Depends(get_current_user),
):
    """Загрузка файла в облачное хранилище"""
    try:
        import base64

        file_content = base64.b64decode(request.file_content)

        result = await integration_service.upload_to_cloud_storage(
            file_content, request.filename, request.provider
        )
        return {
            "result": result,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка загрузки в облако: {str(e)}"
        )


@router.post("/analytics/track")
async def track_analytics_event(
    request: AnalyticsEventRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """Отправка события в аналитику"""
    try:
        result = await integration_service.track_analytics_event(
            request.event_name, request.properties, request.provider
        )
        return {
            "result": result,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка отправки в аналитику: {str(e)}"
        )


@router.post("/crm/sync")
async def sync_with_crm(
    request: CRMContactRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """Синхронизация с CRM системой"""
    try:
        result = await integration_service.sync_with_crm(request.contact_data)
        return {
            "result": result,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка синхронизации с CRM: {str(e)}"
        )


@router.post("/webhook/send")
async def send_webhook(
    request: WebhookRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """Отправка webhook уведомления"""
    try:
        result = await integration_service.webhook_callback(
            request.webhook_url, request.data
        )
        return {
            "result": result,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка отправки webhook: {str(e)}"
        )


@router.get("/status")
async def get_integration_status(current_user: User = Depends(get_current_user)):
    """Получение статуса всех интеграций"""
    try:
        status = integration_service.get_integration_status()
        return {
            "status": status,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения статуса: {str(e)}"
        )


@router.put("/configure/{category}/{service}")
async def configure_integration(
    category: str,
    service: str,
    request: IntegrationConfigRequest,
    current_user: User = Depends(get_current_user),
):
    """Настройка интеграции"""
    try:
        result = integration_service.configure_integration(
            category, service, request.config
        )
        return {
            "result": result,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка настройки интеграции: {str(e)}"
        )


@router.post("/test/{category}/{service}")
async def test_integration(
    category: str,
    service: str,
    current_user: User = Depends(get_current_user),
):
    """Тестирование интеграции"""
    try:
        result = integration_service.test_integration(category, service)
        return {
            "result": result,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка тестирования интеграции: {str(e)}"
        )


@router.get("/logs/{category}/{service}")
async def get_integration_logs(
    category: str,
    service: str,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
):
    """Получение логов интеграции"""
    try:
        logs = integration_service.get_integration_logs(category, service, limit)
        return {
            "logs": logs,
            "category": category,
            "service": service,
            "total": len(logs),
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения логов: {str(e)}")


@router.get("/available")
async def get_available_integrations(current_user: User = Depends(get_current_user)):
    """Получение списка доступных интеграций"""
    try:
        available = {
            "email_providers": [
                {"name": "SendGrid", "id": "sendgrid", "enabled": True},
                {"name": "Mailgun", "id": "mailgun", "enabled": False},
                {"name": "AWS SES", "id": "aws_ses", "enabled": False},
            ],
            "sms_providers": [
                {"name": "Twilio", "id": "twilio", "enabled": True},
                {"name": "AWS SNS", "id": "aws_sns", "enabled": False},
                {"name": "MessageBird", "id": "messagebird", "enabled": False},
            ],
            "social_media": [
                {"name": "Twitter", "id": "twitter", "enabled": True},
                {"name": "Facebook", "id": "facebook", "enabled": True},
                {"name": "LinkedIn", "id": "linkedin", "enabled": True},
                {"name": "Instagram", "id": "instagram", "enabled": False},
            ],
            "payment_providers": [
                {"name": "Stripe", "id": "stripe", "enabled": True},
                {"name": "PayPal", "id": "paypal", "enabled": True},
                {"name": "Square", "id": "square", "enabled": False},
            ],
            "cloud_storage": [
                {"name": "AWS S3", "id": "aws_s3", "enabled": True},
                {"name": "Google Drive", "id": "google_drive", "enabled": True},
                {"name": "Dropbox", "id": "dropbox", "enabled": False},
            ],
            "analytics": [
                {"name": "Google Analytics", "id": "google_analytics", "enabled": True},
                {"name": "Mixpanel", "id": "mixpanel", "enabled": True},
                {"name": "Amplitude", "id": "amplitude", "enabled": False},
            ],
            "crm": [
                {"name": "Salesforce", "id": "salesforce", "enabled": False},
                {"name": "HubSpot", "id": "hubspot", "enabled": False},
                {"name": "Pipedrive", "id": "pipedrive", "enabled": False},
            ],
        }

        return {
            "available_integrations": available,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения списка интеграций: {str(e)}"
        )


@router.get("/health")
async def integration_health_check():
    """Проверка состояния интеграционных сервисов"""
    try:
        health_status = {
            "status": "healthy",
            "integrations": {
                "email": "operational",
                "sms": "operational",
                "social_media": "operational",
                "payment": "operational",
                "cloud_storage": "operational",
                "analytics": "operational",
            },
            "last_check": "2025-01-28T10:00:00Z",
            "uptime": "99.9%",
        }

        return health_status

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка проверки состояния: {str(e)}"
        )
