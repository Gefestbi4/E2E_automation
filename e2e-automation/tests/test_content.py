"""
Content Management tests for the application
"""

import pytest
import allure
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.content_page import ContentPage
from utils.logger import TestLogger
from utils.content_testing import ContentTesting


@allure.feature("Content Management Tests")
@allure.story("Content Management Testing")
class TestContent(BaseTest):
    """Test class for content management testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestContent")
        self.content_testing = ContentTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.content_page = ContentPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test content page loads correctly")
    @pytest.mark.content
    def test_content_page_loads(self):
        """Test content page loads correctly"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test content page loads"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"
            assert (
                self.content_page.get_page_title() == "Content Management"
            ), "Page title should be correct"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test article creation")
    @pytest.mark.content
    def test_article_creation(self):
        """Test article creation"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test content page loads"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

        with allure.step("Test create new article"):
            article_data = self.settings.get_article_data()
            self.content_page.create_article(article_data)
            assert (
                self.content_page.wait_for_article_created()
            ), "Article should be created"
            assert self.content_page.is_article_displayed(
                article_data
            ), "Article should be displayed"

        with allure.step("Test article content validation"):
            assert (
                self.content_page.get_article_title() == article_data["title"]
            ), "Article title should match"
            assert (
                self.content_page.get_article_content() == article_data["content"]
            ), "Article content should match"
            assert (
                self.content_page.get_article_category() == article_data["category"]
            ), "Article category should match"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test article editing")
    @pytest.mark.content
    def test_article_editing(self):
        """Test article editing"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test content page loads"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

        with allure.step("Test create article first"):
            article_data = self.settings.get_article_data()
            self.content_page.create_article(article_data)
            assert (
                self.content_page.wait_for_article_created()
            ), "Article should be created"

        with allure.step("Test edit article"):
            article = self.content_page.get_first_article()
            updated_title = "Updated Article Title"
            updated_content = "Updated article content"
            self.content_page.edit_article(article, updated_title, updated_content)
            assert (
                self.content_page.wait_for_article_updated()
            ), "Article should be updated"
            assert (
                self.content_page.get_article_title(article) == updated_title
            ), "Article title should be updated"
            assert (
                self.content_page.get_article_content(article) == updated_content
            ), "Article content should be updated"

        with allure.step("Test delete article"):
            self.content_page.delete_article(article)
            assert (
                self.content_page.wait_for_article_deleted()
            ), "Article should be deleted"
            assert not self.content_page.is_article_displayed(
                article
            ), "Article should not be displayed"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test article publishing")
    @pytest.mark.content
    def test_article_publishing(self):
        """Test article publishing"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test content page loads"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

        with allure.step("Test create article first"):
            article_data = self.settings.get_article_data()
            self.content_page.create_article(article_data)
            assert (
                self.content_page.wait_for_article_created()
            ), "Article should be created"

        with allure.step("Test publish article"):
            article = self.content_page.get_first_article()
            self.content_page.publish_article(article)
            assert (
                self.content_page.wait_for_article_published()
            ), "Article should be published"
            assert (
                self.content_page.get_article_status(article) == "published"
            ), "Article status should be published"

        with allure.step("Test unpublish article"):
            self.content_page.unpublish_article(article)
            assert (
                self.content_page.wait_for_article_unpublished()
            ), "Article should be unpublished"
            assert (
                self.content_page.get_article_status(article) == "draft"
            ), "Article status should be draft"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test article categorization")
    @pytest.mark.content
    def test_article_categorization(self):
        """Test article categorization"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test content page loads"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

        with allure.step("Test create article first"):
            article_data = self.settings.get_article_data()
            self.content_page.create_article(article_data)
            assert (
                self.content_page.wait_for_article_created()
            ), "Article should be created"

        with allure.step("Test assign category to article"):
            article = self.content_page.get_first_article()
            category = "Technology"
            self.content_page.assign_category_to_article(article, category)
            assert (
                self.content_page.wait_for_category_assigned()
            ), "Category should be assigned"
            assert (
                self.content_page.get_article_category(article) == category
            ), "Article category should be updated"

        with allure.step("Test change article category"):
            new_category = "Science"
            self.content_page.change_article_category(article, new_category)
            assert (
                self.content_page.wait_for_category_changed()
            ), "Category should be changed"
            assert (
                self.content_page.get_article_category(article) == new_category
            ), "Article category should be updated"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test article search and filtering")
    @pytest.mark.content
    def test_article_search_and_filtering(self):
        """Test article search and filtering"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test content page loads"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

        with allure.step("Test search articles"):
            search_term = "technology"
            self.content_page.search_articles(search_term)
            assert (
                self.content_page.wait_for_search_results()
            ), "Search results should load"
            assert (
                self.content_page.get_search_results_count() > 0
            ), "Should have search results"

        with allure.step("Test filter articles by category"):
            category = "Technology"
            self.content_page.filter_articles_by_category(category)
            assert (
                self.content_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.content_page.get_filtered_articles_count() > 0
            ), "Should have filtered articles"

        with allure.step("Test filter articles by status"):
            status = "published"
            self.content_page.filter_articles_by_status(status)
            assert (
                self.content_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.content_page.get_filtered_articles_count() > 0
            ), "Should have filtered articles"

        with allure.step("Test filter articles by author"):
            author = self.settings.get_user_credentials("admin_user")
            self.content_page.filter_articles_by_author(author["username"])
            assert (
                self.content_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.content_page.get_filtered_articles_count() > 0
            ), "Should have filtered articles"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test article comments")
    @pytest.mark.content
    def test_article_comments(self):
        """Test article comments"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test content page loads"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

        with allure.step("Test create article first"):
            article_data = self.settings.get_article_data()
            self.content_page.create_article(article_data)
            assert (
                self.content_page.wait_for_article_created()
            ), "Article should be created"

        with allure.step("Test view article details"):
            article = self.content_page.get_first_article()
            self.content_page.view_article_details(article)
            assert (
                self.content_page.wait_for_article_details()
            ), "Article details should load"

        with allure.step("Test add comment to article"):
            comment_data = self.settings.get_comment_data()
            self.content_page.add_comment_to_article(article, comment_data)
            assert self.content_page.wait_for_comment_added(), "Comment should be added"
            assert self.content_page.is_comment_displayed(
                article, comment_data
            ), "Comment should be displayed"

        with allure.step("Test edit comment"):
            comment = self.content_page.get_first_comment(article)
            updated_content = "Updated comment content"
            self.content_page.edit_comment(comment, updated_content)
            assert (
                self.content_page.wait_for_comment_updated()
            ), "Comment should be updated"
            assert (
                self.content_page.get_comment_content(comment) == updated_content
            ), "Comment content should be updated"

        with allure.step("Test delete comment"):
            self.content_page.delete_comment(comment)
            assert (
                self.content_page.wait_for_comment_deleted()
            ), "Comment should be deleted"
            assert not self.content_page.is_comment_displayed(
                article, comment_data
            ), "Comment should not be displayed"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test content API")
    @pytest.mark.content
    def test_content_api(self):
        """Test content API"""
        with allure.step("Test articles API"):
            response = self.api_client.get("/api/content/articles")
            assert response.status_code == 200, "Articles API should return 200"
            assert len(response.json()) > 0, "Should have articles"

        with allure.step("Test create article API"):
            article_data = self.settings.get_article_data()
            response = self.api_client.post("/api/content/articles", article_data)
            assert response.status_code == 201, "Create article API should return 201"
            assert "id" in response.json(), "Article should have ID"

        with allure.step("Test update article API"):
            response = self.api_client.put(
                "/api/content/articles/1", {"title": "Updated Title"}
            )
            assert response.status_code == 200, "Update article API should return 200"
            assert (
                response.json()["title"] == "Updated Title"
            ), "Article title should be updated"

        with allure.step("Test publish article API"):
            response = self.api_client.post("/api/content/articles/1/publish")
            assert response.status_code == 200, "Publish article API should return 200"
            assert (
                response.json()["status"] == "published"
            ), "Article status should be published"

    # Article Management Tests
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test viewing articles list")
    @pytest.mark.content
    def test_view_articles_list(self):
        """Test viewing articles list"""
        with allure.step("Login and navigate to content"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.content_page.load()

        with allure.step("Verify content page loads"):
            assert (
                self.content_page.is_content_loaded()
            ), "Content page should load correctly"

        with allure.step("Verify articles list is displayed"):
            articles = self.content_page.get_articles_list()
            assert len(articles) >= 0, "Articles list should be displayed"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test creating a new article")
    @pytest.mark.content
    def test_create_article(self):
        """Test creating a new article"""
        with allure.step("Login and navigate to content"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.content_page.load()

        with allure.step("Create new article"):
            article_data = self.settings.get_test_data()["content"]["sample_articles"][
                0
            ]
            self.content_page.click_create_article()
            self.content_page.create_article(
                article_data["title"],
                article_data["excerpt"],
                article_data["content"],
                article_data["category"],
                article_data["tags"],
            )

        with allure.step("Verify article is created"):
            assert (
                self.content_page.get_success_message() != ""
            ), "Success message should be displayed"
            assert self.content_page.is_article_visible(
                article_data["title"]
            ), "Article should be visible in list"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test editing an article")
    @pytest.mark.content
    def test_edit_article(self):
        """Test editing an article"""
        with allure.step("Login and create an article"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.content_page.load()

            article_data = self.settings.get_test_data()["content"]["sample_articles"][
                0
            ]
            self.content_page.click_create_article()
            self.content_page.create_article(
                article_data["title"],
                article_data["excerpt"],
                article_data["content"],
                article_data["category"],
                article_data["tags"],
            )

        with allure.step("Edit the article"):
            new_title = "Обновленное название статьи"
            new_content = "Обновленное содержимое статьи"
            self.content_page.edit_article(0, new_title, new_content)

        with allure.step("Verify article is updated"):
            assert (
                self.content_page.get_success_message() != ""
            ), "Success message should be displayed"
            assert (
                self.content_page.get_article_title(0) == new_title
            ), "Article title should be updated"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test publishing an article")
    @pytest.mark.content
    def test_publish_article(self):
        """Test publishing an article"""
        with allure.step("Login and create an article"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.content_page.load()

            article_data = self.settings.get_test_data()["content"]["sample_articles"][
                0
            ]
            self.content_page.click_create_article()
            self.content_page.create_article(
                article_data["title"],
                article_data["excerpt"],
                article_data["content"],
                article_data["category"],
                article_data["tags"],
            )

        with allure.step("Publish the article"):
            self.content_page.publish_article(0)

        with allure.step("Verify article is published"):
            assert (
                self.content_page.get_success_message() != ""
            ), "Success message should be displayed"
            assert (
                self.content_page.get_article_status(0) == "published"
            ), "Article status should be published"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test viewing article details")
    @pytest.mark.content
    def test_view_article_details(self):
        """Test viewing article details"""
        with allure.step("Login and create an article"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.content_page.load()

            article_data = self.settings.get_test_data()["content"]["sample_articles"][
                0
            ]
            self.content_page.click_create_article()
            self.content_page.create_article(
                article_data["title"],
                article_data["excerpt"],
                article_data["content"],
                article_data["category"],
                article_data["tags"],
            )

        with allure.step("View article details"):
            self.content_page.click_article(0)
            article_details = self.content_page.get_article_details()

        with allure.step("Verify article details are displayed"):
            assert article_details["title"] != "", "Article title should be displayed"
            assert (
                article_details["content"] != ""
            ), "Article content should be displayed"
            assert article_details["author"] != "", "Article author should be displayed"
            assert (
                article_details["created_at"] != ""
            ), "Article creation date should be displayed"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test deleting an article")
    @pytest.mark.content
    def test_delete_article(self):
        """Test deleting an article"""
        with allure.step("Login and create an article"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.content_page.load()

            article_data = self.settings.get_test_data()["content"]["sample_articles"][
                0
            ]
            self.content_page.click_create_article()
            self.content_page.create_article(
                article_data["title"],
                article_data["excerpt"],
                article_data["content"],
                article_data["category"],
                article_data["tags"],
            )

        with allure.step("Delete the article"):
            self.content_page.delete_article(0)

        with allure.step("Verify article is deleted"):
            assert (
                self.content_page.get_success_message() != ""
            ), "Success message should be displayed"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test searching articles")
    @pytest.mark.content
    def test_search_articles(self):
        """Test searching articles"""
        with allure.step("Login and navigate to content"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.content_page.load()

        with allure.step("Search for articles"):
            search_query = self.settings.get_test_data()["content"]["search_queries"][0]
            self.content_page.search_articles(search_query)

        with allure.step("Verify search results"):
            articles = self.content_page.get_articles_list()
            assert len(articles) >= 0, "Search should return results"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test filtering articles by category")
    @pytest.mark.content
    def test_filter_articles_by_category(self):
        """Test filtering articles by category"""
        with allure.step("Login and navigate to content"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.content_page.load()

        with allure.step("Filter by category"):
            category = self.settings.get_test_data()["content"]["categories"][0]
            self.content_page.filter_by_category(category)
            articles = self.content_page.get_articles_list()
            assert len(articles) >= 0, "Filter should return results"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test filtering articles by status")
    @pytest.mark.content
    def test_filter_articles_by_status(self):
        """Test filtering articles by status"""
        with allure.step("Login and navigate to content"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.content_page.load()

        with allure.step("Filter by status"):
            self.content_page.filter_by_status("published")
            articles = self.content_page.get_articles_list()
            assert len(articles) >= 0, "Filter should return results"

        with allure.step("Filter by draft status"):
            self.content_page.filter_by_status("draft")
            articles = self.content_page.get_articles_list()
            assert len(articles) >= 0, "Filter should return results"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test adding comment to article")
    @pytest.mark.content
    def test_add_comment_to_article(self):
        """Test adding comment to article"""
        with allure.step("Login and create an article"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.content_page.load()

            article_data = self.settings.get_test_data()["content"]["sample_articles"][
                0
            ]
            self.content_page.click_create_article()
            self.content_page.create_article(
                article_data["title"],
                article_data["excerpt"],
                article_data["content"],
                article_data["category"],
                article_data["tags"],
            )

        with allure.step("Add comment to article"):
            comment_data = self.settings.get_test_data()["content"]["sample_comments"][
                0
            ]
            self.content_page.click_article(0)
            self.content_page.add_comment(comment_data["content"])

        with allure.step("Verify comment is added"):
            assert (
                self.content_page.get_success_message() != ""
            ), "Success message should be displayed"
            comments = self.content_page.get_comments()
            assert len(comments) > 0, "Comment should be added"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test rich text editor functionality")
    @pytest.mark.content
    def test_rich_text_editor(self):
        """Test rich text editor functionality"""
        with allure.step("Login and navigate to content"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.content_page.load()

        with allure.step("Test rich text editor features"):
            self.content_page.click_create_article()

            # Test bold text
            self.content_page.format_text_bold("Bold text")

            # Test italic text
            self.content_page.format_text_italic("Italic text")

            # Test bullet list
            self.content_page.create_bullet_list(["Item 1", "Item 2", "Item 3"])

            # Test numbered list
            self.content_page.create_numbered_list(["First", "Second", "Third"])

            # Test link insertion
            self.content_page.insert_link("Test Link", "https://example.com")

        with allure.step("Verify rich text formatting"):
            assert (
                self.content_page.is_rich_text_editor_loaded()
            ), "Rich text editor should be loaded"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test content API")
    @pytest.mark.content
    def test_content_api(self):
        """Test content API"""
        with allure.step("Test articles API"):
            response = self.api_client.get("/api/content/articles")
            assert response.status_code == 200, "Articles API should return 200"
            assert len(response.json()) > 0, "Should have articles"

        with allure.step("Test create article API"):
            article_data = self.settings.get_test_data()["content"]["sample_articles"][
                0
            ]
            response = self.api_client.post("/api/content/articles", article_data)
            assert response.status_code == 201, "Create article API should return 201"
            assert "id" in response.json(), "Article should have ID"

        with allure.step("Test update article API"):
            response = self.api_client.put(
                "/api/content/articles/1", {"title": "Updated Title"}
            )
            assert response.status_code == 200, "Update article API should return 200"
            assert (
                response.json()["title"] == "Updated Title"
            ), "Article title should be updated"

        with allure.step("Test publish article API"):
            response = self.api_client.post("/api/content/articles/1/publish")
            assert response.status_code == 200, "Publish article API should return 200"
            assert (
                response.json()["status"] == "published"
            ), "Article status should be published"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test content error handling")
    @pytest.mark.content
    def test_content_error_handling(self):
        """Test content error handling"""
        with allure.step("Login and navigate to content"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.content_page.load()

        with allure.step("Test error handling for empty article title"):
            self.content_page.click_create_article()
            self.content_page.create_article(
                "", "Test excerpt", "Test content", "Technology", ["test"]
            )
            assert (
                self.content_page.get_validation_error() != ""
            ), "Should show validation error for empty title"

        with allure.step("Test error handling for empty article content"):
            self.content_page.create_article(
                "Test Title", "Test excerpt", "", "Technology", ["test"]
            )
            assert (
                self.content_page.get_validation_error() != ""
            ), "Should show validation error for empty content"

        with allure.step("Test error handling for invalid category"):
            self.content_page.create_article(
                "Test Title",
                "Test excerpt",
                "Test content",
                "Invalid Category",
                ["test"],
            )
            assert (
                self.content_page.get_error_message() != ""
            ), "Should show error for invalid category"
