"""
Тесты мониторинга
"""

import pytest
from fastapi.testclient import TestClient
from app import app
from monitoring import MetricsCollector, HealthChecker

client = TestClient(app)


class TestMonitoringEndpoints:
    """Тесты endpoints мониторинга"""

    def test_health_endpoint(self):
        """Тест endpoint здоровья системы"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "checks" in data
        assert isinstance(data["checks"], dict)

    def test_live_endpoint(self):
        """Тест endpoint жизнеспособности"""
        response = client.get("/live")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"
        assert "message" in data
        assert "timestamp" in data

    def test_ready_endpoint(self):
        """Тест endpoint готовности"""
        response = client.get("/ready")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data

    def test_metrics_endpoint(self):
        """Тест endpoint метрик"""
        response = client.get("/metrics")

        assert response.status_code == 200
        assert (
            response.headers["content-type"]
            == "text/plain; version=1.0.0; charset=utf-8"
        )

        # Проверяем, что возвращаются метрики Prometheus
        content = response.text
        assert "http_requests_total" in content
        assert "http_request_duration_seconds" in content

    def test_status_endpoint(self):
        """Тест endpoint статуса"""
        response = client.get("/status")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data


class TestMetricsCollector:
    """Тесты сборщика метрик"""

    def test_metrics_collector_singleton(self):
        """Тест синглтона MetricsCollector"""
        collector1 = MetricsCollector()
        collector2 = MetricsCollector()

        assert collector1 is collector2

    def test_record_request(self):
        """Тест записи метрики запроса"""
        collector = MetricsCollector()

        # Записываем метрику
        collector.record_request("GET", "/test", 200, 0.1)

        # Проверяем, что метрика записана
        samples = collector.request_count.collect()[0].samples
        total_requests = sum(sample.value for sample in samples)
        assert total_requests > 0

    def test_record_error(self):
        """Тест записи метрики ошибки"""
        collector = MetricsCollector()

        # Записываем ошибку
        collector.record_error("GET", "/test", "client_error")

        # Проверяем, что ошибка записана
        samples = collector.error_count.collect()[0].samples
        total_errors = sum(sample.value for sample in samples)
        assert total_errors > 0

    def test_record_business_metric(self):
        """Тест записи бизнес-метрики"""
        collector = MetricsCollector()

        # Записываем бизнес-метрику
        collector.record_business_metric("users_registered", 1)

        # Проверяем, что метрика записана
        samples = collector.business_metrics["users_registered"].collect()[0].samples
        total_users = sum(sample.value for sample in samples)
        assert total_users > 0

    def test_update_system_metrics(self):
        """Тест обновления системных метрик"""
        collector = MetricsCollector()

        # Обновляем системные метрики
        collector.update_system_metrics()

        # Проверяем, что метрики обновлены
        memory_samples = collector.memory_usage.collect()[0].samples
        memory_usage = sum(sample.value for sample in memory_samples)
        assert memory_usage > 0

        cpu_samples = collector.cpu_usage.collect()[0].samples
        cpu_usage = sum(sample.value for sample in cpu_samples)
        assert cpu_usage >= 0


class TestHealthChecker:
    """Тесты проверки здоровья"""

    def test_health_checker_initialization(self):
        """Тест инициализации HealthChecker"""
        checker = HealthChecker()

        assert "database" in checker.checks
        assert "memory" in checker.checks
        assert "disk" in checker.checks
        assert "cpu" in checker.checks

    @pytest.mark.asyncio
    async def test_check_memory(self):
        """Тест проверки памяти"""
        checker = HealthChecker()

        # Выполняем проверку памяти
        result = await checker._check_memory()

        assert "status" in result
        assert "memory_percent" in result
        assert "memory_available_gb" in result
        assert "memory_total_gb" in result
        assert "timestamp" in result

        # Проверяем, что статус валидный
        assert result["status"] in ["healthy", "warning", "critical"]

    @pytest.mark.asyncio
    async def test_check_disk(self):
        """Тест проверки диска"""
        checker = HealthChecker()

        # Выполняем проверку диска
        result = await checker._check_disk()

        assert "status" in result
        assert "disk_percent" in result
        assert "disk_free_gb" in result
        assert "disk_total_gb" in result
        assert "timestamp" in result

        # Проверяем, что статус валидный
        assert result["status"] in ["healthy", "warning", "critical"]

    @pytest.mark.asyncio
    async def test_check_cpu(self):
        """Тест проверки CPU"""
        checker = HealthChecker()

        # Выполняем проверку CPU
        result = await checker._check_cpu()

        assert "status" in result
        assert "cpu_percent" in result
        assert "cpu_count" in result
        assert "timestamp" in result

        # Проверяем, что статус валидный
        assert result["status"] in ["healthy", "warning", "critical"]

    @pytest.mark.asyncio
    async def test_check_all(self):
        """Тест проверки всех компонентов"""
        checker = HealthChecker()

        # Выполняем проверку всех компонентов
        result = await checker.check_all()

        assert "status" in result
        assert "timestamp" in result
        assert "checks" in result

        # Проверяем, что все проверки выполнены
        assert "memory" in result["checks"]
        assert "disk" in result["checks"]
        assert "cpu" in result["checks"]

        # Проверяем, что статус валидный
        assert result["status"] in ["healthy", "unhealthy"]


class TestMonitoringIntegration:
    """Интеграционные тесты мониторинга"""

    def test_metrics_collection_during_request(self):
        """Тест сбора метрик во время запроса"""
        # Делаем несколько запросов
        client.get("/")
        client.get("/health")
        client.get("/live")

        # Получаем метрики
        response = client.get("/metrics")
        assert response.status_code == 200

        content = response.text

        # Проверяем, что метрики записались
        assert "http_requests_total" in content
        assert "http_request_duration_seconds" in content

    def test_health_check_with_metrics(self):
        """Тест проверки здоровья с метриками"""
        # Получаем статус системы
        response = client.get("/status")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "health" in data
        assert "metrics" in data

        # Проверяем структуру данных
        health = data["health"]
        assert "status" in health
        assert "checks" in health

        metrics = data["metrics"]
        assert "system" in metrics
        assert "metrics" in metrics
