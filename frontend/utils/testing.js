// Comprehensive Testing Suite
class TestingSuite {
    constructor() {
        this.testResults = [];
        this.isRunning = false;
        this.currentTest = null;
    }

    async runAllTests() {
        if (this.isRunning) {
            console.warn('Testing suite is already running');
            return;
        }

        this.isRunning = true;
        this.testResults = [];

        console.log('🧪 Starting comprehensive testing suite...');

        try {
            await this.runAuthenticationTests();
            await this.runAPIEndpointTests();
            await this.runFormValidationTests();
            await this.runModuleTests();
            await this.runUIUXTests();
            await this.runErrorHandlingTests();
            await this.runPerformanceTests();

            this.generateTestReport();
        } catch (error) {
            console.error('Testing suite failed:', error);
            if (window.ErrorHandler) {
                window.ErrorHandler.logError(error, { type: 'TESTING_SUITE_FAILED' });
            }
        } finally {
            this.isRunning = false;
        }
    }

    async runAuthenticationTests() {
        console.log('🔐 Running authentication tests...');

        const tests = [
            {
                name: 'Login form validation',
                test: () => this.testLoginFormValidation()
            },
            {
                name: 'Registration form validation',
                test: () => this.testRegistrationFormValidation()
            },
            {
                name: 'API authentication endpoints',
                test: () => this.testAuthEndpoints()
            },
            {
                name: 'Token refresh mechanism',
                test: () => this.testTokenRefresh()
            }
        ];

        for (const test of tests) {
            await this.runTest(test.name, test.test);
        }
    }

    async runAPIEndpointTests() {
        console.log('🌐 Running API endpoint tests...');

        const tests = [
            {
                name: 'API service initialization',
                test: () => this.testAPIServiceInit()
            },
            {
                name: 'Retry logic functionality',
                test: () => this.testRetryLogic()
            },
            {
                name: 'Error handling in API calls',
                test: () => this.testAPIErrorHandling()
            }
        ];

        for (const test of tests) {
            await this.runTest(test.name, test.test);
        }
    }

    async runFormValidationTests() {
        console.log('📝 Running form validation tests...');

        const tests = [
            {
                name: 'Email validation',
                test: () => this.testEmailValidation()
            },
            {
                name: 'Password validation',
                test: () => this.testPasswordValidation()
            },
            {
                name: 'Real-time validation',
                test: () => this.testRealTimeValidation()
            }
        ];

        for (const test of tests) {
            await this.runTest(test.name, test.test);
        }
    }

    async runModuleTests() {
        console.log('📦 Running module tests...');

        const tests = [
            {
                name: 'Analytics module',
                test: () => this.testAnalyticsModule()
            },
            {
                name: 'Social module',
                test: () => this.testSocialModule()
            },
            {
                name: 'Tasks module',
                test: () => this.testTasksModule()
            },
            {
                name: 'E-commerce module',
                test: () => this.testEcommerceModule()
            }
        ];

        for (const test of tests) {
            await this.runTest(test.name, test.test);
        }
    }

    async runUIUXTests() {
        console.log('🎨 Running UI/UX tests...');

        const tests = [
            {
                name: 'Responsive design',
                test: () => this.testResponsiveDesign()
            },
            {
                name: 'Modal functionality',
                test: () => this.testModalFunctionality()
            },
            {
                name: 'Navigation system',
                test: () => this.testNavigationSystem()
            }
        ];

        for (const test of tests) {
            await this.runTest(test.name, test.test);
        }
    }

    async runErrorHandlingTests() {
        console.log('⚠️ Running error handling tests...');

        const tests = [
            {
                name: 'Error handler initialization',
                test: () => this.testErrorHandlerInit()
            },
            {
                name: 'Error logging functionality',
                test: () => this.testErrorLogging()
            },
            {
                name: 'Error notification system',
                test: () => this.testErrorNotifications()
            }
        ];

        for (const test of tests) {
            await this.runTest(test.name, test.test);
        }
    }

    async runPerformanceTests() {
        console.log('⚡ Running performance tests...');

        const tests = [
            {
                name: 'Page load performance',
                test: () => this.testPageLoadPerformance()
            },
            {
                name: 'Memory usage',
                test: () => this.testMemoryUsage()
            },
            {
                name: 'API response times',
                test: () => this.testAPIResponseTimes()
            }
        ];

        for (const test of tests) {
            await this.runTest(test.name, test.test);
        }
    }

    async runTest(testName, testFunction) {
        this.currentTest = testName;
        const startTime = performance.now();

        try {
            console.log(`  🔍 Running: ${testName}`);
            await testFunction();

            const endTime = performance.now();
            const duration = endTime - startTime;

            this.testResults.push({
                name: testName,
                status: 'passed',
                duration: duration,
                error: null
            });

            console.log(`  ✅ Passed: ${testName} (${duration.toFixed(2)}ms)`);
        } catch (error) {
            const endTime = performance.now();
            const duration = endTime - startTime;

            this.testResults.push({
                name: testName,
                status: 'failed',
                duration: duration,
                error: error.message
            });

            console.log(`  ❌ Failed: ${testName} - ${error.message}`);
        }
    }

    // Individual test implementations
    testLoginFormValidation() {
        // Check if FormHandler exists
        if (typeof window.FormHandler === 'undefined') {
            throw new Error('FormHandler not available');
        }

        // Check if validation rules are defined
        const emailInput = document.querySelector('input[name="email"]');
        if (!emailInput) {
            throw new Error('Email input not found');
        }

        // Test email validation
        const invalidEmails = ['invalid', 'test@', '@domain.com', ''];
        for (const email of invalidEmails) {
            emailInput.value = email;
            emailInput.dispatchEvent(new Event('input'));

            const errorElement = document.getElementById('emailError');
            if (!errorElement || !errorElement.textContent) {
                throw new Error(`Email validation failed for: ${email}`);
            }
        }

        // Test valid email
        emailInput.value = 'test@example.com';
        emailInput.dispatchEvent(new Event('input'));

        const errorElement = document.getElementById('emailError');
        if (errorElement && errorElement.textContent) {
            throw new Error('Valid email was marked as invalid');
        }
    }

    testRegistrationFormValidation() {
        const requiredFields = ['firstName', 'lastName', 'email', 'password', 'confirmPassword'];

        for (const fieldName of requiredFields) {
            const field = document.querySelector(`input[name="${fieldName}"]`);
            if (!field) {
                throw new Error(`Required field ${fieldName} not found`);
            }
        }

        // Test password confirmation
        const passwordField = document.querySelector('input[name="password"]');
        const confirmPasswordField = document.querySelector('input[name="confirmPassword"]');

        if (passwordField && confirmPasswordField) {
            passwordField.value = 'TestPassword123!';
            confirmPasswordField.value = 'DifferentPassword123!';
            confirmPasswordField.dispatchEvent(new Event('input'));

            const errorElement = document.getElementById('confirmPasswordError');
            if (!errorElement || !errorElement.textContent) {
                throw new Error('Password confirmation validation failed');
            }
        }
    }

    testAuthEndpoints() {
        if (typeof window.ApiService === 'undefined') {
            throw new Error('ApiService not available');
        }

        const requiredEndpoints = ['LOGIN', 'REGISTER', 'REFRESH', 'LOGOUT'];

        for (const endpoint of requiredEndpoints) {
            const endpointValue = window.ApiService.getEndpoint(endpoint);
            if (!endpointValue) {
                throw new Error(`Endpoint ${endpoint} not defined`);
            }
        }
    }

    testTokenRefresh() {
        if (typeof window.ApiService === 'undefined') {
            throw new Error('ApiService not available');
        }

        // Test if refresh method exists
        if (typeof window.ApiService.refreshAccessToken !== 'function') {
            throw new Error('refreshAccessToken method not available');
        }

        // Test if clearAuth method exists
        if (typeof window.ApiService.clearAuth !== 'function') {
            throw new Error('clearAuth method not available');
        }
    }

    testAPIServiceInit() {
        if (typeof window.ApiService === 'undefined') {
            throw new Error('ApiService not initialized');
        }

        if (!window.ApiService.baseURL) {
            throw new Error('ApiService baseURL not set');
        }

        if (window.ApiService.retryAttempts !== 3) {
            throw new Error('Retry attempts not configured correctly');
        }
    }

    testRetryLogic() {
        // This would require mocking network requests
        // For now, just check if the configuration exists
        if (window.ApiService.retryDelay !== 1000) {
            throw new Error('Retry delay not configured correctly');
        }
    }

    testAPIErrorHandling() {
        if (typeof window.ErrorHandler === 'undefined') {
            throw new Error('ErrorHandler not available');
        }

        // Test if error logging methods exist
        const requiredMethods = ['logError', 'logWarning', 'logInfo', 'getErrorLog'];
        for (const method of requiredMethods) {
            if (typeof window.ErrorHandler[method] !== 'function') {
                throw new Error(`ErrorHandler method ${method} not available`);
            }
        }
    }

    testEmailValidation() {
        if (typeof validateEmail === 'undefined') {
            throw new Error('validateEmail function not available');
        }

        const testCases = [
            { email: 'test@example.com', shouldBeValid: true },
            { email: 'invalid-email', shouldBeValid: false },
            { email: 'test@', shouldBeValid: false },
            { email: '@example.com', shouldBeValid: false }
        ];

        for (const testCase of testCases) {
            const result = validateEmail(testCase.email);
            const isValid = result === null;

            if (isValid !== testCase.shouldBeValid) {
                throw new Error(`Email validation failed for: ${testCase.email}`);
            }
        }
    }

    testPasswordValidation() {
        if (typeof validatePassword === 'undefined') {
            throw new Error('validatePassword function not available');
        }

        const testCases = [
            { password: 'ValidPass123!', shouldBeValid: true },
            { password: 'short', shouldBeValid: false },
            { password: 'nouppercase123!', shouldBeValid: false },
            { password: 'NOLOWERCASE123!', shouldBeValid: false },
            { password: 'NoNumbers!', shouldBeValid: false },
            { password: 'NoSpecialChars123', shouldBeValid: false }
        ];

        for (const testCase of testCases) {
            const result = validatePassword(testCase.password);
            const isValid = result === null;

            if (isValid !== testCase.shouldBeValid) {
                throw new Error(`Password validation failed for: ${testCase.password}`);
            }
        }
    }

    testRealTimeValidation() {
        const form = document.querySelector('#loginForm, #registerForm');
        if (!form) {
            throw new Error('No form found for real-time validation testing');
        }

        // Test if input event listeners are attached
        const inputs = form.querySelectorAll('input');
        for (const input of inputs) {
            // This is a basic check - in a real scenario, you'd test actual validation
            if (!input.name) {
                throw new Error(`Input field missing name attribute: ${input.type}`);
            }
        }
    }

    testAnalyticsModule() {
        if (typeof window.AnalyticsModule === 'undefined') {
            throw new Error('AnalyticsModule not available');
        }

        // Check if module has required methods
        const requiredMethods = ['init', 'loadMetrics', 'renderPage'];
        for (const method of requiredMethods) {
            if (typeof window.AnalyticsModule[method] !== 'function') {
                throw new Error(`AnalyticsModule method ${method} not available`);
            }
        }
    }

    testSocialModule() {
        if (typeof window.SocialModule === 'undefined') {
            throw new Error('SocialModule not available');
        }

        // Check if module has required methods
        const requiredMethods = ['init', 'loadPosts', 'createPost'];
        for (const method of requiredMethods) {
            if (typeof window.SocialModule[method] !== 'function') {
                throw new Error(`SocialModule method ${method} not available`);
            }
        }
    }

    testTasksModule() {
        if (typeof window.TasksModule === 'undefined') {
            throw new Error('TasksModule not available');
        }

        // Check if module has required methods
        const requiredMethods = ['init', 'loadTasks', 'createTask'];
        for (const method of requiredMethods) {
            if (typeof window.TasksModule[method] !== 'function') {
                throw new Error(`TasksModule method ${method} not available`);
            }
        }
    }

    testEcommerceModule() {
        if (typeof window.EcommerceModule === 'undefined') {
            throw new Error('EcommerceModule not available');
        }

        // Check if module has required methods
        const requiredMethods = ['init', 'loadProducts', 'addToCart'];
        for (const method of requiredMethods) {
            if (typeof window.EcommerceModule[method] !== 'function') {
                throw new Error(`EcommerceModule method ${method} not available`);
            }
        }
    }

    testResponsiveDesign() {
        // Test viewport meta tag
        const viewportMeta = document.querySelector('meta[name="viewport"]');
        if (!viewportMeta) {
            throw new Error('Viewport meta tag not found');
        }

        // Test CSS custom properties
        const rootStyles = getComputedStyle(document.documentElement);
        const requiredProperties = [
            '--primary-color',
            '--secondary-color',
            '--border-radius',
            '--transition'
        ];

        for (const property of requiredProperties) {
            const value = rootStyles.getPropertyValue(property);
            if (!value) {
                throw new Error(`CSS custom property ${property} not defined`);
            }
        }
    }

    testModalFunctionality() {
        // Check if modal system exists
        if (typeof window.AdvancedModal === 'undefined') {
            throw new Error('AdvancedModal not available');
        }

        // Test modal creation
        try {
            const modal = new window.AdvancedModal('test-modal', {
                closable: true,
                backdrop: true
            });

            if (!modal) {
                throw new Error('Modal creation failed');
            }
        } catch (error) {
            throw new Error(`Modal functionality test failed: ${error.message}`);
        }
    }

    testNavigationSystem() {
        // Check if navigation elements exist
        const navElements = document.querySelectorAll('nav, .navigation, .sidebar');
        if (navElements.length === 0) {
            throw new Error('Navigation elements not found');
        }

        // Check for navigation links
        const navLinks = document.querySelectorAll('nav a, .navigation a, .sidebar a');
        if (navLinks.length === 0) {
            throw new Error('Navigation links not found');
        }
    }

    testErrorHandlerInit() {
        if (typeof window.ErrorHandler === 'undefined') {
            throw new Error('ErrorHandler not initialized');
        }

        // Test if error log is available
        const errorLog = window.ErrorHandler.getErrorLog();
        if (!Array.isArray(errorLog)) {
            throw new Error('Error log not properly initialized');
        }
    }

    testErrorLogging() {
        if (typeof window.ErrorHandler === 'undefined') {
            throw new Error('ErrorHandler not available');
        }

        // Test error logging
        const testError = new Error('Test error for logging');
        const errorInfo = window.ErrorHandler.logError(testError, { type: 'TEST' });

        if (!errorInfo || !errorInfo.id) {
            throw new Error('Error logging failed');
        }

        // Test warning logging
        window.ErrorHandler.logWarning('Test warning', { type: 'TEST' });

        // Test info logging
        window.ErrorHandler.logInfo('Test info', { type: 'TEST' });
    }

    testErrorNotifications() {
        if (typeof window.ErrorHandler === 'undefined') {
            throw new Error('ErrorHandler not available');
        }

        // Test error toast
        window.ErrorHandler.showErrorToast('Test error notification');

        // Check if toast was created
        const toast = document.querySelector('.error-toast');
        if (!toast) {
            throw new Error('Error toast not created');
        }

        // Clean up
        toast.remove();
    }

    testPageLoadPerformance() {
        // Test if page loaded within reasonable time
        const loadTime = performance.now();
        if (loadTime > 5000) {
            throw new Error(`Page load time too slow: ${loadTime.toFixed(2)}ms`);
        }
    }

    testMemoryUsage() {
        if (performance.memory) {
            const memoryInfo = performance.memory;
            const usedMB = memoryInfo.usedJSHeapSize / 1024 / 1024;

            if (usedMB > 100) {
                throw new Error(`Memory usage too high: ${usedMB.toFixed(2)}MB`);
            }
        }
    }

    testAPIResponseTimes() {
        // This would require actual API calls
        // For now, just check if API service is configured
        if (typeof window.ApiService === 'undefined') {
            throw new Error('ApiService not available for response time testing');
        }
    }

    generateTestReport() {
        const passedTests = this.testResults.filter(test => test.status === 'passed').length;
        const failedTests = this.testResults.filter(test => test.status === 'failed').length;
        const totalTests = this.testResults.length;
        const successRate = ((passedTests / totalTests) * 100).toFixed(2);

        const report = {
            summary: {
                total: totalTests,
                passed: passedTests,
                failed: failedTests,
                successRate: `${successRate}%`,
                duration: this.testResults.reduce((sum, test) => sum + test.duration, 0)
            },
            results: this.testResults
        };

        console.log('📊 Test Report:', report);

        // Display results in UI if possible
        this.displayTestResults(report);

        return report;
    }

    displayTestResults(report) {
        // Create a test results modal
        const modal = new window.AdvancedModal('test-results-modal', {
            closable: true,
            backdrop: true,
            size: 'large'
        });

        const resultsHTML = `
            <div class="test-results">
                <h2>🧪 Test Results</h2>
                <div class="test-summary">
                    <div class="summary-item">
                        <span class="label">Total Tests:</span>
                        <span class="value">${report.summary.total}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">Passed:</span>
                        <span class="value success">${report.summary.passed}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">Failed:</span>
                        <span class="value error">${report.summary.failed}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">Success Rate:</span>
                        <span class="value">${report.summary.successRate}</span>
                    </div>
                </div>
                
                <div class="test-details">
                    <h3>Test Details</h3>
                    <div class="test-list">
                        ${report.results.map(test => `
                            <div class="test-item ${test.status}">
                                <span class="test-name">${test.name}</span>
                                <span class="test-status">${test.status}</span>
                                <span class="test-duration">${test.duration.toFixed(2)}ms</span>
                                ${test.error ? `<span class="test-error">${test.error}</span>` : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;

        const content = {
            title: 'Testing Results',
            body: resultsHTML,
            footer: `
                <button class="btn btn-primary" onclick="window.AdvancedModal.close('test-results-modal')">Close</button>
            `
        };

        modal.show(content);
    }
}

// Initialize testing suite
window.TestingSuite = new TestingSuite();

// Add testing button to UI
document.addEventListener('DOMContentLoaded', () => {
    const runTestsBtn = document.createElement('button');
    runTestsBtn.id = 'run-tests-btn';
    runTestsBtn.className = 'btn btn-secondary';
    runTestsBtn.innerHTML = '🧪 Run Tests';
    runTestsBtn.style.position = 'fixed';
    runTestsBtn.style.bottom = '20px';
    runTestsBtn.style.right = '20px';
    runTestsBtn.style.zIndex = '1000';

    runTestsBtn.addEventListener('click', () => {
        window.TestingSuite.runAllTests();
    });

    document.body.appendChild(runTestsBtn);
});

window.TestingSuite = TestingSuite;
