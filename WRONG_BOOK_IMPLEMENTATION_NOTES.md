# 錯題庫功能實作筆記

本文件記錄本次「錯題庫 / 錯題重練 / 手機接續同步錯題庫」功能的實作方式。功能先在 `web/100-baking/` 驗證，確認後已批次套用到所有線上測驗資料夾，排除 `*-print/` 列印工具。本文也保留可整理成 Codex skill 的步驟。

## 需求摘要

使用者在一般線上測驗中作答錯誤時，答錯的題目要自動加入錯題庫。

使用者進入「錯題重練」時，只顯示錯題庫中的題目。

同一題在錯題重練中連續答對 2 次後，自動從錯題庫移除。

如果錯題重練中答錯，該題保留在錯題庫，且連續答對次數歸零。

本次實作範圍：

- 原始驗證樣板：`web/100-baking/`
- 批次套用範圍：`web/` 下所有具有 `index.html` 與 `course-data.js`、且資料夾名稱不是 `*-print` 的線上測驗。
- 每份測驗修改檔案：
  - `{exam-folder}/index.html`
  - `{exam-folder}/style.css`
- 錯題庫目前只納入選擇題：
  - `single`
  - `multiple`
- 非選擇題 / 手寫題：
  - `text`
  - 本次不納入錯題庫

## 原始頁面架構

這批線上測驗頁多數是單頁靜態 HTML，主要邏輯直接寫在 `index.html` 的 `<script>` 中。

常見狀態結構：

```js
const STORE_KEY = (window.COURSE && window.COURSE.meta && window.COURSE.meta.storeKey)
  ? window.COURSE.meta.storeKey
  : '100-baking-progress-v1';

const store = {
  load() { ... },
  save(s) { localStorage.setItem(STORE_KEY, JSON.stringify(s)); },
  reset() { ... }
};

let state = store.load();
state.gradedQuestions = state.gradedQuestions || {};
```

一般測驗使用 `state` 保存：

```js
{
  tasks: {},
  quiz: {},
  textAnswers: {},
  graded: false,
  gradedQuestions: {},
  lastSection: ''
}
```

選擇題作答存在：

```js
state.quiz[itemId]
```

已批改題目存在：

```js
state.gradedQuestions[itemId]
```

整份試卷已送出存在：

```js
state.graded
```

## 手機接續同步錯題庫

本次後續補強：手機接續同步時，錯題庫也必須一起帶到同步 payload。

原本同步格式是舊版字串：

```text
answers:timeRemaining:graded
```

此格式只同步：

- 選擇題答案
- 剩餘時間
- 是否已批改

缺點：

- 不包含錯題庫。
- 不包含完整 `state.textAnswers`。
- 複選題答案若是 array，會被字串化，格式不夠穩。
- 未來擴充欄位困難。

本次改成新版 `v2:` JSON payload：

```js
{
  version: 2,
  state: {
    tasks: state.tasks || {},
    quiz: state.quiz || {},
    textAnswers: state.textAnswers || {},
    graded: !!state.graded,
    gradedQuestions: state.gradedQuestions || {},
    lastSection: state.lastSection || ''
  },
  timeRemaining: parseInt(timeVal, 10),
  wrongBook: wrongBook || {}
}
```

壓縮輸出：

```js
return `v2:${encodeURIComponent(JSON.stringify(payload))}`;
```

同步 URL 仍沿用既有 hash：

```js
const syncUrl = `${window.location.origin}${window.location.pathname}#sync=${encodeURIComponent(code)}`;
```

所以實際會被 encode 兩層：

1. `compressState()` 內 encode JSON payload。
2. `generateSyncQR()` 放入 URL hash 時再 encode 一次。

解析時要先：

```js
const decoded = decodeURIComponent(str);
```

再判斷：

```js
if (decoded.startsWith('v2:')) {
  const payload = JSON.parse(decodeURIComponent(decoded.slice(3)));
  ...
}
```

### 向後相容

`decompressState()` 保留舊格式解析：

```js
const parts = decoded.split(':');
if (parts.length < 3) return null;
```

這樣舊的 `#sync=` 連結仍可載入，只是舊連結沒有錯題庫資料，因此回傳：

```js
wrongBook: {}
```

### 載入同步資料時寫入錯題庫

在 `store.load()` 解析 sync hash 後，除了保存主作答狀態與剩餘時間，也要保存錯題庫：

```js
if (decompressed.wrongBook) {
  localStorage.setItem(WRONG_BOOK_KEY, JSON.stringify(decompressed.wrongBook));
}
```

這段發生在：

```js
let state = store.load();
```

期間。因為 `wrongBookStore.load()` 會在後面讀取 `WRONG_BOOK_KEY`，所以同步載入時先寫入 localStorage，後續：

```js
let wrongBook = wrongBookStore.load();
```

就會拿到同步過來的錯題庫。

### 同步文案

手機接續 modal 文案也要更新，明確告知會同步：

- 答題進度
- 計時時間
- 錯題庫

範例：

```text
請使用手機相機或 LINE 掃描下方二維碼，即可同步您目前的答題進度、計時時間與錯題庫，在手機上繼續測驗與重練。
```

### QR Code 長度注意

新版 payload 會比舊格式長，尤其錯題庫很多時 QR Code 會更密。

目前仍使用：

```js
correctLevel : QRCode.CorrectLevel.M
```

若彙總題庫錯題很多，可能需要評估：

- 降低同步 payload，只同步必要欄位。
- 改用短碼服務或後端儲存。
- 提供「手動複製連結」作為 QR 掃描失敗時的 fallback。

目前頁面已有手動複製連結，因此可先接受。

## 新增資料結構

### 錯題庫 localStorage key

新增：

```js
const WRONG_BOOK_KEY = `${STORE_KEY}-wrong-book-v1`;
```

設計理由：

- 使用每份試卷自己的 `STORE_KEY` 衍生錯題庫 key。
- 避免不同試卷的錯題庫互相污染。
- 保留版本尾碼 `v1`，後續資料格式若改版，可以建立 `v2`。

### wrongBook

新增：

```js
let wrongBook = wrongBookStore.load();
```

錯題庫資料格式：

```js
{
  "q1": {
    "correctStreak": 0,
    "missedAt": "2026-07-10T03:00:00.000Z",
    "lastPracticedAt": "2026-07-10T03:05:00.000Z"
  },
  "q2": {
    "correctStreak": 1,
    "missedAt": "2026-07-10T03:01:00.000Z",
    "lastPracticedAt": "2026-07-10T03:07:00.000Z"
  }
}
```

欄位說明：

- `correctStreak`：錯題重練中的連續答對次數。
- `missedAt`：首次進入錯題庫的時間。
- `lastPracticedAt`：最近一次錯題重練時間。

目前是否在錯題庫中，是由 `wrongBook[item.id]` 是否存在判斷。

### wrongPracticeMode

新增：

```js
let wrongPracticeMode = false;
```

用途：

- `false`：一般完整試卷模式。
- `true`：錯題重練模式，只渲染錯題庫題目。

### wrongPracticeState

新增：

```js
let wrongPracticeState = { quiz: {}, gradedQuestions: {} };
```

用途：

- 錯題重練使用獨立暫存作答狀態。
- 不使用原本的 `state.quiz`，避免一般測驗已作答或已批改狀態讓錯題重練題卡鎖住。
- 每次進入 / 離開錯題重練會重設。
- 每次錯題重練判題後也會重設，方便同一題繼續下一輪練習。

## 新增 store

新增 `wrongBookStore`：

```js
const wrongBookStore = {
  load() {
    try {
      return JSON.parse(localStorage.getItem(WRONG_BOOK_KEY)) || {};
    } catch {
      return {};
    }
  },
  save(book) {
    localStorage.setItem(WRONG_BOOK_KEY, JSON.stringify(book));
  },
  reset() {
    localStorage.removeItem(WRONG_BOOK_KEY);
  }
};
```

### 清除紀錄整合

原本 `store.reset()` 只清：

```js
localStorage.removeItem(STORE_KEY);
localStorage.removeItem(`${STORE_KEY}-time-remaining`);
```

本次新增：

```js
localStorage.removeItem(WRONG_BOOK_KEY);
```

讓頁面上的「清除所有紀錄」同時清掉：

- 一般作答紀錄
- 計時器
- 錯題庫

## 新增核心函式

### `getWrongBookItems()`

```js
function getWrongBookItems() {
  const quizItems = window.COURSE.quiz || [];
  return quizItems.filter(item => item.type !== 'text' && wrongBook[item.id]);
}
```

用途：

- 從完整題庫中篩出目前錯題庫題目。
- 排除 `text` 題型。
- 保留原本題目順序。

### `getWrongBookCount()`

```js
function getWrongBookCount() {
  return Object.keys(wrongBook).length;
}
```

用途：

- 顯示錯題庫數量。
- 判斷錯題重練按鈕是否 disabled。
- 批改後顯示剩餘錯題數。

### `renderWrongBookPanel(count)`

新增錯題庫 UI 面板，放在測驗區標題與 score card 之間。

面板包含：

- 狀態標題：
  - `錯題庫`
  - `錯題重練中`
- 說明文字。
- `錯題重練` / `返回完整試卷` 按鈕。
- `清空錯題庫` 按鈕。

按鈕重點：

```js
disabled: count === 0 && !wrongPracticeMode
```

錯題庫空時不可進入錯題重練。

### `getWrongBookSummaryText(count)`

依目前錯題數產生說明文字：

- 0 題：提示答錯會自動加入。
- 大於 0 題：顯示待重練題數，提醒連續答對 2 次出庫。

### `updateWrongBookSummary()`

更新面板文字與按鈕 enabled / disabled 狀態。

這個函式很重要，因為一般測驗中答錯入庫時，面板已經存在於 DOM 中。如果只更新 `wrongBook`，但不更新按鈕狀態，`錯題重練` 按鈕會停留在 disabled。

本次測試曾抓到這個問題，後來補上：

```js
const practiceBtn = document.getElementById('wrongPracticeBtn');
if (practiceBtn) practiceBtn.disabled = count === 0 && !wrongPracticeMode;

const clearBtn = document.getElementById('clearWrongBookBtn');
if (clearBtn) clearBtn.disabled = count === 0;
```

### `toggleWrongPracticeMode()`

切換一般試卷 / 錯題重練模式。

```js
function toggleWrongPracticeMode() {
  wrongPracticeMode = !wrongPracticeMode;
  wrongPracticeState = { quiz: {}, gradedQuestions: {} };
  rerenderQuizSection();
  showToast(wrongPracticeMode ? '已進入錯題重練。' : '已返回完整試卷。');
}
```

重點：

- 切換模式時重設 `wrongPracticeState`。
- 使用 `rerenderQuizSection()` 重新渲染整個測驗區。

### `clearWrongBook()`

清空錯題庫。

```js
function clearWrongBook() {
  wrongBook = {};
  wrongBookStore.reset();
  wrongPracticeMode = false;
  wrongPracticeState = { quiz: {}, gradedQuestions: {} };
  rerenderQuizSection();
  showToast('錯題庫已清空。');
}
```

清空後強制回到完整試卷模式。

### `rerenderQuizSection()`

只重新渲染 `#quiz` 區塊，不重載整頁。

```js
function rerenderQuizSection() {
  const oldQuiz = document.getElementById('quiz');
  const newQuiz = renderQuiz();
  if (oldQuiz && newQuiz) {
    oldQuiz.replaceWith(newQuiz);
    updateProgressUI();
  }
}
```

用途：

- 進入錯題重練。
- 返回完整試卷。
- 清空錯題庫。
- 錯題重練判題後刷新題卡。

### `hasChoiceAnswer(item, given)`

判斷使用者是否已作答。

```js
function hasChoiceAnswer(item, given) {
  if (!item) return false;
  if (item.type === 'single') return given !== undefined;
  if (item.type === 'multiple') return Array.isArray(given) && given.length > 0;
  return false;
}
```

用途：

- 整份試卷送出時，只把「有作答且答錯」的題目加入錯題庫。
- 錯題重練送出時，只批改已作答題目。

設計取捨：

- 未作答題目在整卷送出時不自動加入錯題庫。
- 如果產品需求改成「未作答也算錯題」，這裡與 `gradeQuiz()` 的呼叫條件要調整。

### `recordChoiceResult(item, isCorrect, isPractice)`

錯題庫核心狀態轉移函式。

參數：

- `item`：題目物件。
- `isCorrect`：本次是否答對。
- `isPractice`：
  - `false`：一般測驗模式。
  - `true`：錯題重練模式。

一般測驗模式：

- 答錯：加入錯題庫，`correctStreak = 0`。
- 答對：不處理。

錯題重練模式：

- 答對：
  - `correctStreak + 1`
  - 若達 2，從錯題庫刪除。
  - 若未達 2，保留題目並保存 streak。
- 答錯：
  - 保留題目。
  - `correctStreak = 0`
  - 更新 `lastPracticedAt`。

回傳值：

- `true`：該題已出庫。
- `false`：該題仍留在錯題庫，或一般模式未出庫。

這個回傳值用於判斷是否需要刷新錯題重練列表。

## 修改 `renderQuiz()`

原本 `renderQuiz()` 固定渲染：

```js
const items = window.COURSE.quiz || [];
```

本次改成：

```js
const items = window.COURSE.quiz || [];
const wrongItems = getWrongBookItems();
const visibleItems = wrongPracticeMode ? wrongItems : items;
```

然後把原本：

```js
items.forEach(...)
```

改成：

```js
visibleItems.forEach(...)
```

### 依模式切換文案

一般模式：

```text
請在此進行線上答題。選擇題會自動批改...
```

錯題重練模式：

```text
錯題重練只會顯示目前錯題庫內的選擇題。每題連續答對 2 次後會自動從錯題庫移除。
```

### 插入錯題庫面板

```js
const wrongPanel = renderWrongBookPanel(wrongItems.length);
root.append(wrongPanel);
```

### 空狀態

錯題重練模式且沒有題目時：

```js
container.append(el('div', { class: 'wrong-book-empty' }, '目前沒有錯題。一般測驗答錯的題目會自動加入錯題庫。'));
```

### 作答來源切換

原本選項是否選中、題卡是否已批改，全部看 `state`。

本次改成依模式切換：

```js
const answerSource = wrongPracticeMode ? wrongPracticeState.quiz : state.quiz;
const gradedSource = wrongPracticeMode ? wrongPracticeState.gradedQuestions : state.gradedQuestions;
const isGraded = wrongPracticeMode
  ? !!gradedSource[item.id]
  : (state.graded || (gradedSource && gradedSource[item.id]));
```

這是整個功能最重要的改動之一。

如果錯題重練也使用 `state.quiz` / `state.gradedQuestions`，會發生兩個問題：

- 原本一般測驗作答過的題目在錯題重練中直接顯示舊答案。
- 原本已批改的題目在錯題重練中會被鎖住，無法重新練習。

### 送出按鈕文案

一般模式：

```text
送出答案與評分
```

錯題重練模式：

```text
送出本次錯題重練
```

## 修改單題作答流程

### `selectSingleOption(itemId, optIdx)`

原本直接寫入：

```js
state.quiz[itemId] = optIdx;
state.gradedQuestions[itemId] = true;
store.save(state);
gradeSingleQuestion(itemId, optIdx);
```

本次改成依模式選擇狀態來源：

```js
const quizState = wrongPracticeMode ? wrongPracticeState.quiz : state.quiz;
const gradedState = wrongPracticeMode ? wrongPracticeState.gradedQuestions : state.gradedQuestions;
```

鎖定條件：

```js
if ((!wrongPracticeMode && state.graded) || gradedState[itemId]) return;
```

保存策略：

```js
if (!wrongPracticeMode) store.save(state);
```

錯題重練的暫存答案不寫入 localStorage。

判題時傳入目前是否是錯題重練：

```js
gradeSingleQuestion(itemId, optIdx, wrongPracticeMode);
```

### `toggleMultipleOption(itemId, optIdx)`

同樣改成依模式寫入：

```js
const quizState = wrongPracticeMode ? wrongPracticeState.quiz : state.quiz;
```

錯題重練模式不保存到 `store`。

### `confirmMultipleAnswer(itemId)`

複選題需要按「確認選項並看解析」才判題。

本次改動：

- 依模式取 `quizState` / `gradedState`。
- 錯題重練不寫入 `store`。
- 呼叫：

```js
gradeMultipleQuestion(itemId, wrongPracticeMode);
```

## 修改判題函式

### `gradeSingleQuestion(itemId, optIdx, isPractice = false)`

新增 `isPractice` 參數。

判斷正確性：

```js
const isCorrect = optIdx === correct;
```

判題後呼叫：

```js
const removedFromWrongBook = recordChoiceResult(item, isCorrect, isPractice);
```

如果在錯題重練模式，判題後短暫顯示結果，再刷新題卡：

```js
if ((removedFromWrongBook || isPractice) && wrongPracticeMode) {
  setTimeout(() => {
    wrongPracticeState = { quiz: {}, gradedQuestions: {} };
    rerenderQuizSection();
  }, 700);
}
```

為什麼需要刷新：

- 錯題重練中，單題判題後題卡會被標記為 `data-graded="true"`。
- 如果不刷新，該題會被鎖住，使用者無法立刻進行第二次練習。
- 刷新前保留 700ms，讓使用者看得到答對 / 答錯與詳解狀態。

本次測試曾抓到「第一輪答對後題卡仍鎖住」問題，因此補上刷新前清空 `wrongPracticeState`。

### `gradeMultipleQuestion(itemId, isPractice = false)`

新增 `isPractice` 參數。

取答案時依模式切換：

```js
const given = wrongPracticeMode
  ? (wrongPracticeState.quiz[itemId] || [])
  : (state.quiz[itemId] || []);
```

複選題正確性沿用原本邏輯：

```js
let k = 0;
const optionCount = item.options ? item.options.length : 4;
for (let oIdx = 0; oIdx < optionCount; oIdx++) {
  const chosen = given.includes(oIdx);
  const shouldChoose = correct.includes(oIdx);
  if (chosen !== shouldChoose) k++;
}

const isCorrect = k === 0;
```

判題後同樣呼叫：

```js
const removedFromWrongBook = recordChoiceResult(item, isCorrect, isPractice);
```

錯題重練模式判題後也會刷新題卡。

## 修改整份試卷送出流程

### `gradeQuiz()`

函式最前面新增分流：

```js
if (wrongPracticeMode) {
  gradeWrongPractice();
  return;
}
```

這避免錯題重練時誤觸原本整份試卷送出，導致：

- 完整試卷被設為 `state.graded = true`
- 所有題目被鎖住
- 一般作答紀錄被污染

### 一般模式下加入錯題庫

單選題：

```js
if (hasChoiceAnswer(item, given)) {
  recordChoiceResult(item, given === correct, false);
}
```

複選題：

```js
if (hasChoiceAnswer(item, given)) {
  recordChoiceResult(item, k === 0, false);
}
```

注意：

- 只有已作答題目會被記錄。
- 答錯才會加入錯題庫。
- 答對不會從錯題庫移除，因為出庫規則只在錯題重練中生效。

## 新增錯題重練送出流程

### `gradeWrongPractice()`

用途：

- 在錯題重練模式下，批改本次尚未逐題批改的題目。
- 顯示本次錯題重練摘要。

流程：

1. 取得目前錯題：

```js
const quizItems = getWrongBookItems();
```

2. 沒有錯題就提示：

```js
showToast('目前沒有錯題可重練。');
```

3. 逐題檢查是否已作答且尚未批改：

```js
if (!hasChoiceAnswer(item, wrongPracticeState.quiz[item.id]) || wrongPracticeState.gradedQuestions[item.id]) {
  return;
}
```

4. 依題型呼叫單題判題：

```js
if (item.type === 'single') {
  gradeSingleQuestion(item.id, wrongPracticeState.quiz[item.id], true);
} else if (item.type === 'multiple') {
  gradeMultipleQuestion(item.id, true);
}
```

5. 顯示摘要：

```js
scoreCard.append(el('h3', {}, '錯題重練已送出'));
scoreCard.append(el('div', { class: 'score-detail' }, `本次批改 ${answered} 題，目前錯題庫剩餘 ${remaining} 題。連續答對 2 次的題目會自動出庫。`));
```

## 新增 CSS

新增位置：`web/100-baking/style.css`

選擇插在 `.quiz-container` 之後，因為錯題庫面板屬於測驗區 UI。

新增 class：

```css
.wrong-book-panel
.wrong-book-title
.wrong-book-desc
.wrong-book-actions
.wrong-book-btn
.wrong-book-btn.secondary
.wrong-book-btn:disabled
.wrong-book-empty
```

UI 設計目的：

- 面板用 `border-left: 4px solid var(--accent)`，和既有設計 token 保持一致。
- 按鈕使用既有 `var(--accent)`、`var(--danger)`、`var(--surface)`。
- 空狀態使用 dashed border，避免看起來像錯誤訊息。
- 按鈕 disabled 時降低透明度，讓狀態清楚。

## 使用者流程

### 一般測驗答錯入庫

1. 使用者在完整試卷模式作答。
2. 單選題點選後立即判題。
3. 複選題按「確認選項並看解析」後判題。
4. 若答案錯誤：
   - `recordChoiceResult(item, false, false)`
   - 寫入 `wrongBook[item.id]`
   - `correctStreak = 0`
5. 面板更新錯題數。
6. `錯題重練` 按鈕變成可點擊。

### 進入錯題重練

1. 使用者點 `錯題重練`。
2. `wrongPracticeMode = true`
3. `wrongPracticeState` 清空。
4. `renderQuiz()` 改渲染 `getWrongBookItems()`。
5. 頁面只顯示錯題庫中的選擇題。

### 錯題重練答對一次

1. 使用者答對。
2. `correctStreak` 從 0 變 1。
3. 顯示 toast：`答對了！此題連續答對 1 / 2 次。`
4. 700ms 後刷新錯題重練列表。
5. 題目仍保留，可再次練習。

### 錯題重練連續答對兩次

1. 使用者再次答對同一題。
2. `correctStreak` 變 2。
3. `delete wrongBook[item.id]`
4. 寫回 localStorage。
5. 顯示 toast：`已連續答對 2 次，這題已從錯題庫移除。`
6. 700ms 後刷新列表。
7. 該題不再顯示。

### 錯題重練答錯

1. 使用者答錯。
2. 題目保留在錯題庫。
3. `correctStreak = 0`
4. 顯示 toast：`本題仍在錯題庫，連續答對次數已歸零。`
5. 700ms 後刷新列表。

## 驗證方式

本次實作後做過以下驗證：

### 靜態語法檢查

用 Node 抽出主 `<script>`，檢查語法：

```powershell
node -e "const fs=require('fs'); const html=fs.readFileSync('web/100-baking/index.html','utf8'); const scripts=[...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]); new Function(scripts[scripts.length-1]); console.log('main inline script syntax ok');"
```

### 本地伺服器檢查

啟動：

```powershell
cd D:\Aaron-agy\onlineExam_Source\web\100-baking
node dev-server.js
```

確認：

```text
http://localhost:3456/
```

可正常回應。

### Playwright 互動測試

實測流程：

1. 清空 localStorage。
2. 找第一題單選題。
3. 故意點錯答案。
4. 確認錯題庫 localStorage 筆數為 1。
5. 點 `錯題重練`。
6. 點正確答案第一次。
7. 確認錯題庫筆數仍為 1。
8. 點正確答案第二次。
9. 確認錯題庫筆數變 0。

測試曾抓到兩個實作問題：

- 答錯入庫後，`錯題重練` 按鈕仍 disabled。
  - 修正方式：`updateWrongBookSummary()` 同步更新按鈕 disabled 狀態。
- 錯題重練第一次答對後題卡被鎖住，無法第二次作答。
  - 修正方式：判題後清空 `wrongPracticeState` 並重新渲染測驗區。

## 套用到其他試卷的步驟

目前本批 `web/` 內線上測驗已套用完成。本節保留給未來新增試卷、重新產生試卷，或整理成 skill 時使用。

### 1. 找到共同插入點

目標檔案通常是：

```text
{exam-folder}/index.html
```

先確認是否有這些函式或等價函式：

```js
renderQuiz()
selectSingleOption()
toggleMultipleOption()
confirmMultipleAnswer()
gradeSingleQuestion()
gradeMultipleQuestion()
gradeQuiz()
store.reset()
```

有些試卷可能略有差異，要依當份檔案調整。

### 2. 新增錯題庫 key 與 store

在 `STORE_KEY` 後新增：

```js
const WRONG_BOOK_KEY = `${STORE_KEY}-wrong-book-v1`;
```

在 `store.reset()` 加：

```js
localStorage.removeItem(WRONG_BOOK_KEY);
```

在 `state` 初始化後新增：

```js
const wrongBookStore = { ... };
let wrongBook = wrongBookStore.load();
let wrongPracticeMode = false;
let wrongPracticeState = { quiz: {}, gradedQuestions: {} };
```

### 3. 新增錯題庫 helper functions

把以下函式插在 `renderQuiz()` 前：

```js
getWrongBookItems()
getWrongBookCount()
renderWrongBookPanel()
getWrongBookSummaryText()
updateWrongBookSummary()
toggleWrongPracticeMode()
clearWrongBook()
rerenderQuizSection()
hasChoiceAnswer()
recordChoiceResult()
```

### 4. 修改 `renderQuiz()`

把固定渲染全部題目改成：

```js
const wrongItems = getWrongBookItems();
const visibleItems = wrongPracticeMode ? wrongItems : items;
```

插入錯題庫面板：

```js
root.append(renderWrongBookPanel(wrongItems.length));
```

把 `items.forEach` 改為 `visibleItems.forEach`。

把選項狀態來源從 `state.quiz` 改成：

```js
const answerSource = wrongPracticeMode ? wrongPracticeState.quiz : state.quiz;
```

把已批改來源從 `state.gradedQuestions` 改成：

```js
const gradedSource = wrongPracticeMode ? wrongPracticeState.gradedQuestions : state.gradedQuestions;
```

### 5. 修改作答 handler

讓單選、複選、確認複選都依 `wrongPracticeMode` 切換狀態來源。

一般模式才 `store.save(state)`。

呼叫判題函式時傳入：

```js
wrongPracticeMode
```

### 6. 修改判題函式

`gradeSingleQuestion()` 與 `gradeMultipleQuestion()` 加 `isPractice = false` 參數。

判題後呼叫：

```js
recordChoiceResult(item, isCorrect, isPractice);
```

錯題重練模式下判題後刷新列表。

### 7. 修改 `gradeQuiz()`

函式最前面加：

```js
if (wrongPracticeMode) {
  gradeWrongPractice();
  return;
}
```

一般模式下，對已作答的選擇題呼叫：

```js
recordChoiceResult(item, isCorrect, false);
```

### 8. 新增 `gradeWrongPractice()`

負責錯題重練模式的送出與摘要。

### 9. 新增 CSS

把 `.wrong-book-*` 樣式加入該試卷的 `style.css`。

建議插在 `.quiz-container` 附近。

## 批次套用時的注意事項

### 不要改 `STORE_KEY`

錯題庫 key 是從 `STORE_KEY` 衍生。

如果更改 `STORE_KEY`，使用者原有作答紀錄會失效。

### 不要改題目 `id`

錯題庫以題目 `id` 當 key。

如果更改題目 `id`，舊錯題紀錄會找不到題目。

### 題型差異

目前只處理：

```js
item.type === 'single'
item.type === 'multiple'
```

不處理：

```js
item.type === 'text'
```

如果其他試卷有不同題型名稱，需要先 mapping。

### 複選題確認流程

部分試卷可能沒有 `confirmMultipleAnswer()`，或複選題可能也是即時批改。

套用時要依該試卷實際流程接入 `recordChoiceResult()`。

### 彙總題庫效能

彙總題庫可能有 700 題以上。

目前錯題重練每次透過：

```js
window.COURSE.quiz.filter(...)
```

對目前規模可以接受。

若未來題數更大或互動變慢，可建立 `Map`：

```js
const quizById = new Map(window.COURSE.quiz.map(item => [item.id, item]));
```

但這次試作沒有引入額外索引，以降低改動面。

### 已批改整卷後的錯題重練

錯題重練使用 `wrongPracticeState`，不依賴 `state.graded`，所以即使完整試卷已送出，仍可進入錯題重練。

這是刻意設計。

### 未作答是否入庫

目前未作答不入庫。

如果需求改成「送出整卷時未作答也算錯」，要調整：

```js
if (hasChoiceAnswer(item, given)) {
  recordChoiceResult(...)
}
```

移除 `hasChoiceAnswer` 限制，或改成依需求判定。

### 答對是否可自動移除既有錯題

目前只有在錯題重練模式連續答對 2 次才出庫。

一般測驗中答對同一題不會把它從錯題庫移除。

這符合「進入錯誤重練時，連續答對2次自動出庫」的需求。

若未來希望完整試卷答對也計入 streak，需要在一般模式下也對 `isCorrect` 分支處理。

## 建議 skill 化規則

如果要把此功能寫成 skill，建議 skill 流程如下：

1. 掃描目標資料夾中的 `index.html` 與 `style.css`。
2. 確認是否存在 `STORE_KEY`、`renderQuiz()`、`gradeQuiz()`。
3. 確認題型資料結構：
   - 單選答案：`item.answer` 是 number。
   - 複選答案：`item.answer` 是 number array。
   - 選項：`item.options`。
4. 若已存在 `WRONG_BOOK_KEY`，停止或做 diff-aware 更新，避免重複插入。
5. 插入錯題庫 store 與 state。
6. 插入 helper functions。
7. 修改 `renderQuiz()` 的題目來源與狀態來源。
8. 修改單選、複選、確認複選 handler。
9. 修改單題判題與整卷判題。
10. 新增 `gradeWrongPractice()`。
11. 插入 CSS。
12. 執行語法檢查。
13. 如可用，跑瀏覽器互動測試。
14. 回報改動檔案與驗證結果。

## Skill 驗證腳本建議

可用 Playwright 做最小互動驗證：

1. 開啟目標試卷頁。
2. 清空 localStorage。
3. 找第一題 `single`。
4. 故意選錯。
5. 檢查 `{STORE_KEY}-wrong-book-v1` 有 1 筆。
6. 點 `錯題重練`。
7. 選正確答案。
8. 等待刷新後確認錯題仍存在。
9. 再選一次正確答案。
10. 等待刷新後確認錯題移除。

這個測試可以捕捉兩類常見錯誤：

- 錯題已入庫但 UI 按鈕沒有更新。
- 錯題重練判題後題卡被鎖住，無法連續練習。

## 本次實作檔案定位

### JavaScript

主要位置：

```text
web/100-baking/index.html
```

關鍵符號：

```text
WRONG_BOOK_KEY
wrongBookStore
wrongBook
wrongPracticeMode
wrongPracticeState
getWrongBookItems
renderWrongBookPanel
recordChoiceResult
gradeWrongPractice
```

### CSS

主要位置：

```text
web/100-baking/style.css
```

關鍵 class：

```text
wrong-book-panel
wrong-book-title
wrong-book-desc
wrong-book-actions
wrong-book-btn
wrong-book-empty
```

## 後續可改進方向

- 把錯題庫邏輯抽成共用 JS 檔，減少每份試卷重複貼 code。
- 為大型彙總題庫加入錯題分類或搜尋。
- 顯示每題目前 streak，例如 `1 / 2`。
- 新增「只練尚未答對過的錯題」或「只練最近答錯」篩選。
- 支援匯出 / 匯入錯題庫。
- 手機接續同步時，把錯題庫也納入同步 payload。
- 讓使用者手動把題目加入 / 移出錯題庫。
- 設定出庫門檻，例如 2 次、3 次可調。
