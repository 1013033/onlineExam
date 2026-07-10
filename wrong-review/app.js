const EXAM_SOURCES = [];
let wrongItems = [];

const els = {
  list: document.getElementById('reviewList'),
  status: document.getElementById('statusBox'),
  search: document.getElementById('searchInput'),
  sourceFilter: document.getElementById('sourceFilter'),
  totalCount: document.getElementById('totalCount'),
  sourceCount: document.getElementById('sourceCount'),
  visibleCount: document.getElementById('visibleCount')
};

init();

async function init() {
  bindEvents();
  try {
    await collectWrongItems();
    renderSourceOptions();
    renderList();
    applyFilters();
  } catch (error) {
    console.error('Load wrong review failed:', error);
    setStatus('讀取錯題時發生錯誤，請重新整理頁面後再試。');
  }
}

function bindEvents() {
  els.search.addEventListener('input', applyFilters);
  els.sourceFilter.addEventListener('change', applyFilters);
}

async function collectWrongItems() {
  setStatus('正在讀取各試卷錯題庫...');
  const exams = getReviewableExams();
  for (const exam of exams) {
    const course = await loadCourse(exam);
    if (!course || !course.meta || !Array.isArray(course.quiz)) continue;

    const storeKey = course.meta.storeKey;
    if (!storeKey) continue;

    const wrongBookKey = `${storeKey}-wrong-book-v1`;
    const wrongBook = readWrongBook(wrongBookKey);
    const wrongIds = Object.keys(wrongBook);
    if (!wrongIds.length) continue;

    const quizById = new Map(course.quiz.map(item => [item.id, item]));
    wrongIds.forEach(id => {
      const item = quizById.get(id);
      if (!item || item.type === 'text') return;
      wrongItems.push({
        id,
        item,
        exam,
        course,
        wrongBook,
        wrongBookKey,
        wrongMeta: wrongBook[id] || {}
      });
    });
  }

  const sourceMap = new Map();
  wrongItems.forEach(entry => sourceMap.set(entry.exam.href, entry.exam));
  EXAM_SOURCES.splice(0, EXAM_SOURCES.length, ...sourceMap.values());
}

function getReviewableExams() {
  const exams = window.PORTAL && Array.isArray(window.PORTAL.exams) ? window.PORTAL.exams : [];
  return exams.filter(exam => {
    const href = exam.href || '';
    const text = [exam.id, exam.tag, exam.title, exam.desc, href].join(' ').toLowerCase();
    return href.endsWith('/') && !href.includes('-print') && !text.includes('列印') && !text.includes('pdf');
  });
}

async function loadCourse(exam) {
  const href = exam.href || '';
  if (!href) return null;
  const scriptUrl = `../${href.replace(/\/?$/, '/') }course-data.js`;
  return new Promise(resolve => {
    const previous = window.COURSE;
    const script = document.createElement('script');
    script.src = `${scriptUrl}?review=${Date.now()}-${Math.random().toString(16).slice(2)}`;
    script.async = true;
    script.onload = () => {
      const course = window.COURSE;
      window.COURSE = previous;
      script.remove();
      resolve(course);
    };
    script.onerror = () => {
      window.COURSE = previous;
      script.remove();
      console.warn('Skip course-data load failure:', scriptUrl);
      resolve(null);
    };
    document.head.appendChild(script);
  });
}

function readWrongBook(key) {
  try {
    return JSON.parse(localStorage.getItem(key)) || {};
  } catch {
    return {};
  }
}

function renderSourceOptions() {
  const options = ['<option value="all">全部來源</option>'];
  EXAM_SOURCES.forEach(exam => {
    options.push(`<option value="${escapeAttr(exam.href)}">${escapeHtml(exam.title || exam.href)}</option>`);
  });
  els.sourceFilter.innerHTML = options.join('');
}

function renderList() {
  if (!wrongItems.length) {
    els.list.innerHTML = '';
    setStatus('目前沒有尚未出庫的錯題。作答錯誤的題目會自動出現在這裡。');
    updateStats(0);
    return;
  }

  els.status.classList.add('hidden');
  els.list.innerHTML = wrongItems.map(renderWrongCard).join('');
  els.list.querySelectorAll('[data-learned-key]').forEach(button => {
    button.addEventListener('click', () => markLearned(button.dataset.learnedKey));
  });
}

function renderWrongCard(entry, index) {
  const item = entry.item;
  const correctAnswers = Array.isArray(item.answer) ? item.answer : [item.answer];
  const typeLabel = item.type === 'multiple' ? '複選題' : '單選題';
  const streak = Number(entry.wrongMeta.correctStreak || 0);
  const missedAt = entry.wrongMeta.missedAt ? formatDate(entry.wrongMeta.missedAt) : '未記錄';
  const searchText = [
    entry.exam.title,
    entry.exam.tag,
    item.q,
    item.explanation,
    ...(item.options || [])
  ].join(' ');

  return `
    <article class="wrong-card" data-source="${escapeAttr(entry.exam.href)}" data-search="${escapeAttr(searchText)}" data-entry-key="${escapeAttr(entryKey(entry))}">
      <div class="wrong-card-header">
        <div>
          <div class="source-title">${escapeHtml(entry.exam.title || entry.course.meta.title || entry.exam.href)}</div>
          <div class="source-meta">${escapeHtml(entry.exam.tag || '')} · 題號 ${escapeHtml(item.id)} · 首次入庫 ${escapeHtml(missedAt)}</div>
        </div>
        <span class="question-type">${typeLabel}</span>
      </div>
      <div class="wrong-card-body">
        <p class="question">${escapeHtml(item.q || '')}</p>
        <div class="options">
          ${(item.options || []).map((option, optionIndex) => `
            <div class="option ${correctAnswers.includes(optionIndex) ? 'correct' : ''}">
              <span class="option-marker">${String.fromCharCode(65 + optionIndex)}</span>
              <span>${escapeHtml(option)}</span>
            </div>
          `).join('')}
        </div>
        ${item.explanation ? `<div class="explanation">${escapeHtml(item.explanation)}</div>` : ''}
      </div>
      <div class="wrong-card-footer">
        <div class="wrong-state">錯題重練連續答對：${streak} / 2。此總複習頁不會自動出庫。</div>
        <button class="learned-btn" type="button" data-learned-key="${escapeAttr(entryKey(entry))}">我學會了</button>
      </div>
    </article>
  `;
}

function markLearned(key) {
  const index = wrongItems.findIndex(entry => entryKey(entry) === key);
  if (index === -1) return;

  const entry = wrongItems[index];
  const wrongBook = readWrongBook(entry.wrongBookKey);
  delete wrongBook[entry.id];
  localStorage.setItem(entry.wrongBookKey, JSON.stringify(wrongBook));
  wrongItems.splice(index, 1);
  renderSourceOptions();
  renderList();
  applyFilters();
}

function applyFilters() {
  const query = els.search.value.trim().toLowerCase();
  const source = els.sourceFilter.value;
  let visible = 0;

  els.list.querySelectorAll('.wrong-card').forEach(card => {
    const sourceMatch = source === 'all' || card.dataset.source === source;
    const queryMatch = !query || card.dataset.search.toLowerCase().includes(query);
    const show = sourceMatch && queryMatch;
    card.classList.toggle('hidden', !show);
    if (show) visible++;
  });

  updateStats(visible);
  if (wrongItems.length > 0) {
    els.status.classList.toggle('hidden', visible > 0);
    if (visible === 0) setStatus('沒有符合篩選條件的錯題。');
  }
}

function updateStats(visible) {
  const sourceCount = new Set(wrongItems.map(entry => entry.exam.href)).size;
  els.totalCount.textContent = wrongItems.length;
  els.sourceCount.textContent = sourceCount;
  els.visibleCount.textContent = visible;
}

function setStatus(message) {
  els.status.textContent = message;
  els.status.classList.remove('hidden');
}

function entryKey(entry) {
  return `${entry.wrongBookKey}::${entry.id}`;
}

function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '未記錄';
  return date.toLocaleString('zh-TW', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escapeAttr(value) {
  return escapeHtml(value).replace(/\n/g, ' ');
}
