"""
Security tests for the application
"""

import pytest
import allure
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.ecommerce_page import EcommercePage
from pages.social_page import SocialPage
from pages.tasks_page import TasksPage
from pages.content_page import ContentPage
from pages.analytics_page import AnalyticsPage
from utils.logger import TestLogger
from utils.security_testing import SecurityTesting


@allure.feature("Security Tests")
@allure.story("Security Testing")
class TestSecurity(BaseTest):
    """Test class for security testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestSecurity")
        self.security_testing = SecurityTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.ecommerce_page = EcommercePage(self.driver, self)
        self.social_page = SocialPage(self.driver, self)
        self.tasks_page = TasksPage(self.driver, self)
        self.content_page = ContentPage(self.driver, self)
        self.analytics_page = AnalyticsPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test authentication security")
    @pytest.mark.security
    def test_authentication_security(self):
        """Test authentication security"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test password security"):
            # Test password requirements
            assert (
                self.security_testing.test_password_requirements()
            ), "Password requirements should be enforced"

            # Test password hashing
            assert (
                self.security_testing.test_password_hashing()
            ), "Passwords should be properly hashed"

            # Test password strength validation
            assert (
                self.security_testing.test_password_strength_validation()
            ), "Password strength validation should work"

        with allure.step("Test session security"):
            # Test session management
            assert (
                self.security_testing.test_session_management()
            ), "Session management should be secure"

            # Test session timeout
            assert (
                self.security_testing.test_session_timeout()
            ), "Session timeout should be enforced"

            # Test session invalidation
            assert (
                self.security_testing.test_session_invalidation()
            ), "Session invalidation should work"

        with allure.step("Test token security"):
            # Test JWT token security
            assert (
                self.security_testing.test_jwt_token_security()
            ), "JWT tokens should be secure"

            # Test token expiration
            assert (
                self.security_testing.test_token_expiration()
            ), "Token expiration should be enforced"

            # Test token refresh
            assert (
                self.security_testing.test_token_refresh()
            ), "Token refresh should work"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test input validation security")
    @pytest.mark.security
    def test_input_validation_security(self):
        """Test input validation security"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test SQL injection prevention"):
            # Test SQL injection prevention
            assert (
                self.security_testing.test_sql_injection_prevention()
            ), "SQL injection should be prevented"

            # Test parameterized queries
            assert (
                self.security_testing.test_parameterized_queries()
            ), "Parameterized queries should be used"

        with allure.step("Test XSS prevention"):
            # Test XSS prevention
            assert (
                self.security_testing.test_xss_prevention()
            ), "XSS attacks should be prevented"

            # Test input sanitization
            assert (
                self.security_testing.test_input_sanitization()
            ), "Input should be properly sanitized"

        with allure.step("Test CSRF protection"):
            # Test CSRF protection
            assert (
                self.security_testing.test_csrf_protection()
            ), "CSRF attacks should be prevented"

            # Test CSRF tokens
            assert (
                self.security_testing.test_csrf_tokens()
            ), "CSRF tokens should be present"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test authorization security")
    @pytest.mark.security
    def test_authorization_security(self):
        """Test authorization security"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test role-based access control"):
            # Test role-based access control
            assert (
                self.security_testing.test_role_based_access_control()
            ), "Role-based access control should work"

            # Test permission checks
            assert (
                self.security_testing.test_permission_checks()
            ), "Permission checks should be enforced"

        with allure.step("Test resource access control"):
            # Test resource access control
            assert (
                self.security_testing.test_resource_access_control()
            ), "Resource access control should work"

            # Test data isolation
            assert (
                self.security_testing.test_data_isolation()
            ), "Data isolation should be enforced"

        with allure.step("Test API authorization"):
            # Test API authorization
            assert (
                self.security_testing.test_api_authorization()
            ), "API authorization should work"

            # Test endpoint protection
            assert (
                self.security_testing.test_endpoint_protection()
            ), "Endpoints should be properly protected"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test data security")
    @pytest.mark.security
    def test_data_security(self):
        """Test data security"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test data encryption"):
            # Test data encryption at rest
            assert (
                self.security_testing.test_data_encryption_at_rest()
            ), "Data should be encrypted at rest"

            # Test data encryption in transit
            assert (
                self.security_testing.test_data_encryption_in_transit()
            ), "Data should be encrypted in transit"

        with allure.step("Test sensitive data handling"):
            # Test sensitive data handling
            assert (
                self.security_testing.test_sensitive_data_handling()
            ), "Sensitive data should be handled securely"

            # Test data masking
            assert (
                self.security_testing.test_data_masking()
            ), "Sensitive data should be masked"

        with allure.step("Test data backup security"):
            # Test data backup security
            assert (
                self.security_testing.test_data_backup_security()
            ), "Data backups should be secure"

            # Test data recovery security
            assert (
                self.security_testing.test_data_recovery_security()
            ), "Data recovery should be secure"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test network security")
    @pytest.mark.security
    def test_network_security(self):
        """Test network security"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test HTTPS enforcement"):
            # Test HTTPS enforcement
            assert (
                self.security_testing.test_https_enforcement()
            ), "HTTPS should be enforced"

            # Test SSL/TLS configuration
            assert (
                self.security_testing.test_ssl_tls_configuration()
            ), "SSL/TLS should be properly configured"

        with allure.step("Test security headers"):
            # Test security headers
            assert (
                self.security_testing.test_security_headers()
            ), "Security headers should be present"

            # Test CORS configuration
            assert (
                self.security_testing.test_cors_configuration()
            ), "CORS should be properly configured"

        with allure.step("Test rate limiting"):
            # Test rate limiting
            assert (
                self.security_testing.test_rate_limiting()
            ), "Rate limiting should be enforced"

            # Test DDoS protection
            assert (
                self.security_testing.test_ddos_protection()
            ), "DDoS protection should be in place"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test vulnerability scanning")
    @pytest.mark.security
    def test_vulnerability_scanning(self):
        """Test vulnerability scanning"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test OWASP Top 10 vulnerabilities"):
            # Test OWASP Top 10 vulnerabilities
            owasp_results = self.security_testing.test_owasp_top_10()
            assert (
                owasp_results["vulnerabilities"] == 0
            ), f"No OWASP Top 10 vulnerabilities should be found, actual: {owasp_results['vulnerabilities']}"

        with allure.step("Test common vulnerabilities"):
            # Test common vulnerabilities
            common_vulns = self.security_testing.test_common_vulnerabilities()
            assert (
                len(common_vulns) == 0
            ), f"No common vulnerabilities should be found, actual: {common_vulns}"

        with allure.step("Test security misconfigurations"):
            # Test security misconfigurations
            misconfigs = self.security_testing.test_security_misconfigurations()
            assert (
                len(misconfigs) == 0
            ), f"No security misconfigurations should be found, actual: {misconfigs}"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test security monitoring")
    @pytest.mark.security
    def test_security_monitoring(self):
        """Test security monitoring"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test security event logging"):
            # Test security event logging
            assert (
                self.security_testing.test_security_event_logging()
            ), "Security events should be logged"

            # Test log integrity
            assert (
                self.security_testing.test_log_integrity()
            ), "Logs should be tamper-proof"

        with allure.step("Test security alerts"):
            # Test security alerts
            assert (
                self.security_testing.test_security_alerts()
            ), "Security alerts should be configured"

            # Test incident response
            assert (
                self.security_testing.test_incident_response()
            ), "Incident response should be in place"

        with allure.step("Test security metrics"):
            # Test security metrics
            metrics = self.security_testing.collect_security_metrics()
            assert (
                "threats_blocked" in metrics
            ), "Threats blocked metric should be collected"
            assert (
                "vulnerabilities_found" in metrics
            ), "Vulnerabilities found metric should be collected"
            assert (
                "security_events" in metrics
            ), "Security events metric should be collected"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test security compliance")
    @pytest.mark.security
    def test_security_compliance(self):
        """Test security compliance"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test GDPR compliance"):
            # Test GDPR compliance
            gdpr_results = self.security_testing.test_gdpr_compliance()
            assert gdpr_results["compliant"], "Should be GDPR compliant"
            assert (
                gdpr_results["score"] >= 90
            ), f"GDPR compliance score should be at least 90, actual: {gdpr_results['score']}"

        with allure.step("Test PCI DSS compliance"):
            # Test PCI DSS compliance
            pci_results = self.security_testing.test_pci_dss_compliance()
            assert pci_results["compliant"], "Should be PCI DSS compliant"
            assert (
                pci_results["score"] >= 90
            ), f"PCI DSS compliance score should be at least 90, actual: {pci_results['score']}"

        with allure.step("Test ISO 27001 compliance"):
            # Test ISO 27001 compliance
            iso_results = self.security_testing.test_iso_27001_compliance()
            assert iso_results["compliant"], "Should be ISO 27001 compliant"
            assert (
                iso_results["score"] >= 90
            ), f"ISO 27001 compliance score should be at least 90, actual: {iso_results['score']}"
