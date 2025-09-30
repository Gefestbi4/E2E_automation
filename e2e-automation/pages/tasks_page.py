from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger
from utils.screenshot import Screenshot
from config.settings import Settings


class TasksPage(BasePage):
    """
    Page Object для страницы управления задачами (Kanban доски).
    """

    # Локаторы элементов управления задачами
    TASKS_HEADER = (By.XPATH, "//div[@id='tasks-page']/div[@class='page-header']/h1")
    BOARDS_LIST = (By.ID, "boards-list")
    BOARD_CARD = (By.CSS_SELECTOR, ".board-card")

    # Локаторы для создания доски
    CREATE_BOARD_BUTTON = (By.ID, "create-board-btn")
    BOARD_NAME_INPUT = (By.ID, "board-name-input")
    BOARD_DESCRIPTION_INPUT = (By.ID, "board-description-input")
    BOARD_VISIBILITY_SELECT = (By.ID, "board-visibility")
    CREATE_BOARD_SUBMIT = (By.ID, "create-board-submit")

    # Локаторы для доски
    BOARD_HEADER = (By.XPATH, "//div[@id='board-page']/div[@class='page-header']/h1")
    BOARD_COLUMNS = (By.ID, "board-columns")
    TODO_COLUMN = (By.ID, "todo-column")
    IN_PROGRESS_COLUMN = (By.ID, "in-progress-column")
    DONE_COLUMN = (By.ID, "done-column")

    # Локаторы для задач
    TASK_CARD = (By.CSS_SELECTOR, ".task-card")
    ADD_TASK_BUTTON = (By.ID, "add-task-btn")
    TASK_TITLE_INPUT = (By.ID, "task-title-input")
    TASK_DESCRIPTION_INPUT = (By.ID, "task-description-input")
    TASK_PRIORITY_SELECT = (By.ID, "task-priority")
    TASK_DEADLINE_INPUT = (By.ID, "task-deadline")
    CREATE_TASK_SUBMIT = (By.ID, "create-task-submit")

    # Локаторы для редактирования задачи
    EDIT_TASK_BUTTON = (By.CSS_SELECTOR, ".task-card .edit-task-btn")
    SAVE_TASK_BUTTON = (By.ID, "save-task-btn")

    # Локаторы для удаления задачи
    DELETE_TASK_BUTTON = (By.CSS_SELECTOR, ".task-card .delete-task-btn")
    CONFIRM_DELETE_BUTTON = (By.ID, "confirm-delete-btn")

    # Локаторы для комментариев к задаче
    COMMENTS_TAB = (By.ID, "comments-tab")
    COMMENT_INPUT = (By.ID, "comment-input")
    SEND_COMMENT_BUTTON = (By.ID, "send-comment-btn")
    COMMENT_ITEM = (By.CSS_SELECTOR, ".comment-item")

    # Локаторы для назначения исполнителя
    ASSIGN_TASK_BUTTON = (By.CSS_SELECTOR, ".task-card .assign-task-btn")
    ASSIGNEE_SELECT = (By.ID, "assignee-select")
    TASK_ASSIGNEE = (By.CSS_SELECTOR, ".task-card .task-assignee")

    # Локаторы для фильтрации
    FILTERS_BUTTON = (By.ID, "filters-btn")
    PRIORITY_FILTER = (By.ID, "priority-filter")
    ASSIGNEE_FILTER = (By.ID, "assignee-filter")
    DEADLINE_FILTER = (By.ID, "deadline-filter")

    # Локаторы для поиска
    SEARCH_TASKS_INPUT = (By.ID, "search-tasks-input")
    SEARCH_TASKS_BUTTON = (By.ID, "search-tasks-btn")

    # Локаторы для действий с доской
    BOARD_ACTIONS = (By.ID, "board-actions")
    BOARD_SETTINGS_BUTTON = (By.ID, "board-settings-btn")

    # Локаторы для уведомлений
    SUCCESS_MESSAGE = (By.ID, "success-message")
    ERROR_MESSAGE = (By.ID, "error-message")

    def __init__(self, driver, logger: Logger, screenshot: Screenshot):
        super().__init__(driver, logger, screenshot)
        self.url = f"{Settings.FRONTEND_URL}#tasks"

    def load(self):
        """Загружает страницу управления задачами."""
        self.driver.get(self.url)
        self.logger.info(f"Загружена страница управления задачами: {self.url}")
        self._wait_for_element_visible(
            self.TASKS_HEADER, "Заголовок управления задачами"
        )

    def is_tasks_loaded(self) -> bool:
        """Проверяет, загружена ли страница управления задачами."""
        return (
            self._get_element_text(self.TASKS_HEADER, "Заголовок управления задачами")
            == "Task Management"
        )

    def get_boards_list(self) -> list:
        """Возвращает список досок."""
        self.logger.info("Получаем список досок")
        return self.driver.find_elements(*self.BOARD_CARD)

    def get_board_name(self, board_index: int = 0) -> str:
        """Возвращает название доски по индексу."""
        boards = self.get_boards_list()
        if board_index < len(boards):
            return boards[board_index].find_element(By.CSS_SELECTOR, ".board-name").text
        return ""

    def get_board_description(self, board_index: int = 0) -> str:
        """Возвращает описание доски по индексу."""
        boards = self.get_boards_list()
        if board_index < len(boards):
            return (
                boards[board_index]
                .find_element(By.CSS_SELECTOR, ".board-description")
                .text
            )
        return ""

    def click_create_board(self):
        """Нажимает кнопку создания доски."""
        self._click_element(self.CREATE_BOARD_BUTTON, "Кнопка 'Новая доска'")

    def create_board(self, name: str, description: str, visibility: str = "private"):
        """Создает новую доску."""
        self.logger.info(f"Создаем доску: {name}")
        self._type_into_element(self.BOARD_NAME_INPUT, name, "Название доски")
        self._type_into_element(
            self.BOARD_DESCRIPTION_INPUT, description, "Описание доски"
        )
        self._find_element(self.BOARD_VISIBILITY_SELECT, "Видимость доски").send_keys(
            visibility
        )
        self._click_element(self.CREATE_BOARD_SUBMIT, "Кнопка 'Создать доску'")

    def click_board(self, board_index: int = 0):
        """Открывает доску по индексу."""
        self.logger.info(f"Открываем доску {board_index}")
        boards = self.get_boards_list()
        if board_index < len(boards):
            boards[board_index].click()

    def is_board_loaded(self) -> bool:
        """Проверяет, загружена ли доска."""
        try:
            self._wait_for_element_visible(self.BOARD_HEADER, "Заголовок доски")
            return True
        except:
            return False

    def get_board_columns(self) -> list:
        """Возвращает список колонок доски."""
        return self.driver.find_elements(*self.BOARD_COLUMNS)

    def get_tasks_in_column(self, column_name: str) -> list:
        """Возвращает список задач в колонке."""
        column_id = f"{column_name.lower().replace(' ', '-')}-column"
        column = self._find_element((By.ID, column_id), f"Колонка {column_name}")
        return column.find_elements(*self.TASK_CARD)

    def click_add_task(self, column_name: str = "todo"):
        """Нажимает кнопку добавления задачи в колонку."""
        column_id = f"{column_name.lower().replace(' ', '-')}-column"
        column = self._find_element((By.ID, column_id), f"Колонка {column_name}")
        add_button = column.find_element(*self.ADD_TASK_BUTTON)
        add_button.click()

    def create_task(
        self,
        title: str,
        description: str,
        priority: str = "medium",
        deadline: str = None,
    ):
        """Создает новую задачу."""
        self.logger.info(f"Создаем задачу: {title}")
        self._type_into_element(self.TASK_TITLE_INPUT, title, "Название задачи")
        self._type_into_element(
            self.TASK_DESCRIPTION_INPUT, description, "Описание задачи"
        )
        self._find_element(self.TASK_PRIORITY_SELECT, "Приоритет задачи").send_keys(
            priority
        )

        if deadline:
            self._type_into_element(
                self.TASK_DEADLINE_INPUT, deadline, "Дедлайн задачи"
            )

        self._click_element(self.CREATE_TASK_SUBMIT, "Кнопка 'Создать задачу'")

    def get_task_title(self, task_index: int = 0) -> str:
        """Возвращает название задачи по индексу."""
        tasks = self.driver.find_elements(*self.TASK_CARD)
        if task_index < len(tasks):
            return tasks[task_index].find_element(By.CSS_SELECTOR, ".task-title").text
        return ""

    def get_task_description(self, task_index: int = 0) -> str:
        """Возвращает описание задачи по индексу."""
        tasks = self.driver.find_elements(*self.TASK_CARD)
        if task_index < len(tasks):
            return (
                tasks[task_index]
                .find_element(By.CSS_SELECTOR, ".task-description")
                .text
            )
        return ""

    def get_task_priority(self, task_index: int = 0) -> str:
        """Возвращает приоритет задачи по индексу."""
        tasks = self.driver.find_elements(*self.TASK_CARD)
        if task_index < len(tasks):
            return (
                tasks[task_index].find_element(By.CSS_SELECTOR, ".task-priority").text
            )
        return ""

    def get_task_assignee(self, task_index: int = 0) -> str:
        """Возвращает исполнителя задачи по индексу."""
        tasks = self.driver.find_elements(*self.TASK_CARD)
        if task_index < len(tasks):
            try:
                return tasks[task_index].find_element(*self.TASK_ASSIGNEE).text
            except:
                return ""
        return ""

    def click_task(self, task_index: int = 0):
        """Кликает на задачу для просмотра деталей."""
        tasks = self.driver.find_elements(*self.TASK_CARD)
        if task_index < len(tasks):
            tasks[task_index].click()

    def edit_task(self, task_index: int, new_title: str, new_description: str):
        """Редактирует задачу."""
        self.logger.info(f"Редактируем задачу {task_index}")
        tasks = self.driver.find_elements(*self.TASK_CARD)
        if task_index < len(tasks):
            edit_button = tasks[task_index].find_element(*self.EDIT_TASK_BUTTON)
            edit_button.click()
            self._type_into_element(
                self.TASK_TITLE_INPUT, new_title, "Редактирование названия задачи"
            )
            self._type_into_element(
                self.TASK_DESCRIPTION_INPUT,
                new_description,
                "Редактирование описания задачи",
            )
            self._click_element(self.SAVE_TASK_BUTTON, "Кнопка 'Сохранить'")

    def delete_task(self, task_index: int):
        """Удаляет задачу."""
        self.logger.info(f"Удаляем задачу {task_index}")
        tasks = self.driver.find_elements(*self.TASK_CARD)
        if task_index < len(tasks):
            delete_button = tasks[task_index].find_element(*self.DELETE_TASK_BUTTON)
            delete_button.click()
            self._click_element(self.CONFIRM_DELETE_BUTTON, "Кнопка 'Да, удалить'")

    def add_comment_to_task(self, task_index: int, comment: str):
        """Добавляет комментарий к задаче."""
        self.logger.info(f"Добавляем комментарий к задаче {task_index}")
        self.click_task(task_index)
        self._click_element(self.COMMENTS_TAB, "Вкладка 'Комментарии'")
        self._type_into_element(self.COMMENT_INPUT, comment, "Поле комментария")
        self._click_element(self.SEND_COMMENT_BUTTON, "Кнопка 'Отправить комментарий'")

    def get_comments(self) -> list:
        """Возвращает список комментариев."""
        return self.driver.find_elements(*self.COMMENT_ITEM)

    def get_comment_content(self, comment_index: int = 0) -> str:
        """Возвращает содержимое комментария по индексу."""
        comments = self.get_comments()
        if comment_index < len(comments):
            return (
                comments[comment_index]
                .find_element(By.CSS_SELECTOR, ".comment-content")
                .text
            )
        return ""

    def assign_task(self, task_index: int, assignee: str):
        """Назначает исполнителя задачи."""
        self.logger.info(f"Назначаем исполнителя {assignee} для задачи {task_index}")
        tasks = self.driver.find_elements(*self.TASK_CARD)
        if task_index < len(tasks):
            assign_button = tasks[task_index].find_element(*self.ASSIGN_TASK_BUTTON)
            assign_button.click()
            self._find_element(self.ASSIGNEE_SELECT, "Выбор исполнителя").send_keys(
                assignee
            )

    def drag_task_to_column(self, task_index: int, target_column: str):
        """Перетаскивает задачу в другую колонку."""
        self.logger.info(f"Перетаскиваем задачу {task_index} в колонку {target_column}")
        tasks = self.driver.find_elements(*self.TASK_CARD)
        if task_index < len(tasks):
            task = tasks[task_index]
            target_column_id = f"{target_column.lower().replace(' ', '-')}-column"
            target = self._find_element(
                (By.ID, target_column_id), f"Целевая колонка {target_column}"
            )

            # Используем ActionChains для drag and drop
            from selenium.webdriver.common.action_chains import ActionChains

            ActionChains(self.driver).drag_and_drop(task, target).perform()

    def click_filters(self):
        """Открывает панель фильтров."""
        self._click_element(self.FILTERS_BUTTON, "Кнопка 'Фильтры'")

    def filter_by_priority(self, priority: str):
        """Фильтрует задачи по приоритету."""
        self._find_element(self.PRIORITY_FILTER, "Фильтр по приоритету").send_keys(
            priority
        )

    def filter_by_assignee(self, assignee: str):
        """Фильтрует задачи по исполнителю."""
        self._find_element(self.ASSIGNEE_FILTER, "Фильтр по исполнителю").send_keys(
            assignee
        )

    def filter_by_deadline(self, deadline_filter: str):
        """Фильтрует задачи по дедлайну."""
        self._find_element(self.DEADLINE_FILTER, "Фильтр по дедлайну").send_keys(
            deadline_filter
        )

    def search_tasks(self, query: str):
        """Ищет задачи по запросу."""
        self.logger.info(f"Ищем задачи по запросу: {query}")
        self._type_into_element(self.SEARCH_TASKS_INPUT, query, "Поле поиска задач")
        self._click_element(self.SEARCH_TASKS_BUTTON, "Кнопка поиска задач")

    def get_success_message(self) -> str:
        """Возвращает сообщение об успехе."""
        return self._get_element_text(self.SUCCESS_MESSAGE, "Сообщение об успехе")

    def get_error_message(self) -> str:
        """Возвращает сообщение об ошибке."""
        return self._get_element_text(self.ERROR_MESSAGE, "Сообщение об ошибке")

    def is_task_in_column(self, task_title: str, column_name: str) -> bool:
        """Проверяет, есть ли задача в определенной колонке."""
        tasks = self.get_tasks_in_column(column_name)
        for task in tasks:
            if task.find_element(By.CSS_SELECTOR, ".task-title").text == task_title:
                return True
        return False
