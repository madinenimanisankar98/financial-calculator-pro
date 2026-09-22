/* =============================================================
   learn.js — Learn modal content loading & English/Telugu switch
   ============================================================= */

let currentLearnLang = 'en';
let learnCache = {};

async function fetchLearnContent(lang) {
  if (learnCache[lang]) return learnCache[lang];
  const res = await fetch(`/api/learn?lang=${lang}`);
  const json = await res.json();
  learnCache[lang] = json.data;
  return json.data;
}

function renderLearnContent(content) {
  const body = document.getElementById('learnBody');
  const order = ['savings', 'emi', 'gst', 'percentage'];
  body.innerHTML = order.map(key => {
    const block = content[key];
    if (!block) return '';
    return `
      <div class="learn-block">
        <h3>${escapeHtml(block.title)}</h3>
        <div class="formula">${escapeHtml(block.formula)}</div>
        <p>${escapeHtml(block.explanation)}</p>
        <p><em>${escapeHtml(block.example)}</em></p>
        <p class="tip">💡 ${escapeHtml(block.tip)}</p>
      </div>
    `;
  }).join('');
}

async function loadLearnModal(lang) {
  currentLearnLang = lang;
  const body = document.getElementById('learnBody');
  body.innerHTML = '<p class="placeholder-text">Loading...</p>';
  try {
    const content = await fetchLearnContent(lang);
    renderLearnContent(content);
  } catch (err) {
    body.innerHTML = '<p class="placeholder-text">Could not load content. Please try again.</p>';
  }
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
