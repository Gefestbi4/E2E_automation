// Task management service
class TasksService {
    constructor() {
        this.api = window.ApiService;
    }

    async getProjects() {
        return this.api.get('/api/tasks/projects');
    }

    async createProject(projectData) {
        return this.api.post('/api/tasks/projects', projectData);
    }

    async getProject(id) {
        return this.api.get(`/api/tasks/projects/${id}`);
    }

    async updateProject(id, projectData) {
        return this.api.put(`/api/tasks/projects/${id}`, projectData);
    }

    async deleteProject(id) {
        return this.api.delete(`/api/tasks/projects/${id}`);
    }

    async getBoards(projectId) {
        return this.api.get(`/api/tasks/projects/${projectId}/boards`);
    }

    async createBoard(projectId, boardData) {
        return this.api.post(`/api/tasks/projects/${projectId}/boards`, boardData);
    }

    async getBoard(id) {
        return this.api.get(`/api/tasks/boards/${id}`);
    }

    async updateBoard(id, boardData) {
        return this.api.put(`/api/tasks/boards/${id}`, boardData);
    }

    async deleteBoard(id) {
        return this.api.delete(`/api/tasks/boards/${id}`);
    }

    async getTasks(boardId, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.api.get(`/api/tasks/boards/${boardId}/tasks?${queryString}`);
    }

    async createTask(boardId, taskData) {
        return this.api.post(`/api/tasks/boards/${boardId}/tasks`, taskData);
    }

    async getTask(id) {
        return this.api.get(`/api/tasks/tasks/${id}`);
    }

    async updateTask(id, taskData) {
        return this.api.put(`/api/tasks/tasks/${id}`, taskData);
    }

    async deleteTask(id) {
        return this.api.delete(`/api/tasks/tasks/${id}`);
    }

    async moveTask(taskId, newColumnId, newPosition) {
        return this.api.put(`/api/tasks/tasks/${taskId}/move`, {
            column_id: newColumnId,
            position: newPosition
        });
    }

    async getTaskComments(taskId) {
        return this.api.get(`/api/tasks/tasks/${taskId}/comments`);
    }

    async addTaskComment(taskId, commentData) {
        return this.api.post(`/api/tasks/tasks/${taskId}/comments`, commentData);
    }

    async updateTaskComment(commentId, commentData) {
        return this.api.put(`/api/tasks/comments/${commentId}`, commentData);
    }

    async deleteTaskComment(commentId) {
        return this.api.delete(`/api/tasks/comments/${commentId}`);
    }

    async addTaskAttachment(taskId, file) {
        const formData = new FormData();
        formData.append('file', file);
        return this.api.upload(`/api/tasks/tasks/${taskId}/attachments`, formData);
    }

    async deleteTaskAttachment(attachmentId) {
        return this.api.delete(`/api/tasks/attachments/${attachmentId}`);
    }

    async startTimeEntry(taskId) {
        return this.api.post(`/api/tasks/tasks/${taskId}/time-entries`);
    }

    async stopTimeEntry(timeEntryId) {
        return this.api.put(`/api/tasks/time-entries/${timeEntryId}/stop`);
    }

    async getTimeEntries(taskId) {
        return this.api.get(`/api/tasks/tasks/${taskId}/time-entries`);
    }
}

// Создаем экземпляр и экспортируем для глобального доступа
window.TasksService = new TasksService();
