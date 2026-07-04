# 114-4 北北基學測國文模擬考試

> **內容管理**：所有網頁文字（題目、選項、解析、單元說明、入口頁卡片）均集中在 `content.md`。修改它，其他都不用碰。

---

## ✏️ 修改考試內容

**唯一要編輯的檔案：**

```
web/114-4-chinese/content.md
```

---

## 🚀 本地開發（改 MD → 瀏覽器自動刷新）

```powershell
cd web/114-4-chinese
npm run dev
```

瀏覽器開啟 **http://localhost:3456/**，存檔 `content.md` 後頁面自動刷新。

---

## 🔨 Build（更新靜態 JS 資料）

```powershell
cd web/114-4-chinese
npm run build
```

這會重新產生 `course-data.js`（考試頁資料）和 `../portal-data.js`（入口頁資料）。

---

## 🌐 部署到 GitHub Pages

每次修改 `content.md` 後執行：

```powershell
cd web/114-4-chinese
npm run build

# 在 web/ 的 git repo 下 push
cd ..
git add -A
git commit -m "content: update"
git push
```

`course-data.js` 和 `portal-data.js` 都是靜態 JS，直接由 GitHub Pages 提供，無需任何 server-side 功能。

---

## 📁 檔案說明

| 檔案 | 用途 |
|---|---|
| `content.md` | ⭐ **唯一要改的檔案** |
| `course-data.js` | ⚙️ 自動生成，勿手改 |
| `../portal-data.js` | ⚙️ 自動生成，勿手改 |
| `md-to-data.js` | 解析器：content.md → course-data.js |
| `dev-server.js` | 本地 hot-reload dev server（port 3456）|
| `index.html` | 考試頁 SPA（UI 框架，不含文字） |
| `style.css` | 設計系統樣式 |
| `viewer.html` | Markdown 試卷閱讀器 |

---

## 📝 content.md 結構

```
# META          ← 課程基本資訊（標題、計時秒數、學習目標、時程表）
# DAY1          ← 考試單元（單元一/二/三、任務清單、插圖）
# MATERIALS     ← 可下載素材清單
# QUIZ          ← 所有考題（Q1 ～ Q36）
# PORTAL        ← 入口頁（頁面標題 + 考試卡片）
```

---

## 📋 題目格式速查

### 單選題

```markdown
## Q1 · 單選題

題目文字...

- (A) 選項 A
- (B) 選項 B
- (C) 選項 C
- (D) 選項 D

```yaml
answer: A          ← 正確答案字母
unit: day1.u-1
explanation: |
  【答案】(A)
  【解析】...
```
```

### 多選題

```markdown
## Q25 · 多選題

題目文字...

- (A) 選項 A
- (B) 選項 B
- (C) 選項 C
- (D) 選項 D
- (E) 選項 E

```yaml
answer: [B, D, E]  ← 正確答案字母列表
unit: day1.u-2
explanation: |
  【答案】(B)(D)(E)
  【解析】...
```
```

### 手寫 / 非選擇題

```markdown
## Q34 · 手寫混合題

題目文字...

```yaml
type: text
unit: day1.u-3
subQuestions:
  - label: "① 問題一（字數限制）"
    placeholder: 提示文字
  - label: "② 問題二（字數限制）"
    placeholder: 提示文字
answer:
  "0": 第一格參考答案
  "1": 第二格參考答案
explanation: |
  【評分標準】...
```
```

---

## 🔧 META 區段常用欄位

| 欄位 | 說明 | 範例 |
|---|---|---|
| `title` | 考試標題 | `北北基 114 學年度學測國文模擬考試` |
| `subtitle` | 考試副標 | `國語文綜合能力測驗線上考場` |
| `storeKey` | localStorage 鍵（唯一識別） | `peipeiki-114-chinese-mock-progress-v1` |
| `timerSeconds` | 考試秒數 | `5400`（= 90 分鐘）|
| `instructions` | 作答說明文字（可選）| 空白則使用預設值 |
| `format` | 考試時間說明 | `線上自主練習 / 90 分鐘限時挑戰` |

---

## ➕ 如何新增試卷

1. 在 `web/` 下建立新資料夾，例如 `web/114-4-english/`。
2. 將 `114-4-chinese/` 的下列檔案複製過去：
   `index.html`、`style.css`、`viewer.html`、`package.json`、`md-to-data.js`、`dev-server.js`
3. 建立新的 `content.md`，填寫 `# META`、`# DAY1`、`# QUIZ`、`# PORTAL` 區段。
4. 執行 `npm run build`。
5. 在 `114-4-chinese/content.md` 的 `# PORTAL > ## 考試卡片` 加一個新 yaml 區段 → `npm run build` → 入口頁自動出現新卡片。
