/**
 * Система управления настройками и приватностью
 * Полная система настроек пользователя
 */

class SettingsManager {
    constructor() {
        this.apiBase = 'http://localhost:5000';
        this.currentSettings = {};
        this.isLoading = false;
    }

    /**
     * Инициализация системы настроек
     */
    init() {
        this.createSettingsUI();
        this.setupEventListeners();
        this.loadUserSettings();
        console.log('⚙️ Settings Manager initialized');
    }

    /**
     * Создание UI для настроек
     */
    createSettingsUI() {
        // Создаем контейнер для настроек
        const settingsContainer = document.createElement('div');
        settingsContainer.className = 'settings-container';
        settingsContainer.innerHTML = `
            <div class="settings-header">
                <h2><i class="fas fa-cog"></i> Настройки</h2>
                <div class="settings-actions">
                    <button id="save-all-settings-btn" class="btn btn-primary">
                        <i class="fas fa-save"></i> Сохранить все
                    </button>
                    <button id="reset-settings-btn" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Сбросить
                    </button>
                </div>
            </div>

            <div class="settings-content">
                <div class="settings-sidebar">
                    <nav class="settings-nav">
                        <a href="#profile" class="nav-item active" data-tab="profile">
                            <i class="fas fa-user"></i> Профиль
                        </a>
                        <a href="#privacy" class="nav-item" data-tab="privacy">
                            <i class="fas fa-shield-alt"></i> Приватность
                        </a>
                        <a href="#notifications" class="nav-item" data-tab="notifications">
                            <i class="fas fa-bell"></i> Уведомления
                        </a>
                        <a href="#security" class="nav-item" data-tab="security">
                            <i class="fas fa-lock"></i> Безопасность
                        </a>
                        <a href="#appearance" class="nav-item" data-tab="appearance">
                            <i class="fas fa-palette"></i> Внешний вид
                        </a>
                        <a href="#content" class="nav-item" data-tab="content">
                            <i class="fas fa-filter"></i> Контент
                        </a>
                        <a href="#social" class="nav-item" data-tab="social">
                            <i class="fas fa-users"></i> Социальные
                        </a>
                        <a href="#data" class="nav-item" data-tab="data">
                            <i class="fas fa-database"></i> Данные
                        </a>
                    </nav>
                </div>

                <div class="settings-main">
                    <!-- Профиль -->
                    <div id="profile-tab" class="settings-tab active">
                        <h3>Настройки профиля</h3>
                        <div class="settings-form">
                            <div class="form-group">
                                <label>Имя пользователя</label>
                                <input type="text" id="username" class="form-control">
                            </div>
                            <div class="form-group">
                                <label>Email</label>
                                <input type="email" id="email" class="form-control">
                            </div>
                            <div class="form-group">
                                <label>Полное имя</label>
                                <input type="text" id="full_name" class="form-control">
                            </div>
                            <div class="form-group">
                                <label>О себе</label>
                                <textarea id="bio" class="form-control" rows="3"></textarea>
                            </div>
                            <div class="form-group">
                                <label>Местоположение</label>
                                <input type="text" id="location" class="form-control">
                            </div>
                            <div class="form-group">
                                <label>Веб-сайт</label>
                                <input type="url" id="website" class="form-control">
                            </div>
                        </div>
                    </div>

                    <!-- Приватность -->
                    <div id="privacy-tab" class="settings-tab">
                        <h3>Настройки приватности</h3>
                        <div class="settings-form">
                            <div class="form-group">
                                <label>Видимость профиля</label>
                                <select id="profile_visibility" class="form-control">
                                    <option value="public">Публичный</option>
                                    <option value="friends">Только друзья</option>
                                    <option value="private">Приватный</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="show_email" class="form-check-input">
                                    <label class="form-check-label" for="show_email">Показывать email</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="show_location" class="form-check-input">
                                    <label class="form-check-label" for="show_location">Показывать местоположение</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="show_online_status" class="form-check-input">
                                    <label class="form-check-label" for="show_online_status">Показывать статус онлайн</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <label>Кто может писать сообщения</label>
                                <select id="allow_direct_messages" class="form-control">
                                    <option value="everyone">Все</option>
                                    <option value="friends">Только друзья</option>
                                    <option value="none">Никто</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Уведомления -->
                    <div id="notifications-tab" class="settings-tab">
                        <h3>Настройки уведомлений</h3>
                        <div class="settings-form">
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="email_notifications" class="form-check-input">
                                    <label class="form-check-label" for="email_notifications">Email уведомления</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="push_notifications" class="form-check-input">
                                    <label class="form-check-label" for="push_notifications">Push уведомления</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="new_follower" class="form-check-input">
                                    <label class="form-check-label" for="new_follower">Новые подписчики</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="new_like" class="form-check-input">
                                    <label class="form-check-label" for="new_like">Новые лайки</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="new_comment" class="form-check-input">
                                    <label class="form-check-label" for="new_comment">Новые комментарии</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="new_message" class="form-check-input">
                                    <label class="form-check-label" for="new_message">Новые сообщения</label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Безопасность -->
                    <div id="security-tab" class="settings-tab">
                        <h3>Настройки безопасности</h3>
                        <div class="settings-form">
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="two_factor_enabled" class="form-check-input">
                                    <label class="form-check-label" for="two_factor_enabled">Двухфакторная аутентификация</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="login_notifications" class="form-check-input">
                                    <label class="form-check-label" for="login_notifications">Уведомления о входах</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <label>Таймаут сессии (минуты)</label>
                                <input type="number" id="session_timeout" class="form-control" min="5" max="480">
                            </div>
                            <div class="form-group">
                                <label>Максимум попыток входа</label>
                                <input type="number" id="max_login_attempts" class="form-control" min="3" max="10">
                            </div>
                        </div>
                    </div>

                    <!-- Внешний вид -->
                    <div id="appearance-tab" class="settings-tab">
                        <h3>Настройки внешнего вида</h3>
                        <div class="settings-form">
                            <div class="form-group">
                                <label>Тема</label>
                                <select id="theme" class="form-control">
                                    <option value="light">Светлая</option>
                                    <option value="dark">Темная</option>
                                    <option value="auto">Автоматически</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Язык</label>
                                <select id="language" class="form-control">
                                    <option value="ru">Русский</option>
                                    <option value="en">English</option>
                                    <option value="es">Español</option>
                                    <option value="fr">Français</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Часовой пояс</label>
                                <select id="timezone" class="form-control">
                                    <option value="Europe/Moscow">Москва (UTC+3)</option>
                                    <option value="Europe/London">Лондон (UTC+0)</option>
                                    <option value="America/New_York">Нью-Йорк (UTC-5)</option>
                                    <option value="Asia/Tokyo">Токио (UTC+9)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="compact_mode" class="form-check-input">
                                    <label class="form-check-label" for="compact_mode">Компактный режим</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="show_animations" class="form-check-input">
                                    <label class="form-check-label" for="show_animations">Показывать анимации</label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Контент -->
                    <div id="content-tab" class="settings-tab">
                        <h3>Настройки контента</h3>
                        <div class="settings-form">
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="auto_play_videos" class="form-check-input">
                                    <label class="form-check-label" for="auto_play_videos">Автовоспроизведение видео</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="show_nsfw_content" class="form-check-input">
                                    <label class="form-check-label" for="show_nsfw_content">Показывать NSFW контент</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <label>Фильтрация контента</label>
                                <select id="content_filtering" class="form-control">
                                    <option value="strict">Строгая</option>
                                    <option value="moderate">Умеренная</option>
                                    <option value="off">Отключена</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="auto_save_drafts" class="form-check-input">
                                    <label class="form-check-label" for="auto_save_drafts">Автосохранение черновиков</label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Социальные -->
                    <div id="social-tab" class="settings-tab">
                        <h3>Социальные настройки</h3>
                        <div class="settings-form">
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="auto_follow_back" class="form-check-input">
                                    <label class="form-check-label" for="auto_follow_back">Автоматически подписываться в ответ</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="show_follow_suggestions" class="form-check-input">
                                    <label class="form-check-label" for="show_follow_suggestions">Показывать предложения подписок</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="allow_tagging" class="form-check-input">
                                    <label class="form-check-label" for="allow_tagging">Разрешить тегирование</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input type="checkbox" id="allow_mentions" class="form-check-input">
                                    <label class="form-check-label" for="allow_mentions">Разрешить упоминания</label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Данные -->
                    <div id="data-tab" class="settings-tab">
                        <h3>Управление данными</h3>
                        <div class="settings-form">
                            <div class="form-group">
                                <h4>Экспорт данных</h4>
                                <p>Скачайте копию всех ваших данных</p>
                                <button id="export-data-btn" class="btn btn-primary">
                                    <i class="fas fa-download"></i> Экспортировать данные
                                </button>
                            </div>
                            <div class="form-group">
                                <h4>Удаление данных</h4>
                                <p>Навсегда удалите все ваши данные (необратимо)</p>
                                <button id="delete-data-btn" class="btn btn-danger">
                                    <i class="fas fa-trash"></i> Удалить все данные
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Добавляем стили
        this.addStyles();

        // Добавляем в DOM
        document.body.appendChild(settingsContainer);
    }

    /**
     * Добавление CSS стилей
     */
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .settings-container {
                max-width: 1200px;
                margin: 20px auto;
                padding: 20px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }

            .settings-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #eee;
            }

            .settings-header h2 {
                margin: 0;
                color: #333;
            }

            .settings-actions {
                display: flex;
                gap: 10px;
            }

            .settings-content {
                display: grid;
                grid-template-columns: 250px 1fr;
                gap: 30px;
            }

            .settings-sidebar {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
            }

            .settings-nav {
                display: flex;
                flex-direction: column;
                gap: 5px;
            }

            .nav-item {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 12px 16px;
                color: #666;
                text-decoration: none;
                border-radius: 6px;
                transition: all 0.2s ease;
            }

            .nav-item:hover {
                background: #e9ecef;
                color: #333;
            }

            .nav-item.active {
                background: #007bff;
                color: white;
            }

            .nav-item i {
                width: 20px;
                text-align: center;
            }

            .settings-main {
                background: white;
                border-radius: 8px;
                padding: 30px;
            }

            .settings-tab {
                display: none;
            }

            .settings-tab.active {
                display: block;
            }

            .settings-tab h3 {
                margin: 0 0 25px 0;
                color: #333;
                font-size: 24px;
            }

            .settings-form {
                display: grid;
                gap: 20px;
            }

            .form-group {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }

            .form-group label {
                font-weight: 500;
                color: #555;
            }

            .form-control {
                padding: 10px 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                transition: border-color 0.2s ease;
            }

            .form-control:focus {
                outline: none;
                border-color: #007bff;
                box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
            }

            .form-check {
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .form-check-input {
                margin: 0;
            }

            .form-check-label {
                margin: 0;
                cursor: pointer;
            }

            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            }

            .btn-primary {
                background: #007bff;
                color: white;
            }

            .btn-primary:hover {
                background: #0056b3;
            }

            .btn-secondary {
                background: #6c757d;
                color: white;
            }

            .btn-secondary:hover {
                background: #545b62;
            }

            .btn-danger {
                background: #dc3545;
                color: white;
            }

            .btn-danger:hover {
                background: #c82333;
            }

            @media (max-width: 768px) {
                .settings-content {
                    grid-template-columns: 1fr;
                }
                
                .settings-sidebar {
                    order: 2;
                }
                
                .settings-nav {
                    flex-direction: row;
                    overflow-x: auto;
                    gap: 10px;
                }
                
                .nav-item {
                    white-space: nowrap;
                    min-width: fit-content;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        // Навигация по табам
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchTab(item.dataset.tab);
            });
        });

        // Сохранение всех настроек
        document.getElementById('save-all-settings-btn').addEventListener('click', () => {
            this.saveAllSettings();
        });

        // Сброс настроек
        document.getElementById('reset-settings-btn').addEventListener('click', () => {
            this.resetSettings();
        });

        // Экспорт данных
        document.getElementById('export-data-btn').addEventListener('click', () => {
            this.exportUserData();
        });

        // Удаление данных
        document.getElementById('delete-data-btn').addEventListener('click', () => {
            this.deleteUserData();
        });
    }

    /**
     * Переключение табов
     */
    switchTab(tabName) {
        // Убираем активный класс со всех табов и навигации
        document.querySelectorAll('.settings-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });

        // Активируем выбранный таб
        document.getElementById(`${tabName}-tab`).classList.add('active');
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    }

    /**
     * Загрузка настроек пользователя
     */
    async loadUserSettings() {
        try {
            this.isLoading = true;
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/settings/`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.currentSettings = data.settings;
            this.populateSettingsForm();

        } catch (error) {
            this.showError(`Ошибка загрузки настроек: ${error.message}`);
        } finally {
            this.isLoading = false;
            this.showLoading(false);
        }
    }

    /**
     * Заполнение формы настроек
     */
    populateSettingsForm() {
        const settings = this.currentSettings;

        // Профиль
        if (settings.profile) {
            document.getElementById('username').value = settings.profile.username || '';
            document.getElementById('email').value = settings.profile.email || '';
            document.getElementById('full_name').value = settings.profile.full_name || '';
            document.getElementById('bio').value = settings.profile.bio || '';
            document.getElementById('location').value = settings.profile.location || '';
            document.getElementById('website').value = settings.profile.website || '';
        }

        // Приватность
        if (settings.privacy) {
            document.getElementById('profile_visibility').value = settings.privacy.profile_visibility || 'public';
            document.getElementById('show_email').checked = settings.privacy.show_email || false;
            document.getElementById('show_location').checked = settings.privacy.show_location || false;
            document.getElementById('show_online_status').checked = settings.privacy.show_online_status || false;
            document.getElementById('allow_direct_messages').value = settings.privacy.allow_direct_messages || 'everyone';
        }

        // Уведомления
        if (settings.notifications) {
            document.getElementById('email_notifications').checked = settings.notifications.email_notifications || false;
            document.getElementById('push_notifications').checked = settings.notifications.push_notifications || false;
            document.getElementById('new_follower').checked = settings.notifications.new_follower || false;
            document.getElementById('new_like').checked = settings.notifications.new_like || false;
            document.getElementById('new_comment').checked = settings.notifications.new_comment || false;
            document.getElementById('new_message').checked = settings.notifications.new_message || false;
        }

        // Безопасность
        if (settings.security) {
            document.getElementById('two_factor_enabled').checked = settings.security.two_factor_enabled || false;
            document.getElementById('login_notifications').checked = settings.security.login_notifications || false;
            document.getElementById('session_timeout').value = settings.security.session_timeout || 30;
            document.getElementById('max_login_attempts').value = settings.security.max_login_attempts || 5;
        }

        // Внешний вид
        if (settings.appearance) {
            document.getElementById('theme').value = settings.appearance.theme || 'light';
            document.getElementById('language').value = settings.appearance.language || 'ru';
            document.getElementById('timezone').value = settings.appearance.timezone || 'Europe/Moscow';
            document.getElementById('compact_mode').checked = settings.appearance.compact_mode || false;
            document.getElementById('show_animations').checked = settings.appearance.show_animations || false;
        }

        // Контент
        if (settings.content) {
            document.getElementById('auto_play_videos').checked = settings.content.auto_play_videos || false;
            document.getElementById('show_nsfw_content').checked = settings.content.show_nsfw_content || false;
            document.getElementById('content_filtering').value = settings.content.content_filtering || 'moderate';
            document.getElementById('auto_save_drafts').checked = settings.content.auto_save_drafts || false;
        }

        // Социальные
        if (settings.social) {
            document.getElementById('auto_follow_back').checked = settings.social.auto_follow_back || false;
            document.getElementById('show_follow_suggestions').checked = settings.social.show_follow_suggestions || false;
            document.getElementById('allow_tagging').checked = settings.social.allow_tagging || false;
            document.getElementById('allow_mentions').checked = settings.social.allow_mentions || false;
        }
    }

    /**
     * Сохранение всех настроек
     */
    async saveAllSettings() {
        try {
            this.isLoading = true;
            this.showLoading(true);

            // Собираем все настройки
            const settings = {
                profile: {
                    username: document.getElementById('username').value,
                    email: document.getElementById('email').value,
                    full_name: document.getElementById('full_name').value,
                    bio: document.getElementById('bio').value,
                    location: document.getElementById('location').value,
                    website: document.getElementById('website').value,
                },
                privacy: {
                    profile_visibility: document.getElementById('profile_visibility').value,
                    show_email: document.getElementById('show_email').checked,
                    show_location: document.getElementById('show_location').checked,
                    show_online_status: document.getElementById('show_online_status').checked,
                    allow_direct_messages: document.getElementById('allow_direct_messages').value,
                },
                notifications: {
                    email_notifications: document.getElementById('email_notifications').checked,
                    push_notifications: document.getElementById('push_notifications').checked,
                    new_follower: document.getElementById('new_follower').checked,
                    new_like: document.getElementById('new_like').checked,
                    new_comment: document.getElementById('new_comment').checked,
                    new_message: document.getElementById('new_message').checked,
                },
                security: {
                    two_factor_enabled: document.getElementById('two_factor_enabled').checked,
                    login_notifications: document.getElementById('login_notifications').checked,
                    session_timeout: parseInt(document.getElementById('session_timeout').value),
                    max_login_attempts: parseInt(document.getElementById('max_login_attempts').value),
                },
                appearance: {
                    theme: document.getElementById('theme').value,
                    language: document.getElementById('language').value,
                    timezone: document.getElementById('timezone').value,
                    compact_mode: document.getElementById('compact_mode').checked,
                    show_animations: document.getElementById('show_animations').checked,
                },
                content: {
                    auto_play_videos: document.getElementById('auto_play_videos').checked,
                    show_nsfw_content: document.getElementById('show_nsfw_content').checked,
                    content_filtering: document.getElementById('content_filtering').value,
                    auto_save_drafts: document.getElementById('auto_save_drafts').checked,
                },
                social: {
                    auto_follow_back: document.getElementById('auto_follow_back').checked,
                    show_follow_suggestions: document.getElementById('show_follow_suggestions').checked,
                    allow_tagging: document.getElementById('allow_tagging').checked,
                    allow_mentions: document.getElementById('allow_mentions').checked,
                },
            };

            // Отправляем на сервер
            const response = await fetch(`${this.apiBase}/api/settings/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({ settings })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            this.showSuccess('Настройки сохранены успешно');

        } catch (error) {
            this.showError(`Ошибка сохранения настроек: ${error.message}`);
        } finally {
            this.isLoading = false;
            this.showLoading(false);
        }
    }

    /**
     * Сброс настроек
     */
    async resetSettings() {
        if (!confirm('Вы уверены, что хотите сбросить все настройки к значениям по умолчанию?')) {
            return;
        }

        try {
            this.isLoading = true;
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/settings/reset`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            this.showSuccess('Настройки сброшены к значениям по умолчанию');
            this.loadUserSettings();

        } catch (error) {
            this.showError(`Ошибка сброса настроек: ${error.message}`);
        } finally {
            this.isLoading = false;
            this.showLoading(false);
        }
    }

    /**
     * Экспорт данных пользователя
     */
    async exportUserData() {
        try {
            this.isLoading = true;
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/settings/export`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();

            // Создаем и скачиваем файл
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `user_data_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            this.showSuccess('Данные экспортированы успешно');

        } catch (error) {
            this.showError(`Ошибка экспорта данных: ${error.message}`);
        } finally {
            this.isLoading = false;
            this.showLoading(false);
        }
    }

    /**
     * Удаление данных пользователя
     */
    async deleteUserData() {
        if (!confirm('ВНИМАНИЕ: Это действие необратимо! Все ваши данные будут удалены навсегда. Продолжить?')) {
            return;
        }

        if (!confirm('Последнее предупреждение: Вы действительно хотите удалить ВСЕ свои данные?')) {
            return;
        }

        try {
            this.isLoading = true;
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/settings/data`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            this.showSuccess('Все данные удалены. Вы будете перенаправлены на страницу входа.');

            // Перенаправляем на страницу входа
            setTimeout(() => {
                window.location.href = '/login.html';
            }, 3000);

        } catch (error) {
            this.showError(`Ошибка удаления данных: ${error.message}`);
        } finally {
            this.isLoading = false;
            this.showLoading(false);
        }
    }

    /**
     * Показ загрузки
     */
    showLoading(show) {
        const container = document.querySelector('.settings-container');
        if (show) {
            container.style.opacity = '0.6';
            container.style.pointerEvents = 'none';
        } else {
            container.style.opacity = '1';
            container.style.pointerEvents = 'auto';
        }
    }

    /**
     * Показ ошибки
     */
    showError(message) {
        if (window.Toast && typeof window.Toast.error === 'function') {
            window.Toast.error(message);
        } else {
            alert(`Ошибка: ${message}`);
        }
    }

    /**
     * Показ успеха
     */
    showSuccess(message) {
        if (window.Toast && typeof window.Toast.success === 'function') {
            window.Toast.success(message);
        } else {
            alert(`Успех: ${message}`);
        }
    }
}

// Экспорт для глобального доступа
console.log('⚙️ SettingsManager class defined:', typeof SettingsManager);
window.SettingsManager = SettingsManager;
window.settingsManager = new SettingsManager();
console.log('⚙️ SettingsManager exported to window:', typeof window.SettingsManager);
