// Утилиты для работы с аватарами
class AvatarUtils {
    // Встроенный SVG аватар в формате data URI
    static getDefaultAvatar() {
        return 'data:image/svg+xml;base64,' + btoa(`
            <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="32" cy="32" r="32" fill="#E5E7EB"/>
                <circle cx="32" cy="24" r="10" fill="#9CA3AF"/>
                <path d="M16 48C16 40 22 34 32 34C42 34 48 40 48 48V52H16V48Z" fill="#9CA3AF"/>
            </svg>
        `);
    }

    // Создает аватар с инициалами
    static createInitialsAvatar(name, size = 64) {
        const initials = name
            .split(' ')
            .map(word => word.charAt(0))
            .join('')
            .toUpperCase()
            .substring(0, 2);

        const colors = [
            '#3498db', '#e74c3c', '#2ecc71', '#f39c12',
            '#9b59b6', '#1abc9c', '#34495e', '#e67e22'
        ];

        const colorIndex = name.length % colors.length;
        const backgroundColor = colors[colorIndex];

        return `data:image/svg+xml;base64,${btoa(`
            <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="${size / 2}" cy="${size / 2}" r="${size / 2}" fill="${backgroundColor}"/>
                <text x="${size / 2}" y="${size / 2 + size / 8}" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="${size / 3}" font-weight="bold">${initials}</text>
            </svg>
        `)}`;
    }

    // Устанавливает дефолтный аватар для элемента
    static setDefaultAvatar(imgElement) {
        if (imgElement) {
            imgElement.src = this.getDefaultAvatar();
            imgElement.onerror = null; // Убираем обработчик ошибок
        }
    }

    // Устанавливает аватар с инициалами
    static setInitialsAvatar(imgElement, name) {
        if (imgElement && name) {
            imgElement.src = this.createInitialsAvatar(name);
            imgElement.onerror = null;
        }
    }

    // Обработчик ошибки загрузки аватара
    static handleAvatarError(imgElement, fallbackName = null) {
        if (imgElement) {
            if (fallbackName) {
                imgElement.src = this.createInitialsAvatar(fallbackName);
            } else {
                imgElement.src = this.getDefaultAvatar();
            }
            // Убираем обработчик ошибок, чтобы избежать бесконечного цикла
            imgElement.onerror = null;
        }
    }
}

// Экспорт для глобального доступа
window.AvatarUtils = AvatarUtils;
