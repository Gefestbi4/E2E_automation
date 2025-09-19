// Глобальные функции для модальных окон (доступны сразу)
window.openModal = function(jobId) {
  if (window.modalManager) {
    window.modalManager.openModal(jobId);
  } else {
    console.log('modalManager еще не инициализирован, ждем...');
    // Если modalManager еще не готов, ждем немного и пробуем снова
    setTimeout(() => {
      if (window.modalManager) {
        window.modalManager.openModal(jobId);
      }
    }, 100);
  }
};

window.closeModal = function() {
  if (window.modalManager) {
    window.modalManager.closeModal();
  }
};

// Управление темами
class ThemeManager {
  constructor() {
    this.init();
  }

  init() {
    // Проверяем сохраненную тему или системные предпочтения
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');
    
    this.setTheme(initialTheme);
    this.setupToggleButton();
  }

  setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    // Обновляем иконку
    const themeIcon = document.querySelector('.theme-icon');
    if (themeIcon) {
      themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
  }

  toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    this.setTheme(newTheme);
  }

  setupToggleButton() {
    const toggleButton = document.getElementById('theme-toggle');
    if (toggleButton) {
      toggleButton.addEventListener('click', () => this.toggleTheme());
    }
  }
}

// Управление модальными окнами
class ModalManager {
  constructor() {
    this.overlay = document.getElementById('modal-overlay');
    this.modalBody = document.getElementById('modal-body');
    this.jobData = this.getJobData();
    this.init();
  }

  init() {
    // Закрытие модального окна по ESC
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.closeModal();
      }
    });
  }

  openModal(jobId) {
    const jobInfo = this.jobData[jobId];
    if (!jobInfo) return;

    this.modalBody.innerHTML = `
      <h2 class="modal-title">${jobInfo.title}</h2>
      <div class="modal-period">${jobInfo.period}</div>
      <div class="modal-company">${jobInfo.company}</div>
      <div class="modal-description">
        ${jobInfo.description}
      </div>
    `;

    this.overlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Блокируем прокрутку
  }

  closeModal() {
    this.overlay.classList.remove('active');
    document.body.style.overflow = ''; // Восстанавливаем прокрутку
  }

  getJobData() {
    return {
      'senior-cloudike': {
        title: 'Senior QA Engineer',
        period: '2022 - настоящее время',
        company: 'Cloudike Inc',
        description: `
          <h4>Основные обязанности:</h4>
          <ul>
            <li><strong>Руководство процессом тестирования</strong> - планирование, координация и контроль качества тестирования всех продуктов компании</li>
            <li><strong>Ментoring junior и middle QA</strong> - обучение новых сотрудников, проведение код-ревью тест-кейсов</li>
            <li><strong>Создание стратегии тестирования</strong> - разработка тест-планов, выбор методологий и инструментов</li>
            <li><strong>Автоматизация процессов</strong> - внедрение CI/CD для тестирования, настройка автоматических проверок</li>
            <li><strong>Кроссплатформенное тестирование</strong> - веб, мобильные приложения (iOS/Android), десктопные клиенты</li>
          </ul>
          
          <h4>Ключевые достижения:</h4>
          <ul>
            <li>Сократил время тестирования релизов на 40% за счет оптимизации процессов</li>
            <li>Внедрил систему регрессионного тестирования с покрытием 95% критического функционала</li>
            <li>Обучил и адаптировал 5 новых QA-специалистов</li>
            <li>Снизил количество багов в продакшене на 60% благодаря улучшению процессов</li>
          </ul>

          <h4>Технологии и инструменты:</h4>
          <ul>
            <li>Jira, TestRail, Confluence</li>
            <li>Postman, Charles Proxy, Swagger</li>
            <li>Chrome DevTools, Safari Web Inspector</li>
            <li>Git, Jenkins, Docker</li>
            <li>SQL, MongoDB</li>
          </ul>
        `
      },
      'middle-cloudike': {
        title: 'Middle QA Engineer',
        period: '2021 - 2022',
        company: 'Cloudike Inc',
        description: `
          <h4>Основные обязанности:</h4>
          <ul>
            <li><strong>Функциональное тестирование</strong> - полное покрытие новых фич и исправлений</li>
            <li><strong>Регрессионное тестирование</strong> - обеспечение стабильности существующего функционала</li>
            <li><strong>API тестирование</strong> - проверка REST API, интеграций с внешними сервисами</li>
            <li><strong>Мобильное тестирование</strong> - iOS и Android приложения, адаптивная верстка</li>
            <li><strong>Составление документации</strong> - тест-кейсы, чек-листы, отчеты о багах</li>
          </ul>
          
          <h4>Ключевые достижения:</h4>
          <ul>
            <li>Создал библиотеку тест-кейсов для основных модулей системы (500+ кейсов)</li>
            <li>Выявил и помог исправить 300+ критических багов</li>
            <li>Оптимизировал процесс smoke-тестирования, сократив время с 4 до 1.5 часов</li>
            <li>Провел тестирование 15+ крупных релизов без критических инцидентов</li>
          </ul>

          <h4>Проекты:</h4>
          <ul>
            <li>Тестирование системы синхронизации файлов</li>
            <li>Проверка интеграции с облачными хранилищами</li>
            <li>Тестирование системы резервного копирования</li>
            <li>Проверка многопользовательского доступа и разграничения прав</li>
          </ul>
        `
      },
      'junior-cloudike': {
        title: 'Junior QA Engineer',
        period: '2020 - 2021',
        company: 'Cloudike Inc',
        description: `
          <h4>Основные обязанности:</h4>
          <ul>
            <li><strong>Ручное тестирование</strong> - выполнение тест-кейсов, поиск багов в веб и мобильных приложениях</li>
            <li><strong>Smoke testing</strong> - ежедневная проверка основного функционала после деплоев</li>
            <li><strong>UI/UX тестирование</strong> - проверка интерфейса на разных браузерах и устройствах</li>
            <li><strong>Баг-репорты</strong> - детальное описание найденных проблем с шагами воспроизведения</li>
            <li><strong>Изучение продукта</strong> - глубокое понимание бизнес-логики и пользовательских сценариев</li>
          </ul>
          
          <h4>Ключевые достижения:</h4>
          <ul>
            <li>Быстро освоил продуктовую область облачных хранилищ</li>
            <li>Нашел 150+ багов различной критичности за первый год</li>
            <li>Изучил основы тестирования API и баз данных</li>
            <li>Получил опыт работы с iOS и Android приложениями</li>
          </ul>

          <h4>Изученные технологии:</h4>
          <ul>
            <li>Основы HTTP/HTTPS, REST API</li>
            <li>SQL запросы для проверки данных</li>
            <li>Инструменты разработчика браузеров</li>
            <li>Системы баг-трекинга (Jira)</li>
            <li>Методологии тестирования</li>
          </ul>
        `
      },
      'junior-top10': {
        title: 'Junior QA Engineer',
        period: '2019 - 2020',
        company: 'TOP 10 Education Project Silicon Valley',
        description: `
          <h4>Основные обязанности:</h4>
          <ul>
            <li><strong>Тестирование образовательной платформы</strong> - проверка курсов, тестов, системы оценок</li>
            <li><strong>Пользовательское тестирование</strong> - проверка удобства использования для студентов и преподавателей</li>
            <li><strong>Кроссбраузерное тестирование</strong> - обеспечение работы на всех популярных браузерах</li>
            <li><strong>Мобильная адаптация</strong> - проверка корректности отображения на мобильных устройствах</li>
            <li><strong>Контент-тестирование</strong> - проверка образовательных материалов, видео, документов</li>
          </ul>
          
          <h4>Первый опыт в QA:</h4>
          <ul>
            <li>Изучил основы методологий тестирования</li>
            <li>Освоил принципы написания тест-кейсов</li>
            <li>Получил опыт работы в команде разработки</li>
            <li>Научился работать с системами управления проектами</li>
          </ul>

          <h4>Проекты:</h4>
          <ul>
            <li>Тестирование системы регистрации и авторизации</li>
            <li>Проверка загрузки и воспроизведения видео-контента</li>
            <li>Тестирование системы прогресса обучения</li>
            <li>Проверка интеграции с платежными системами</li>
          </ul>

          <h4>Полученные навыки:</h4>
          <ul>
            <li>Понимание жизненного цикла разработки ПО</li>
            <li>Опыт работы в Agile/Scrum команде</li>
            <li>Базовые знания HTML/CSS для лучшего понимания веб-приложений</li>
            <li>Начальные навыки работы с базами данных</li>
          </ul>
        `
      }
    };
  }
}


// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
  window.themeManager = new ThemeManager();
  window.modalManager = new ModalManager();
  
  console.log('🎨 Система тем и модальных окон инициализирована');
});