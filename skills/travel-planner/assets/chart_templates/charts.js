/**
 * Travel Planner - Chart Configuration
 * Using Chart.js for data visualization
 */

class TravelCharts {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.charts = {};
  }

  // Initialize all charts
  initCharts(chartConfigs) {
    chartConfigs.forEach(config => {
      this.createChart(config);
    });
  }

  // Create a single chart
  createChart(config) {
    const canvas = document.createElement('canvas');
    canvas.id = config.id || `chart-${Date.now()}`;
    canvas.style.maxHeight = '300px';

    if (config.container) {
      document.getElementById(config.container).appendChild(canvas);
    } else {
      this.container.appendChild(canvas);
    }

    this.charts[config.id] = new Chart(canvas, {
      type: config.type,
      data: {
        labels: config.labels,
        datasets: config.datasets || []
      },
      options: config.options || {}
    });

    return this.charts[config.id];
  }

  // Update chart data
  updateChart(chartId, newData) {
    if (this.charts[chartId]) {
      this.charts[chartId].data = newData;
      this.charts[chartId].update();
    }
  }

  // Destroy all charts
  destroy() {
    Object.values(this.charts).forEach(chart => {
      chart.destroy();
    });
    this.charts = {};
  }
}

// Helper functions for common charts
function createBudgetChart(container, budget) {
  const categories = ['交通', '住宿', '餐饮', '门票', '购物', '其他'];
  const values = [
    budget.transport,
    budget.accommodation,
    budget.food,
    budget.tickets,
    budget.shopping,
    budget.other
  ];
  const colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#1abc9c'];

  return new Chart(container, {
    type: 'bar',
    data: {
      labels: categories,
      datasets: [{
        label: '预算 (元)',
        data: values,
        backgroundColor: colors,
        borderRadius: 8
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: {
        legend: { display: false }
      }
    }
  });
}

function createExpenseDonut(container, expenses) {
  const labels = Object.keys(expenses);
  const values = Object.values(expenses);
  const colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6'];

  return new Chart(container, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: colors,
        borderWidth: 2,
        borderColor: '#fff'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'right'
        }
      }
    }
  });
}

function createWeatherChart(container, forecast) {
  const labels = forecast.map(d => d.date.slice(5)); // MM-DD format
  const dayTemps = forecast.map(d => parseFloat(d.day_temp));
  const nightTemps = forecast.map(d => parseFloat(d.night_temp));

  return new Chart(container, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: '最高温度',
          data: dayTemps,
          borderColor: '#e74c3c',
          backgroundColor: 'rgba(231, 76, 60, 0.1)',
          fill: true,
          tension: 0.4
        },
        {
          label: '最低温度',
          data: nightTemps,
          borderColor: '#3498db',
          backgroundColor: 'rgba(52, 152, 219, 0.1)',
          fill: true,
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' }
      },
      scales: {
        y: {
          beginAtZero: false
        }
      }
    }
  });
}
