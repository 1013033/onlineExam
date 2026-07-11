# 線上考場 Web 目錄說明

本目錄是線上考場的靜態網站成品，整合各年度技藝競賽、技能檢定學科題庫、彙總題庫與列印工具。網站以純前端方式運作，主要由 HTML、CSS、JavaScript 與題庫資料檔組成，可直接部署到靜態主機，例如 GitHub Pages、Nginx、Apache 或任何支援靜態檔案的服務。

## 目前功能

- 平台首頁：列出所有線上考場與列印工具。
- 分年度試題：依年度與類別建立獨立線上測驗。
- 彙總試題：將多年度題目整理為大型去重題庫。
- 技能檢定題庫：包含中餐、西餐、烘焙等乙級、丙級題庫。
- 試題列印工具：提供瀏覽器列印與另存 PDF 的版面調整介面。
- 線上測驗：支援作答、即時批改、詳解顯示、計時、進度保存、下次進入自動回到上次作答題目、手機接續。
- 錯題庫與錯題重練：已套用於所有線上測驗資料夾，答錯會自動進入錯題庫，錯題重練連續答對 2 次後自動出庫，手機接續同步也會包含錯題庫。

## 目錄結構

```text
web/
├── index.html
├── portal-data.js
├── package.json
├── README.md
├── 100-baking/
├── 100-chinese-cooking/
├── 101-baking/
├── ...
├── 100-114-chinese-cooking-summary/
├── 100-114-baking-print/
├── 115-baking-b/
├── 115-baking-b-print/
└── ...
```

## 入口檔案

### `index.html`

平台首頁。負責讀取 `portal-data.js`，並把所有考場與列印工具渲染成卡片入口。

常見維護情境：

- 調整平台首頁版面。
- 調整搜尋、分類、卡片樣式。
- 修改入口頁標題、頁尾或整體視覺。

### `portal-data.js`

平台入口資料。內含 `window.PORTAL`，描述首頁要顯示的所有考場與工具。

每一筆通常包含：

```js
{
  id: "exam-100-baking",
  tag: "技藝競賽學科-烘焙",
  title: "100 學年度烘焙職種學科正式試卷",
  desc: "試卷簡介",
  time: "60 分鐘",
  questions: "共 50 題",
  score: "滿分 100 分",
  href: "100-baking/",
  btnText: "進入線上考場"
}
```

注意：此檔案看起來是由工具產生的資料檔。若後續有正式產生流程，應優先從來源資料更新，再重新產生，不建議長期手動改大量內容。

### `package.json`

目前根目錄只提供簡單的靜態服務指令：

```bash
npm run serve
```

此指令會透過 `npx serve .` 啟動靜態伺服器。

## 試卷資料夾類型

### 線上測驗資料夾

例如：

- `100-baking/`
- `100-chinese-cooking/`
- `108-baking/`
- `115-chinese-cooking-b/`
- `100-114-chinese-cooking-summary/`

常見檔案：

```text
index.html
style.css
course-data.js
content.md
viewer.html
package.json
dev-server.js
md-to-data.js
parse_questions.py
course-package/
```

不同資料夾不一定全部都有以上檔案，依試卷來源與產生方式而定。

### 列印工具資料夾

例如：

- `100-114-baking-print/`
- `100-114-chinese-cooking-print/`
- `115-baking-b-print/`
- `115-chinese-cooking-c-print/`

常見檔案：

```text
index.html
style.css
app.js
data.js
```

列印工具通常不走 `course-data.js` 結構，而是由 `data.js` 提供題目資料，再由 `app.js` 渲染列印版面與控制項。

## 線上測驗資料夾檔案職責

### `index.html`

該份試卷的主要測驗頁。通常包含：

- 側欄導覽。
- 題目渲染。
- 單選與複選作答。
- 送出與評分。
- 詳解顯示。
- 作答進度保存。
- 下次進入同一份試卷時，自動回到上次作答的題目位置。
- 計時器。
- 主題切換。
- 手機接續作答。

所有線上測驗版 `index.html` 均包含錯題庫、錯題重練、上次作答位置恢復與手機接續同步錯題庫功能。

### `style.css`

該份試卷的視覺樣式。包含：

- 版面。
- 側欄。
- 測驗卡片。
- 選項狀態。
- 詳解區塊。
- 分數卡片。
- 響應式版面。

### `course-data.js`

題庫與課程資料。通常由 `content.md` 或其他來源產生，並掛到 `window.COURSE`。

常見欄位：

```js
window.COURSE = {
  meta: {
    title: "...",
    storeKey: "...",
    timerSeconds: 3600
  },
  materials: [],
  quiz: []
};
```

重要欄位：

- `meta.storeKey`：localStorage 的儲存鍵，用來保存作答進度。
- `meta.timerSeconds`：測驗秒數。
- `quiz`：題目陣列。
- `materials`：相關下載或教材連結。

### `content.md`

題庫或頁面內容的 Markdown 來源檔。若資料夾有 `md-to-data.js`，通常代表 `course-data.js` 可以由此檔重新產生。

### `md-to-data.js`

把 `content.md` 轉成 `course-data.js` 的工具。

常用指令：

```bash
cd web/100-baking
npm run build
```

或啟動 watch：

```bash
npm run build:watch
```

### `dev-server.js`

該試卷資料夾的本地開發伺服器，通常會提供：

- 靜態檔案服務。
- `content.md` 變更後自動重新產生 `course-data.js`。
- 熱重載。

常用指令：

```bash
cd web/100-baking
npm run dev
```

預設通常從 `http://localhost:3456/` 開始，若 port 被占用，部分 `dev-server.js` 會自動改用下一個可用 port。

### `viewer.html`

用於在頁面中開啟 Markdown 或相關素材的檢視器。

## 列印工具檔案職責

### `index.html`

列印工具頁面框架。

### `style.css`

列印版面與控制面板樣式，通常包含螢幕顯示與 `@media print` 設定。

### `app.js`

列印工具主程式，負責：

- 渲染題目。
- 調整字體大小。
- 調整行距。
- 調整題目與選項間距。
- 控制出處顯示位置。
- 控制選項排列方式。
- 呼叫瀏覽器列印。

### `data.js`

列印工具題庫資料。

## 本地啟動方式

### 啟動整個平台首頁

```bash
cd D:\Aaron-agy\onlineExam_Source\web
npm run serve
```

啟動後依終端機顯示的網址開啟，一般會是：

```text
http://localhost:3000/
```

實際 port 取決於 `serve` 套件與當時環境。

### 啟動單一試卷開發伺服器

```bash
cd D:\Aaron-agy\onlineExam_Source\web\100-baking
npm run dev
```

通常開啟：

```text
http://localhost:3456/
```

此方式適合修改該份試卷的 `content.md`、`index.html`、`style.css` 或測試互動功能。

### 直接開啟 HTML

多數頁面是純靜態檔案，但建議仍透過本地伺服器開啟，原因是：

- 相對路徑較穩定。
- `fetch` 或 iframe 載入素材時比較不容易被瀏覽器安全限制擋下。
- 行為更接近部署後環境。

## 更新題庫流程

若該資料夾有 `content.md` 與 `md-to-data.js`：

1. 修改 `content.md`。
2. 執行：

```bash
npm run build
```

3. 確認 `course-data.js` 已更新。
4. 開啟本地頁面檢查題目、答案與詳解。
5. 確認 Git diff，只提交必要檔案。

若該資料夾沒有 `content.md` 或 `md-to-data.js`：

1. 先確認題庫來源。
2. 檢查資料是否直接維護在 `course-data.js`、`data.js` 或其他產生流程。
3. 避免未確認來源時手動大量改產生檔。

## 新增一份線上測驗

建議流程：

1. 複製一份結構相近的試卷資料夾。
2. 修改資料夾名稱，例如 `116-baking/`。
3. 修改該資料夾中的：
   - `index.html` 標題與 redirect 路徑。
   - `course-data.js` 或來源 `content.md`。
   - `package.json` 的 `name` 與描述。
   - `meta.storeKey`，避免 localStorage 與其他試卷衝突。
4. 若有 `content.md`，執行 `npm run build`。
5. 在 `portal-data.js` 新增首頁入口。
6. 開啟平台首頁確認入口連結正常。
7. 開啟新試卷確認作答、評分、詳解與計時正常。

## 新增一份列印工具

建議流程：

1. 複製相近的 `*-print/` 資料夾。
2. 修改 `data.js` 題庫資料。
3. 修改 `index.html` 頁面標題。
4. 視需要調整 `app.js` 控制邏輯。
5. 視需要調整 `style.css` 列印版面。
6. 在 `portal-data.js` 新增工具入口。
7. 用瀏覽器列印預覽確認版面。

## localStorage 與作答紀錄

線上測驗會使用瀏覽器 `localStorage` 保存作答狀態。

主要用途：

- 保存選擇題作答。
- 保存非選擇題文字作答。
- 保存是否已批改。
- 保存計時器剩餘時間。
- 保存錯題庫資料。
- 保存最後作答題號，供下次進入同一份試卷時自動回到上次作答位置。

每份試卷應使用獨立的 `meta.storeKey`。例如：

```js
storeKey: "100-baking-progress-v1"
```

計時器會使用：

```text
{storeKey}-time-remaining
```

錯題庫使用：

```text
{storeKey}-wrong-book-v1
```

最後作答位置會保存在每份試卷原本的 `{storeKey}` JSON 內容中，例如：

```js
{
  lastSection: "quiz",
  lastQuestion: "q12"
}
```

此欄位會隨首頁「備份與還原」一起備份，也會隨手機接續同步 payload 一起帶到另一台裝置。

若要清除瀏覽器中的測驗紀錄，可使用頁面上的「清除所有紀錄」，或在瀏覽器 DevTools 的 Application / Storage 中清除該站 localStorage。

## 錯題庫功能狀態

目前錯題庫功能已套用在所有線上測驗資料夾：

```text
*-print/ 以外、且具有 course-data.js 的測驗資料夾
```

目前行為：

- 一般測驗中，選擇題答錯會自動加入錯題庫。
- 錯題庫只收選擇題，不收手寫或非選擇題。
- 點擊「錯題重練」後，只顯示目前錯題庫中的題目。
- 錯題重練答對 1 次後保留在錯題庫。
- 同一題連續答對 2 次後自動出庫。
- 錯題重練中答錯會把連續答對次數歸零。
- 「清空錯題庫」只清除該份試卷的錯題庫。
- 「清除所有紀錄」會清除作答進度、計時器與錯題庫。
- 手機接續同步會帶入作答進度、計時時間、錯題庫與最後作答題號。

維護時需注意：

- 每份試卷的 `STORE_KEY` 必須不同。
- 彙總題庫題數較多，錯題庫 UI 需要確認長列表效能。
- 如果題目含複選題，要確認「確認選項並看解析」按鈕流程正常。
- 如果題目含手寫題，需決定是否納入錯題庫；目前版本不納入手寫題。

## 維護注意事項

- 不要任意改動 `meta.storeKey`，否則使用者既有作答紀錄會失效。
- 不要任意改題目 `id`，否則作答紀錄、錯題庫與題目對應會失效。
- 修改 `course-data.js` 前先確認它是否由 `content.md` 產生。
- 修改 `portal-data.js` 前先確認是否有產生流程，避免覆蓋入口資料。
- 執行 `npm run dev` 可能會自動重新產生資料檔，提交前務必檢查 Git diff。
- 列印工具修改後一定要檢查瀏覽器列印預覽，不只看螢幕版面。
- 大型彙總題庫檔案較大，修改時避免不必要的格式化，減少 diff 噪音。

## 建議驗證清單

修改任何線上測驗後，建議至少檢查：

- 首頁入口可正常進入試卷。
- 試卷頁面無 JavaScript console error。
- 單選題可作答並顯示正確答案與詳解。
- 複選題可選多個選項並確認答案。
- 送出整份試卷後分數正確。
- 計時器可開始、暫停、時間到自動送出。
- 清除紀錄後頁面狀態重置。
- 手機或窄螢幕下側欄與按鈕不重疊。
- 若有錯題庫，答錯入庫、錯題重練、連續答對 2 次出庫都正常。

修改列印工具後，建議至少檢查：

- 題目數量正確。
- 選項排列正確。
- 字體大小與行距控制有效。
- 出處顯示位置正確。
- 列印預覽沒有題目被截斷。
- 另存 PDF 後版面可讀。

## 部署

此目錄可作為靜態網站部署。部署時需包含：

- `index.html`
- `portal-data.js`
- 所有試卷資料夾
- 所有列印工具資料夾
- 各資料夾內的 CSS、JS、資料檔與素材

若部署到 GitHub Pages，通常可直接把 `web/` 內容作為站台根目錄，或在部署流程中指定 `web/` 為發布資料夾。

## 常見問題

### 首頁有入口，但點進去 404

檢查 `portal-data.js` 中該筆資料的 `href` 是否與實際資料夾名稱一致。

### 進入試卷後樣式或題庫沒有載入

檢查：

- 該資料夾是否有 `style.css`。
- 該資料夾是否有 `course-data.js`。
- 網址是否缺少結尾斜線 `/`。
- 瀏覽器 console 是否有路徑錯誤。

### 作答紀錄互相影響

檢查不同試卷的 `meta.storeKey` 是否重複。

### 修改 `content.md` 後頁面沒變

執行：

```bash
npm run build
```

確認 `course-data.js` 已重新產生。

### 執行開發伺服器後出現大量非預期 diff

部分產生工具可能會重寫資料檔。提交前請用：

```bash
git diff
git status --short
```

只保留本次需求必要的改動。
