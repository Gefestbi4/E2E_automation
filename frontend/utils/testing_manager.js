/**
 * Менеджер системы тестирования
 */

class TestingManager {
    constructor() {
        this.testResults = [];
        this.testSuites = [];
        this.isRunning = false;
        this.currentTestType = null;
        this.testProgress = 0;
        this.testStatus = 'idle'; // idle, running, completed, error

        this.init();
    }

    init() {
        console.log('🧪 Initializing testing system...');
        this.loadTestResults();
        this.setupEventListeners();
        console.log('🧪 Testing system initialized successfully');
    }

    setupEventListeners() {
        // Обработчики для кнопок тестирования
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-test-type]')) {
                const testType = e.target.dataset.testType;
                this.runTestType(testType);
            }
        });
    }

    async runTestType(testType) {
        try {
            this.isRunning = true;
            this.currentTestType = testType;
            this.testStatus = 'running';
            this.testProgress = 0;

            console.log(`🧪 Running ${testType} tests...`);

            // Показываем модальное окно тестирования
            this.showTestingModal(testType);

            // Запускаем тесты
            const response = await this.callTestAPI(testType);

            if (response.ok) {
                const result = await response.json();
                this.handleTestResult(testType, result);
            } else {
                throw new Error(`Test API error: ${response.status}`);
            }

        } catch (error) {
            console.error(`Error running ${testType} tests:`, error);
            this.handleTestError(testType, error);
        } finally {
            this.isRunning = false;
            this.testStatus = 'completed';
        }
    }

    async callTestAPI(testType) {
        const endpoints = {
            'unit': '/api/testing/run/unit',
            'integration': '/api/testing/run/integration',
            'performance': '/api/testing/run/performance',
            'security': '/api/testing/run/security',
            'load': '/api/testing/run/load',
            'smoke': '/api/testing/run/smoke',
            'all': '/api/testing/run/all'
        };

        const endpoint = endpoints[testType];
        if (!endpoint) {
            throw new Error(`Unknown test type: ${testType}`);
        }

        return await window.ApiService.request(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
    }

    handleTestResult(testType, result) {
        console.log(`✅ ${testType} tests completed:`, result);

        // Обновляем прогресс
        this.testProgress = 100;

        // Сохраняем результат
        if (testType === 'all') {
            // Для всех тестов - сохраняем каждый набор
            Object.entries(result).forEach(([type, suite]) => {
                this.testSuites.push(suite);
            });
        } else {
            // Для одного типа тестов
            this.testSuites.push(result);
        }

        // Сохраняем в localStorage
        this.saveTestResults();

        // Обновляем UI
        this.updateTestingModal(testType, result);

        // Показываем уведомление
        if (window.Toast) {
            window.Toast.success(`${testType} тесты завершены успешно!`);
        }
    }

    handleTestError(testType, error) {
        console.error(`❌ ${testType} tests failed:`, error);

        this.testStatus = 'error';
        this.testProgress = 0;

        // Обновляем UI с ошибкой
        this.updateTestingModal(testType, null, error);

        // Показываем уведомление об ошибке
        if (window.Toast) {
            window.Toast.error(`Ошибка выполнения ${testType} тестов: ${error.message}`);
        }
    }

    showTestingModal(testType) {
        const modal = document.getElementById('testing-modal');
        if (!modal) {
            this.createTestingModal();
        }

        // Обновляем заголовок
        const title = modal.querySelector('.modal-title');
        title.textContent = `Выполнение ${testType} тестов`;

        // Сбрасываем прогресс
        this.testProgress = 0;
        this.updateProgressBar();

        // Показываем модальное окно
        modal.style.display = 'flex';
    }

    createTestingModal() {
        const modalHTML = `
            <div id="testing-modal" class="modal" style="display: none;">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title">Выполнение тестов</h3>
                        <button class="modal-close" onclick="this.closest('.modal').style.display='none'">&times;</button>
                    </div>
                    <div class="modal-body">
                        <div class="testing-progress">
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 0%"></div>
                            </div>
                            <div class="progress-text">0%</div>
                        </div>
                        <div class="testing-status">
                            <div class="status-indicator">
                                <i class="fas fa-spinner fa-spin"></i>
                                <span>Выполнение тестов...</span>
                            </div>
                        </div>
                        <div class="testing-results" style="display: none;">
                            <div class="results-summary"></div>
                            <div class="results-details"></div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="this.closest('.modal').style.display='none'">
                            Закрыть
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    updateTestingModal(testType, result, error = null) {
        const modal = document.getElementById('testing-modal');
        if (!modal) return;

        const progressBar = modal.querySelector('.progress-fill');
        const progressText = modal.querySelector('.progress-text');
        const statusIndicator = modal.querySelector('.status-indicator');
        const testingResults = modal.querySelector('.testing-results');
        const resultsSummary = modal.querySelector('.results-summary');
        const resultsDetails = modal.querySelector('.results-details');

        // Обновляем прогресс
        this.updateProgressBar();

        if (error) {
            // Показываем ошибку
            statusIndicator.innerHTML = `
                <i class="fas fa-exclamation-triangle text-danger"></i>
                <span>Ошибка выполнения тестов</span>
            `;

            testingResults.style.display = 'block';
            resultsSummary.innerHTML = `
                <div class="alert alert-danger">
                    <h5>Ошибка выполнения тестов</h5>
                    <p>${error.message}</p>
                </div>
            `;
            resultsDetails.innerHTML = '';

        } else if (result) {
            // Показываем результаты
            statusIndicator.innerHTML = `
                <i class="fas fa-check-circle text-success"></i>
                <span>Тесты завершены</span>
            `;

            testingResults.style.display = 'block';

            if (testType === 'all') {
                // Результаты всех тестов
                resultsSummary.innerHTML = this.renderAllTestsSummary(result);
                resultsDetails.innerHTML = this.renderAllTestsDetails(result);
            } else {
                // Результаты одного типа тестов
                resultsSummary.innerHTML = this.renderTestSummary(result);
                resultsDetails.innerHTML = this.renderTestDetails(result);
            }
        }
    }

    updateProgressBar() {
        const modal = document.getElementById('testing-modal');
        if (!modal) return;

        const progressBar = modal.querySelector('.progress-fill');
        const progressText = modal.querySelector('.progress-text');

        if (progressBar) {
            progressBar.style.width = `${this.testProgress}%`;
        }
        if (progressText) {
            progressText.textContent = `${this.testProgress}%`;
        }
    }

    renderTestSummary(result) {
        const successRate = result.success_rate || 0;
        const statusClass = successRate >= 90 ? 'success' : successRate >= 70 ? 'warning' : 'danger';

        return `
            <div class="test-summary">
                <h5>Результаты тестов</h5>
                <div class="summary-stats">
                    <div class="stat-item">
                        <span class="stat-label">Всего тестов:</span>
                        <span class="stat-value">${result.total_tests}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Пройдено:</span>
                        <span class="stat-value text-success">${result.passed_tests}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Провалено:</span>
                        <span class="stat-value text-danger">${result.failed_tests}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Пропущено:</span>
                        <span class="stat-value text-warning">${result.skipped_tests}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Успешность:</span>
                        <span class="stat-value text-${statusClass}">${successRate}%</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Время выполнения:</span>
                        <span class="stat-value">${result.duration.toFixed(2)}с</span>
                    </div>
                </div>
            </div>
        `;
    }

    renderTestDetails(result) {
        return `
            <div class="test-details">
                <h6>Детали выполнения</h6>
                <div class="detail-item">
                    <span class="detail-label">ID набора тестов:</span>
                    <span class="detail-value">${result.suite_id}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Тип тестов:</span>
                    <span class="detail-value">${result.test_type}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Время начала:</span>
                    <span class="detail-value">${new Date(result.timestamp).toLocaleString()}</span>
                </div>
            </div>
        `;
    }

    renderAllTestsSummary(results) {
        let totalTests = 0;
        let totalPassed = 0;
        let totalFailed = 0;
        let totalSkipped = 0;
        let totalDuration = 0;

        Object.values(results).forEach(result => {
            totalTests += result.total_tests;
            totalPassed += result.passed_tests;
            totalFailed += result.failed_tests;
            totalSkipped += result.skipped_tests;
            totalDuration += result.duration;
        });

        const overallSuccessRate = totalTests > 0 ? (totalPassed / totalTests * 100) : 0;
        const statusClass = overallSuccessRate >= 90 ? 'success' : overallSuccessRate >= 70 ? 'warning' : 'danger';

        return `
            <div class="all-tests-summary">
                <h5>Общие результаты тестирования</h5>
                <div class="summary-stats">
                    <div class="stat-item">
                        <span class="stat-label">Всего тестов:</span>
                        <span class="stat-value">${totalTests}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Пройдено:</span>
                        <span class="stat-value text-success">${totalPassed}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Провалено:</span>
                        <span class="stat-value text-danger">${totalFailed}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Пропущено:</span>
                        <span class="stat-value text-warning">${totalSkipped}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Общая успешность:</span>
                        <span class="stat-value text-${statusClass}">${overallSuccessRate.toFixed(2)}%</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Общее время:</span>
                        <span class="stat-value">${totalDuration.toFixed(2)}с</span>
                    </div>
                </div>
            </div>
        `;
    }

    renderAllTestsDetails(results) {
        let detailsHTML = '<div class="all-tests-details"><h6>Результаты по типам тестов</h6>';

        Object.entries(results).forEach(([testType, result]) => {
            const successRate = result.success_rate || 0;
            const statusClass = successRate >= 90 ? 'success' : successRate >= 70 ? 'warning' : 'danger';

            detailsHTML += `
                <div class="test-type-result">
                    <div class="test-type-header">
                        <h6>${testType.toUpperCase()} тесты</h6>
                        <span class="success-rate text-${statusClass}">${successRate}%</span>
                    </div>
                    <div class="test-type-stats">
                        <span class="stat">Всего: ${result.total_tests}</span>
                        <span class="stat text-success">Пройдено: ${result.passed_tests}</span>
                        <span class="stat text-danger">Провалено: ${result.failed_tests}</span>
                        <span class="stat text-warning">Пропущено: ${result.skipped_tests}</span>
                        <span class="stat">Время: ${result.duration.toFixed(2)}с</span>
                    </div>
                </div>
            `;
        });

        detailsHTML += '</div>';
        return detailsHTML;
    }

    async loadTestResults() {
        try {
            const response = await window.ApiService.request('/api/testing/results', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (response.ok) {
                this.testResults = await response.json();
            }
        } catch (error) {
            console.error('Error loading test results:', error);
        }
    }

    async loadTestSuites() {
        try {
            const response = await window.ApiService.request('/api/testing/suites', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (response.ok) {
                this.testSuites = await response.json();
            }
        } catch (error) {
            console.error('Error loading test suites:', error);
        }
    }

    async getTestStatistics() {
        try {
            const response = await window.ApiService.request('/api/testing/statistics', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error('Error loading test statistics:', error);
            return null;
        }
    }

    saveTestResults() {
        try {
            localStorage.setItem('testResults', JSON.stringify(this.testResults));
            localStorage.setItem('testSuites', JSON.stringify(this.testSuites));
        } catch (error) {
            console.error('Error saving test results:', error);
        }
    }

    openTestingDashboard() {
        this.showTestingDashboard();
    }

    showTestingDashboard() {
        const modal = document.getElementById('testing-dashboard-modal');
        if (!modal) {
            this.createTestingDashboard();
        }

        // Загружаем данные
        this.loadDashboardData();

        // Показываем модальное окно
        modal.style.display = 'flex';
    }

    createTestingDashboard() {
        const modalHTML = `
            <div id="testing-dashboard-modal" class="modal" style="display: none;">
                <div class="modal-content large">
                    <div class="modal-header">
                        <h3 class="modal-title">Панель тестирования</h3>
                        <button class="modal-close" onclick="this.closest('.modal').style.display='none'">&times;</button>
                    </div>
                    <div class="modal-body">
                        <div class="testing-dashboard">
                            <div class="dashboard-tabs">
                                <button class="tab-btn active" data-tab="overview">Обзор</button>
                                <button class="tab-btn" data-tab="results">Результаты</button>
                                <button class="tab-btn" data-tab="suites">Наборы тестов</button>
                                <button class="tab-btn" data-tab="statistics">Статистика</button>
                            </div>
                            
                            <div class="tab-content">
                                <div id="overview-tab" class="tab-pane active">
                                    <div class="overview-content">
                                        <div class="quick-actions">
                                            <h5>Быстрые действия</h5>
                                            <div class="action-buttons">
                                                <button class="btn btn-primary" data-test-type="smoke">
                                                    <i class="fas fa-fire"></i> Smoke тесты
                                                </button>
                                                <button class="btn btn-success" data-test-type="unit">
                                                    <i class="fas fa-cube"></i> Unit тесты
                                                </button>
                                                <button class="btn btn-info" data-test-type="integration">
                                                    <i class="fas fa-link"></i> Интеграционные
                                                </button>
                                                <button class="btn btn-warning" data-test-type="performance">
                                                    <i class="fas fa-tachometer-alt"></i> Производительность
                                                </button>
                                                <button class="btn btn-danger" data-test-type="security">
                                                    <i class="fas fa-shield-alt"></i> Безопасность
                                                </button>
                                                <button class="btn btn-dark" data-test-type="load">
                                                    <i class="fas fa-weight-hanging"></i> Нагрузочные
                                                </button>
                                                <button class="btn btn-secondary" data-test-type="all">
                                                    <i class="fas fa-play"></i> Все тесты
                                                </button>
                                            </div>
                                        </div>
                                        
                                        <div class="recent-results">
                                            <h5>Последние результаты</h5>
                                            <div class="recent-results-list"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div id="results-tab" class="tab-pane">
                                    <div class="results-content">
                                        <div class="results-filters">
                                            <select id="test-type-filter">
                                                <option value="">Все типы</option>
                                                <option value="unit">Unit</option>
                                                <option value="integration">Integration</option>
                                                <option value="performance">Performance</option>
                                                <option value="security">Security</option>
                                                <option value="load">Load</option>
                                                <option value="smoke">Smoke</option>
                                            </select>
                                            <select id="status-filter">
                                                <option value="">Все статусы</option>
                                                <option value="passed">Пройдено</option>
                                                <option value="failed">Провалено</option>
                                                <option value="skipped">Пропущено</option>
                                                <option value="error">Ошибка</option>
                                            </select>
                                            <button class="btn btn-primary" onclick="window.testingManager.filterResults()">
                                                Фильтровать
                                            </button>
                                        </div>
                                        <div class="results-list"></div>
                                    </div>
                                </div>
                                
                                <div id="suites-tab" class="tab-pane">
                                    <div class="suites-content">
                                        <div class="suites-list"></div>
                                    </div>
                                </div>
                                
                                <div id="statistics-tab" class="tab-pane">
                                    <div class="statistics-content">
                                        <div class="stats-overview"></div>
                                        <div class="stats-charts"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="this.closest('.modal').style.display='none'">
                            Закрыть
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.setupDashboardEventListeners();
    }

    setupDashboardEventListeners() {
        // Обработчики вкладок
        document.addEventListener('click', (e) => {
            if (e.target.matches('.tab-btn')) {
                this.switchTab(e.target.dataset.tab);
            }
        });
    }

    switchTab(tabName) {
        // Убираем активный класс со всех вкладок и панелей
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));

        // Активируем выбранную вкладку и панель
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');

        // Загружаем данные для вкладки
        this.loadTabData(tabName);
    }

    async loadDashboardData() {
        await Promise.all([
            this.loadTestResults(),
            this.loadTestSuites()
        ]);

        this.updateOverviewTab();
        this.updateResultsTab();
        this.updateSuitesTab();
        this.updateStatisticsTab();
    }

    updateOverviewTab() {
        const recentResultsList = document.querySelector('.recent-results-list');
        if (!recentResultsList) return;

        const recentSuites = this.testSuites.slice(-5).reverse();

        if (recentSuites.length === 0) {
            recentResultsList.innerHTML = '<p class="text-muted">Нет результатов тестирования</p>';
            return;
        }

        recentResultsList.innerHTML = recentSuites.map(suite => `
            <div class="recent-result-item">
                <div class="result-header">
                    <span class="result-name">${suite.suite_name}</span>
                    <span class="result-type">${suite.test_type}</span>
                </div>
                <div class="result-stats">
                    <span class="stat text-success">${suite.passed_tests}</span>
                    <span class="stat text-danger">${suite.failed_tests}</span>
                    <span class="stat text-warning">${suite.skipped_tests}</span>
                    <span class="stat">${suite.success_rate}%</span>
                </div>
                <div class="result-time">
                    ${new Date(suite.timestamp).toLocaleString()}
                </div>
            </div>
        `).join('');
    }

    updateResultsTab() {
        const resultsList = document.querySelector('.results-list');
        if (!resultsList) return;

        if (this.testResults.length === 0) {
            resultsList.innerHTML = '<p class="text-muted">Нет результатов тестов</p>';
            return;
        }

        resultsList.innerHTML = this.testResults.map(result => `
            <div class="result-item">
                <div class="result-info">
                    <div class="result-name">${result.test_name}</div>
                    <div class="result-meta">
                        <span class="result-type">${result.test_type}</span>
                        <span class="result-duration">${result.duration.toFixed(2)}с</span>
                        <span class="result-time">${new Date(result.timestamp).toLocaleString()}</span>
                    </div>
                </div>
                <div class="result-status">
                    <span class="status-badge status-${result.status}">${result.status}</span>
                </div>
                ${result.error ? `<div class="result-error">${result.error}</div>` : ''}
            </div>
        `).join('');
    }

    updateSuitesTab() {
        const suitesList = document.querySelector('.suites-list');
        if (!suitesList) return;

        if (this.testSuites.length === 0) {
            suitesList.innerHTML = '<p class="text-muted">Нет наборов тестов</p>';
            return;
        }

        suitesList.innerHTML = this.testSuites.map(suite => `
            <div class="suite-item">
                <div class="suite-header">
                    <div class="suite-name">${suite.suite_name}</div>
                    <div class="suite-type">${suite.test_type}</div>
                </div>
                <div class="suite-stats">
                    <div class="stat-group">
                        <span class="stat-label">Всего:</span>
                        <span class="stat-value">${suite.total_tests}</span>
                    </div>
                    <div class="stat-group">
                        <span class="stat-label">Пройдено:</span>
                        <span class="stat-value text-success">${suite.passed_tests}</span>
                    </div>
                    <div class="stat-group">
                        <span class="stat-label">Провалено:</span>
                        <span class="stat-value text-danger">${suite.failed_tests}</span>
                    </div>
                    <div class="stat-group">
                        <span class="stat-label">Успешность:</span>
                        <span class="stat-value">${suite.success_rate}%</span>
                    </div>
                </div>
                <div class="suite-meta">
                    <span class="suite-duration">${suite.duration.toFixed(2)}с</span>
                    <span class="suite-time">${new Date(suite.timestamp).toLocaleString()}</span>
                </div>
            </div>
        `).join('');
    }

    async updateStatisticsTab() {
        const statsOverview = document.querySelector('.stats-overview');
        const statsCharts = document.querySelector('.stats-charts');

        if (!statsOverview || !statsCharts) return;

        const stats = await this.getTestStatistics();
        if (!stats) {
            statsOverview.innerHTML = '<p class="text-muted">Не удалось загрузить статистику</p>';
            return;
        }

        // Обзор статистики
        statsOverview.innerHTML = `
            <div class="stats-summary">
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-vial"></i>
                    </div>
                    <div class="stat-content">
                        <div class="stat-number">${stats.total_tests}</div>
                        <div class="stat-label">Всего тестов</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-layer-group"></i>
                    </div>
                    <div class="stat-content">
                        <div class="stat-number">${stats.total_suites}</div>
                        <div class="stat-label">Наборов тестов</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-percentage"></i>
                    </div>
                    <div class="stat-content">
                        <div class="stat-number">${stats.success_rate}%</div>
                        <div class="stat-label">Успешность</div>
                    </div>
                </div>
            </div>
        `;

        // Графики статистики
        statsCharts.innerHTML = `
            <div class="charts-container">
                <div class="chart-section">
                    <h6>Статистика по типам тестов</h6>
                    <div class="chart-placeholder">
                        <canvas id="test-types-chart" width="400" height="200"></canvas>
                    </div>
                </div>
                <div class="chart-section">
                    <h6>Статистика по статусам</h6>
                    <div class="chart-placeholder">
                        <canvas id="test-status-chart" width="400" height="200"></canvas>
                    </div>
                </div>
            </div>
        `;

        // Здесь можно добавить создание графиков с помощью Chart.js
        this.createCharts(stats);
    }

    createCharts(stats) {
        // Простая реализация графиков без внешних библиотек
        // В реальном приложении здесь будет Chart.js или аналогичная библиотека
        console.log('Creating charts for statistics:', stats);
    }

    loadTabData(tabName) {
        switch (tabName) {
            case 'overview':
                this.updateOverviewTab();
                break;
            case 'results':
                this.updateResultsTab();
                break;
            case 'suites':
                this.updateSuitesTab();
                break;
            case 'statistics':
                this.updateStatisticsTab();
                break;
        }
    }

    filterResults() {
        const typeFilter = document.getElementById('test-type-filter')?.value;
        const statusFilter = document.getElementById('status-filter')?.value;

        // Здесь будет логика фильтрации результатов
        console.log('Filtering results:', { typeFilter, statusFilter });
    }
}

// Создаем глобальный экземпляр
window.testingManager = new TestingManager();
