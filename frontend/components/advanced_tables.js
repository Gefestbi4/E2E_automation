/**
 * Продвинутая система таблиц
 * Поддерживает сортировку, фильтрацию, пагинацию, выбор строк, экспорт данных
 */

class AdvancedTable {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            data: [],
            columns: [],
            sortable: true,
            filterable: true,
            selectable: true,
            pagination: true,
            pageSize: 10,
            searchable: true,
            exportable: true,
            responsive: true,
            loading: false,
            emptyMessage: 'Нет данных для отображения',
            ...options
        };

        this.currentPage = 1;
        this.sortColumn = null;
        this.sortDirection = 'asc';
        this.filteredData = [];
        this.selectedRows = new Set();
        this.searchTerm = '';

        this.init();
    }

    /**
     * Инициализация таблицы
     */
    init() {
        this.filteredData = [...this.options.data];
        this.render();
        this.setupEventListeners();
    }

    /**
     * Рендеринг таблицы
     */
    render() {
        this.container.innerHTML = `
            <div class="advanced-table">
                ${this.renderToolbar()}
                ${this.renderTable()}
                ${this.renderPagination()}
            </div>
        `;
    }

    /**
     * Рендеринг панели инструментов
     */
    renderToolbar() {
        return `
            <div class="table-toolbar">
                <div class="toolbar-left">
                    ${this.options.searchable ? this.renderSearch() : ''}
                    ${this.options.filterable ? this.renderFilters() : ''}
                </div>
                <div class="toolbar-right">
                    ${this.options.exportable ? this.renderExportButtons() : ''}
                    ${this.options.selectable ? this.renderSelectionInfo() : ''}
                </div>
            </div>
        `;
    }

    /**
     * Рендеринг поиска
     */
    renderSearch() {
        return `
            <div class="table-search">
                <input type="text" 
                       class="search-input" 
                       placeholder="Поиск..." 
                       value="${this.searchTerm}">
                <button class="search-clear" type="button" title="Очистить поиск">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
    }

    /**
     * Рендеринг фильтров
     */
    renderFilters() {
        const filterableColumns = this.options.columns.filter(col => col.filterable !== false);

        return `
            <div class="table-filters">
                ${filterableColumns.map(column => `
                    <select class="filter-select" data-column="${column.key}">
                        <option value="">Все ${column.title}</option>
                        ${this.getUniqueValues(column.key).map(value => `
                            <option value="${value}">${value}</option>
                        `).join('')}
                    </select>
                `).join('')}
            </div>
        `;
    }

    /**
     * Рендеринг кнопок экспорта
     */
    renderExportButtons() {
        return `
            <div class="export-buttons">
                <button class="btn btn-sm btn-outline" data-export="csv">
                    <i class="fas fa-file-csv"></i> CSV
                </button>
                <button class="btn btn-sm btn-outline" data-export="json">
                    <i class="fas fa-file-code"></i> JSON
                </button>
                <button class="btn btn-sm btn-outline" data-export="excel">
                    <i class="fas fa-file-excel"></i> Excel
                </button>
            </div>
        `;
    }

    /**
     * Рендеринг информации о выборе
     */
    renderSelectionInfo() {
        return `
            <div class="selection-info">
                <span class="selected-count">${this.selectedRows.size} выбрано</span>
                <button class="btn btn-sm btn-danger" data-action="clear-selection">
                    <i class="fas fa-times"></i> Очистить
                </button>
            </div>
        `;
    }

    /**
     * Рендеринг таблицы
     */
    renderTable() {
        const data = this.getCurrentPageData();

        return `
            <div class="table-container">
                <table class="table">
                    <thead>
                        <tr>
                            ${this.options.selectable ? '<th class="select-column"><input type="checkbox" class="select-all"></th>' : ''}
                            ${this.options.columns.map(column => `
                                <th class="${column.sortable !== false ? 'sortable' : ''}" 
                                    data-column="${column.key}">
                                    ${column.title}
                                    ${column.sortable !== false ? '<i class="sort-icon fas fa-sort"></i>' : ''}
                                </th>
                            `).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${data.length > 0 ? data.map((row, index) => this.renderRow(row, index)).join('') : this.renderEmptyRow()}
                    </tbody>
                </table>
            </div>
        `;
    }

    /**
     * Рендеринг строки таблицы
     */
    renderRow(row, index) {
        const rowId = row.id || index;
        const isSelected = this.selectedRows.has(rowId);

        return `
            <tr class="${isSelected ? 'selected' : ''}" data-id="${rowId}">
                ${this.options.selectable ? `
                    <td class="select-column">
                        <input type="checkbox" class="row-select" ${isSelected ? 'checked' : ''}>
                    </td>
                ` : ''}
                ${this.options.columns.map(column => `
                    <td class="${column.className || ''}">
                        ${this.renderCell(row, column)}
                    </td>
                `).join('')}
            </tr>
        `;
    }

    /**
     * Рендеринг ячейки
     */
    renderCell(row, column) {
        const value = this.getNestedValue(row, column.key);

        if (column.render) {
            return column.render(value, row);
        }

        if (column.type === 'date') {
            return this.formatDate(value);
        }

        if (column.type === 'number') {
            return this.formatNumber(value);
        }

        if (column.type === 'boolean') {
            return value ? '<i class="fas fa-check text-success"></i>' : '<i class="fas fa-times text-danger"></i>';
        }

        if (column.type === 'actions') {
            return this.renderActions(value, row);
        }

        return this.escapeHtml(String(value || ''));
    }

    /**
     * Рендеринг действий
     */
    renderActions(actions, row) {
        if (!actions || !Array.isArray(actions)) return '';

        return `
            <div class="action-buttons">
                ${actions.map(action => `
                    <button class="btn btn-sm ${action.className || 'btn-outline'}" 
                            data-action="${action.action}" 
                            data-id="${row.id}"
                            title="${action.title || action.label}">
                        <i class="${action.icon}"></i>
                        ${action.label}
                    </button>
                `).join('')}
            </div>
        `;
    }

    /**
     * Рендеринг пустой строки
     */
    renderEmptyRow() {
        const colSpan = this.options.columns.length + (this.options.selectable ? 1 : 0);
        return `
            <tr>
                <td colspan="${colSpan}" class="empty-message">
                    <div class="empty-state">
                        <i class="fas fa-inbox"></i>
                        <p>${this.options.emptyMessage}</p>
                    </div>
                </td>
            </tr>
        `;
    }

    /**
     * Рендеринг пагинации
     */
    renderPagination() {
        if (!this.options.pagination) return '';

        const totalPages = Math.ceil(this.filteredData.length / this.options.pageSize);
        if (totalPages <= 1) return '';

        return `
            <div class="table-pagination">
                <div class="pagination-info">
                    Показано ${this.getCurrentPageData().length} из ${this.filteredData.length} записей
                </div>
                <div class="pagination-controls">
                    <button class="btn btn-sm" data-page="prev" ${this.currentPage === 1 ? 'disabled' : ''}>
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    ${this.renderPageNumbers(totalPages)}
                    <button class="btn btn-sm" data-page="next" ${this.currentPage === totalPages ? 'disabled' : ''}>
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Рендеринг номеров страниц
     */
    renderPageNumbers(totalPages) {
        const pages = [];
        const maxVisible = 5;

        let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2));
        let end = Math.min(totalPages, start + maxVisible - 1);

        if (end - start + 1 < maxVisible) {
            start = Math.max(1, end - maxVisible + 1);
        }

        for (let i = start; i <= end; i++) {
            pages.push(`
                <button class="btn btn-sm ${i === this.currentPage ? 'btn-primary' : ''}" 
                        data-page="${i}">
                    ${i}
                </button>
            `);
        }

        return pages.join('');
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        // Поиск
        const searchInput = this.container.querySelector('.search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchTerm = e.target.value;
                this.applyFilters();
            });
        }

        // Очистка поиска
        const searchClear = this.container.querySelector('.search-clear');
        if (searchClear) {
            searchClear.addEventListener('click', () => {
                this.searchTerm = '';
                searchInput.value = '';
                this.applyFilters();
            });
        }

        // Фильтры
        const filterSelects = this.container.querySelectorAll('.filter-select');
        filterSelects.forEach(select => {
            select.addEventListener('change', () => {
                this.applyFilters();
            });
        });

        // Сортировка
        const sortableHeaders = this.container.querySelectorAll('.sortable');
        sortableHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const column = header.dataset.column;
                this.sort(column);
            });
        });

        // Выбор строк
        const selectAll = this.container.querySelector('.select-all');
        if (selectAll) {
            selectAll.addEventListener('change', (e) => {
                this.toggleAllRows(e.target.checked);
            });
        }

        const rowSelects = this.container.querySelectorAll('.row-select');
        rowSelects.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const row = e.target.closest('tr');
                const rowId = row.dataset.id;
                this.toggleRowSelection(rowId, e.target.checked);
            });
        });

        // Пагинация
        const paginationButtons = this.container.querySelectorAll('[data-page]');
        paginationButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const page = e.target.dataset.page;
                this.goToPage(page);
            });
        });

        // Экспорт
        const exportButtons = this.container.querySelectorAll('[data-export]');
        exportButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const format = e.target.dataset.export;
                this.exportData(format);
            });
        });

        // Действия
        const actionButtons = this.container.querySelectorAll('[data-action]');
        actionButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                const id = e.target.dataset.id;
                this.handleAction(action, id);
            });
        });
    }

    /**
     * Применение фильтров
     */
    applyFilters() {
        let filtered = [...this.options.data];

        // Поиск
        if (this.searchTerm) {
            filtered = filtered.filter(row => {
                return this.options.columns.some(column => {
                    const value = this.getNestedValue(row, column.key);
                    return String(value).toLowerCase().includes(this.searchTerm.toLowerCase());
                });
            });
        }

        // Фильтры по колонкам
        const filterSelects = this.container.querySelectorAll('.filter-select');
        filterSelects.forEach(select => {
            const column = select.dataset.column;
            const value = select.value;
            if (value) {
                filtered = filtered.filter(row => {
                    const rowValue = this.getNestedValue(row, column);
                    return String(rowValue) === value;
                });
            }
        });

        this.filteredData = filtered;
        this.currentPage = 1;
        this.render();
        this.setupEventListeners();
    }

    /**
     * Сортировка
     */
    sort(column) {
        if (this.sortColumn === column) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.sortColumn = column;
            this.sortDirection = 'asc';
        }

        this.filteredData.sort((a, b) => {
            const aValue = this.getNestedValue(a, column);
            const bValue = this.getNestedValue(b, column);

            let comparison = 0;
            if (aValue < bValue) comparison = -1;
            if (aValue > bValue) comparison = 1;

            return this.sortDirection === 'desc' ? -comparison : comparison;
        });

        this.render();
        this.setupEventListeners();
    }

    /**
     * Переход на страницу
     */
    goToPage(page) {
        if (page === 'prev') {
            this.currentPage = Math.max(1, this.currentPage - 1);
        } else if (page === 'next') {
            const totalPages = Math.ceil(this.filteredData.length / this.options.pageSize);
            this.currentPage = Math.min(totalPages, this.currentPage + 1);
        } else {
            this.currentPage = parseInt(page);
        }

        this.render();
        this.setupEventListeners();
    }

    /**
     * Получение данных текущей страницы
     */
    getCurrentPageData() {
        if (!this.options.pagination) {
            return this.filteredData;
        }

        const start = (this.currentPage - 1) * this.options.pageSize;
        const end = start + this.options.pageSize;
        return this.filteredData.slice(start, end);
    }

    /**
     * Переключение выбора всех строк
     */
    toggleAllRows(selected) {
        const rowSelects = this.container.querySelectorAll('.row-select');
        rowSelects.forEach(checkbox => {
            checkbox.checked = selected;
            const row = checkbox.closest('tr');
            const rowId = row.dataset.id;
            this.toggleRowSelection(rowId, selected);
        });
    }

    /**
     * Переключение выбора строки
     */
    toggleRowSelection(rowId, selected) {
        if (selected) {
            this.selectedRows.add(rowId);
        } else {
            this.selectedRows.delete(rowId);
        }

        this.updateSelectionInfo();
    }

    /**
     * Обновление информации о выборе
     */
    updateSelectionInfo() {
        const selectedCount = this.container.querySelector('.selected-count');
        if (selectedCount) {
            selectedCount.textContent = `${this.selectedRows.size} выбрано`;
        }
    }

    /**
     * Экспорт данных
     */
    exportData(format) {
        const data = this.selectedRows.size > 0 ?
            this.options.data.filter(row => this.selectedRows.has(row.id || row)) :
            this.filteredData;

        switch (format) {
            case 'csv':
                this.exportToCSV(data);
                break;
            case 'json':
                this.exportToJSON(data);
                break;
            case 'excel':
                this.exportToExcel(data);
                break;
        }
    }

    /**
     * Экспорт в CSV
     */
    exportToCSV(data) {
        const headers = this.options.columns.map(col => col.title);
        const rows = data.map(row =>
            this.options.columns.map(col => this.getNestedValue(row, col.key))
        );

        const csvContent = [headers, ...rows]
            .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
            .join('\n');

        this.downloadFile(csvContent, 'data.csv', 'text/csv');
    }

    /**
     * Экспорт в JSON
     */
    exportToJSON(data) {
        const jsonContent = JSON.stringify(data, null, 2);
        this.downloadFile(jsonContent, 'data.json', 'application/json');
    }

    /**
     * Экспорт в Excel (базовая реализация)
     */
    exportToExcel(data) {
        // Простая реализация - в реальном проекте лучше использовать библиотеку
        this.exportToCSV(data);
    }

    /**
     * Скачивание файла
     */
    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    /**
     * Обработка действий
     */
    handleAction(action, id) {
        const row = this.options.data.find(r => (r.id || r) === id);

        // Событие действия
        this.container.dispatchEvent(new CustomEvent('table:action', {
            detail: { action, id, row }
        }));
    }

    /**
     * Получение вложенного значения
     */
    getNestedValue(obj, path) {
        return path.split('.').reduce((current, key) => current?.[key], obj);
    }

    /**
     * Получение уникальных значений для фильтра
     */
    getUniqueValues(columnKey) {
        const values = this.options.data.map(row => this.getNestedValue(row, columnKey));
        return [...new Set(values)].filter(v => v !== null && v !== undefined).sort();
    }

    /**
     * Форматирование даты
     */
    formatDate(value) {
        if (!value) return '';
        const date = new Date(value);
        return date.toLocaleDateString('ru-RU');
    }

    /**
     * Форматирование числа
     */
    formatNumber(value) {
        if (value === null || value === undefined) return '';
        return new Intl.NumberFormat('ru-RU').format(value);
    }

    /**
     * Экранирование HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Обновление данных
     */
    updateData(newData) {
        this.options.data = newData;
        this.filteredData = [...newData];
        this.selectedRows.clear();
        this.currentPage = 1;
        this.render();
        this.setupEventListeners();
    }

    /**
     * Добавление строки
     */
    addRow(row) {
        this.options.data.push(row);
        this.updateData(this.options.data);
    }

    /**
     * Удаление строки
     */
    removeRow(id) {
        this.options.data = this.options.data.filter(row => (row.id || row) !== id);
        this.updateData(this.options.data);
    }

    /**
     * Обновление строки
     */
    updateRow(id, updates) {
        const index = this.options.data.findIndex(row => (row.id || row) === id);
        if (index !== -1) {
            this.options.data[index] = { ...this.options.data[index], ...updates };
            this.updateData(this.options.data);
        }
    }
}

// Экспорт для глобального доступа
window.AdvancedTable = AdvancedTable;
