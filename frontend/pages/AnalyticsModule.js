// Analytics Module
console.log('📊 AnalyticsModule script loading...');

class AnalyticsModule {
    constructor() {
        this.dashboards = [];
        this.reports = [];
        this.metrics = {};
        this.init();
    }

    init() {
        console.log('📊 AnalyticsModule initialized');
        this.loadDashboards();
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            const createDashboardBtn = document.getElementById('create-dashboard-btn');
            if (createDashboardBtn) {
                createDashboardBtn.addEventListener('click', () => this.createCustomDashboard());
            }

            const generateReportBtn = document.getElementById('generate-report-btn');
            if (generateReportBtn) {
                generateReportBtn.addEventListener('click', () => this.generateReport());
            }
        });
    }

    async loadDashboards() {
        try {
            console.log('📊 Loading dashboards...');
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 100));
            this.dashboards = [
                { id: 1, name: 'Main Dashboard', widgets: 5, lastUpdated: new Date() },
                { id: 2, name: 'E-commerce Analytics', widgets: 3, lastUpdated: new Date() }
            ];
            this.renderDashboards();
        } catch (error) {
            console.error('Error loading dashboards:', error);
        }
    }

    renderDashboards() {
        const dashboardsContainer = document.getElementById('dashboards-container');
        if (!dashboardsContainer) return;

        dashboardsContainer.innerHTML = this.dashboards.map(dashboard => `
            <div class="dashboard-card">
                <h3>${dashboard.name}</h3>
                <p>Widgets: ${dashboard.widgets}</p>
                <p>Last updated: ${dashboard.lastUpdated.toLocaleDateString()}</p>
                <div class="dashboard-actions">
                    <button onclick="AnalyticsModule.openDashboard(${dashboard.id})">Open</button>
                    <button onclick="AnalyticsModule.editDashboard(${dashboard.id})">Edit</button>
                </div>
            </div>
        `).join('');
    }

    createCustomDashboard() {
        console.log('📊 Creating custom dashboard');
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Create Custom Dashboard</h2>
                <form id="create-dashboard-form">
                    <input type="text" id="dashboard-name" placeholder="Dashboard name" required>
                    <select id="dashboard-template">
                        <option value="basic">Basic Dashboard</option>
                        <option value="ecommerce">E-commerce Dashboard</option>
                        <option value="social">Social Media Dashboard</option>
                        <option value="custom">Custom Dashboard</option>
                    </select>
                    <button type="submit">Create Dashboard</button>
                </form>
            </div>
        `;
        document.body.appendChild(modal);
        modal.style.display = 'block';

        document.getElementById('create-dashboard-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('dashboard-name').value;
            const template = document.getElementById('dashboard-template').value;
            if (name.trim()) {
                this.createDashboard(name, template);
                modal.remove();
            }
        });

        modal.querySelector('.close').addEventListener('click', () => {
            modal.remove();
        });
    }

    generateReport() {
        console.log('📊 Generating report');
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Generate Report</h2>
                <form id="generate-report-form">
                    <select id="report-type">
                        <option value="summary">Summary Report</option>
                        <option value="detailed">Detailed Report</option>
                        <option value="custom">Custom Report</option>
                    </select>
                    <input type="date" id="report-start-date" required>
                    <input type="date" id="report-end-date" required>
                    <button type="submit">Generate Report</button>
                </form>
            </div>
        `;
        document.body.appendChild(modal);
        modal.style.display = 'block';

        document.getElementById('generate-report-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const type = document.getElementById('report-type').value;
            const startDate = document.getElementById('report-start-date').value;
            const endDate = document.getElementById('report-end-date').value;
            this.generateReportData(type, startDate, endDate);
            modal.remove();
        });

        modal.querySelector('.close').addEventListener('click', () => {
            modal.remove();
        });
    }

    async createDashboard(name, template) {
        try {
            const newDashboard = {
                id: Date.now(),
                name: name,
                template: template,
                widgets: 0,
                lastUpdated: new Date()
            };
            this.dashboards.push(newDashboard);
            this.renderDashboards();
            console.log('📊 Dashboard created:', newDashboard);
        } catch (error) {
            console.error('Error creating dashboard:', error);
        }
    }

    async generateReportData(type, startDate, endDate) {
        try {
            console.log('📊 Generating report:', type, 'from', startDate, 'to', endDate);
            // Simulate report generation
            await new Promise(resolve => setTimeout(resolve, 1000));
            console.log('📊 Report generated successfully');
            // Show success message or download report
        } catch (error) {
            console.error('Error generating report:', error);
        }
    }

    openDashboard(dashboardId) {
        const dashboard = this.dashboards.find(d => d.id === dashboardId);
        if (dashboard) {
            console.log('📊 Opening dashboard:', dashboard.name);
            // Navigate to dashboard view
        }
    }

    editDashboard(dashboardId) {
        const dashboard = this.dashboards.find(d => d.id === dashboardId);
        if (dashboard) {
            console.log('📊 Editing dashboard:', dashboard.name);
            // Show edit modal
        }
    }

    // Analytics methods for testing
    getMetrics() {
        return {
            users: 150,
            sessions: 1200,
            pageViews: 5000,
            bounceRate: 0.35
        };
    }

    getReports() {
        return this.reports;
    }

    getDashboards() {
        return this.dashboards;
    }
}

// Export for global access
window.AnalyticsModule = AnalyticsModule;
console.log('📊 AnalyticsModule class exported to window:', typeof window.AnalyticsModule);
