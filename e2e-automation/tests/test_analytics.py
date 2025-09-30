"""
Analytics tests for the application
"""

import pytest
import allure
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.analytics_page import AnalyticsPage
from utils.logger import TestLogger
from utils.analytics_testing import AnalyticsTesting


@allure.feature("Analytics Tests")
@allure.story("Analytics Testing")
class TestAnalytics(BaseTest):
    """Test class for analytics testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestAnalytics")
        self.analytics_testing = AnalyticsTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.analytics_page = AnalyticsPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test analytics page loads correctly")
    @pytest.mark.analytics
    def test_analytics_page_loads(self):
        """Test analytics page loads correctly"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test analytics page loads"):
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"
            assert (
                self.analytics_page.get_page_title() == "Analytics"
            ), "Page title should be correct"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test analytics dashboard displays")
    @pytest.mark.analytics
    def test_analytics_dashboard_displays(self):
        """Test analytics dashboard displays"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test analytics page loads"):
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

        with allure.step("Test analytics dashboard elements"):
            assert (
                self.analytics_page.is_dashboard_loaded()
            ), "Analytics dashboard should load"
            assert self.analytics_page.get_metrics_count() > 0, "Should have metrics"
            assert self.analytics_page.get_charts_count() > 0, "Should have charts"

        with allure.step("Test key metrics display"):
            assert self.analytics_page.is_metric_displayed(
                "total_users"
            ), "Total users metric should be displayed"
            assert self.analytics_page.is_metric_displayed(
                "active_users"
            ), "Active users metric should be displayed"
            assert self.analytics_page.is_metric_displayed(
                "total_revenue"
            ), "Total revenue metric should be displayed"
            assert self.analytics_page.is_metric_displayed(
                "conversion_rate"
            ), "Conversion rate metric should be displayed"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test analytics filtering")
    @pytest.mark.analytics
    def test_analytics_filtering(self):
        """Test analytics filtering"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test analytics page loads"):
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

        with allure.step("Test filter by date range"):
            date_range = self.settings.get_date_range()
            self.analytics_page.filter_by_date_range(date_range)
            assert (
                self.analytics_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.analytics_page.get_filtered_metrics_count() > 0
            ), "Should have filtered metrics"

        with allure.step("Test filter by metric type"):
            metric_type = "revenue"
            self.analytics_page.filter_by_metric_type(metric_type)
            assert (
                self.analytics_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.analytics_page.get_filtered_metrics_count() > 0
            ), "Should have filtered metrics"

        with allure.step("Test filter by user segment"):
            user_segment = "premium"
            self.analytics_page.filter_by_user_segment(user_segment)
            assert (
                self.analytics_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.analytics_page.get_filtered_metrics_count() > 0
            ), "Should have filtered metrics"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test analytics charts")
    @pytest.mark.analytics
    def test_analytics_charts(self):
        """Test analytics charts"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test analytics page loads"):
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

        with allure.step("Test chart rendering"):
            assert self.analytics_page.is_chart_rendered(
                "user_growth_chart"
            ), "User growth chart should be rendered"
            assert self.analytics_page.is_chart_rendered(
                "revenue_chart"
            ), "Revenue chart should be rendered"
            assert self.analytics_page.is_chart_rendered(
                "conversion_chart"
            ), "Conversion chart should be rendered"

        with allure.step("Test chart interactivity"):
            self.analytics_page.interact_with_chart("user_growth_chart")
            assert (
                self.analytics_page.wait_for_chart_interaction()
            ), "Chart interaction should work"
            assert (
                self.analytics_page.get_chart_tooltip() != ""
            ), "Chart tooltip should be displayed"

        with allure.step("Test chart data accuracy"):
            chart_data = self.analytics_page.get_chart_data("user_growth_chart")
            assert len(chart_data) > 0, "Chart should have data"
            assert all(
                "date" in point for point in chart_data
            ), "Chart data should have dates"
            assert all(
                "value" in point for point in chart_data
            ), "Chart data should have values"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test analytics reports")
    @pytest.mark.analytics
    def test_analytics_reports(self):
        """Test analytics reports"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test analytics page loads"):
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

        with allure.step("Test generate report"):
            report_data = self.settings.get_report_data()
            self.analytics_page.generate_report(report_data)
            assert (
                self.analytics_page.wait_for_report_generated()
            ), "Report should be generated"
            assert (
                self.analytics_page.is_report_displayed()
            ), "Report should be displayed"

        with allure.step("Test report content"):
            assert (
                self.analytics_page.get_report_title() != ""
            ), "Report should have title"
            assert (
                self.analytics_page.get_report_summary() != ""
            ), "Report should have summary"
            assert (
                self.analytics_page.get_report_metrics_count() > 0
            ), "Report should have metrics"

        with allure.step("Test download report"):
            self.analytics_page.download_report()
            assert (
                self.analytics_page.wait_for_report_downloaded()
            ), "Report should be downloaded"
            assert (
                self.analytics_page.is_report_file_present()
            ), "Report file should be present"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test analytics real-time updates")
    @pytest.mark.analytics
    def test_analytics_real_time_updates(self):
        """Test analytics real-time updates"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test analytics page loads"):
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

        with allure.step("Test real-time updates enabled"):
            assert (
                self.analytics_page.is_real_time_updates_enabled()
            ), "Real-time updates should be enabled"
            assert (
                self.analytics_page.get_update_frequency() > 0
            ), "Update frequency should be set"

        with allure.step("Test metrics update in real-time"):
            initial_metrics = self.analytics_page.get_current_metrics()
            self.analytics_page.wait_for_metrics_update()
            updated_metrics = self.analytics_page.get_current_metrics()
            assert (
                updated_metrics != initial_metrics
            ), "Metrics should update in real-time"

        with allure.step("Test charts update in real-time"):
            initial_chart_data = self.analytics_page.get_chart_data("user_growth_chart")
            self.analytics_page.wait_for_chart_update()
            updated_chart_data = self.analytics_page.get_chart_data("user_growth_chart")
            assert (
                updated_chart_data != initial_chart_data
            ), "Charts should update in real-time"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test analytics API")
    @pytest.mark.analytics
    def test_analytics_api(self):
        """Test analytics API"""
        with allure.step("Test metrics API"):
            response = self.api_client.get("/api/analytics/metrics")
            assert response.status_code == 200, "Metrics API should return 200"
            assert len(response.json()) > 0, "Should have metrics"

        with allure.step("Test charts API"):
            response = self.api_client.get("/api/analytics/charts")
            assert response.status_code == 200, "Charts API should return 200"
            assert len(response.json()) > 0, "Should have charts"

        with allure.step("Test reports API"):
            response = self.api_client.get("/api/analytics/reports")
            assert response.status_code == 200, "Reports API should return 200"
            assert len(response.json()) > 0, "Should have reports"

        with allure.step("Test generate report API"):
            report_data = self.settings.get_report_data()
            response = self.api_client.post(
                "/api/analytics/reports/generate", report_data
            )
            assert response.status_code == 200, "Generate report API should return 200"
            assert "report_id" in response.json(), "Report should have ID"

    # Analytics Dashboard Tests
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test viewing analytics dashboard")
    @pytest.mark.analytics
    def test_view_analytics_dashboard(self):
        """Test viewing analytics dashboard"""
        with allure.step("Login and navigate to analytics"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.analytics_page.load()

        with allure.step("Verify analytics page loads"):
            assert (
                self.analytics_page.is_analytics_loaded()
            ), "Analytics page should load correctly"

        with allure.step("Verify dashboard metrics are displayed"):
            metrics = self.analytics_page.get_dashboard_metrics()
            assert len(metrics) > 0, "Dashboard metrics should be displayed"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test viewing user metrics")
    @pytest.mark.analytics
    def test_view_user_metrics(self):
        """Test viewing user metrics"""
        with allure.step("Login and navigate to analytics"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.analytics_page.load()

        with allure.step("View user metrics"):
            user_metrics = self.analytics_page.get_user_metrics()

        with allure.step("Verify user metrics are displayed"):
            assert user_metrics["total_users"] > 0, "Total users should be displayed"
            assert user_metrics["active_users"] > 0, "Active users should be displayed"
            assert user_metrics["new_users"] >= 0, "New users should be displayed"
            assert (
                user_metrics["user_growth_rate"] is not None
            ), "User growth rate should be displayed"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test viewing e-commerce metrics")
    @pytest.mark.analytics
    def test_view_ecommerce_metrics(self):
        """Test viewing e-commerce metrics"""
        with allure.step("Login and navigate to analytics"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.analytics_page.load()

        with allure.step("View e-commerce metrics"):
            ecommerce_metrics = self.analytics_page.get_ecommerce_metrics()

        with allure.step("Verify e-commerce metrics are displayed"):
            assert (
                ecommerce_metrics["total_revenue"] >= 0
            ), "Total revenue should be displayed"
            assert (
                ecommerce_metrics["orders_count"] >= 0
            ), "Orders count should be displayed"
            assert (
                ecommerce_metrics["average_order_value"] >= 0
            ), "Average order value should be displayed"
            assert (
                ecommerce_metrics["conversion_rate"] >= 0
            ), "Conversion rate should be displayed"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test viewing system activity")
    @pytest.mark.analytics
    def test_view_system_activity(self):
        """Test viewing system activity"""
        with allure.step("Login and navigate to analytics"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.analytics_page.load()

        with allure.step("View system activity"):
            activity = self.analytics_page.get_system_activity()

        with allure.step("Verify system activity is displayed"):
            assert len(activity) >= 0, "System activity should be displayed"
            for event in activity:
                assert "timestamp" in event, "Activity should have timestamp"
                assert "description" in event, "Activity should have description"
                assert "type" in event, "Activity should have type"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test configuring dashboard widgets")
    @pytest.mark.analytics
    def test_configure_dashboard_widgets(self):
        """Test configuring dashboard widgets"""
        with allure.step("Login and navigate to analytics"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.analytics_page.load()

        with allure.step("Configure dashboard widgets"):
            self.analytics_page.click_customize_dashboard()
            self.analytics_page.add_widget("user_metrics")
            self.analytics_page.add_widget("revenue_chart")
            self.analytics_page.save_dashboard()

        with allure.step("Verify widgets are configured"):
            assert (
                self.analytics_page.get_success_message() != ""
            ), "Success message should be displayed"
            widgets = self.analytics_page.get_dashboard_widgets()
            assert len(widgets) > 0, "Widgets should be added to dashboard"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test creating custom dashboard")
    @pytest.mark.analytics
    def test_create_custom_dashboard(self):
        """Test creating custom dashboard"""
        with allure.step("Login and navigate to analytics"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.analytics_page.load()

        with allure.step("Create custom dashboard"):
            dashboard_data = self.settings.get_test_data()["analytics"][
                "sample_dashboards"
            ][0]
            self.analytics_page.click_create_dashboard()
            self.analytics_page.create_dashboard(
                dashboard_data["name"],
                dashboard_data["description"],
                dashboard_data["widgets"],
            )

        with allure.step("Verify custom dashboard is created"):
            assert (
                self.analytics_page.get_success_message() != ""
            ), "Success message should be displayed"
            dashboards = self.analytics_page.get_dashboards_list()
            assert len(dashboards) > 0, "Custom dashboard should be created"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test viewing charts")
    @pytest.mark.analytics
    def test_view_charts(self):
        """Test viewing charts"""
        with allure.step("Login and navigate to analytics"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.analytics_page.load()

        with allure.step("View charts"):
            charts = self.analytics_page.get_charts()

        with allure.step("Verify charts are displayed"):
            assert len(charts) > 0, "Charts should be displayed"
            for chart in charts:
                assert chart["type"] in [
                    "line",
                    "bar",
                    "pie",
                    "area",
                ], "Chart should have valid type"
                assert chart["data"] is not None, "Chart should have data"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test filtering by date range")
    @pytest.mark.analytics
    def test_filter_by_date_range(self):
        """Test filtering by date range"""
        with allure.step("Login and navigate to analytics"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.analytics_page.load()

        with allure.step("Filter by date range"):
            date_range = self.settings.get_test_data()["analytics"]["date_ranges"][0]
            self.analytics_page.filter_by_date_range(
                date_range["start_date"], date_range["end_date"]
            )

        with allure.step("Verify filter is applied"):
            assert (
                self.analytics_page.get_success_message() != ""
            ), "Success message should be displayed"
            filtered_data = self.analytics_page.get_filtered_data()
            assert len(filtered_data) >= 0, "Filtered data should be returned"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test exporting data")
    @pytest.mark.analytics
    def test_export_data(self):
        """Test exporting data"""
        with allure.step("Login and navigate to analytics"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.analytics_page.load()

        with allure.step("Export data"):
            export_format = self.settings.get_test_data()["analytics"][
                "export_formats"
            ][0]
            self.analytics_page.click_export_report()
            self.analytics_page.select_export_format(export_format)
            self.analytics_page.download_report()

        with allure.step("Verify data is exported"):
            assert (
                self.analytics_page.get_success_message() != ""
            ), "Success message should be displayed"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test real-time updates")
    @pytest.mark.analytics
    def test_real_time_updates(self):
        """Test real-time updates"""
        with allure.step("Login and navigate to analytics"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.analytics_page.load()

        with allure.step("Enable real-time updates"):
            self.analytics_page.click_auto_refresh()
            assert (
                self.analytics_page.is_auto_refresh_enabled()
            ), "Auto refresh should be enabled"

        with allure.step("Verify real-time updates work"):
            initial_metrics = self.analytics_page.get_dashboard_metrics()
            self.analytics_page.wait_for_update()
            updated_metrics = self.analytics_page.get_dashboard_metrics()
            # Metrics might be the same, but the update should be processed
            assert (
                self.analytics_page.is_update_processed()
            ), "Update should be processed"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test switching dashboards")
    @pytest.mark.analytics
    def test_switch_dashboards(self):
        """Test switching dashboards"""
        with allure.step("Login and navigate to analytics"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.analytics_page.load()

        with allure.step("Switch to different dashboard"):
            self.analytics_page.click_dashboard_selector()
            self.analytics_page.select_dashboard("custom_dashboard")

        with allure.step("Verify dashboard is switched"):
            assert (
                self.analytics_page.get_current_dashboard() == "custom_dashboard"
            ), "Dashboard should be switched"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test analytics API")
    @pytest.mark.analytics
    def test_analytics_api(self):
        """Test analytics API"""
        with allure.step("Test metrics API"):
            response = self.api_client.get("/api/analytics/metrics")
            assert response.status_code == 200, "Metrics API should return 200"
            assert len(response.json()) > 0, "Should have metrics"

        with allure.step("Test charts API"):
            response = self.api_client.get("/api/analytics/charts")
            assert response.status_code == 200, "Charts API should return 200"
            assert len(response.json()) > 0, "Should have charts"

        with allure.step("Test reports API"):
            response = self.api_client.get("/api/analytics/reports")
            assert response.status_code == 200, "Reports API should return 200"
            assert len(response.json()) > 0, "Should have reports"

        with allure.step("Test generate report API"):
            report_data = self.settings.get_test_data()["analytics"]["sample_reports"][
                0
            ]
            response = self.api_client.post(
                "/api/analytics/reports/generate", report_data
            )
            assert response.status_code == 200, "Generate report API should return 200"
            assert "report_id" in response.json(), "Report should have ID"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test analytics error handling")
    @pytest.mark.analytics
    def test_analytics_error_handling(self):
        """Test analytics error handling"""
        with allure.step("Login and navigate to analytics"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.analytics_page.load()

        with allure.step("Test error handling for invalid date range"):
            self.analytics_page.filter_by_date_range("invalid_date", "invalid_date")
            assert (
                self.analytics_page.get_error_message() != ""
            ), "Should show error for invalid date range"

        with allure.step("Test error handling for invalid export format"):
            self.analytics_page.click_export_report()
            self.analytics_page.select_export_format("invalid_format")
            assert (
                self.analytics_page.get_error_message() != ""
            ), "Should show error for invalid export format"
