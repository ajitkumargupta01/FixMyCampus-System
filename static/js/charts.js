// Chart initialization for dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Status Chart
    const statusCtx = document.getElementById('statusChart');
    if (statusCtx) {
        const statusData = JSON.parse(statusCtx.getAttribute('data-status'));
        const statusLabels = Object.keys(statusData);
        const statusValues = Object.values(statusData);
        
        const statusColors = {
            'Pending': '#f59e0b',
            'In Progress': '#3b82f6',
            'Resolved': '#10b981'
        };
        
        new Chart(statusCtx, {
            type: 'bar',
            data: {
                labels: statusLabels,
                datasets: [{
                    label: 'Number of Issues',
                    data: statusValues,
                    backgroundColor: statusLabels.map(label => statusColors[label] || '#9ca3af'),
                    borderWidth: 0,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }

    // Category Chart
    const categoryCtx = document.getElementById('categoryChart');
    if (categoryCtx) {
        const categoryData = JSON.parse(categoryCtx.getAttribute('data-category'));
        const categoryLabels = Object.keys(categoryData);
        const categoryValues = Object.values(categoryData);
        
        const categoryColors = [
            '#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', 
            '#ec4899', '#6366f1', '#14b8a6', '#f97316', '#8b5cf6'
        ];
        
        new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: categoryLabels,
                datasets: [{
                    data: categoryValues,
                    backgroundColor: categoryColors.slice(0, categoryLabels.length),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: false
                    }
                }
            }
        });
    }

    // Time Trend Chart for Admin Dashboard
    const trendChartCtx = document.getElementById('trendChart');
    if (trendChartCtx) {
        const trendData = JSON.parse(trendChartCtx.getAttribute('data-trend'));
        
        new Chart(trendChartCtx, {
            type: 'line',
            data: {
                labels: trendData.dates,
                datasets: [{
                    label: 'Issues Reported',
                    data: trendData.counts,
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
});