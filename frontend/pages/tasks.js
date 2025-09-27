// Task management page module
class TasksModule {
    constructor() {
        this.tasksService = new TasksService();
        this.isInitialized = false;
    }

    async init() {
        if (this.isInitialized) return;

        console.log('Initializing Tasks module...');

        try {
            await this.loadProjects();
            this.bindEvents();
            this.isInitialized = true;
            console.log('Tasks module initialized successfully');
        } catch (error) {
            console.error('Failed to initialize Tasks module:', error);
            throw error;
        }
    }

    async loadProjects() {
        try {
            // Mock data for demo
            const projects = [
                {
                    id: 1,
                    name: 'Demo Project',
                    description: 'Демо-проект для тестирования системы управления задачами',
                    status: 'active',
                    tasks_count: 5,
                    completed_tasks: 2
                },
                {
                    id: 2,
                    name: 'Test Project',
                    description: 'Тестовый проект с различными задачами',
                    status: 'active',
                    tasks_count: 8,
                    completed_tasks: 3
                }
            ];

            this.renderProjects(projects);
        } catch (error) {
            console.error('Failed to load projects:', error);
            this.renderError('Failed to load projects');
        }
    }

    renderProjects(projects) {
        const tasksElement = document.getElementById('tasks-page');
        if (!tasksElement) return;

        tasksElement.innerHTML = `
            <div class="page-header">
                <h1>Task Management</h1>
                <p>Система управления задачами</p>
            </div>

            <div class="tasks-content">
                <div class="projects-section">
                    <div class="section-header">
                        <h2>Проекты</h2>
                        <button class="btn btn-primary" id="add-project-btn">Создать проект</button>
                    </div>
                    
                    <div class="projects-grid">
                        ${projects.map(project => `
                            <div class="project-card" data-project-id="${project.id}">
                                <div class="project-header">
                                    <h3 class="project-name">${project.name}</h3>
                                    <span class="project-status status-${project.status}">${project.status}</span>
                                </div>
                                <div class="project-description">
                                    <p>${project.description}</p>
                                </div>
                                <div class="project-stats">
                                    <div class="stat">
                                        <span class="stat-label">Задач:</span>
                                        <span class="stat-value">${project.tasks_count}</span>
                                    </div>
                                    <div class="stat">
                                        <span class="stat-label">Выполнено:</span>
                                        <span class="stat-value">${project.completed_tasks}</span>
                                    </div>
                                </div>
                                <div class="project-progress">
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: ${(project.completed_tasks / project.tasks_count) * 100}%"></div>
                                    </div>
                                    <span class="progress-text">${Math.round((project.completed_tasks / project.tasks_count) * 100)}% выполнено</span>
                                </div>
                                <div class="project-actions">
                                    <button class="btn btn-secondary btn-sm" onclick="this.viewProject(${project.id})">Открыть</button>
                                    <button class="btn btn-primary btn-sm" onclick="this.addTask(${project.id})">Добавить задачу</button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="quick-actions">
                    <h2>Быстрые действия</h2>
                    <div class="actions-grid">
                        <button class="action-card" id="view-all-tasks">
                            <div class="action-icon">📋</div>
                            <div class="action-content">
                                <h4>Все задачи</h4>
                                <p>Просмотр всех задач</p>
                            </div>
                        </button>
                        <button class="action-card" id="my-tasks">
                            <div class="action-icon">👤</div>
                            <div class="action-content">
                                <h4>Мои задачи</h4>
                                <p>Задачи, назначенные мне</p>
                            </div>
                        </button>
                        <button class="action-card" id="overdue-tasks">
                            <div class="action-icon">⏰</div>
                            <div class="action-content">
                                <h4>Просроченные</h4>
                                <p>Задачи с истекшим сроком</p>
                            </div>
                        </button>
                        <button class="action-card" id="reports">
                            <div class="action-icon">📊</div>
                            <div class="action-content">
                                <h4>Отчеты</h4>
                                <p>Аналитика и отчеты</p>
                            </div>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    renderError(message) {
        const tasksElement = document.getElementById('tasks-page');
        if (!tasksElement) return;

        tasksElement.innerHTML = `
            <div class="page-header">
                <h1>Task Management</h1>
                <p>Система управления задачами</p>
            </div>
            <div class="error-message">
                <p>${message}</p>
                <button class="btn btn-primary" onclick="window.App.modules.tasks.loadProjects()">Попробовать снова</button>
            </div>
        `;
    }

    bindEvents() {
        // Add project button
        document.addEventListener('click', (e) => {
            if (e.target.id === 'add-project-btn') {
                this.showAddProjectModal();
            }
        });

        // Quick actions
        document.addEventListener('click', (e) => {
            if (e.target.closest('#view-all-tasks')) {
                Toast.info('Функция просмотра всех задач будет реализована');
            } else if (e.target.closest('#my-tasks')) {
                Toast.info('Функция просмотра моих задач будет реализована');
            } else if (e.target.closest('#overdue-tasks')) {
                Toast.info('Функция просмотра просроченных задач будет реализована');
            } else if (e.target.closest('#reports')) {
                Toast.info('Функция отчетов будет реализована');
            }
        });
    }

    showAddProjectModal() {
        Toast.info('Функция создания проекта будет реализована в следующих версиях');
    }

    onPageShow() {
        console.log('Tasks page shown');
        if (!this.isInitialized) {
            this.init();
        }
    }
}

// Export for global access
window.TasksModule = TasksModule;
