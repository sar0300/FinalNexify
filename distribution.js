document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('expenseChart').getContext('2d');

    const data = {
        labels: ['Utilities', 'Entertainment', 'Food', 'Health', 'Transport', 'Others'],
        datasets: [{
            label: 'Monthly Expense Distribution',
            data: [15, 20, 25, 10, 15, 15], // Example data; replace with real values
            backgroundColor: [
                '#FF6384',
                '#36A2EB',
                '#FFCE56',
                '#4BC0C0',
                '#FF9F40',
                '#C9CBCF'
            ],
            borderColor: '#ffffff',
            borderWidth: 1
        }]
    };

    const config = {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            let label = tooltipItem.label || '';
                            if (tooltipItem.raw !== undefined) {
                                label += ': ' + tooltipItem.raw + '%'; // Show percentage in tooltip
                            }
                            return label;
                        }
                    }
                }
            }
        }
    };

    new Chart(ctx, config);
});
