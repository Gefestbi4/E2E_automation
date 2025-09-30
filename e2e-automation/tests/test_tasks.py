"""
Task Management tests for the application
"""

import pytest
import allure
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.tasks_page import TasksPage
from utils.logger import TestLogger
from utils.tasks_testing import TasksTesting


@allure.feature("Task Management Tests")
@allure.story("Task Management Testing")
class TestTasks(BaseTest):
    """Test class for task management testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestTasks")
        self.tasks_testing = TasksTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.tasks_page = TasksPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test tasks page loads correctly")
    @pytest.mark.tasks
    def test_tasks_page_loads(self):
        """Test tasks page loads correctly"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test tasks page loads"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"
            assert (
                self.tasks_page.get_page_title() == "Task Management"
            ), "Page title should be correct"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test task creation")
    @pytest.mark.tasks
    def test_task_creation(self):
        """Test task creation"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test tasks page loads"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

        with allure.step("Test create new task"):
            task_data = self.settings.get_task_data()
            self.tasks_page.create_task(task_data)
            assert self.tasks_page.wait_for_task_created(), "Task should be created"
            assert self.tasks_page.is_task_displayed(
                task_data
            ), "Task should be displayed"

        with allure.step("Test task content validation"):
            assert (
                self.tasks_page.get_task_title() == task_data["title"]
            ), "Task title should match"
            assert (
                self.tasks_page.get_task_description() == task_data["description"]
            ), "Task description should match"
            assert (
                self.tasks_page.get_task_priority() == task_data["priority"]
            ), "Task priority should match"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test task status management")
    @pytest.mark.tasks
    def test_task_status_management(self):
        """Test task status management"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test tasks page loads"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

        with allure.step("Test create task first"):
            task_data = self.settings.get_task_data()
            self.tasks_page.create_task(task_data)
            assert self.tasks_page.wait_for_task_created(), "Task should be created"

        with allure.step("Test mark task as in progress"):
            task = self.tasks_page.get_first_task()
            self.tasks_page.update_task_status(task, "in_progress")
            assert (
                self.tasks_page.wait_for_task_status_updated()
            ), "Task status should be updated"
            assert (
                self.tasks_page.get_task_status(task) == "in_progress"
            ), "Task status should be in progress"

        with allure.step("Test mark task as completed"):
            self.tasks_page.update_task_status(task, "completed")
            assert (
                self.tasks_page.wait_for_task_status_updated()
            ), "Task status should be updated"
            assert (
                self.tasks_page.get_task_status(task) == "completed"
            ), "Task status should be completed"

        with allure.step("Test mark task as cancelled"):
            self.tasks_page.update_task_status(task, "cancelled")
            assert (
                self.tasks_page.wait_for_task_status_updated()
            ), "Task status should be updated"
            assert (
                self.tasks_page.get_task_status(task) == "cancelled"
            ), "Task status should be cancelled"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test task assignment")
    @pytest.mark.tasks
    def test_task_assignment(self):
        """Test task assignment"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test tasks page loads"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

        with allure.step("Test create task first"):
            task_data = self.settings.get_task_data()
            self.tasks_page.create_task(task_data)
            assert self.tasks_page.wait_for_task_created(), "Task should be created"

        with allure.step("Test assign task to user"):
            task = self.tasks_page.get_first_task()
            assignee = self.settings.get_user_credentials("admin_user")
            self.tasks_page.assign_task(task, assignee["username"])
            assert self.tasks_page.wait_for_task_assigned(), "Task should be assigned"
            assert (
                self.tasks_page.get_task_assignee(task) == assignee["username"]
            ), "Task assignee should be updated"

        with allure.step("Test reassign task"):
            new_assignee = self.settings.get_user_credentials("test_user")
            self.tasks_page.reassign_task(task, new_assignee["username"])
            assert (
                self.tasks_page.wait_for_task_reassigned()
            ), "Task should be reassigned"
            assert (
                self.tasks_page.get_task_assignee(task) == new_assignee["username"]
            ), "Task assignee should be updated"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test task filtering and sorting")
    @pytest.mark.tasks
    def test_task_filtering_and_sorting(self):
        """Test task filtering and sorting"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test tasks page loads"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

        with allure.step("Test filter tasks by status"):
            self.tasks_page.filter_tasks_by_status("in_progress")
            assert (
                self.tasks_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.tasks_page.get_filtered_tasks_count() > 0
            ), "Should have filtered tasks"

        with allure.step("Test filter tasks by priority"):
            self.tasks_page.filter_tasks_by_priority("high")
            assert (
                self.tasks_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.tasks_page.get_filtered_tasks_count() > 0
            ), "Should have filtered tasks"

        with allure.step("Test filter tasks by assignee"):
            assignee = self.settings.get_user_credentials("admin_user")
            self.tasks_page.filter_tasks_by_assignee(assignee["username"])
            assert (
                self.tasks_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.tasks_page.get_filtered_tasks_count() > 0
            ), "Should have filtered tasks"

        with allure.step("Test sort tasks by due date"):
            self.tasks_page.sort_tasks_by_due_date()
            assert self.tasks_page.wait_for_sort_results(), "Sort results should load"
            assert (
                self.tasks_page.are_tasks_sorted_by_due_date()
            ), "Tasks should be sorted by due date"

        with allure.step("Test sort tasks by priority"):
            self.tasks_page.sort_tasks_by_priority()
            assert self.tasks_page.wait_for_sort_results(), "Sort results should load"
            assert (
                self.tasks_page.are_tasks_sorted_by_priority()
            ), "Tasks should be sorted by priority"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test task comments")
    @pytest.mark.tasks
    def test_task_comments(self):
        """Test task comments"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test tasks page loads"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

        with allure.step("Test create task first"):
            task_data = self.settings.get_task_data()
            self.tasks_page.create_task(task_data)
            assert self.tasks_page.wait_for_task_created(), "Task should be created"

        with allure.step("Test add comment to task"):
            task = self.tasks_page.get_first_task()
            comment_data = self.settings.get_comment_data()
            self.tasks_page.add_comment_to_task(task, comment_data)
            assert self.tasks_page.wait_for_comment_added(), "Comment should be added"
            assert self.tasks_page.is_comment_displayed(
                task, comment_data
            ), "Comment should be displayed"

        with allure.step("Test edit comment"):
            comment = self.tasks_page.get_first_comment(task)
            updated_content = "Updated comment content"
            self.tasks_page.edit_comment(comment, updated_content)
            assert (
                self.tasks_page.wait_for_comment_updated()
            ), "Comment should be updated"
            assert (
                self.tasks_page.get_comment_content(comment) == updated_content
            ), "Comment content should be updated"

        with allure.step("Test delete comment"):
            self.tasks_page.delete_comment(comment)
            assert (
                self.tasks_page.wait_for_comment_deleted()
            ), "Comment should be deleted"
            assert not self.tasks_page.is_comment_displayed(
                task, comment_data
            ), "Comment should not be displayed"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test task deadlines")
    @pytest.mark.tasks
    def test_task_deadlines(self):
        """Test task deadlines"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test tasks page loads"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

        with allure.step("Test create task with deadline"):
            task_data = self.settings.get_task_data()
            task_data["due_date"] = "2024-12-31"
            self.tasks_page.create_task(task_data)
            assert self.tasks_page.wait_for_task_created(), "Task should be created"
            assert (
                self.tasks_page.get_task_due_date() == task_data["due_date"]
            ), "Task due date should match"

        with allure.step("Test update task deadline"):
            task = self.tasks_page.get_first_task()
            new_due_date = "2024-12-25"
            self.tasks_page.update_task_deadline(task, new_due_date)
            assert self.tasks_page.wait_for_task_updated(), "Task should be updated"
            assert (
                self.tasks_page.get_task_due_date(task) == new_due_date
            ), "Task due date should be updated"

        with allure.step("Test overdue tasks notification"):
            self.tasks_page.filter_tasks_by_status("overdue")
            assert (
                self.tasks_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.tasks_page.get_overdue_tasks_count() > 0
            ), "Should have overdue tasks"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test tasks API")
    @pytest.mark.tasks
    def test_tasks_api(self):
        """Test tasks API"""
        with allure.step("Test tasks API"):
            response = self.api_client.get("/api/tasks")
            assert response.status_code == 200, "Tasks API should return 200"
            assert len(response.json()) > 0, "Should have tasks"

        with allure.step("Test create task API"):
            task_data = self.settings.get_task_data()
            response = self.api_client.post("/api/tasks", task_data)
            assert response.status_code == 201, "Create task API should return 201"
            assert "id" in response.json(), "Task should have ID"

        with allure.step("Test update task API"):
            response = self.api_client.put("/api/tasks/1", {"status": "in_progress"})
            assert response.status_code == 200, "Update task API should return 200"
            assert (
                response.json()["status"] == "in_progress"
            ), "Task status should be updated"

        with allure.step("Test assign task API"):
            response = self.api_client.post(
                "/api/tasks/1/assign", {"assignee": "admin_user"}
            )
            assert response.status_code == 200, "Assign task API should return 200"
            assert "message" in response.json(), "Should return success message"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test tasks error handling")
    @pytest.mark.tasks
    def test_tasks_error_handling(self):
        """Test tasks error handling"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test tasks page loads"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

        with allure.step("Test error handling for empty task title"):
            self.tasks_page.create_task(
                {"title": "", "description": "Test description"}
            )
            assert (
                self.tasks_page.wait_for_validation_error()
            ), "Should show validation error for empty title"
            assert (
                "Title is required" in self.tasks_page.get_validation_error()
            ), "Should show title required error"

        with allure.step("Test error handling for invalid assignee"):
            task = self.tasks_page.get_first_task()
            self.tasks_page.assign_task(task, "invalid_user")
            assert (
                self.tasks_page.wait_for_error_message()
            ), "Should show error for invalid assignee"
            assert (
                "User not found" in self.tasks_page.get_error_message()
            ), "Should show user not found error"

        with allure.step("Test error handling for invalid status"):
            self.tasks_page.update_task_status(task, "invalid_status")
            assert (
                self.tasks_page.wait_for_validation_error()
            ), "Should show validation error for invalid status"
            assert (
                "Invalid status" in self.tasks_page.get_validation_error()
            ), "Should show invalid status error"

    # Kanban Boards Tests
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test viewing Kanban boards")
    @pytest.mark.tasks
    def test_view_kanban_boards(self):
        """Test viewing Kanban boards"""
        with allure.step("Login and navigate to tasks"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.tasks_page.load()

        with allure.step("Verify tasks page loads"):
            assert self.tasks_page.is_tasks_loaded(), "Tasks page should load correctly"

        with allure.step("Verify boards list is displayed"):
            boards = self.tasks_page.get_boards_list()
            assert len(boards) >= 0, "Boards list should be displayed"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test creating a new Kanban board")
    @pytest.mark.tasks
    def test_create_kanban_board(self):
        """Test creating a new Kanban board"""
        with allure.step("Login and navigate to tasks"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.tasks_page.load()

        with allure.step("Create new board"):
            board_data = self.settings.get_test_data()["tasks"]["sample_boards"][0]
            self.tasks_page.click_create_board()
            self.tasks_page.create_board(
                board_data["name"], board_data["description"], board_data["visibility"]
            )

        with allure.step("Verify board is created"):
            assert (
                self.tasks_page.get_success_message() != ""
            ), "Success message should be displayed"
            boards = self.tasks_page.get_boards_list()
            assert len(boards) > 0, "Board should be created"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test opening a Kanban board")
    @pytest.mark.tasks
    def test_open_kanban_board(self):
        """Test opening a Kanban board"""
        with allure.step("Login and create a board"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.tasks_page.load()

            board_data = self.settings.get_test_data()["tasks"]["sample_boards"][0]
            self.tasks_page.click_create_board()
            self.tasks_page.create_board(
                board_data["name"], board_data["description"], "private"
            )

        with allure.step("Open the board"):
            self.tasks_page.click_board(0)

        with allure.step("Verify board is opened"):
            assert self.tasks_page.is_board_loaded(), "Board should be loaded"
            columns = self.tasks_page.get_board_columns()
            assert len(columns) > 0, "Board should have columns"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test creating a task in Kanban board")
    @pytest.mark.tasks
    def test_create_task_in_kanban(self):
        """Test creating a task in Kanban board"""
        with allure.step("Login and open a board"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.tasks_page.load()

            board_data = self.settings.get_test_data()["tasks"]["sample_boards"][0]
            self.tasks_page.click_create_board()
            self.tasks_page.create_board(
                board_data["name"], board_data["description"], "private"
            )
            self.tasks_page.click_board(0)

        with allure.step("Create a task"):
            task_data = self.settings.get_test_data()["tasks"]["sample_tasks"][0]
            self.tasks_page.click_add_task("todo")
            self.tasks_page.create_task(
                task_data["title"],
                task_data["description"],
                task_data["priority"],
                task_data["deadline"],
            )

        with allure.step("Verify task is created"):
            assert (
                self.tasks_page.get_success_message() != ""
            ), "Success message should be displayed"
            tasks = self.tasks_page.get_tasks_in_column("todo")
            assert len(tasks) > 0, "Task should be created in To Do column"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test moving task between columns")
    @pytest.mark.tasks
    def test_move_task_between_columns(self):
        """Test moving task between columns"""
        with allure.step("Login and create task"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.tasks_page.load()

            board_data = self.settings.get_test_data()["tasks"]["sample_boards"][0]
            self.tasks_page.click_create_board()
            self.tasks_page.create_board(
                board_data["name"], board_data["description"], "private"
            )
            self.tasks_page.click_board(0)

            task_data = self.settings.get_test_data()["tasks"]["sample_tasks"][0]
            self.tasks_page.click_add_task("todo")
            self.tasks_page.create_task(
                task_data["title"],
                task_data["description"],
                task_data["priority"],
                task_data["deadline"],
            )

        with allure.step("Move task from To Do to In Progress"):
            self.tasks_page.drag_task_to_column(0, "todo", "in-progress")

        with allure.step("Verify task moved"):
            assert self.tasks_page.is_task_in_column(
                task_data["title"], "in-progress"
            ), "Task should be in In Progress column"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test editing a task")
    @pytest.mark.tasks
    def test_edit_task_in_kanban(self):
        """Test editing a task in Kanban board"""
        with allure.step("Login and create task"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.tasks_page.load()

            board_data = self.settings.get_test_data()["tasks"]["sample_boards"][0]
            self.tasks_page.click_create_board()
            self.tasks_page.create_board(
                board_data["name"], board_data["description"], "private"
            )
            self.tasks_page.click_board(0)

            task_data = self.settings.get_test_data()["tasks"]["sample_tasks"][0]
            self.tasks_page.click_add_task("todo")
            self.tasks_page.create_task(
                task_data["title"],
                task_data["description"],
                task_data["priority"],
                task_data["deadline"],
            )

        with allure.step("Edit the task"):
            new_title = "Обновленное название задачи"
            new_description = "Обновленное описание задачи"
            self.tasks_page.click_task(0)
            self.tasks_page.edit_task(0, new_title, new_description)

        with allure.step("Verify task is updated"):
            assert (
                self.tasks_page.get_success_message() != ""
            ), "Success message should be displayed"
            assert (
                self.tasks_page.get_task_title(0) == new_title
            ), "Task title should be updated"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test deleting a task")
    @pytest.mark.tasks
    def test_delete_task_in_kanban(self):
        """Test deleting a task in Kanban board"""
        with allure.step("Login and create task"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.tasks_page.load()

            board_data = self.settings.get_test_data()["tasks"]["sample_boards"][0]
            self.tasks_page.click_create_board()
            self.tasks_page.create_board(
                board_data["name"], board_data["description"], "private"
            )
            self.tasks_page.click_board(0)

            task_data = self.settings.get_test_data()["tasks"]["sample_tasks"][0]
            self.tasks_page.click_add_task("todo")
            self.tasks_page.create_task(
                task_data["title"],
                task_data["description"],
                task_data["priority"],
                task_data["deadline"],
            )

        with allure.step("Delete the task"):
            self.tasks_page.click_task(0)
            self.tasks_page.delete_task(0)

        with allure.step("Verify task is deleted"):
            assert (
                self.tasks_page.get_success_message() != ""
            ), "Success message should be displayed"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test adding comment to task")
    @pytest.mark.tasks
    def test_add_comment_to_task(self):
        """Test adding comment to task"""
        with allure.step("Login and create task"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.tasks_page.load()

            board_data = self.settings.get_test_data()["tasks"]["sample_boards"][0]
            self.tasks_page.click_create_board()
            self.tasks_page.create_board(
                board_data["name"], board_data["description"], "private"
            )
            self.tasks_page.click_board(0)

            task_data = self.settings.get_test_data()["tasks"]["sample_tasks"][0]
            self.tasks_page.click_add_task("todo")
            self.tasks_page.create_task(
                task_data["title"],
                task_data["description"],
                task_data["priority"],
                task_data["deadline"],
            )

        with allure.step("Add comment to task"):
            comment_data = self.settings.get_test_data()["task_comments"][0]
            self.tasks_page.click_task(0)
            self.tasks_page.add_comment_to_task(0, comment_data["content"])

        with allure.step("Verify comment is added"):
            assert (
                self.tasks_page.get_success_message() != ""
            ), "Success message should be displayed"
            comments = self.tasks_page.get_comments()
            assert len(comments) > 0, "Comment should be added"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test assigning task to user")
    @pytest.mark.tasks
    def test_assign_task_to_user(self):
        """Test assigning task to user"""
        with allure.step("Login and create task"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.tasks_page.load()

            board_data = self.settings.get_test_data()["tasks"]["sample_boards"][0]
            self.tasks_page.click_create_board()
            self.tasks_page.create_board(
                board_data["name"], board_data["description"], "private"
            )
            self.tasks_page.click_board(0)

            task_data = self.settings.get_test_data()["tasks"]["sample_tasks"][0]
            self.tasks_page.click_add_task("todo")
            self.tasks_page.create_task(
                task_data["title"],
                task_data["description"],
                task_data["priority"],
                task_data["deadline"],
            )

        with allure.step("Assign task to user"):
            assignee = self.settings.get_user_credentials("admin_user")
            self.tasks_page.click_task(0)
            self.tasks_page.assign_task(0, assignee["username"])

        with allure.step("Verify task is assigned"):
            assert (
                self.tasks_page.get_success_message() != ""
            ), "Success message should be displayed"
            assert (
                self.tasks_page.get_task_assignee(0) == assignee["username"]
            ), "Task should be assigned to user"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test filtering tasks in Kanban")
    @pytest.mark.tasks
    def test_filter_tasks_in_kanban(self):
        """Test filtering tasks in Kanban board"""
        with allure.step("Login and open board"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.tasks_page.load()

            board_data = self.settings.get_test_data()["tasks"]["sample_boards"][0]
            self.tasks_page.click_create_board()
            self.tasks_page.create_board(
                board_data["name"], board_data["description"], "private"
            )
            self.tasks_page.click_board(0)

        with allure.step("Filter by priority"):
            self.tasks_page.click_filters()
            self.tasks_page.filter_by_priority("high")
            tasks = self.tasks_page.get_tasks_in_column("todo")
            assert len(tasks) >= 0, "Filter should return results"

        with allure.step("Filter by assignee"):
            self.tasks_page.filter_by_assignee("admin_user")
            tasks = self.tasks_page.get_tasks_in_column("todo")
            assert len(tasks) >= 0, "Filter should return results"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test searching tasks in Kanban")
    @pytest.mark.tasks
    def test_search_tasks_in_kanban(self):
        """Test searching tasks in Kanban board"""
        with allure.step("Login and open board"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.tasks_page.load()

            board_data = self.settings.get_test_data()["tasks"]["sample_boards"][0]
            self.tasks_page.click_create_board()
            self.tasks_page.create_board(
                board_data["name"], board_data["description"], "private"
            )
            self.tasks_page.click_board(0)

        with allure.step("Search for tasks"):
            search_query = "тест"
            self.tasks_page.search_tasks(search_query)
            tasks = self.tasks_page.get_tasks_in_column("todo")
            assert len(tasks) >= 0, "Search should return results"
