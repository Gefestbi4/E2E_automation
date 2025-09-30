from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger
from utils.screenshot import Screenshot
from config.settings import Settings


class SocialPage(BasePage):
    """
    Page Object для страницы социальной сети.
    """

    # Локаторы элементов социальной сети
    SOCIAL_HEADER = (By.XPATH, "//div[@id='social-page']/div[@class='page-header']/h1")
    POSTS_FEED = (By.ID, "posts-feed")
    POST_CARD = (By.CSS_SELECTOR, ".post-card")

    # Локаторы для создания поста
    CREATE_POST_BUTTON = (By.ID, "create-post-btn")
    POST_CONTENT_INPUT = (By.ID, "post-content-input")
    POST_IMAGE_UPLOAD = (By.ID, "post-image-upload")
    POST_VISIBILITY_SELECT = (By.ID, "post-visibility")
    PUBLISH_POST_BUTTON = (By.ID, "publish-post-btn")

    # Локаторы для поста
    POST_TITLE = (By.CSS_SELECTOR, ".post-card .post-title")
    POST_CONTENT = (By.CSS_SELECTOR, ".post-card .post-content")
    POST_AUTHOR = (By.CSS_SELECTOR, ".post-card .post-author")
    POST_TIMESTAMP = (By.CSS_SELECTOR, ".post-card .post-timestamp")
    POST_IMAGE = (By.CSS_SELECTOR, ".post-card .post-image")

    # Локаторы для взаимодействия с постом
    LIKE_BUTTON = (By.CSS_SELECTOR, ".post-card .like-btn")
    LIKE_COUNT = (By.CSS_SELECTOR, ".post-card .like-count")
    COMMENT_BUTTON = (By.CSS_SELECTOR, ".post-card .comment-btn")
    COMMENT_COUNT = (By.CSS_SELECTOR, ".post-card .comment-count")
    SHARE_BUTTON = (By.CSS_SELECTOR, ".post-card .share-btn")

    # Локаторы для редактирования поста
    EDIT_POST_BUTTON = (By.CSS_SELECTOR, ".post-card .edit-post-btn")
    SAVE_POST_BUTTON = (By.ID, "save-post-btn")

    # Локаторы для удаления поста
    DELETE_POST_BUTTON = (By.CSS_SELECTOR, ".post-card .delete-post-btn")
    CONFIRM_DELETE_BUTTON = (By.ID, "confirm-delete-btn")

    # Локаторы для комментариев
    COMMENT_INPUT = (By.ID, "comment-input")
    SEND_COMMENT_BUTTON = (By.ID, "send-comment-btn")
    COMMENT_ITEM = (By.CSS_SELECTOR, ".comment-item")
    COMMENT_AUTHOR = (By.CSS_SELECTOR, ".comment-item .comment-author")
    COMMENT_CONTENT = (By.CSS_SELECTOR, ".comment-item .comment-content")
    COMMENT_TIMESTAMP = (By.CSS_SELECTOR, ".comment-item .comment-timestamp")

    # Локаторы для поиска и фильтрации
    SEARCH_POSTS_INPUT = (By.ID, "search-posts-input")
    SEARCH_POSTS_BUTTON = (By.ID, "search-posts-btn")
    FILTER_MY_POSTS = (By.ID, "filter-my-posts")
    FILTER_POPULAR = (By.ID, "filter-popular")
    FILTER_RECENT = (By.ID, "filter-recent")

    # Локаторы для загрузки изображений
    ADD_IMAGE_BUTTON = (By.ID, "add-image-btn")
    IMAGE_UPLOAD_INPUT = (By.ID, "image-upload-input")
    IMAGE_PREVIEW = (By.ID, "image-preview")

    # Локаторы для детальной информации о посте
    POST_DETAILS = (By.ID, "post-details")
    POST_DETAILS_TITLE = (By.CSS_SELECTOR, ".post-details .post-title")
    POST_DETAILS_CONTENT = (By.CSS_SELECTOR, ".post-details .post-content")
    POST_DETAILS_AUTHOR = (By.CSS_SELECTOR, ".post-details .post-author")
    POST_DETAILS_TIMESTAMP = (By.CSS_SELECTOR, ".post-details .post-timestamp")
    POST_DETAILS_LIKES = (By.CSS_SELECTOR, ".post-details .post-likes")
    POST_DETAILS_COMMENTS = (By.CSS_SELECTOR, ".post-details .post-comments")

    # Локаторы для поделиться
    SHARE_MENU = (By.ID, "share-menu")
    COPY_LINK_BUTTON = (By.ID, "copy-link-btn")
    SHARE_SOCIAL_BUTTON = (By.ID, "share-social-btn")

    # Локаторы для уведомлений
    SUCCESS_MESSAGE = (By.ID, "success-message")
    ERROR_MESSAGE = (By.ID, "error-message")

    def __init__(self, driver, logger: Logger, screenshot: Screenshot):
        super().__init__(driver, logger, screenshot)
        self.url = f"{Settings.FRONTEND_URL}#social"

    def load(self):
        """Загружает страницу социальной сети."""
        self.driver.get(self.url)
        self.logger.info(f"Загружена страница социальной сети: {self.url}")
        self._wait_for_element_visible(self.SOCIAL_HEADER, "Заголовок социальной сети")

    def is_social_loaded(self) -> bool:
        """Проверяет, загружена ли страница социальной сети."""
        return (
            self._get_element_text(self.SOCIAL_HEADER, "Заголовок социальной сети")
            == "Social Network"
        )

    def get_posts_feed(self) -> list:
        """Возвращает список постов в ленте."""
        self.logger.info("Получаем список постов в ленте")
        return self.driver.find_elements(*self.POST_CARD)

    def click_create_post(self):
        """Нажимает кнопку создания поста."""
        self._click_element(self.CREATE_POST_BUTTON, "Кнопка 'Создать пост'")

    def create_post(
        self, content: str, visibility: str = "public", image_path: str = None
    ):
        """Создает новый пост."""
        self.logger.info(f"Создаем пост с содержимым: {content}")
        self._type_into_element(self.POST_CONTENT_INPUT, content, "Содержимое поста")

        if visibility:
            self._find_element(
                self.POST_VISIBILITY_SELECT, "Выбор видимости поста"
            ).send_keys(visibility)

        if image_path:
            self.upload_post_image(image_path)

        self._click_element(self.PUBLISH_POST_BUTTON, "Кнопка 'Опубликовать'")

    def upload_post_image(self, image_path: str):
        """Загружает изображение к посту."""
        self.logger.info(f"Загружаем изображение: {image_path}")
        image_input = self._find_element(self.POST_IMAGE_UPLOAD, "Загрузка изображения")
        image_input.send_keys(image_path)

    def get_post_content(self, post_index: int = 0) -> str:
        """Возвращает содержимое поста по индексу."""
        posts = self.get_posts_feed()
        if post_index < len(posts):
            return posts[post_index].find_element(*self.POST_CONTENT).text
        return ""

    def get_post_author(self, post_index: int = 0) -> str:
        """Возвращает автора поста по индексу."""
        posts = self.get_posts_feed()
        if post_index < len(posts):
            return posts[post_index].find_element(*self.POST_AUTHOR).text
        return ""

    def get_post_timestamp(self, post_index: int = 0) -> str:
        """Возвращает время публикации поста по индексу."""
        posts = self.get_posts_feed()
        if post_index < len(posts):
            return posts[post_index].find_element(*self.POST_TIMESTAMP).text
        return ""

    def like_post(self, post_index: int = 0):
        """Ставит лайк посту."""
        self.logger.info(f"Ставим лайк посту {post_index}")
        posts = self.get_posts_feed()
        if post_index < len(posts):
            like_button = posts[post_index].find_element(*self.LIKE_BUTTON)
            like_button.click()

    def get_like_count(self, post_index: int = 0) -> int:
        """Возвращает количество лайков поста."""
        posts = self.get_posts_feed()
        if post_index < len(posts):
            try:
                like_count_text = posts[post_index].find_element(*self.LIKE_COUNT).text
                return int(like_count_text)
            except ValueError:
                return 0
        return 0

    def comment_on_post(self, post_index: int, comment: str):
        """Добавляет комментарий к посту."""
        self.logger.info(f"Добавляем комментарий к посту {post_index}: {comment}")
        posts = self.get_posts_feed()
        if post_index < len(posts):
            comment_button = posts[post_index].find_element(*self.COMMENT_BUTTON)
            comment_button.click()
            self._type_into_element(self.COMMENT_INPUT, comment, "Поле комментария")
            self._click_element(
                self.SEND_COMMENT_BUTTON, "Кнопка 'Отправить комментарий'"
            )

    def get_comment_count(self, post_index: int = 0) -> int:
        """Возвращает количество комментариев поста."""
        posts = self.get_posts_feed()
        if post_index < len(posts):
            try:
                comment_count_text = (
                    posts[post_index].find_element(*self.COMMENT_COUNT).text
                )
                return int(comment_count_text)
            except ValueError:
                return 0
        return 0

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

    def edit_post(self, post_index: int, new_content: str):
        """Редактирует пост."""
        self.logger.info(f"Редактируем пост {post_index}")
        posts = self.get_posts_feed()
        if post_index < len(posts):
            edit_button = posts[post_index].find_element(*self.EDIT_POST_BUTTON)
            edit_button.click()
            self._type_into_element(
                self.POST_CONTENT_INPUT, new_content, "Редактирование поста"
            )
            self._click_element(self.SAVE_POST_BUTTON, "Кнопка 'Сохранить'")

    def delete_post(self, post_index: int):
        """Удаляет пост."""
        self.logger.info(f"Удаляем пост {post_index}")
        posts = self.get_posts_feed()
        if post_index < len(posts):
            delete_button = posts[post_index].find_element(*self.DELETE_POST_BUTTON)
            delete_button.click()
            self._click_element(self.CONFIRM_DELETE_BUTTON, "Кнопка 'Да, удалить'")

    def click_post(self, post_index: int):
        """Кликает на пост для просмотра деталей."""
        posts = self.get_posts_feed()
        if post_index < len(posts):
            posts[post_index].click()

    def get_post_details(self) -> dict:
        """Возвращает детальную информацию о посте."""
        return {
            "title": self._get_element_text(self.POST_DETAILS_TITLE, "Заголовок поста"),
            "content": self._get_element_text(
                self.POST_DETAILS_CONTENT, "Содержимое поста"
            ),
            "author": self._get_element_text(self.POST_DETAILS_AUTHOR, "Автор поста"),
            "timestamp": self._get_element_text(
                self.POST_DETAILS_TIMESTAMP, "Время публикации"
            ),
            "likes": self._get_element_text(
                self.POST_DETAILS_LIKES, "Количество лайков"
            ),
            "comments": self._get_element_text(
                self.POST_DETAILS_COMMENTS, "Количество комментариев"
            ),
        }

    def share_post(self, post_index: int):
        """Делится постом."""
        self.logger.info(f"Делимся постом {post_index}")
        posts = self.get_posts_feed()
        if post_index < len(posts):
            share_button = posts[post_index].find_element(*self.SHARE_BUTTON)
            share_button.click()

    def copy_post_link(self):
        """Копирует ссылку на пост."""
        self._click_element(self.COPY_LINK_BUTTON, "Кнопка 'Скопировать ссылку'")

    def search_posts(self, query: str):
        """Ищет посты по запросу."""
        self.logger.info(f"Ищем посты по запросу: {query}")
        self._type_into_element(self.SEARCH_POSTS_INPUT, query, "Поле поиска постов")
        self._click_element(self.SEARCH_POSTS_BUTTON, "Кнопка поиска постов")

    def filter_my_posts(self):
        """Фильтрует только мои посты."""
        self._click_element(self.FILTER_MY_POSTS, "Фильтр 'Мои посты'")

    def filter_popular_posts(self):
        """Фильтрует популярные посты."""
        self._click_element(self.FILTER_POPULAR, "Фильтр 'Популярные'")

    def filter_recent_posts(self):
        """Фильтрует недавние посты."""
        self._click_element(self.FILTER_RECENT, "Фильтр 'Недавние'")

    def upload_image(self, image_path: str):
        """Загружает изображение."""
        self.logger.info(f"Загружаем изображение: {image_path}")
        self._click_element(self.ADD_IMAGE_BUTTON, "Кнопка 'Добавить изображение'")
        image_input = self._find_element(
            self.IMAGE_UPLOAD_INPUT, "Поле загрузки изображения"
        )
        image_input.send_keys(image_path)

    def get_success_message(self) -> str:
        """Возвращает сообщение об успехе."""
        return self._get_element_text(self.SUCCESS_MESSAGE, "Сообщение об успехе")

    def get_error_message(self) -> str:
        """Возвращает сообщение об ошибке."""
        return self._get_element_text(self.ERROR_MESSAGE, "Сообщение об ошибке")

    def is_post_visible(self, post_content: str) -> bool:
        """Проверяет, виден ли пост с определенным содержимым."""
        posts = self.get_posts_feed()
        for post in posts:
            if post.find_element(*self.POST_CONTENT).text == post_content:
                return True
        return False
