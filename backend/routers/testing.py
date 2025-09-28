"""
API для комплексного тестирования
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from services.testing_service import testing_service, TestType
from auth import get_current_user
from models import User

router = APIRouter(prefix="/api/testing", tags=["testing"])


class TestRunRequest(BaseModel):
    test_type: str
    test_names: Optional[List[str]] = None
    parallel: Optional[bool] = None


class TestResultResponse(BaseModel):
    test_id: str
    test_name: str
    test_type: str
    status: str
    duration: float
    message: str
    timestamp: str
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class TestSuiteResponse(BaseModel):
    suite_id: str
    suite_name: str
    test_type: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    duration: float
    timestamp: str
    success_rate: float


class TestStatisticsResponse(BaseModel):
    total_tests: int
    total_suites: int
    success_rate: float
    by_type: Dict[str, Dict[str, int]]
    by_status: Dict[str, int]
    recent_failures: List[TestResultResponse]


@router.post("/run/unit", response_model=TestSuiteResponse)
async def run_unit_tests_api(current_user: User = Depends(get_current_user)):
    """Запустить unit тесты."""
    try:
        # В реальном приложении здесь будет проверка разрешений
        # if not await roles_service.check_user_permission(current_user.id, "run_tests"):
        #     raise HTTPException(status_code=403, detail="Not enough permissions")

        suite = await testing_service.run_unit_tests()
        return TestSuiteResponse(**testing_service._test_suite_to_dict(suite))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка запуска unit тестов: {str(e)}"
        )


@router.post("/run/integration", response_model=TestSuiteResponse)
async def run_integration_tests_api(current_user: User = Depends(get_current_user)):
    """Запустить интеграционные тесты."""
    try:
        suite = await testing_service.run_integration_tests()
        return TestSuiteResponse(**testing_service._test_suite_to_dict(suite))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка запуска интеграционных тестов: {str(e)}"
        )


@router.post("/run/performance", response_model=TestSuiteResponse)
async def run_performance_tests_api(current_user: User = Depends(get_current_user)):
    """Запустить тесты производительности."""
    try:
        suite = await testing_service.run_performance_tests()
        return TestSuiteResponse(**testing_service._test_suite_to_dict(suite))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка запуска тестов производительности: {str(e)}",
        )


@router.post("/run/security", response_model=TestSuiteResponse)
async def run_security_tests_api(current_user: User = Depends(get_current_user)):
    """Запустить тесты безопасности."""
    try:
        suite = await testing_service.run_security_tests()
        return TestSuiteResponse(**testing_service._test_suite_to_dict(suite))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка запуска тестов безопасности: {str(e)}"
        )


@router.post("/run/load", response_model=TestSuiteResponse)
async def run_load_tests_api(current_user: User = Depends(get_current_user)):
    """Запустить нагрузочные тесты."""
    try:
        suite = await testing_service.run_load_tests()
        return TestSuiteResponse(**testing_service._test_suite_to_dict(suite))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка запуска нагрузочных тестов: {str(e)}"
        )


@router.post("/run/smoke", response_model=TestSuiteResponse)
async def run_smoke_tests_api(current_user: User = Depends(get_current_user)):
    """Запустить smoke тесты."""
    try:
        suite = await testing_service.run_smoke_tests()
        return TestSuiteResponse(**testing_service._test_suite_to_dict(suite))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка запуска smoke тестов: {str(e)}"
        )


@router.post("/run/all", response_model=Dict[str, TestSuiteResponse])
async def run_all_tests_api(
    background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)
):
    """Запустить все тесты."""
    try:
        # В реальном приложении это может быть долгая операция,
        # поэтому можно запустить в фоне
        results = await testing_service.run_all_tests()

        # Конвертируем результаты
        response = {}
        for test_type, suite in results.items():
            response[test_type] = TestSuiteResponse(
                **testing_service._test_suite_to_dict(suite)
            )

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка запуска всех тестов: {str(e)}"
        )


@router.get("/results", response_model=List[TestResultResponse])
async def get_test_results_api(
    test_type: Optional[str] = Query(None, description="Тип тестов для фильтрации"),
    status: Optional[str] = Query(None, description="Статус тестов для фильтрации"),
    limit: int = Query(100, description="Максимальное количество результатов"),
    current_user: User = Depends(get_current_user),
):
    """Получить результаты тестов."""
    try:
        results = await testing_service.get_test_results(test_type, status, limit)
        return [TestResultResponse(**result) for result in results]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения результатов тестов: {str(e)}"
        )


@router.get("/suites", response_model=List[TestSuiteResponse])
async def get_test_suites_api(
    limit: int = Query(50, description="Максимальное количество наборов тестов"),
    current_user: User = Depends(get_current_user),
):
    """Получить наборы тестов."""
    try:
        suites = await testing_service.get_test_suites(limit)
        return [TestSuiteResponse(**suite) for suite in suites]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения наборов тестов: {str(e)}"
        )


@router.get("/statistics", response_model=TestStatisticsResponse)
async def get_test_statistics_api(current_user: User = Depends(get_current_user)):
    """Получить статистику тестов."""
    try:
        stats = await testing_service.get_test_statistics()
        return TestStatisticsResponse(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения статистики тестов: {str(e)}"
        )


@router.get("/types", response_model=List[str])
async def get_test_types_api(current_user: User = Depends(get_current_user)):
    """Получить доступные типы тестов."""
    try:
        return [test_type.value for test_type in TestType]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения типов тестов: {str(e)}"
        )


@router.get("/status", response_model=Dict[str, Any])
async def get_testing_status_api(current_user: User = Depends(get_current_user)):
    """Получить статус системы тестирования."""
    try:
        stats = await testing_service.get_test_statistics()

        # Определяем общий статус
        if stats["total_tests"] == 0:
            status = "no_tests"
        elif stats["success_rate"] >= 95:
            status = "excellent"
        elif stats["success_rate"] >= 85:
            status = "good"
        elif stats["success_rate"] >= 70:
            status = "warning"
        else:
            status = "critical"

        return {
            "status": status,
            "message": f"Success rate: {stats['success_rate']}%",
            "statistics": stats,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения статуса тестирования: {str(e)}"
        )


@router.delete("/results", response_model=Dict[str, str])
async def clear_test_results_api(current_user: User = Depends(get_current_user)):
    """Очистить результаты тестов."""
    try:
        # В реальном приложении здесь будет проверка разрешений
        # if not await roles_service.check_user_permission(current_user.id, "manage_tests"):
        #     raise HTTPException(status_code=403, detail="Not enough permissions")

        testing_service.test_results.clear()
        testing_service.test_suites.clear()

        return {"message": "Результаты тестов очищены"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка очистки результатов тестов: {str(e)}"
        )
