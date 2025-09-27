"""
Схемы для Analytics модуля
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from .base import BaseSchema, TimestampMixin
from .auth import UserResponse


class MetricBase(BaseSchema):
    """Базовая схема метрики"""

    name: str = Field(..., min_length=1, max_length=100, description="Название метрики")
    value: float = Field(..., description="Значение метрики")
    unit: Optional[str] = Field(None, max_length=20, description="Единица измерения")
    description: Optional[str] = Field(None, description="Описание метрики")


class MetricCreate(MetricBase):
    """Схема создания метрики"""

    category: str = Field(
        ..., min_length=1, max_length=100, description="Категория метрики"
    )


class MetricUpdate(BaseSchema):
    """Схема обновления метрики"""

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Название метрики"
    )
    value: Optional[float] = Field(None, description="Значение метрики")
    unit: Optional[str] = Field(None, max_length=20, description="Единица измерения")
    description: Optional[str] = Field(None, description="Описание метрики")
    category: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Категория метрики"
    )


class MetricResponse(MetricBase, TimestampMixin):
    """Схема ответа с данными метрики"""

    id: int = Field(..., description="ID метрики")
    category: str = Field(..., description="Категория метрики")


class MetricListResponse(BaseSchema):
    """Схема ответа со списком метрик"""

    items: List[MetricResponse] = Field(..., description="Список метрик")
    total: int = Field(..., description="Общее количество метрик")
    skip: int = Field(..., description="Количество пропущенных метрик")
    limit: int = Field(..., description="Лимит метрик")


class ChartDataPoint(BaseSchema):
    """Схема точки данных для графика"""

    label: str = Field(..., description="Метка точки")
    value: float = Field(..., description="Значение точки")
    color: Optional[str] = Field(None, description="Цвет точки")


class ChartData(BaseSchema):
    """Схема данных графика"""

    labels: List[str] = Field(..., description="Метки осей")
    datasets: List[Dict[str, Any]] = Field(..., description="Наборы данных")
    type: str = Field(..., description="Тип графика")


class DashboardWidgetBase(BaseSchema):
    """Базовая схема виджета дашборда"""

    title: str = Field(
        ..., min_length=1, max_length=100, description="Название виджета"
    )
    type: str = Field(..., description="Тип виджета")
    position_x: int = Field(0, ge=0, description="Позиция X")
    position_y: int = Field(0, ge=0, description="Позиция Y")
    width: int = Field(4, ge=1, le=12, description="Ширина виджета")
    height: int = Field(4, ge=1, le=12, description="Высота виджета")
    config: Dict[str, Any] = Field(
        default_factory=dict, description="Конфигурация виджета"
    )


class DashboardWidgetCreate(DashboardWidgetBase):
    """Схема создания виджета дашборда"""

    dashboard_id: int = Field(..., gt=0, description="ID дашборда")


class DashboardWidgetUpdate(BaseSchema):
    """Схема обновления виджета дашборда"""

    title: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Название виджета"
    )
    position_x: Optional[int] = Field(None, ge=0, description="Позиция X")
    position_y: Optional[int] = Field(None, ge=0, description="Позиция Y")
    width: Optional[int] = Field(None, ge=1, le=12, description="Ширина виджета")
    height: Optional[int] = Field(None, ge=1, le=12, description="Высота виджета")
    config: Optional[Dict[str, Any]] = Field(None, description="Конфигурация виджета")


class DashboardWidgetResponse(DashboardWidgetBase, TimestampMixin):
    """Схема ответа с данными виджета дашборда"""

    id: int = Field(..., description="ID виджета")
    dashboard_id: int = Field(..., description="ID дашборда")
    data: Optional[Dict[str, Any]] = Field(None, description="Данные виджета")


class DashboardBase(BaseSchema):
    """Базовая схема дашборда"""

    name: str = Field(
        ..., min_length=1, max_length=100, description="Название дашборда"
    )
    description: Optional[str] = Field(None, description="Описание дашборда")
    is_public: bool = Field(False, description="Публичный ли дашборд")
    is_default: bool = Field(False, description="Дашборд по умолчанию")


class DashboardCreate(DashboardBase):
    """Схема создания дашборда"""

    pass


class DashboardUpdate(BaseSchema):
    """Схема обновления дашборда"""

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Название дашборда"
    )
    description: Optional[str] = Field(None, description="Описание дашборда")
    is_public: Optional[bool] = Field(None, description="Публичный ли дашборд")
    is_default: Optional[bool] = Field(None, description="Дашборд по умолчанию")


class DashboardFilters(BaseSchema):
    """Фильтры для поиска дашбордов"""

    is_public: Optional[bool] = Field(None, description="Публичные дашборды")
    is_default: Optional[bool] = Field(None, description="Дашборды по умолчанию")
    search: Optional[str] = Field(None, description="Поиск по названию и описанию")


class DashboardResponse(DashboardBase, TimestampMixin):
    """Схема ответа с данными дашборда"""

    id: int = Field(..., description="ID дашборда")
    created_by: UserResponse = Field(..., description="Создатель дашборда")
    widgets: List[DashboardWidgetResponse] = Field(
        default_factory=list, description="Виджеты дашборда"
    )
    widgets_count: int = Field(0, description="Количество виджетов")


class DashboardListResponse(BaseSchema):
    """Схема ответа со списком дашбордов"""

    items: List[DashboardResponse] = Field(..., description="Список дашбордов")
    total: int = Field(..., description="Общее количество дашбордов")
    skip: int = Field(..., description="Количество пропущенных дашбордов")
    limit: int = Field(..., description="Лимит дашбордов")


class ReportBase(BaseSchema):
    """Базовая схема отчета"""

    name: str = Field(..., min_length=1, max_length=100, description="Название отчета")
    description: Optional[str] = Field(None, description="Описание отчета")
    type: str = Field(..., description="Тип отчета")
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Параметры отчета"
    )
    schedule: Optional[str] = Field(None, description="Расписание отчета")


class ReportCreate(ReportBase):
    """Схема создания отчета"""

    pass


class ReportUpdate(BaseSchema):
    """Схема обновления отчета"""

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Название отчета"
    )
    description: Optional[str] = Field(None, description="Описание отчета")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Параметры отчета")
    schedule: Optional[str] = Field(None, description="Расписание отчета")


class ReportResponse(ReportBase, TimestampMixin):
    """Схема ответа с данными отчета"""

    id: int = Field(..., description="ID отчета")
    created_by: UserResponse = Field(..., description="Создатель отчета")
    last_run: Optional[datetime] = Field(None, description="Последний запуск")
    next_run: Optional[datetime] = Field(None, description="Следующий запуск")
    is_active: bool = Field(True, description="Активен ли отчет")


class ReportListResponse(BaseSchema):
    """Схема ответа со списком отчетов"""

    items: List[ReportResponse] = Field(..., description="Список отчетов")
    total: int = Field(..., description="Общее количество отчетов")
    skip: int = Field(..., description="Количество пропущенных отчетов")
    limit: int = Field(..., description="Лимит отчетов")


class ActivityEvent(BaseSchema):
    """Схема события активности"""

    type: str = Field(..., description="Тип события")
    message: str = Field(..., description="Сообщение события")
    timestamp: datetime = Field(..., description="Время события")
    icon: Optional[str] = Field(None, description="Иконка события")
    user: Optional[UserResponse] = Field(None, description="Пользователь события")
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Дополнительные данные"
    )


class ActivityFeedResponse(BaseSchema):
    """Схема ответа с лентой активности"""

    events: List[ActivityEvent] = Field(..., description="События активности")
    total: int = Field(..., description="Общее количество событий")
    skip: int = Field(..., description="Количество пропущенных событий")
    limit: int = Field(..., description="Лимит событий")


class DashboardDataResponse(BaseSchema):
    """Схема ответа с данными дашборда"""

    metrics: List[MetricResponse] = Field(..., description="Метрики")
    charts: List[ChartData] = Field(..., description="Графики")
    recent_activity: List[ActivityEvent] = Field(
        ..., description="Последняя активность"
    )
    summary: Dict[str, Any] = Field(..., description="Сводка данных")


class ExportRequest(BaseSchema):
    """Схема запроса экспорта данных"""

    format: str = Field(..., description="Формат экспорта")
    data_type: str = Field(..., description="Тип данных")
    filters: Optional[Dict[str, Any]] = Field(None, description="Фильтры")
    date_from: Optional[datetime] = Field(None, description="Дата начала")
    date_to: Optional[datetime] = Field(None, description="Дата окончания")


class ExportResponse(BaseSchema):
    """Схема ответа экспорта данных"""

    file_url: str = Field(..., description="URL файла экспорта")
    filename: str = Field(..., description="Имя файла")
    expires_at: datetime = Field(..., description="Время истечения ссылки")
    file_size: int = Field(..., description="Размер файла")


class AnalyticsFilters(BaseSchema):
    """Схема фильтров для аналитики"""

    date_from: Optional[datetime] = Field(None, description="Дата начала")
    date_to: Optional[datetime] = Field(None, description="Дата окончания")
    category: Optional[str] = Field(None, description="Категория метрик")
    user_id: Optional[int] = Field(None, gt=0, description="Фильтр по пользователю")


# Missing filters
class MetricFilters(BaseSchema):
    """Фильтры для поиска метрик"""

    category: Optional[str] = Field(None, description="Категория метрик")
    is_active: Optional[bool] = Field(None, description="Активные метрики")
    search: Optional[str] = Field(None, description="Поиск по названию и описанию")


class ReportFilters(BaseSchema):
    """Фильтры для поиска отчетов"""

    report_type: Optional[str] = Field(None, description="Тип отчета")
    is_public: Optional[bool] = Field(None, description="Публичные отчеты")
    search: Optional[str] = Field(None, description="Поиск по названию и описанию")


class AlertFilters(BaseSchema):
    """Фильтры для поиска алертов"""

    is_active: Optional[bool] = Field(None, description="Активные алерты")
    search: Optional[str] = Field(None, description="Поиск по названию и описанию")


# Missing Alert schemas
class AlertBase(BaseSchema):
    """Базовая схема алерта"""

    name: str = Field(..., min_length=1, max_length=255, description="Название алерта")
    description: Optional[str] = Field(None, description="Описание алерта")
    condition: Dict[str, Any] = Field(..., description="Условие срабатывания")
    threshold: float = Field(..., description="Порог срабатывания")
    is_active: bool = Field(True, description="Активен ли алерт")


class AlertCreate(AlertBase):
    """Схема создания алерта"""

    pass


class AlertUpdate(BaseSchema):
    """Схема обновления алерта"""

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Название алерта"
    )
    description: Optional[str] = Field(None, description="Описание алерта")
    condition: Optional[Dict[str, Any]] = Field(
        None, description="Условие срабатывания"
    )
    threshold: Optional[float] = Field(None, description="Порог срабатывания")
    is_active: Optional[bool] = Field(None, description="Активен ли алерт")


class AlertResponse(AlertBase, TimestampMixin):
    """Схема ответа с данными алерта"""

    id: int = Field(..., description="ID алерта")
    created_by: UserResponse = Field(..., description="Создатель алерта")
    triggered_count: int = Field(0, description="Количество срабатываний")
    last_triggered: Optional[datetime] = Field(
        None, description="Последнее срабатывание"
    )


class AlertListResponse(BaseSchema):
    """Схема ответа со списком алертов"""

    items: List[AlertResponse] = Field(..., description="Список алертов")
    total: int = Field(..., description="Общее количество алертов")
    skip: int = Field(..., description="Количество пропущенных алертов")
    limit: int = Field(..., description="Лимит алертов")


# Missing Event schemas
class EventBase(BaseSchema):
    """Базовая схема события"""

    event_type: str = Field(
        ..., min_length=1, max_length=100, description="Тип события"
    )
    event_data: Dict[str, Any] = Field(..., description="Данные события")
    user_agent: Optional[str] = Field(None, description="User Agent")
    ip_address: Optional[str] = Field(None, description="IP адрес")


class EventCreate(EventBase):
    """Схема создания события"""

    pass


class EventResponse(EventBase, TimestampMixin):
    """Схема ответа с данными события"""

    id: int = Field(..., description="ID события")
    user: Optional[UserResponse] = Field(None, description="Пользователь")


class EventListResponse(BaseSchema):
    """Схема ответа со списком событий"""

    items: List[EventResponse] = Field(..., description="Список событий")
    total: int = Field(..., description="Общее количество событий")
    skip: int = Field(..., description="Количество пропущенных событий")
    limit: int = Field(..., description="Лимит событий")
    module: Optional[str] = Field(None, description="Фильтр по модулю")
