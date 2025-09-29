// Tasks Module
console.log('📋 TasksModule script loading...');

class TasksModule {
    constructor() {
        this.projects = [];
        this.tasks = [];
        this.currentProject = null;
        this.init();
    }

    init() {
        console.log('📋 TasksModule initialized');
        this.loadProjects();
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            const createProjectBtn = document.getElementById('create-project-btn');
            if (createProjectBtn) {
                createProjectBtn.addEventListener('click', () => this.showCreateProjectModal());
            }

            const createBoardBtn = document.getElementById('create-board-btn');
            if (createBoardBtn) {
                createBoardBtn.addEventListener('click', () => this.showCreateBoardModal());
            }
        });
    }

    async loadProjects() {
        try {
            console.log('📋 Loading projects...');
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 100));
            this.projects = [
                { id: 1, name: 'Project Alpha', description: 'Main project', tasks: 5, completed: 2 },
                { id: 2, name: 'Project Beta', description: 'Secondary project', tasks: 3, completed: 1 }
            ];
            this.renderProjects();
        } catch (error) {
            console.error('Error loading projects:', error);
        }
    }

    renderProjects() {
        const projectsContainer = document.getElementById('projects-container');
        if (!projectsContainer) return;

        projectsContainer.innerHTML = this.projects.map(project => `
            <div class="project-card">
                <h3>${project.name}</h3>
                <p>${project.description}</p>
                <div class="project-stats">
                    <span>Tasks: ${project.tasks}</span>
                    <span>Completed: ${project.completed}</span>
                </div>
                <div class="project-actions">
                    <button onclick="TasksModule.openProject(${project.id})">Open</button>
                    <button onclick="TasksModule.editProject(${project.id})">Edit</button>
                </div>
            </div>
        `).join('');
    }

    showCreateProjectModal() {
        console.log('📋 Showing create project modal');
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Create New Project</h2>
                <form id="create-project-form">
                    <input type="text" id="project-name" placeholder="Project name" required>
                    <textarea id="project-description" placeholder="Project description"></textarea>
                    <button type="submit">Create Project</button>
                </form>
            </div>
        `;
        document.body.appendChild(modal);
        modal.style.display = 'block';

        document.getElementById('create-project-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('project-name').value;
            const description = document.getElementById('project-description').value;
            if (name.trim()) {
                this.createProject(name, description);
                modal.remove();
            }
        });

        modal.querySelector('.close').addEventListener('click', () => {
            modal.remove();
        });
    }

    showCreateBoardModal() {
        console.log('📋 Showing create board modal');
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Create New Board</h2>
                <form id="create-board-form">
                    <input type="text" id="board-name" placeholder="Board name" required>
                    <select id="board-project">
                        ${this.projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('')}
                    </select>
                    <button type="submit">Create Board</button>
                </form>
            </div>
        `;
        document.body.appendChild(modal);
        modal.style.display = 'block';

        document.getElementById('create-board-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('board-name').value;
            const projectId = document.getElementById('board-project').value;
            if (name.trim()) {
                this.createBoard(name, projectId);
                modal.remove();
            }
        });

        modal.querySelector('.close').addEventListener('click', () => {
            modal.remove();
        });
    }

    async createProject(name, description) {
        try {
            const newProject = {
                id: Date.now(),
                name: name,
                description: description,
                tasks: 0,
                completed: 0
            };
            this.projects.push(newProject);
            this.renderProjects();
            console.log('📋 Project created:', newProject);
        } catch (error) {
            console.error('Error creating project:', error);
        }
    }

    async createBoard(name, projectId) {
        try {
            console.log('📋 Creating board:', name, 'for project:', projectId);
            // Implement board creation
        } catch (error) {
            console.error('Error creating board:', error);
        }
    }

    openProject(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (project) {
            this.currentProject = project;
            console.log('📋 Opening project:', project.name);
            // Navigate to project view
        }
    }

    editProject(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (project) {
            console.log('📋 Editing project:', project.name);
            // Show edit modal
        }
    }
}

// Export for global access
window.TasksModule = TasksModule;
console.log('📋 TasksModule class exported to window:', typeof window.TasksModule);
