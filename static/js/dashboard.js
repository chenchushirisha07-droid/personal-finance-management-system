document.addEventListener("DOMContentLoaded", () => {
    // Expense Doughnut Chart
    const expenseCtx = document.getElementById('expenseChart');
    if (expenseCtx) {
        new Chart(expenseCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Rent', 'Groceries', 'Transport', 'Utilities', 'Education'],
                datasets: [{
                    data: [15000, 8500, 3500, 4000, 7500],
                    backgroundColor: ['#12233F', '#16A878', '#64748B', '#E8F7F0', '#3b82f6'],
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: { responsive: true, cutout: '75%', plugins: { legend: { position: 'bottom' } } }
        });
    }

    // Income vs Expense Bar Chart
    const trendCtx = document.getElementById('trendChart');
    if (trendCtx) {
        new Chart(trendCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                datasets: [
                    { label: 'Income', data: [15000, 15000, 15000, 15000], backgroundColor: '#E8F7F0' },
                    { label: 'Expenses', data: [12000, 8000, 9500, 9000], backgroundColor: '#16A878' }
                ]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }
});