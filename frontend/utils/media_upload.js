/**
 * Система загрузки медиафайлов
 * Поддерживает изображения, видео, документы
 */

class MediaUploadManager {
    constructor() {
        this.apiBase = 'http://localhost:5000';
        this.maxFileSize = 50 * 1024 * 1024; // 50MB
        this.maxImageSize = 10 * 1024 * 1024; // 10MB
        this.maxVideoSize = 100 * 1024 * 1024; // 100MB
        this.allowedTypes = {
            image: ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/bmp'],
            video: ['video/mp4', 'video/avi', 'video/mov', 'video/wmv', 'video/flv', 'video/webm'],
            document: ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'application/rtf']
        };
        this.uploadQueue = [];
        this.isUploading = false;
    }

    /**
     * Инициализация системы загрузки
     */
    init() {
        this.setupEventListeners();
        this.createUploadUI();
        console.log('📁 Media Upload Manager initialized');
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        // Drag & Drop
        document.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.stopPropagation();
        });

        document.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.handleFiles(e.dataTransfer.files);
        });

        // Click to upload
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('media-upload-trigger')) {
                this.openFileDialog();
            }
        });
    }

    /**
     * Создание UI для загрузки
     */
    createUploadUI() {
        // Создаем контейнер для загрузки
        const uploadContainer = document.createElement('div');
        uploadContainer.className = 'media-upload-container';
        uploadContainer.innerHTML = `
            <div class="media-upload-area" id="media-upload-area">
                <div class="upload-content">
                    <i class="fas fa-cloud-upload-alt upload-icon"></i>
                    <h3>Перетащите файлы сюда</h3>
                    <p>или <button class="btn btn-primary media-upload-trigger">выберите файлы</button></p>
                    <div class="upload-info">
                        <small>Поддерживаемые форматы: JPG, PNG, GIF, MP4, PDF, DOC</small>
                        <br>
                        <small>Максимальный размер: 50MB</small>
                    </div>
                </div>
                <input type="file" id="media-file-input" multiple accept="image/*,video/*,.pdf,.doc,.docx,.txt" style="display: none;">
            </div>
            <div class="upload-progress-container" id="upload-progress-container" style="display: none;">
                <div class="upload-progress">
                    <div class="progress-bar" id="upload-progress-bar"></div>
                    <span class="progress-text" id="upload-progress-text">0%</span>
                </div>
            </div>
            <div class="uploaded-files" id="uploaded-files"></div>
        `;

        // Добавляем стили
        this.addStyles();

        // Добавляем в DOM
        document.body.appendChild(uploadContainer);

        // Настраиваем обработчик файлов
        const fileInput = document.getElementById('media-file-input');
        fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });
    }

    /**
     * Добавление CSS стилей
     */
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .media-upload-container {
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
            }

            .media-upload-area {
                border: 2px dashed #ddd;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                background: #fafafa;
                transition: all 0.3s ease;
                cursor: pointer;
            }

            .media-upload-area:hover {
                border-color: #007bff;
                background: #f0f8ff;
            }

            .media-upload-area.dragover {
                border-color: #007bff;
                background: #e3f2fd;
                transform: scale(1.02);
            }

            .upload-content {
                pointer-events: none;
            }

            .upload-icon {
                font-size: 48px;
                color: #007bff;
                margin-bottom: 20px;
            }

            .upload-info {
                margin-top: 20px;
                color: #666;
            }

            .upload-progress-container {
                margin: 20px 0;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
            }

            .upload-progress {
                position: relative;
                height: 20px;
                background: #e9ecef;
                border-radius: 10px;
                overflow: hidden;
            }

            .progress-bar {
                height: 100%;
                background: linear-gradient(90deg, #007bff, #0056b3);
                width: 0%;
                transition: width 0.3s ease;
            }

            .progress-text {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-weight: bold;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            }

            .uploaded-files {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }

            .file-item {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                background: white;
                transition: transform 0.2s ease;
            }

            .file-item:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }

            .file-preview {
                width: 100%;
                height: 120px;
                object-fit: cover;
                border-radius: 4px;
                margin-bottom: 10px;
            }

            .file-info {
                font-size: 12px;
                color: #666;
            }

            .file-actions {
                margin-top: 10px;
                display: flex;
                gap: 5px;
            }

            .btn-sm {
                padding: 4px 8px;
                font-size: 11px;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Обработка выбранных файлов
     */
    async handleFiles(files) {
        const fileArray = Array.from(files);

        // Валидация файлов
        const validFiles = [];
        const errors = [];

        for (const file of fileArray) {
            const validation = this.validateFile(file);
            if (validation.valid) {
                validFiles.push(file);
            } else {
                errors.push(`${file.name}: ${validation.error}`);
            }
        }

        // Показываем ошибки
        if (errors.length > 0) {
            this.showError(errors.join('<br>'));
        }

        // Загружаем валидные файлы
        if (validFiles.length > 0) {
            await this.uploadFiles(validFiles);
        }
    }

    /**
     * Валидация файла
     */
    validateFile(file) {
        // Проверка размера
        if (file.size > this.maxFileSize) {
            return { valid: false, error: 'Файл слишком большой' };
        }

        // Проверка типа
        const fileType = this.getFileType(file.type);
        if (fileType === 'unknown') {
            return { valid: false, error: 'Неподдерживаемый формат' };
        }

        // Дополнительные проверки по типу
        if (fileType === 'image' && file.size > this.maxImageSize) {
            return { valid: false, error: 'Изображение слишком большое' };
        }

        if (fileType === 'video' && file.size > this.maxVideoSize) {
            return { valid: false, error: 'Видео слишком большое' };
        }

        return { valid: true };
    }

    /**
     * Определение типа файла
     */
    getFileType(mimeType) {
        for (const [type, types] of Object.entries(this.allowedTypes)) {
            if (types.includes(mimeType)) {
                return type;
            }
        }
        return 'unknown';
    }

    /**
     * Загрузка файлов на сервер
     */
    async uploadFiles(files) {
        this.isUploading = true;
        this.showProgress(true);

        try {
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                await this.uploadSingleFile(file, i + 1, files.length);
            }

            this.showSuccess(`Успешно загружено ${files.length} файлов`);
        } catch (error) {
            this.showError(`Ошибка загрузки: ${error.message}`);
        } finally {
            this.isUploading = false;
            this.showProgress(false);
        }
    }

    /**
     * Загрузка одного файла
     */
    async uploadSingleFile(file, current, total) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${this.apiBase}/api/media/upload`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            this.displayUploadedFile(result);
            this.updateProgress((current / total) * 100);

        } catch (error) {
            console.error('Upload error:', error);
            throw error;
        }
    }

    /**
     * Отображение загруженного файла
     */
    displayUploadedFile(fileInfo) {
        const container = document.getElementById('uploaded-files');
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';

        let preview = '';
        if (fileInfo.file_type === 'image') {
            preview = `<img src="${fileInfo.url}" alt="${fileInfo.filename}" class="file-preview">`;
        } else if (fileInfo.file_type === 'video') {
            preview = `<video src="${fileInfo.url}" class="file-preview" controls></video>`;
        } else {
            preview = `<div class="file-preview" style="display: flex; align-items: center; justify-content: center; background: #f8f9fa;">
                <i class="fas fa-file" style="font-size: 48px; color: #6c757d;"></i>
            </div>`;
        }

        fileItem.innerHTML = `
            ${preview}
            <div class="file-info">
                <strong>${fileInfo.filename}</strong><br>
                <small>${this.formatFileSize(fileInfo.file_size)} • ${fileInfo.file_type}</small>
            </div>
            <div class="file-actions">
                <button class="btn btn-sm btn-primary" onclick="window.open('${fileInfo.url}', '_blank')">
                    <i class="fas fa-eye"></i> Просмотр
                </button>
                <button class="btn btn-sm btn-secondary" onclick="navigator.clipboard.writeText('${fileInfo.url}')">
                    <i class="fas fa-copy"></i> Копировать
                </button>
                <button class="btn btn-sm btn-danger" onclick="this.closest('.file-item').remove()">
                    <i class="fas fa-trash"></i> Удалить
                </button>
            </div>
        `;

        container.appendChild(fileItem);
    }

    /**
     * Форматирование размера файла
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    /**
     * Показ прогресса загрузки
     */
    showProgress(show) {
        const container = document.getElementById('upload-progress-container');
        container.style.display = show ? 'block' : 'none';
    }

    /**
     * Обновление прогресса
     */
    updateProgress(percent) {
        const bar = document.getElementById('upload-progress-bar');
        const text = document.getElementById('upload-progress-text');

        bar.style.width = `${percent}%`;
        text.textContent = `${Math.round(percent)}%`;
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

    /**
     * Открытие диалога выбора файлов
     */
    openFileDialog() {
        document.getElementById('media-file-input').click();
    }

    /**
     * Получение списка файлов пользователя
     */
    async getUserFiles(page = 1, perPage = 20) {
        try {
            const response = await fetch(`${this.apiBase}/api/media/files?page=${page}&per_page=${perPage}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching files:', error);
            throw error;
        }
    }
}

// Экспорт для глобального доступа
console.log('📁 MediaUploadManager class defined:', typeof MediaUploadManager);
window.MediaUploadManager = MediaUploadManager;
console.log('📁 MediaUploadManager exported to window:', typeof window.MediaUploadManager);
