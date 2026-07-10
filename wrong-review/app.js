const WRONG_BOOK_SUFFIX = '-wrong-book-v1';
const RENDER_BATCH_SIZE = 80;
const EXAM_SOURCES = [];

let wrongItems = [];
let filteredItems = [];
let renderToken = 0;
let filterTimer = null;

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
    applyFilters();
  } catch (error) {
    console.error('Load wrong review failed:', error);
    setStatus('載入錯題複習失敗，請重新整理頁面後再試。');
  }
}

function bindEvents() {
  els.search.addEventListener('input', scheduleFilters);
  els.sourceFilter.addEventListener('change', applyFilters);
  els.list.addEventListener('click', event => {
    const button = event.target.closest('[data-learned-key]');
    if (!button) return;
    markLearned(button.dataset.learnedKey);
  });
}

async function collectWrongItems() {
  setStatus('正在整理錯題紀錄...');

  const exams = getReviewableExams();
  const wrongBookEntries = getWrongBookEntries();
  const examsWithWrongBooks = exams
    .map(exam => ({
      exam,
      wrongBooks: wrongBookEntries.filter(entry => isWrongBookForExam(entry, exam))
    }))
    .filter(entry => entry.wrongBooks.length > 0);

  if (!examsWithWrongBooks.length) return;

  let loaded = 0;
  for (const { exam, wrongBooks } of examsWithWrongBooks) {
    loaded += 1;
    setStatus(`正在載入錯題來源 ${loaded} / ${examsWithWrongBooks.length}...`);

    const course = await loadCourse(exam);
    if (!course || !course.meta || !Array.isArray(course.quiz)) continue;

    const quizById = new Map(course.quiz.map(item => [String(item.id), item]));
    for (const wrongBookEntry of wrongBooks) {
      for (const id of Object.keys(wrongBookEntry.wrongBook)) {
        const item = quizById.get(String(id));
        if (!item || item.type === 'text') continue;

        wrongItems.push(createWrongEntry({
          id,
          item,
          exam,
          course,
          wrongBookEntry
        }));
      }
    }
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

function getWrongBookEntries() {
  const entries = [];
  for (let index = 0; index < localStorage.length; index += 1) {
    const key = localStorage.key(index);
    if (!key || !key.endsWith(WRONG_BOOK_SUFFIX)) continue;

    const wrongBook = readWrongBook(key);
    if (!Object.keys(wrongBook).length) continue;

    entries.push({
      key,
      storeKey: key.slice(0, -WRONG_BOOK_SUFFIX.length),
      wrongBook
    });
  }
  return entries;
}

function isWrongBookForExam(entry, exam) {
  const slug = String(exam.href || '').replace(/\/$/, '');
  return Boolean(slug) && entry.storeKey.startsWith(`${slug}-`);
}

function createWrongEntry({ id, item, exam, course, wrongBookEntry }) {
  const wrongMeta = wrongBookEntry.wrongBook[id] || {};
  return {
    id,
    item,
    exam,
    course,
    wrongBookKey: wrongBookEntry.key,
    wrongMeta,
    key: `${wrongBookEntry.key}::${id}`,
    searchText: [
      exam.title,
      exam.tag,
      course.meta && course.meta.title,
      item.q,
      item.explanation,
      ...(item.options || [])
    ].join(' ').toLowerCase()
  };
}

async function loadCourse(exam) {
  const href = exam.href || '';
  if (!href) return null;

  const scriptUrl = `../${href.replace(/\/?$/, '/')}course-data.js`;
  return new Promise(resolve => {
    const previous = window.COURSE;
    const script = document.createElement('script');
    script.src = `${scriptUrl}?review=${Date.now()}`;
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

function scheduleFilters() {
  window.clearTimeout(filterTimer);
  filterTimer = window.setTimeout(applyFilters, 120);
}

function applyFilters() {
  const query = els.search.value.trim().toLowerCase();
  const source = els.sourceFilter.value;

  filteredItems = wrongItems.filter(entry => {
    const sourceMatch = source === 'all' || entry.exam.href === source;
    const queryMatch = !query || entry.searchText.includes(query);
    return sourceMatch && queryMatch;
  });

  updateStats(filteredItems.length);
  renderList(filteredItems);
}

function renderList(items) {
  renderToken += 1;
  const currentToken = renderToken;

  if (!wrongItems.length) {
    els.list.innerHTML = '';
    setStatus('目前沒有錯題。作答錯誤的題目會自動收進這裡。');
    updateStats(0);
    return;
  }

  if (!items.length) {
    els.list.innerHTML = '';
    setStatus('沒有符合篩選條件的錯題。');
    return;
  }

  els.status.classList.add('hidden');
  els.list.innerHTML = '';

  let index = 0;
  const appendBatch = deadline => {
    if (currentToken !== renderToken) return;

    const html = [];
    const batchEnd = Math.min(index + RENDER_BATCH_SIZE, items.length);
    while (index < batchEnd) {
      html.push(renderWrongCard(items[index]));
      index += 1;
    }

    els.list.insertAdjacentHTML('beforeend', html.join(''));
    if (index < items.length) {
      requestRenderCallback(appendBatch);
    }
  };

  requestRenderCallback(appendBatch);
}

function requestRenderCallback(callback) {
  if ('requestIdleCallback' in window) {
    window.requestIdleCallback(callback, { timeout: 120 });
    return;
  }
  window.setTimeout(() => callback({ timeRemaining: () => 0 }), 0);
}

function renderWrongCard(entry) {
  const item = entry.item;
  const correctAnswers = Array.isArray(item.answer) ? item.answer : [item.answer];
  const typeLabel = item.type === 'multiple' ? '複選題' : '單選題';
  const streak = Number(entry.wrongMeta.correctStreak || 0);
  const missedAt = entry.wrongMeta.missedAt ? formatDate(entry.wrongMeta.missedAt) : '未記錄';

  return `
    <article class="wrong-card" data-source="${escapeAttr(entry.exam.href)}" data-entry-key="${escapeAttr(entry.key)}">
      <div class="wrong-card-header">
        <div>
          <div class="source-title">${escapeHtml(entry.exam.title || entry.course.meta.title || entry.exam.href)}</div>
          <div class="source-meta">${escapeHtml(entry.exam.tag || '')} ・ 題號 ${escapeHtml(item.id)} ・ 最近答錯 ${escapeHtml(missedAt)}</div>
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
        <div class="wrong-state">連續答對進度：${streak} / 2。達標後可從錯題本移除。</div>
        <button class="learned-btn" type="button" data-learned-key="${escapeAttr(entry.key)}">標記已學會</button>
      </div>
    </article>
  `;
}

function markLearned(key) {
  const index = wrongItems.findIndex(entry => entry.key === key);
  if (index === -1) return;

  const entry = wrongItems[index];
  const wrongBook = readWrongBook(entry.wrongBookKey);
  delete wrongBook[entry.id];
  localStorage.setItem(entry.wrongBookKey, JSON.stringify(wrongBook));

  wrongItems.splice(index, 1);
  refreshSourceOptionsAfterRemoval();
  applyFilters();
}

function refreshSourceOptionsAfterRemoval() {
  const currentSource = els.sourceFilter.value;
  const sourceMap = new Map();
  wrongItems.forEach(entry => sourceMap.set(entry.exam.href, entry.exam));
  EXAM_SOURCES.splice(0, EXAM_SOURCES.length, ...sourceMap.values());
  renderSourceOptions();

  if (currentSource === 'all' || sourceMap.has(currentSource)) {
    els.sourceFilter.value = currentSource;
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
