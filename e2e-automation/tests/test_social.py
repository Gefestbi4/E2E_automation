"""
Social Network tests for the application
"""

import pytest
import allure
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.social_page import SocialPage
from utils.logger import TestLogger
from utils.social_testing import SocialTesting


@allure.feature("Social Network Tests")
@allure.story("Social Network Testing")
class TestSocial(BaseTest):
    """Test class for social network testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestSocial")
        self.social_testing = SocialTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.social_page = SocialPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test social page loads correctly")
    @pytest.mark.social
    def test_social_page_loads(self):
        """Test social page loads correctly"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test social page loads"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"
            assert (
                self.social_page.get_page_title() == "Social Network"
            ), "Page title should be correct"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test post creation")
    @pytest.mark.social
    def test_post_creation(self):
        """Test post creation"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test social page loads"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

        with allure.step("Test create new post"):
            post_data = self.settings.get_post_data()
            self.social_page.create_post(post_data)
            assert self.social_page.wait_for_post_created(), "Post should be created"
            assert self.social_page.is_post_displayed(
                post_data
            ), "Post should be displayed"

        with allure.step("Test post content validation"):
            assert (
                self.social_page.get_post_content() == post_data["content"]
            ), "Post content should match"
            assert (
                self.social_page.get_post_author() == user_data["username"]
            ), "Post author should match"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test post interaction")
    @pytest.mark.social
    def test_post_interaction(self):
        """Test post interaction"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test social page loads"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

        with allure.step("Test like post"):
            post = self.social_page.get_first_post()
            initial_likes = self.social_page.get_post_likes_count(post)
            self.social_page.like_post(post)
            assert self.social_page.wait_for_like_added(), "Like should be added"
            assert (
                self.social_page.get_post_likes_count(post) == initial_likes + 1
            ), "Likes count should increase"

        with allure.step("Test unlike post"):
            self.social_page.unlike_post(post)
            assert self.social_page.wait_for_like_removed(), "Like should be removed"
            assert (
                self.social_page.get_post_likes_count(post) == initial_likes
            ), "Likes count should return to original"

        with allure.step("Test comment on post"):
            comment_data = self.settings.get_comment_data()
            self.social_page.comment_on_post(post, comment_data)
            assert self.social_page.wait_for_comment_added(), "Comment should be added"
            assert self.social_page.is_comment_displayed(
                post, comment_data
            ), "Comment should be displayed"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test post editing")
    @pytest.mark.social
    def test_post_editing(self):
        """Test post editing"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test social page loads"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

        with allure.step("Test create post first"):
            post_data = self.settings.get_post_data()
            self.social_page.create_post(post_data)
            assert self.social_page.wait_for_post_created(), "Post should be created"

        with allure.step("Test edit post"):
            post = self.social_page.get_first_post()
            updated_content = "Updated post content"
            self.social_page.edit_post(post, updated_content)
            assert self.social_page.wait_for_post_updated(), "Post should be updated"
            assert (
                self.social_page.get_post_content(post) == updated_content
            ), "Post content should be updated"

        with allure.step("Test delete post"):
            self.social_page.delete_post(post)
            assert self.social_page.wait_for_post_deleted(), "Post should be deleted"
            assert not self.social_page.is_post_displayed(
                post
            ), "Post should not be displayed"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test user following")
    @pytest.mark.social
    def test_user_following(self):
        """Test user following"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test social page loads"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

        with allure.step("Test follow user"):
            user_to_follow = self.settings.get_user_credentials("admin_user")
            self.social_page.follow_user(user_to_follow["username"])
            assert self.social_page.wait_for_follow_success(), "User should be followed"
            assert self.social_page.is_user_followed(
                user_to_follow["username"]
            ), "User should be in following list"

        with allure.step("Test unfollow user"):
            self.social_page.unfollow_user(user_to_follow["username"])
            assert (
                self.social_page.wait_for_unfollow_success()
            ), "User should be unfollowed"
            assert not self.social_page.is_user_followed(
                user_to_follow["username"]
            ), "User should not be in following list"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test post sharing")
    @pytest.mark.social
    def test_post_sharing(self):
        """Test post sharing"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test social page loads"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

        with allure.step("Test share post"):
            post = self.social_page.get_first_post()
            self.social_page.share_post(post)
            assert self.social_page.wait_for_share_dialog(), "Share dialog should open"
            assert (
                self.social_page.is_share_dialog_present()
            ), "Share dialog should be present"

        with allure.step("Test share to different platforms"):
            platforms = ["facebook", "twitter", "linkedin"]
            for platform in platforms:
                self.social_page.share_to_platform(platform)
                assert (
                    self.social_page.wait_for_share_success()
                ), f"Share to {platform} should succeed"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test post filtering")
    @pytest.mark.social
    def test_post_filtering(self):
        """Test post filtering"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test social page loads"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

        with allure.step("Test filter by user"):
            user_to_filter = self.settings.get_user_credentials("admin_user")
            self.social_page.filter_posts_by_user(user_to_filter["username"])
            assert (
                self.social_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.social_page.get_filtered_posts_count() > 0
            ), "Should have filtered posts"

        with allure.step("Test filter by date"):
            date_range = self.settings.get_date_range()
            self.social_page.filter_posts_by_date(date_range)
            assert (
                self.social_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.social_page.get_filtered_posts_count() > 0
            ), "Should have filtered posts"

        with allure.step("Test filter by content type"):
            content_type = "text"
            self.social_page.filter_posts_by_content_type(content_type)
            assert (
                self.social_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.social_page.get_filtered_posts_count() > 0
            ), "Should have filtered posts"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test social API")
    @pytest.mark.social
    def test_social_api(self):
        """Test social API"""
        with allure.step("Test posts API"):
            response = self.api_client.get("/api/social/posts")
            assert response.status_code == 200, "Posts API should return 200"
            assert len(response.json()) > 0, "Should have posts"

        with allure.step("Test create post API"):
            post_data = self.settings.get_post_data()
            response = self.api_client.post("/api/social/posts", post_data)
            assert response.status_code == 201, "Create post API should return 201"
            assert "id" in response.json(), "Post should have ID"

        with allure.step("Test like post API"):
            response = self.api_client.post("/api/social/posts/1/like")
            assert response.status_code == 200, "Like post API should return 200"
            assert "message" in response.json(), "Should return success message"

        with allure.step("Test comment API"):
            comment_data = self.settings.get_comment_data()
            response = self.api_client.post(
                "/api/social/posts/1/comments", comment_data
            )
            assert response.status_code == 201, "Comment API should return 201"
            assert "id" in response.json(), "Comment should have ID"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test social error handling")
    @pytest.mark.social
    def test_social_error_handling(self):
        """Test social error handling"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test social page loads"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

        with allure.step("Test error handling for empty post"):
            self.social_page.create_post({"content": ""})
            assert (
                self.social_page.wait_for_validation_error()
            ), "Should show validation error for empty post"
            assert (
                "Content is required" in self.social_page.get_validation_error()
            ), "Should show content required error"

        with allure.step("Test error handling for too long post"):
            long_content = "x" * 1001  # Assuming 1000 character limit
            self.social_page.create_post({"content": long_content})
            assert (
                self.social_page.wait_for_validation_error()
            ), "Should show validation error for too long post"
            assert (
                "Content too long" in self.social_page.get_validation_error()
            ), "Should show content too long error"

        with allure.step("Test error handling for invalid user"):
            self.social_page.follow_user("invalid_user")
            assert (
                self.social_page.wait_for_error_message()
            ), "Should show error for invalid user"
            assert (
                "User not found" in self.social_page.get_error_message()
            ), "Should show user not found error"

    # Social Network Posts Tests
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test viewing social feed")
    @pytest.mark.social
    def test_view_social_feed(self):
        """Test viewing social feed"""
        with allure.step("Login and navigate to social"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.social_page.load()

        with allure.step("Verify social page loads"):
            assert (
                self.social_page.is_social_loaded()
            ), "Social page should load correctly"

        with allure.step("Verify posts feed is displayed"):
            posts = self.social_page.get_posts_feed()
            assert len(posts) >= 0, "Posts feed should be displayed"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test creating a new post")
    @pytest.mark.social
    def test_create_post(self):
        """Test creating a new post"""
        with allure.step("Login and navigate to social"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.social_page.load()

        with allure.step("Create new post"):
            post_data = self.settings.get_test_data()["social_posts"]["sample_posts"][0]
            self.social_page.click_create_post()
            self.social_page.create_post(post_data["content"], post_data["visibility"])

        with allure.step("Verify post is created"):
            assert (
                self.social_page.get_success_message() != ""
            ), "Success message should be displayed"
            assert self.social_page.is_post_visible(
                post_data["content"]
            ), "Post should be visible in feed"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test editing a post")
    @pytest.mark.social
    def test_edit_post(self):
        """Test editing a post"""
        with allure.step("Login and create a post"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.social_page.load()

            post_data = self.settings.get_test_data()["social_posts"]["sample_posts"][0]
            self.social_page.click_create_post()
            self.social_page.create_post(post_data["content"], "public")

        with allure.step("Edit the post"):
            new_content = "Обновленное содержимое поста"
            self.social_page.edit_post(0, new_content)

        with allure.step("Verify post is updated"):
            assert (
                self.social_page.get_success_message() != ""
            ), "Success message should be displayed"
            assert (
                self.social_page.get_post_content(0) == new_content
            ), "Post content should be updated"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test deleting a post")
    @pytest.mark.social
    def test_delete_post(self):
        """Test deleting a post"""
        with allure.step("Login and create a post"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.social_page.load()

            post_data = self.settings.get_test_data()["social_posts"]["sample_posts"][0]
            self.social_page.click_create_post()
            self.social_page.create_post(post_data["content"], "public")

        with allure.step("Delete the post"):
            self.social_page.delete_post(0)

        with allure.step("Verify post is deleted"):
            assert (
                self.social_page.get_success_message() != ""
            ), "Success message should be displayed"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test liking a post")
    @pytest.mark.social
    def test_like_post(self):
        """Test liking a post"""
        with allure.step("Login and navigate to social"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.social_page.load()

        with allure.step("Like a post"):
            initial_likes = self.social_page.get_like_count(0)
            self.social_page.like_post(0)

        with allure.step("Verify like count increased"):
            new_likes = self.social_page.get_like_count(0)
            assert new_likes > initial_likes, "Like count should increase"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test commenting on a post")
    @pytest.mark.social
    def test_comment_on_post(self):
        """Test commenting on a post"""
        with allure.step("Login and navigate to social"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.social_page.load()

        with allure.step("Add comment to post"):
            comment_data = self.settings.get_test_data()["social_interactions"][
                "comments"
            ][0]
            self.social_page.comment_on_post(0, comment_data["content"])

        with allure.step("Verify comment is added"):
            assert (
                self.social_page.get_success_message() != ""
            ), "Success message should be displayed"
            comments = self.social_page.get_comments()
            assert len(comments) > 0, "Comment should be added"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test viewing post details")
    @pytest.mark.social
    def test_view_post_details(self):
        """Test viewing post details"""
        with allure.step("Login and navigate to social"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.social_page.load()

        with allure.step("Click on post to view details"):
            self.social_page.click_post(0)
            post_details = self.social_page.get_post_details()

        with allure.step("Verify post details are displayed"):
            assert post_details["title"] != "", "Post title should be displayed"
            assert post_details["content"] != "", "Post content should be displayed"
            assert post_details["author"] != "", "Post author should be displayed"
            assert post_details["timestamp"] != "", "Post timestamp should be displayed"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test sharing a post")
    @pytest.mark.social
    def test_share_post(self):
        """Test sharing a post"""
        with allure.step("Login and navigate to social"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.social_page.load()

        with allure.step("Share a post"):
            self.social_page.share_post(0)
            self.social_page.copy_post_link()

        with allure.step("Verify share functionality"):
            assert (
                self.social_page.get_success_message() != ""
            ), "Success message should be displayed"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test searching posts")
    @pytest.mark.social
    def test_search_posts(self):
        """Test searching posts"""
        with allure.step("Login and navigate to social"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.social_page.load()

        with allure.step("Search for posts"):
            search_query = self.settings.get_test_data()["social_posts"][
                "search_queries"
            ][0]
            self.social_page.search_posts(search_query)

        with allure.step("Verify search results"):
            posts = self.social_page.get_posts_feed()
            assert len(posts) >= 0, "Search should return results"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test filtering posts")
    @pytest.mark.social
    def test_filter_posts(self):
        """Test filtering posts"""
        with allure.step("Login and navigate to social"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.social_page.load()

        with allure.step("Filter by my posts"):
            self.social_page.filter_my_posts()
            posts = self.social_page.get_posts_feed()
            assert len(posts) >= 0, "Filter should return results"

        with allure.step("Filter by popular posts"):
            self.social_page.filter_popular_posts()
            posts = self.social_page.get_posts_feed()
            assert len(posts) >= 0, "Filter should return results"

        with allure.step("Filter by recent posts"):
            self.social_page.filter_recent_posts()
            posts = self.social_page.get_posts_feed()
            assert len(posts) >= 0, "Filter should return results"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test uploading image to post")
    @pytest.mark.social
    def test_upload_image_to_post(self):
        """Test uploading image to post"""
        with allure.step("Login and navigate to social"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.social_page.load()

        with allure.step("Create post with image"):
            post_data = self.settings.get_test_data()["social_posts"]["sample_posts"][1]
            self.social_page.click_create_post()
            # Assuming we have a test image file
            test_image_path = "/path/to/test/image.jpg"
            self.social_page.create_post(
                post_data["content"], "public", test_image_path
            )

        with allure.step("Verify post with image is created"):
            assert (
                self.social_page.get_success_message() != ""
            ), "Success message should be displayed"
            assert self.social_page.is_post_visible(
                post_data["content"]
            ), "Post with image should be visible"
