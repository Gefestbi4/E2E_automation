// Tasks page module - simplified version
class TasksPage {
    constructor() {
        this.tasks = [];
        this.init();
    }

    async init() {
        await this.loadTasks();
        this.setupEventListeners();
    }

    async loadTasks() {
        try {
            const tasks = await window.ApiService.getTasks();
            this.tasks = tasks;
            this.renderTasks();
        } catch (error) {
            console.error('Failed to load tasks:', error);
        }
    }

    renderTasks() {
        const container = document.getElementById('tasks-container');
        if (!container) return;

        container.innerHTML = `
            <div class="tasks-header">
                <h1>Задачи</h1>
                <button class="btn btn-primary" onclick="tasksPage.showCreateTaskModal()">
                    Создать задачу
                </button>
            </div>
            <div class="tasks-list">
                ${this.tasks.map(task => this.renderTask(task)).join('')}
            </div>
        `;
    }

    renderTask(task) {
        return `
            <div class="task-card" data-task-id="${task.id}">
                <div class="task-header">
                    <h3>${task.title}</h3>
                    <div class="task-actions">
                        <button class="btn btn-sm btn-outline" onclick="tasksPage.editTask('${task.id}')">
                            Редактировать
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="tasksPage.deleteTask('${task.id}')">
                            Удалить
                        </button>
                    </div>
                </div>
                <div class="task-content">
                    <p>${task.description || 'Без описания'}</p>
                </div>
                <div class="task-meta">
                    <span class="task-status">${task.status}</span>
                    <span class="task-priority">${task.priority}</span>
                </div>
            </div>
        `;
    }

    setupEventListeners() {
        // Basic event listeners
    }

    async createTask(taskData) {
        try {
            await window.ApiService.createTask(taskData);
            await this.loadTasks();
        } catch (error) {
            console.error('Failed to create task:', error);
        }
    }

    async editTask(taskId) {
        console.log('Edit task:', taskId);
    }

    async deleteTask(taskId) {
        if (!confirm('Удалить задачу?')) return;

        try {
            await window.ApiService.deleteTask(taskId);
            await this.loadTasks();
        } catch (error) {
            console.error('Failed to delete task:', error);
        }
    }

    showCreateTaskModal() {
        console.log('Show create task modal');
    }
}

// Initialize
let tasksPage;
// TasksPage will be initialized by app.js

window.TasksPage = TasksPage;
