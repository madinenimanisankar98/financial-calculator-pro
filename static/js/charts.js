/* =============================================================
   charts.js — Chart.js graphing configurations
   ============================================================= */

const chartInstances = {};

function destroyChart(key) {
  if (chartInstances[key]) {
    chartInstances[key].destroy();
    delete chartInstances[key];
  }
}

const CHART_DEFAULTS = {
  color: '#e6fdf7',
  borderColor: 'rgba(255,255,255,0.08)',
};

Chart.defaults.color = CHART_DEFAULTS.color;
Chart.defaults.borderColor = CHART_DEFAULTS.borderColor;
Chart.defaults.font.family = "'Segoe UI', sans-serif";

/* ---------------- Savings charts ---------------- */
function renderSavingsCharts(data) {
  document.getElementById('savingsCharts').style.display = 'grid';

  // 1. Expenses vs Savings doughnut
  destroyChart('savingsPie');
  const pieCtx = document.getElementById('savingsPieChart');
  chartInstances.savingsPie = new Chart(pieCtx, {
    type: 'doughnut',
    data: {
      labels: ['Available Savings', 'Expenses'],
      datasets: [{
        data: [Math.max(data.available_savings, 0), data.monthly_expenses || 0],
        backgroundColor: ['#10b981', '#374151'],
        borderWidth: 0,
      }],
    },
    options: { animation: { animateScale: true, duration: 1200 }, plugins: { legend: { position: 'bottom' } } },
  });

  // 2. Savings accumulation timeline
  destroyChart('savingsLine');
  const lineCtx = document.getElementById('savingsLineChart');
  const timeline = data.timeline || [];
  chartInstances.savingsLine = new Chart(lineCtx, {
    type: 'line',
    data: {
      labels: timeline.map(p => `M${p.month}`),
      datasets: [{
        label: 'Saved (₹)',
        data: timeline.map(p => p.saved),
        borderColor: '#10b981',
        backgroundColor: 'rgba(16,185,129,0.2)',
        fill: true,
        tension: 0.35,
        pointRadius: 2,
      }],
    },
    options: {
      animation: { duration: 1200, easing: 'easeOutQuart' },
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } },
    },
  });

  // 3. Goal progress fill bar (animated width)
  const bar = document.getElementById('savingsProgressBar');
  const label = document.getElementById('savingsProgressLabel');
  const progress = Math.min(data.progress_percent || 0, 100);
  requestAnimationFrame(() => {
    bar.style.width = progress + '%';
    label.textContent = progress + '%';
  });
}

/* ---------------- EMI charts ---------------- */
function renderEmiCharts(data) {
  document.getElementById('emiCharts').style.display = 'grid';

  destroyChart('emiPie');
  const pieCtx = document.getElementById('emiPieChart');
  chartInstances.emiPie = new Chart(pieCtx, {
    type: 'doughnut',
    data: {
      labels: ['Principal', 'Total Interest'],
      datasets: [{
        data: [data.principal, data.total_interest],
        backgroundColor: ['#a855f7', '#f472b6'],
        borderWidth: 0,
      }],
    },
    options: { animation: { animateScale: true, duration: 1200 }, plugins: { legend: { position: 'bottom' } } },
  });

  destroyChart('emiLine');
  const lineCtx = document.getElementById('emiLineChart');
  const schedule = data.amortization || [];
  chartInstances.emiLine = new Chart(lineCtx, {
    type: 'line',
    data: {
      labels: schedule.map(p => `M${p.month}`),
      datasets: [{
        label: 'Remaining Balance (₹)',
        data: schedule.map(p => p.balance),
        borderColor: '#a855f7',
        backgroundColor: 'rgba(168,85,247,0.2)',
        fill: true,
        tension: 0.3,
        pointRadius: 1,
      }],
    },
    options: {
      animation: { duration: 1200, easing: 'easeOutQuart' },
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } },
    },
  });
}

/* ---------------- GST chart ---------------- */
function renderGstChart(data) {
  document.getElementById('gstCharts').style.display = 'grid';

  destroyChart('gstBar');
  const barCtx = document.getElementById('gstBarChart');
  chartInstances.gstBar = new Chart(barCtx, {
    type: 'bar',
    data: {
      labels: ['Base Price', 'GST Amount'],
      datasets: [{
        data: [data.base_price, data.gst_amount],
        backgroundColor: ['#f59e0b', '#fbbf24'],
        borderRadius: 8,
      }],
    },
    options: {
      animation: { duration: 1000, easing: 'easeOutBack' },
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } },
    },
  });
}

/* ---------------- Percentage gauge ---------------- */
function renderPercentageChart(data) {
  document.getElementById('percentageCharts').style.display = 'grid';

  destroyChart('pctGauge');
  const ctx = document.getElementById('percentageGaugeChart');
  const pct = Math.min(Math.max(data.percentage, 0), 100);
  chartInstances.pctGauge = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: [`${data.percentage}%`, 'Remaining'],
      datasets: [{
        data: [pct, 100 - pct],
        backgroundColor: ['#06b6d4', '#1f2937'],
        borderWidth: 0,
        circumference: 270,
        rotation: 225,
      }],
    },
    options: {
      animation: { animateRotate: true, duration: 1200 },
      cutout: '70%',
      plugins: { legend: { position: 'bottom' } },
    },
  });
}
