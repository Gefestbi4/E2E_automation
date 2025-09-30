from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger
from utils.screenshot import Screenshot
from config.settings import Settings


class ContentPage(BasePage):
    """
    Page Object для страницы управления контентом (статьи).
    """

    # Локаторы элементов управления контентом
    CONTENT_HEADER = (
        By.XPATH,
        "//div[@id='content-page']/div[@class='page-header']/h1",
    )
    ARTICLES_LIST = (By.ID, "articles-list")
    ARTICLE_CARD = (By.CSS_SELECTOR, ".article-card")

    # Локаторы для создания статьи
    CREATE_ARTICLE_BUTTON = (By.ID, "create-article-btn")
    ARTICLE_TITLE_INPUT = (By.ID, "article-title-input")
    ARTICLE_EXCERPT_INPUT = (By.ID, "article-excerpt-input")
    ARTICLE_CONTENT_EDITOR = (By.ID, "article-content-editor")
    ARTICLE_CATEGORY_SELECT = (By.ID, "article-category-select")
    ARTICLE_TAGS_INPUT = (By.ID, "article-tags-input")
    ARTICLE_IMAGE_UPLOAD = (By.ID, "article-image-upload")
    SAVE_DRAFT_BUTTON = (By.ID, "save-draft-btn")
    PUBLISH_ARTICLE_BUTTON = (By.ID, "publish-article-btn")

    # Локаторы для редактирования статьи
    EDIT_ARTICLE_BUTTON = (By.CSS_SELECTOR, ".article-card .edit-article-btn")
    SAVE_ARTICLE_BUTTON = (By.ID, "save-article-btn")

    # Локаторы для удаления статьи
    DELETE_ARTICLE_BUTTON = (By.CSS_SELECTOR, ".article-card .delete-article-btn")
    CONFIRM_DELETE_BUTTON = (By.ID, "confirm-delete-btn")

    # Локаторы для просмотра статьи
    ARTICLE_TITLE = (By.CSS_SELECTOR, ".article-card .article-title")
    ARTICLE_EXCERPT = (By.CSS_SELECTOR, ".article-card .article-excerpt")
    ARTICLE_AUTHOR = (By.CSS_SELECTOR, ".article-card .article-author")
    ARTICLE_DATE = (By.CSS_SELECTOR, ".article-card .article-date")
    ARTICLE_STATUS = (By.CSS_SELECTOR, ".article-card .article-status")
    ARTICLE_CATEGORY = (By.CSS_SELECTOR, ".article-card .article-category")
    ARTICLE_TAGS = (By.CSS_SELECTOR, ".article-card .article-tags")

    # Локаторы для детального просмотра статьи
    ARTICLE_DETAILS = (By.ID, "article-details")
    ARTICLE_DETAILS_TITLE = (By.CSS_SELECTOR, ".article-details .article-title")
    ARTICLE_DETAILS_CONTENT = (By.CSS_SELECTOR, ".article-details .article-content")
    ARTICLE_DETAILS_AUTHOR = (By.CSS_SELECTOR, ".article-details .article-author")
    ARTICLE_DETAILS_DATE = (By.CSS_SELECTOR, ".article-details .article-date")
    ARTICLE_DETAILS_CATEGORY = (By.CSS_SELECTOR, ".article-details .article-category")
    ARTICLE_DETAILS_TAGS = (By.CSS_SELECTOR, ".article-details .article-tags")
    ARTICLE_DETAILS_VIEWS = (By.CSS_SELECTOR, ".article-details .article-views")

    # Локаторы для действий со статьей
    ARTICLE_ACTIONS = (By.ID, "article-actions")
    EDIT_ARTICLE_DETAILS_BUTTON = (
        By.CSS_SELECTOR,
        ".article-details .edit-article-btn",
    )
    DELETE_ARTICLE_DETAILS_BUTTON = (
        By.CSS_SELECTOR,
        ".article-details .delete-article-btn",
    )
    SHARE_ARTICLE_BUTTON = (By.CSS_SELECTOR, ".article-details .share-article-btn")

    # Локаторы для поиска и фильтрации
    SEARCH_ARTICLES_INPUT = (By.ID, "search-articles-input")
    SEARCH_ARTICLES_BUTTON = (By.ID, "search-articles-btn")
    CATEGORY_FILTER = (By.ID, "category-filter")
    STATUS_FILTER = (By.ID, "status-filter")

    # Локаторы для комментариев
    COMMENTS_SECTION = (By.ID, "comments-section")
    COMMENT_INPUT = (By.ID, "comment-input")
    SEND_COMMENT_BUTTON = (By.ID, "send-comment-btn")
    COMMENT_ITEM = (By.CSS_SELECTOR, ".comment-item")
    COMMENT_AUTHOR = (By.CSS_SELECTOR, ".comment-item .comment-author")
    COMMENT_CONTENT = (By.CSS_SELECTOR, ".comment-item .comment-content")
    COMMENT_DATE = (By.CSS_SELECTOR, ".comment-item .comment-date")

    # Локаторы для rich text редактора
    BOLD_BUTTON = (By.ID, "bold-btn")
    ITALIC_BUTTON = (By.ID, "italic-btn")
    UNDERLINE_BUTTON = (By.ID, "underline-btn")
    HEADING_SELECT = (By.ID, "heading-select")
    BULLET_LIST_BUTTON = (By.ID, "bullet-list-btn")
    NUMBERED_LIST_BUTTON = (By.ID, "numbered-list-btn")
    LINK_BUTTON = (By.ID, "link-btn")
    IMAGE_BUTTON = (By.ID, "image-btn")

    # Локаторы для подтверждения публикации
    CONFIRM_PUBLISH_BUTTON = (By.ID, "confirm-publish-btn")

    # Локаторы для уведомлений
    SUCCESS_MESSAGE = (By.ID, "success-message")
    ERROR_MESSAGE = (By.ID, "error-message")

    def __init__(self, driver, logger: Logger, screenshot: Screenshot):
        super().__init__(driver, logger, screenshot)
        self.url = f"{Settings.FRONTEND_URL}#content"

    def load(self):
        """Загружает страницу управления контентом."""
        self.driver.get(self.url)
        self.logger.info(f"Загружена страница управления контентом: {self.url}")
        self._wait_for_element_visible(
            self.CONTENT_HEADER, "Заголовок управления контентом"
        )

    def is_content_loaded(self) -> bool:
        """Проверяет, загружена ли страница управления контентом."""
        return (
            self._get_element_text(
                self.CONTENT_HEADER, "Заголовок управления контентом"
            )
            == "Content Management"
        )

    def get_articles_list(self) -> list:
        """Возвращает список статей."""
        self.logger.info("Получаем список статей")
        return self.driver.find_elements(*self.ARTICLE_CARD)

    def get_article_title(self, article_index: int = 0) -> str:
        """Возвращает заголовок статьи по индексу."""
        articles = self.get_articles_list()
        if article_index < len(articles):
            return articles[article_index].find_element(*self.ARTICLE_TITLE).text
        return ""

    def get_article_excerpt(self, article_index: int = 0) -> str:
        """Возвращает краткое описание статьи по индексу."""
        articles = self.get_articles_list()
        if article_index < len(articles):
            return articles[article_index].find_element(*self.ARTICLE_EXCERPT).text
        return ""

    def get_article_author(self, article_index: int = 0) -> str:
        """Возвращает автора статьи по индексу."""
        articles = self.get_articles_list()
        if article_index < len(articles):
            return articles[article_index].find_element(*self.ARTICLE_AUTHOR).text
        return ""

    def get_article_date(self, article_index: int = 0) -> str:
        """Возвращает дату публикации статьи по индексу."""
        articles = self.get_articles_list()
        if article_index < len(articles):
            return articles[article_index].find_element(*self.ARTICLE_DATE).text
        return ""

    def get_article_status(self, article_index: int = 0) -> str:
        """Возвращает статус статьи по индексу."""
        articles = self.get_articles_list()
        if article_index < len(articles):
            return articles[article_index].find_element(*self.ARTICLE_STATUS).text
        return ""

    def get_article_category(self, article_index: int = 0) -> str:
        """Возвращает категорию статьи по индексу."""
        articles = self.get_articles_list()
        if article_index < len(articles):
            return articles[article_index].find_element(*self.ARTICLE_CATEGORY).text
        return ""

    def get_article_tags(self, article_index: int = 0) -> str:
        """Возвращает теги статьи по индексу."""
        articles = self.get_articles_list()
        if article_index < len(articles):
            return articles[article_index].find_element(*self.ARTICLE_TAGS).text
        return ""

    def click_create_article(self):
        """Нажимает кнопку создания статьи."""
        self._click_element(self.CREATE_ARTICLE_BUTTON, "Кнопка 'Новая статья'")

    def create_article(
        self,
        title: str,
        excerpt: str,
        content: str,
        category: str,
        tags: list,
        image_path: str = None,
    ):
        """Создает новую статью."""
        self.logger.info(f"Создаем статью: {title}")
        self._type_into_element(self.ARTICLE_TITLE_INPUT, title, "Заголовок статьи")
        self._type_into_element(
            self.ARTICLE_EXCERPT_INPUT, excerpt, "Краткое описание статьи"
        )

        # Используем rich text редактор для содержимого
        self._type_into_element(
            self.ARTICLE_CONTENT_EDITOR, content, "Содержимое статьи"
        )

        self._find_element(self.ARTICLE_CATEGORY_SELECT, "Категория статьи").send_keys(
            category
        )

        # Добавляем теги
        tags_string = ", ".join(tags)
        self._type_into_element(self.ARTICLE_TAGS_INPUT, tags_string, "Теги статьи")

        if image_path:
            self.upload_article_image(image_path)

        self._click_element(self.SAVE_DRAFT_BUTTON, "Кнопка 'Сохранить черновик'")

    def upload_article_image(self, image_path: str):
        """Загружает изображение к статье."""
        self.logger.info(f"Загружаем изображение к статье: {image_path}")
        image_input = self._find_element(
            self.ARTICLE_IMAGE_UPLOAD, "Загрузка изображения статьи"
        )
        image_input.send_keys(image_path)

    def publish_article(self, article_index: int = 0):
        """Публикует статью."""
        self.logger.info(f"Публикуем статью {article_index}")
        articles = self.get_articles_list()
        if article_index < len(articles):
            publish_button = articles[article_index].find_element(
                *self.PUBLISH_ARTICLE_BUTTON
            )
            publish_button.click()
            self._click_element(
                self.CONFIRM_PUBLISH_BUTTON, "Кнопка 'Да, опубликовать'"
            )

    def click_edit_article(self, article_index: int = 0):
        """Нажимает кнопку редактирования статьи."""
        articles = self.get_articles_list()
        if article_index < len(articles):
            edit_button = articles[article_index].find_element(
                *self.EDIT_ARTICLE_BUTTON
            )
            edit_button.click()

    def edit_article(
        self,
        article_index: int,
        new_title: str,
        new_content: str,
        new_tags: list = None,
    ):
        """Редактирует статью."""
        self.logger.info(f"Редактируем статью {article_index}")
        self.click_edit_article(article_index)
        self._type_into_element(
            self.ARTICLE_TITLE_INPUT, new_title, "Редактирование заголовка статьи"
        )
        self._type_into_element(
            self.ARTICLE_CONTENT_EDITOR,
            new_content,
            "Редактирование содержимого статьи",
        )

        if new_tags:
            tags_string = ", ".join(new_tags)
            self._type_into_element(
                self.ARTICLE_TAGS_INPUT, tags_string, "Редактирование тегов статьи"
            )

        self._click_element(self.SAVE_ARTICLE_BUTTON, "Кнопка 'Сохранить'")

    def click_article(self, article_index: int = 0):
        """Кликает на статью для просмотра деталей."""
        articles = self.get_articles_list()
        if article_index < len(articles):
            articles[article_index].click()

    def get_article_details(self) -> dict:
        """Возвращает детальную информацию о статье."""
        return {
            "title": self._get_element_text(
                self.ARTICLE_DETAILS_TITLE, "Заголовок статьи"
            ),
            "content": self._get_element_text(
                self.ARTICLE_DETAILS_CONTENT, "Содержимое статьи"
            ),
            "author": self._get_element_text(
                self.ARTICLE_DETAILS_AUTHOR, "Автор статьи"
            ),
            "date": self._get_element_text(
                self.ARTICLE_DETAILS_DATE, "Дата публикации"
            ),
            "category": self._get_element_text(
                self.ARTICLE_DETAILS_CATEGORY, "Категория статьи"
            ),
            "tags": self._get_element_text(self.ARTICLE_DETAILS_TAGS, "Теги статьи"),
            "views": self._get_element_text(
                self.ARTICLE_DETAILS_VIEWS, "Количество просмотров"
            ),
        }

    def delete_article(self, article_index: int):
        """Удаляет статью."""
        self.logger.info(f"Удаляем статью {article_index}")
        articles = self.get_articles_list()
        if article_index < len(articles):
            delete_button = articles[article_index].find_element(
                *self.DELETE_ARTICLE_BUTTON
            )
            delete_button.click()
            self._click_element(self.CONFIRM_DELETE_BUTTON, "Кнопка 'Да, удалить'")

    def search_articles(self, query: str):
        """Ищет статьи по запросу."""
        self.logger.info(f"Ищем статьи по запросу: {query}")
        self._type_into_element(self.SEARCH_ARTICLES_INPUT, query, "Поле поиска статей")
        self._click_element(self.SEARCH_ARTICLES_BUTTON, "Кнопка поиска статей")

    def filter_by_category(self, category: str):
        """Фильтрует статьи по категории."""
        self._find_element(self.CATEGORY_FILTER, "Фильтр по категории").send_keys(
            category
        )

    def filter_by_status(self, status: str):
        """Фильтрует статьи по статусу."""
        self._find_element(self.STATUS_FILTER, "Фильтр по статусу").send_keys(status)

    def add_comment_to_article(self, comment: str):
        """Добавляет комментарий к статье."""
        self.logger.info(f"Добавляем комментарий к статье: {comment}")
        self._type_into_element(self.COMMENT_INPUT, comment, "Поле комментария")
        self._click_element(self.SEND_COMMENT_BUTTON, "Кнопка 'Отправить комментарий'")

    def get_comments(self) -> list:
        """Возвращает список комментариев."""
        return self.driver.find_elements(*self.COMMENT_ITEM)

    def get_comment_content(self, comment_index: int = 0) -> str:
        """Возвращает содержимое комментария по индексу."""
        comments = self.get_comments()
        if comment_index < len(comments):
            return comments[comment_index].find_element(*self.COMMENT_CONTENT).text
        return ""

    def get_comment_author(self, comment_index: int = 0) -> str:
        """Возвращает автора комментария по индексу."""
        comments = self.get_comments()
        if comment_index < len(comments):
            return comments[comment_index].find_element(*self.COMMENT_AUTHOR).text
        return ""

    def get_comment_date(self, comment_index: int = 0) -> str:
        """Возвращает дату комментария по индексу."""
        comments = self.get_comments()
        if comment_index < len(comments):
            return comments[comment_index].find_element(*self.COMMENT_DATE).text
        return ""

    def use_rich_text_editor(self, feature: str, text: str = None):
        """Использует функции rich text редактора."""
        self.logger.info(f"Используем функцию редактора: {feature}")

        if feature == "bold":
            self._click_element(self.BOLD_BUTTON, "Кнопка 'Жирный'")
        elif feature == "italic":
            self._click_element(self.ITALIC_BUTTON, "Кнопка 'Курсив'")
        elif feature == "underline":
            self._click_element(self.UNDERLINE_BUTTON, "Кнопка 'Подчеркнутый'")
        elif feature == "heading":
            self._find_element(self.HEADING_SELECT, "Выбор заголовка").send_keys(
                "Заголовок 2"
            )
        elif feature == "bullet_list":
            self._click_element(
                self.BULLET_LIST_BUTTON, "Кнопка 'Маркированный список'"
            )
        elif feature == "numbered_list":
            self._click_element(
                self.NUMBERED_LIST_BUTTON, "Кнопка 'Нумерованный список'"
            )
        elif feature == "link":
            self._click_element(self.LINK_BUTTON, "Кнопка 'Ссылка'")
        elif feature == "image":
            self._click_element(self.IMAGE_BUTTON, "Кнопка 'Изображение'")

    def get_success_message(self) -> str:
        """Возвращает сообщение об успехе."""
        return self._get_element_text(self.SUCCESS_MESSAGE, "Сообщение об успехе")

    def get_error_message(self) -> str:
        """Возвращает сообщение об ошибке."""
        return self._get_element_text(self.ERROR_MESSAGE, "Сообщение об ошибке")

    def is_article_visible(self, article_title: str) -> bool:
        """Проверяет, видна ли статья с определенным заголовком."""
        articles = self.get_articles_list()
        for article in articles:
            if article.find_element(*self.ARTICLE_TITLE).text == article_title:
                return True
        return False

    def is_article_published(self, article_title: str) -> bool:
        """Проверяет, опубликована ли статья."""
        articles = self.get_articles_list()
        for article in articles:
            if article.find_element(*self.ARTICLE_TITLE).text == article_title:
                status = article.find_element(*self.ARTICLE_STATUS).text
                return status.lower() == "published"
        return False
