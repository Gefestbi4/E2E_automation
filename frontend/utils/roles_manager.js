/**
 * Менеджер ролей и разрешений
 */

class RolesManager {
    constructor() {
        this.roles = [];
        this.permissions = [];
        this.userRoles = [];
        this.userPermissions = [];
        this.isInitialized = false;
    }

    /**
     * Инициализация менеджера ролей
     */
    async init() {
        console.log('🔐 Initializing Roles Manager...');

        try {
            // Загружаем роли и разрешения
            await this.loadRoles();
            await this.loadPermissions();

            // Инициализируем UI
            this.initUI();

            this.isInitialized = true;
            console.log('🔐 Roles Manager initialized successfully');

        } catch (error) {
            console.error('🔐 Failed to initialize Roles Manager:', error);
        }
    }

    /**
     * Загрузка ролей
     */
    async loadRoles() {
        try {
            const response = await window.ApiService.get('/api/roles/');
            this.roles = response;
            console.log('🔐 Roles loaded:', this.roles.length);
            return response;
        } catch (error) {
            console.error('🔐 Failed to load roles:', error);
            return [];
        }
    }

    /**
     * Загрузка разрешений
     */
    async loadPermissions() {
        try {
            const response = await window.ApiService.get('/api/roles/permissions/');
            this.permissions = response;
            console.log('🔐 Permissions loaded:', this.permissions.length);
            return response;
        } catch (error) {
            console.error('🔐 Failed to load permissions:', error);
            return [];
        }
    }

    /**
     * Загрузка ролей пользователя
     */
    async loadUserRoles(userId) {
        try {
            const response = await window.ApiService.get(`/api/roles/user/${userId}/roles`);
            this.userRoles = response;
            console.log('🔐 User roles loaded:', this.userRoles.length);
            return response;
        } catch (error) {
            console.error('🔐 Failed to load user roles:', error);
            return [];
        }
    }

    /**
     * Загрузка разрешений пользователя
     */
    async loadUserPermissions(userId) {
        try {
            const response = await window.ApiService.get(`/api/roles/user/${userId}/permissions`);
            this.userPermissions = response;
            console.log('🔐 User permissions loaded:', this.userPermissions.length);
            return response;
        } catch (error) {
            console.error('🔐 Failed to load user permissions:', error);
            return [];
        }
    }

    /**
     * Создание роли
     */
    async createRole(roleData) {
        try {
            const response = await window.ApiService.post('/api/roles/', roleData);
            console.log('🔐 Role created:', response);

            // Обновляем список ролей
            await this.loadRoles();

            if (window.Toast && typeof window.Toast.success === 'function') {
                window.Toast.success('Роль создана успешно');
            } else {
                alert('Роль создана успешно');
            }

            return response;
        } catch (error) {
            console.error('🔐 Failed to create role:', error);
            throw error;
        }
    }

    /**
     * Обновление роли
     */
    async updateRole(roleId, roleData) {
        try {
            const response = await window.ApiService.put(`/api/roles/${roleId}`, roleData);
            console.log('🔐 Role updated:', response);

            // Обновляем список ролей
            await this.loadRoles();

            if (window.Toast && typeof window.Toast.success === 'function') {
                window.Toast.success('Роль обновлена успешно');
            } else {
                alert('Роль обновлена успешно');
            }

            return response;
        } catch (error) {
            console.error('🔐 Failed to update role:', error);
            throw error;
        }
    }

    /**
     * Удаление роли
     */
    async deleteRole(roleId) {
        try {
            await window.ApiService.delete(`/api/roles/${roleId}`);
            console.log('🔐 Role deleted:', roleId);

            // Обновляем список ролей
            await this.loadRoles();

            if (window.Toast && typeof window.Toast.success === 'function') {
                window.Toast.success('Роль удалена успешно');
            } else {
                alert('Роль удалена успешно');
            }

        } catch (error) {
            console.error('🔐 Failed to delete role:', error);
            throw error;
        }
    }

    /**
     * Назначение роли пользователю
     */
    async assignRoleToUser(userId, roleId, expiresAt = null) {
        try {
            const response = await window.ApiService.post(`/api/roles/user/${userId}/assign`, {
                role_id: roleId,
                expires_at: expiresAt
            });

            console.log('🔐 Role assigned to user:', response);

            if (window.Toast && typeof window.Toast.success === 'function') {
                window.Toast.success('Роль назначена пользователю');
            } else {
                alert('Роль назначена пользователю');
            }

            return response;
        } catch (error) {
            console.error('🔐 Failed to assign role:', error);
            throw error;
        }
    }

    /**
     * Удаление роли у пользователя
     */
    async removeRoleFromUser(userId, roleId) {
        try {
            await window.ApiService.delete(`/api/roles/user/${userId}/role/${roleId}`);
            console.log('🔐 Role removed from user');

            if (window.Toast && typeof window.Toast.success === 'function') {
                window.Toast.success('Роль удалена у пользователя');
            } else {
                alert('Роль удалена у пользователя');
            }

        } catch (error) {
            console.error('🔐 Failed to remove role:', error);
            throw error;
        }
    }

    /**
     * Проверка разрешения
     */
    async checkPermission(permissionName) {
        try {
            const response = await window.ApiService.get(`/api/roles/check/${permissionName}`);
            return response.has_permission;
        } catch (error) {
            console.error('🔐 Failed to check permission:', error);
            return false;
        }
    }

    /**
     * Обновление разрешений роли
     */
    async updateRolePermissions(roleId, permissionIds) {
        try {
            const response = await window.ApiService.put(`/api/roles/${roleId}/permissions`, permissionIds);
            console.log('🔐 Role permissions updated:', response);

            if (window.Toast && typeof window.Toast.success === 'function') {
                window.Toast.success('Разрешения роли обновлены');
            } else {
                alert('Разрешения роли обновлены');
            }

            return response;
        } catch (error) {
            console.error('🔐 Failed to update role permissions:', error);
            throw error;
        }
    }

    /**
     * Инициализация UI
     */
    initUI() {
        // Создаем модальное окно для управления ролями
        this.createRolesModal();

        // Добавляем обработчики событий
        this.attachEventListeners();
    }

    /**
     * Создание модального окна для управления ролями
     */
    createRolesModal() {
        const modalHTML = `
            <div id="roles-management-modal" class="modal fade" tabindex="-1">
                <div class="modal-dialog modal-xl">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-shield-alt"></i>
                                Управление ролями и разрешениями
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <!-- Левая панель: Роли -->
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between align-items-center mb-3">
                                        <h6>Роли</h6>
                                        <button type="button" class="btn btn-primary btn-sm" onclick="window.rolesManager.showCreateRoleModal()">
                                            <i class="fas fa-plus"></i>
                                            Создать роль
                                        </button>
                                    </div>
                                    
                                    <div id="roles-list" class="roles-list">
                                        <!-- Роли будут загружены здесь -->
                                    </div>
                                </div>
                                
                                <!-- Правая панель: Разрешения -->
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between align-items-center mb-3">
                                        <h6>Разрешения</h6>
                                        <div class="btn-group" role="group">
                                            <button type="button" class="btn btn-sm btn-outline-primary" onclick="window.rolesManager.filterPermissions('all')">
                                                Все
                                            </button>
                                            <button type="button" class="btn btn-sm btn-outline-primary" onclick="window.rolesManager.filterPermissions('users')">
                                                Пользователи
                                            </button>
                                            <button type="button" class="btn btn-sm btn-outline-primary" onclick="window.rolesManager.filterPermissions('posts')">
                                                Посты
                                            </button>
                                            <button type="button" class="btn btn-sm btn-outline-primary" onclick="window.rolesManager.filterPermissions('products')">
                                                Товары
                                            </button>
                                        </div>
                                    </div>
                                    
                                    <div id="permissions-list" class="permissions-list">
                                        <!-- Разрешения будут загружены здесь -->
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Панель управления ролями пользователей -->
                            <div class="row mt-4">
                                <div class="col-12">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">Управление ролями пользователей</h6>
                                        </div>
                                        <div class="card-body">
                                            <div class="row">
                                                <div class="col-md-6">
                                                    <label for="user-id-input" class="form-label">ID пользователя</label>
                                                    <input type="number" class="form-control" id="user-id-input" placeholder="Введите ID пользователя">
                                                </div>
                                                <div class="col-md-4">
                                                    <label for="role-select" class="form-label">Роль</label>
                                                    <select class="form-select" id="role-select">
                                                        <option value="">Выберите роль</option>
                                                    </select>
                                                </div>
                                                <div class="col-md-2">
                                                    <label class="form-label">&nbsp;</label>
                                                    <div class="d-grid">
                                                        <button type="button" class="btn btn-success btn-sm" onclick="window.rolesManager.assignRoleToUserFromUI()">
                                                            Назначить
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button type="button" class="btn btn-info" onclick="window.rolesManager.loadStatistics()">
                                <i class="fas fa-chart-bar"></i>
                                Статистика
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Модальное окно создания роли -->
            <div id="create-role-modal" class="modal fade" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Создание роли</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <form id="create-role-form">
                                <div class="mb-3">
                                    <label for="role-name" class="form-label">Имя роли</label>
                                    <input type="text" class="form-control" id="role-name" required>
                                </div>
                                <div class="mb-3">
                                    <label for="role-display-name" class="form-label">Отображаемое имя</label>
                                    <input type="text" class="form-control" id="role-display-name" required>
                                </div>
                                <div class="mb-3">
                                    <label for="role-description" class="form-label">Описание</label>
                                    <textarea class="form-control" id="role-description" rows="3"></textarea>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Разрешения</label>
                                    <div id="permissions-checkboxes" class="permissions-checkboxes">
                                        <!-- Чекбоксы разрешений будут загружены здесь -->
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                            <button type="button" class="btn btn-primary" onclick="window.rolesManager.createRoleFromForm()">
                                Создать роль
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Добавляем модальные окна в DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    /**
     * Прикрепление обработчиков событий
     */
    attachEventListeners() {
        // Обработчик для кнопки открытия модального окна
        document.addEventListener('click', (e) => {
            if (e.target && e.target.id === 'test-roles-btn') {
                this.openRolesModal();
            }
        });
    }

    /**
     * Открытие модального окна управления ролями
     */
    async openRolesModal() {
        try {
            // Загружаем актуальные данные
            await this.loadRoles();
            await this.loadPermissions();

            // Обновляем UI
            this.updateRolesUI();
            this.updatePermissionsUI();
            this.updateRoleSelect();

            // Показываем модальное окно
            const modal = new bootstrap.Modal(document.getElementById('roles-management-modal'));
            modal.show();

        } catch (error) {
            console.error('🔐 Failed to open roles modal:', error);
        }
    }

    /**
     * Обновление UI ролей
     */
    updateRolesUI() {
        const container = document.getElementById('roles-list');
        if (!container) return;

        if (this.roles.length === 0) {
            container.innerHTML = '<div class="text-center text-muted">Нет ролей</div>';
            return;
        }

        const rolesHTML = this.roles.map(role => {
            const systemBadge = role.is_system ? '<span class="badge bg-warning">Системная</span>' : '';
            const activeBadge = role.is_active ? '<span class="badge bg-success">Активна</span>' : '<span class="badge bg-secondary">Неактивна</span>';

            return `
                <div class="card mb-2">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="flex-grow-1">
                                <h6 class="card-title mb-1">${role.display_name}</h6>
                                <p class="card-text text-muted small mb-2">${role.name}</p>
                                <p class="card-text small mb-2">${role.description || 'Нет описания'}</p>
                                <div class="mb-2">
                                    ${systemBadge}
                                    ${activeBadge}
                                    <span class="badge bg-info">${role.permissions.length} разрешений</span>
                                </div>
                            </div>
                            <div class="btn-group-vertical btn-group-sm">
                                <button class="btn btn-outline-primary btn-sm" onclick="window.rolesManager.editRole(${role.id})">
                                    <i class="fas fa-edit"></i>
                                </button>
                                ${!role.is_system ?
                    `<button class="btn btn-outline-danger btn-sm" onclick="window.rolesManager.deleteRole(${role.id})">
                                        <i class="fas fa-trash"></i>
                                    </button>` : ''
                }
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = rolesHTML;
    }

    /**
     * Обновление UI разрешений
     */
    updatePermissionsUI() {
        const container = document.getElementById('permissions-list');
        if (!container) return;

        if (this.permissions.length === 0) {
            container.innerHTML = '<div class="text-center text-muted">Нет разрешений</div>';
            return;
        }

        const permissionsHTML = this.permissions.map(permission => {
            const resourceBadge = `<span class="badge bg-primary">${permission.resource}</span>`;
            const actionBadge = `<span class="badge bg-secondary">${permission.action}</span>`;

            return `
                <div class="card mb-2">
                    <div class="card-body py-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="flex-grow-1">
                                <h6 class="card-title mb-1 small">${permission.display_name}</h6>
                                <p class="card-text text-muted small mb-1">${permission.name}</p>
                                <div>
                                    ${resourceBadge}
                                    ${actionBadge}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = permissionsHTML;
    }

    /**
     * Обновление селекта ролей
     */
    updateRoleSelect() {
        const select = document.getElementById('role-select');
        if (!select) return;

        const options = this.roles
            .filter(role => role.is_active)
            .map(role => `<option value="${role.id}">${role.display_name}</option>`)
            .join('');

        select.innerHTML = '<option value="">Выберите роль</option>' + options;
    }

    /**
     * Показать модальное окно создания роли
     */
    async showCreateRoleModal() {
        // Загружаем разрешения для чекбоксов
        await this.loadPermissions();
        this.updatePermissionsCheckboxes();

        // Показываем модальное окно
        const modal = new bootstrap.Modal(document.getElementById('create-role-modal'));
        modal.show();
    }

    /**
     * Обновление чекбоксов разрешений
     */
    updatePermissionsCheckboxes() {
        const container = document.getElementById('permissions-checkboxes');
        if (!container) return;

        // Группируем разрешения по ресурсам
        const groupedPermissions = {};
        this.permissions.forEach(permission => {
            if (!groupedPermissions[permission.resource]) {
                groupedPermissions[permission.resource] = [];
            }
            groupedPermissions[permission.resource].push(permission);
        });

        const checkboxesHTML = Object.entries(groupedPermissions).map(([resource, permissions]) => {
            const resourcePermissions = permissions.map(permission => `
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="${permission.id}" id="perm-${permission.id}">
                    <label class="form-check-label" for="perm-${permission.id}">
                        ${permission.display_name}
                    </label>
                </div>
            `).join('');

            return `
                <div class="mb-3">
                    <h6 class="text-capitalize">${resource}</h6>
                    ${resourcePermissions}
                </div>
            `;
        }).join('');

        container.innerHTML = checkboxesHTML;
    }

    /**
     * Создание роли из формы
     */
    async createRoleFromForm() {
        try {
            const name = document.getElementById('role-name').value;
            const displayName = document.getElementById('role-display-name').value;
            const description = document.getElementById('role-description').value;

            if (!name || !displayName) {
                alert('Заполните обязательные поля');
                return;
            }

            // Собираем выбранные разрешения
            const selectedPermissions = Array.from(document.querySelectorAll('#permissions-checkboxes input:checked'))
                .map(checkbox => parseInt(checkbox.value));

            const roleData = {
                name: name,
                display_name: displayName,
                description: description,
                permissions: selectedPermissions
            };

            await this.createRole(roleData);

            // Закрываем модальное окно
            const modal = bootstrap.Modal.getInstance(document.getElementById('create-role-modal'));
            modal.hide();

            // Очищаем форму
            document.getElementById('create-role-form').reset();

        } catch (error) {
            console.error('🔐 Failed to create role from form:', error);
        }
    }

    /**
     * Назначение роли пользователю из UI
     */
    async assignRoleToUserFromUI() {
        try {
            const userId = document.getElementById('user-id-input').value;
            const roleId = document.getElementById('role-select').value;

            if (!userId || !roleId) {
                alert('Заполните все поля');
                return;
            }

            await this.assignRoleToUser(parseInt(userId), parseInt(roleId));

            // Очищаем поля
            document.getElementById('user-id-input').value = '';
            document.getElementById('role-select').value = '';

        } catch (error) {
            console.error('🔐 Failed to assign role from UI:', error);
        }
    }

    /**
     * Фильтрация разрешений
     */
    filterPermissions(resource) {
        const permissions = resource === 'all'
            ? this.permissions
            : this.permissions.filter(p => p.resource === resource);

        const container = document.getElementById('permissions-list');
        if (!container) return;

        if (permissions.length === 0) {
            container.innerHTML = '<div class="text-center text-muted">Нет разрешений</div>';
            return;
        }

        const permissionsHTML = permissions.map(permission => {
            const resourceBadge = `<span class="badge bg-primary">${permission.resource}</span>`;
            const actionBadge = `<span class="badge bg-secondary">${permission.action}</span>`;

            return `
                <div class="card mb-2">
                    <div class="card-body py-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="flex-grow-1">
                                <h6 class="card-title mb-1 small">${permission.display_name}</h6>
                                <p class="card-text text-muted small mb-1">${permission.name}</p>
                                <div>
                                    ${resourceBadge}
                                    ${actionBadge}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = permissionsHTML;
    }

    /**
     * Загрузка статистики
     */
    async loadStatistics() {
        try {
            const response = await window.ApiService.get('/api/roles/statistics');
            console.log('🔐 Statistics loaded:', response);

            // Показываем статистику в alert (можно заменить на модальное окно)
            const statsText = `
Статистика ролей:
- Всего ролей: ${response.total_roles}
- Активных ролей: ${response.active_roles}
- Системных ролей: ${response.system_roles}
- Всего разрешений: ${response.total_permissions}
- Назначений ролей: ${Object.values(response.role_assignments).reduce((a, b) => a + b, 0)}
            `;

            alert(statsText);

        } catch (error) {
            console.error('🔐 Failed to load statistics:', error);
        }
    }

    /**
     * Редактирование роли
     */
    editRole(roleId) {
        const role = this.roles.find(r => r.id === roleId);
        if (!role) return;

        // Здесь можно открыть модальное окно редактирования
        console.log('🔐 Editing role:', role);
        alert(`Редактирование роли: ${role.display_name}`);
    }
}

// Создаем глобальный экземпляр
window.rolesManager = new RolesManager();
