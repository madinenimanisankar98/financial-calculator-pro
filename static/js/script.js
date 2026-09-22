/* =============================================================
   script.js — Navigation, form validation & API handlers
   ============================================================= */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initSavingsForm();
  initEmiForm();
  initGstForm();
  initPercentageForm();
  initModals();
  initLanguageToggle();
  initChat();
});

/* ---------------------------------------------------------------
   Navigation between Home dashboard and calculator views
   --------------------------------------------------------------- */
function initNavigation() {
  const views = document.querySelectorAll('.view');
  const backBtn = document.getElementById('btnBackHome');

  function showView(id) {
    views.forEach(v => v.classList.toggle('active', v.id === id));
    backBtn.classList.toggle('hidden', id === 'homeView');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  document.querySelectorAll('.calc-card').forEach(card => {
    card.addEventListener('click', () => showView(card.dataset.target));
  });

  backBtn.addEventListener('click', () => showView('homeView'));

  window.showView = showView; // expose for other handlers if needed
}

/* ---------------------------------------------------------------
   Helpers
   --------------------------------------------------------------- */
function formatCurrency(value) {
  if (value === null || value === undefined || isNaN(value)) return '—';
  return '₹' + Number(value).toLocaleString('en-IN', { maximumFractionDigits: 2 });
}

function resultRow(label, value, opts = {}) {
  const cls = opts.highlight ? 'result-value highlight' : 'result-value';
  return `<div class="result-row"><span class="result-label">${label}</span><span class="${cls}">${value}</span></div>`;
}

async function postJSON(url, payload) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return res.json();
}

/* ---------------------------------------------------------------
   Savings Calculator
   --------------------------------------------------------------- */
const SAVINGS_QUOTES = [
  "Do not save what is left after spending; spend what is left after saving.",
  "A goal without a plan is just a wish — you now have both.",
  "Small savings today become the big wins of tomorrow.",
  "The habit of saving is itself an education in self-command.",
  "Every rupee saved is a rupee earning you freedom.",
  "Consistency beats intensity — steady monthly savings win the race.",
  "Wealth isn't about how much you earn, it's about how much you keep.",
  "Your future self is built by the savings decisions you make today.",
];

function initSavingsForm() {
  const form = document.getElementById('savingsForm');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const payload = {
      monthly_income: fd.get('monthly_income'),
      monthly_expenses: fd.get('monthly_expenses'),
      goal_name: fd.get('goal_name'),
      goal_price: fd.get('goal_price'),
      target_value: fd.get('target_value') || null,
      target_unit: fd.get('target_unit'),
    };

    const resultsEl = document.getElementById('savingsResults');
    resultsEl.innerHTML = '<p class="placeholder-text">Calculating...</p>';

    const { success, data, error } = await postJSON('/api/calculate/savings', payload);
    if (!success) {
      resultsEl.innerHTML = `<p class="placeholder-text">${error}</p>`;
      return;
    }

    if (data.error) {
      resultsEl.innerHTML = `<p class="placeholder-text">${data.error}</p>`;
      document.getElementById('savingsCharts').style.display = 'none';
      return;
    }

    resultsEl.innerHTML = buildSavingsResultHtml(data);

    // Compute a rough "progress" for the fill bar: how close available savings
    // gets you in one month towards the goal.
    data.progress_percent = data.goal_price > 0
      ? Math.min(Math.round((data.available_savings / data.goal_price) * 100), 100)
      : 0;

    renderSavingsCharts(data);
  });
}

function buildSavingsResultHtml(data) {
  const goalName = escapeHtmlLocal(data.goal_name || 'Your Goal');
  const quote = SAVINGS_QUOTES[Math.floor(Math.random() * SAVINGS_QUOTES.length)];

  let html = '';

  // ---- Hero: goal name + goal price, big and bold ----
  html += `
    <div class="savings-hero">
      <span class="savings-hero-label">Your Goal</span>
      <h3 class="savings-hero-goal">${goalName}</h3>
      <div class="savings-hero-price">${formatCurrency(data.goal_price)}</div>
    </div>
  `;

  // ---- Stat cards: income, expenses, available savings, time to goal ----
  html += `
    <div class="stat-grid">
      <div class="stat-card">
        <span class="stat-icon">💵</span>
        <span class="stat-label">Monthly Income</span>
        <span class="stat-value">${formatCurrency(data.monthly_income)}</span>
      </div>
      <div class="stat-card">
        <span class="stat-icon">🧾</span>
        <span class="stat-label">Monthly Expenses</span>
        <span class="stat-value">${formatCurrency(data.monthly_expenses)}</span>
      </div>
      <div class="stat-card highlight">
        <span class="stat-icon">💰</span>
        <span class="stat-label">Available Savings</span>
        <span class="stat-value">${formatCurrency(data.available_savings)}</span>
      </div>
      <div class="stat-card">
        <span class="stat-icon">⏳</span>
        <span class="stat-label">Time to Reach Goal</span>
        <span class="stat-value">${data.estimated_years}y ${data.estimated_remaining_months}m</span>
        <span class="stat-subvalue">${data.estimated_total_days} days total</span>
      </div>
    </div>
  `;

  // ---- Target comparison (only if user gave a target period) ----
  if (data.target) {
    html += `
      <div class="target-card">
        <h4>🎯 Target Comparison</h4>
        <div class="result-row"><span class="result-label">Your Target</span><span class="result-value">${data.target.target_months} months</span></div>
        <div class="result-row"><span class="result-label">Required Monthly Savings</span><span class="result-value">${formatCurrency(data.target.required_monthly_savings)}</span></div>
        <div class="result-row"><span class="result-label">Status</span><span class="status-badge ${data.target.status}">${data.target.status}</span></div>
      </div>
    `;
  }

  // ---- Plain-English timeline summary ----
  html += `<div class="timeline-summary">${buildTimelineSummary(data)}</div>`;

  // ---- Animated motivational quote ----
  html += `
    <div class="quote-box">
      <span class="quote-mark">“</span>
      <p class="quote-text">${escapeHtmlLocal(quote)}</p>
    </div>
  `;

  return html;
}

function buildTimelineSummary(data) {
  const timeline = data.timeline || [];
  if (timeline.length < 2 || data.available_savings <= 0) {
    return `<h4>📈 What this means</h4><p>We couldn't build a timeline because your available savings is too low right now. Try reducing expenses or increasing income to start making progress toward your goal.</p>`;
  }

  const checkpointMonth = Math.min(3, timeline.length - 1);
  const checkpointSaved = timeline[checkpointMonth].saved;
  const checkpointPercent = data.goal_price > 0
    ? Math.min(Math.round((checkpointSaved / data.goal_price) * 100), 100)
    : 0;

  const halfwayIndex = timeline.findIndex(p => p.saved >= data.goal_price / 2);
  const halfwayMonth = halfwayIndex >= 0 ? timeline[halfwayIndex].month : null;

  const finalMonth = data.estimated_months;

  let text = `<h4>📈 What this means</h4>`;
  text += `<p>Starting from ₹0, you're on track to save about <strong>${formatCurrency(data.available_savings)}</strong> every month. `;
  text += `By <strong>month ${checkpointMonth}</strong>, you'll have saved roughly <strong>${formatCurrency(checkpointSaved)}</strong> — about <strong>${checkpointPercent}%</strong> of your ${formatCurrency(data.goal_price)} goal. `;

  if (halfwayMonth !== null) {
    text += `You'll cross the <strong>halfway mark around month ${halfwayMonth}</strong>. `;
  }

  text += `At this pace, you're projected to fully reach your goal in about <strong>${finalMonth} months</strong> `;
  text += `(${data.estimated_years} year${data.estimated_years !== 1 ? 's' : ''} and ${data.estimated_remaining_months} month${data.estimated_remaining_months !== 1 ? 's' : ''}), `;
  text += `assuming your income and expenses stay roughly the same.</p>`;

  return text;
}

/* ---------------------------------------------------------------
   EMI Calculator
   --------------------------------------------------------------- */
function initEmiForm() {
  const form = document.getElementById('emiForm');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const payload = {
      principal: fd.get('principal'),
      annual_rate: fd.get('annual_rate'),
      tenure_value: fd.get('tenure_value'),
      tenure_unit: fd.get('tenure_unit'),
      emis_paid: fd.get('emis_paid') || 0,
    };

    const resultsEl = document.getElementById('emiResults');
    resultsEl.innerHTML = '<p class="placeholder-text">Calculating...</p>';

    const { success, data, error } = await postJSON('/api/calculate/emi', payload);
    if (!success) {
      resultsEl.innerHTML = `<p class="placeholder-text">${error}</p>`;
      return;
    }

    let html = '';
    html += resultRow('Monthly EMI', formatCurrency(data.emi), { highlight: true });
    html += resultRow('Total Payable', formatCurrency(data.total_payable));
    html += resultRow('Total Interest', formatCurrency(data.total_interest));
    if (data.remaining_balance !== undefined) {
      html += resultRow(`Remaining Balance (after ${data.emis_paid} EMIs)`, formatCurrency(data.remaining_balance));
    }

    resultsEl.innerHTML = html;
    renderEmiCharts(data);
  });
}

/* ---------------------------------------------------------------
   GST Calculator
   --------------------------------------------------------------- */
function initGstForm() {
  const form = document.getElementById('gstForm');
  const chips = document.querySelectorAll('#gstChips .chip');
  const customInput = document.getElementById('gstCustomInput');

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      customInput.value = chip.dataset.value;
    });
  });

  customInput.addEventListener('input', () => {
    chips.forEach(c => c.classList.toggle('active', c.dataset.value === customInput.value));
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const payload = {
      product_name: fd.get('product_name') || 'Product',
      price: fd.get('price'),
      mode: fd.get('mode'),
      gst_percent: customInput.value,
    };

    const resultsEl = document.getElementById('gstResults');
    resultsEl.innerHTML = '<p class="placeholder-text">Calculating...</p>';

    const { success, data, error } = await postJSON('/api/calculate/gst', payload);
    if (!success) {
      resultsEl.innerHTML = `<p class="placeholder-text">${error}</p>`;
      return;
    }

    let html = '';
    html += resultRow('Product', escapeHtmlLocal(data.product_name));
    html += resultRow('Base Price', formatCurrency(data.base_price));
    html += resultRow(`GST (${data.gst_percent}%)`, formatCurrency(data.gst_amount));
    html += resultRow('Final Price', formatCurrency(data.final_price), { highlight: true });

    resultsEl.innerHTML = html;
    renderGstChart(data);
  });
}

/* ---------------------------------------------------------------
   Percentage Calculator
   --------------------------------------------------------------- */
function initPercentageForm() {
  const form = document.getElementById('percentageForm');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const payload = {
      total_amount: fd.get('total_amount'),
      percentage: fd.get('percentage'),
    };

    const resultsEl = document.getElementById('percentageResults');
    resultsEl.innerHTML = '<p class="placeholder-text">Calculating...</p>';

    const { success, data, error } = await postJSON('/api/calculate/percentage', payload);
    if (!success) {
      resultsEl.innerHTML = `<p class="placeholder-text">${error}</p>`;
      return;
    }

    let html = '';
    html += resultRow(`${data.percentage}% of Total`, formatCurrency(data.value), { highlight: true });
    html += resultRow('Remainder', formatCurrency(data.remainder));

    resultsEl.innerHTML = html;
    renderPercentageChart(data);
  });
}

/* ---------------------------------------------------------------
   Modals (Learn + Ask AI)
   --------------------------------------------------------------- */
function initModals() {
  const learnModal = document.getElementById('learnModal');
  const askModal = document.getElementById('askModal');

  document.getElementById('btnLearn').addEventListener('click', () => {
    learnModal.classList.remove('hidden');
    loadLearnModal(currentLearnLang);
  });

  document.getElementById('btnAsk').addEventListener('click', () => {
    askModal.classList.remove('hidden');
  });

  document.querySelectorAll('[data-close]').forEach(btn => {
    btn.addEventListener('click', () => {
      document.getElementById(btn.dataset.close).classList.add('hidden');
    });
  });

  [learnModal, askModal].forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.classList.add('hidden');
    });
  });
}

/* ---------------------------------------------------------------
   Language toggle (English / Telugu) - drives the Learn section
   --------------------------------------------------------------- */
function initLanguageToggle() {
  const buttons = document.querySelectorAll('.lang-btn');
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const lang = btn.dataset.lang;
      currentLearnLang = lang;
      const learnModal = document.getElementById('learnModal');
      if (!learnModal.classList.contains('hidden')) {
        loadLearnModal(lang);
      }
    });
  });
}

/* ---------------------------------------------------------------
   Ask Questions AI chat
   --------------------------------------------------------------- */
function initChat() {
  const form = document.getElementById('chatForm');
  const input = document.getElementById('chatInput');
  const window_ = document.getElementById('chatWindow');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    appendChatMessage(question, 'user');
    input.value = '';

    const thinkingEl = appendChatMessage('Thinking...', 'bot');

    try {
      const { data } = await postJSON('/api/ask-ai', { question });
      thinkingEl.textContent = data.answer;
    } catch (err) {
      thinkingEl.textContent = "Sorry, something went wrong. Please try again.";
    }
    window_.scrollTop = window_.scrollHeight;
  });

  function appendChatMessage(text, role) {
    const msg = document.createElement('div');
    msg.className = `chat-msg ${role}`;
    msg.textContent = text;
    window_.appendChild(msg);
    window_.scrollTop = window_.scrollHeight;
    return msg;
  }
}

function escapeHtmlLocal(str) {
  const div = document.createElement('div');
  div.textContent = str ?? '';
  return div.innerHTML;
}
