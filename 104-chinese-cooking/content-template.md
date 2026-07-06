# META

```yaml
title: 114學年度學科模擬考場 - 測驗名稱
subtitle: 副標題描述文字
program: 職種/科目類別
organizer: 主辦/學校單位
dates: 114學年度
location: 線上測驗系統
format: 線上自主練習 / 60 分鐘限時挑戰
instructor: 指導團隊
storeKey: 114-unique-storekey-v1   # LocalStorage 唯一的進度快取 Key (切勿與其他科目重複)
timerSeconds: 3600                  # 測驗倒數時間 (秒，3600 = 60分鐘)
```

# DAY1

```yaml
id: day1
title: 課程與測驗主軸
```

## 單元一：第一部分主題名稱

```yaml
id: u-1
subtitle: 第 1 題至第 15 題，每題 2 分，共 30 分
time: 00:00 ~ 00:20
```

### 學習目標

- 理解該單元的核心學理與標準規範。
- 熟悉常見的基本概念與常識題型。

### 任務清單

- [d1-u1-t1] 完成本單元測驗作答。
- [d1-u1-t2] 閱讀錯題解析，釐清盲點。

### 插圖

- day1-u1-culture | hero | 飲食文化與餐飲管理示意圖   # 可自訂插圖 key 值

---

# MATERIALS

- [MD] exam-materials.md | 測驗完整試卷與解答 (提供考生下載/彈窗檢視的檔案)

---

# PORTAL

```yaml
title: 學術能力模擬檢測入口
subtitle: 歡迎來到模擬考試線上平台。本系統已依照不同試題與科目分類，請點擊下方對應的卡片進入考場進行線上作答與評分。
```

## 考試卡片

```yaml
id: exam-unique-id                  # 入口卡片的唯一 ID
tag: 學科分類標籤
title: 卡片標題名稱
desc: 考試簡介說明，讓考生暸解測驗內容與範圍。
time: 60 分鐘                        # 顯示在卡片上的考試時間
questions: 共 50 題                  # 顯示在卡片上的題數
score: 滿分 100 分                   # 顯示在卡片上的總分
href: unique-folder-name/           # 考場連結子路徑 (例如 114-cooking/)
btnText: 進入線上考場
```

---

# QUIZ

## Q1 · 單選題

這是單選題的題目描述文字？

- (A) 選項 A 文字
- (B) 選項 B 文字
- (C) 選項 C 文字
- (D) 選項 D 文字

```yaml
answer: B                           # 正確答案 (對應 B 索引 1)
unit: day1.u-1
explanation: |
  【答案】(B)
  【出處】教科書參考文獻/來源頁數
  【AI 分析】
  這裡寫入詳細的 AI 解析，說明為什麼 (B) 是正確的，以及其他選項為什麼是錯的。
```

## Q2 · 多選題

這是多選題的題目描述？（複選題）

- (A) 選項 A
- (B) 選項 B
- (C) 選項 C
- (D) 選項 D

```yaml
answer: [0, 2]                      # 正確答案索引陣列 (A 與 C)
unit: day1.u-1
explanation: |
  【答案】(A)(C)
  【出處】參考文獻
  【AI 分析】
  說明正確選項的原因與背景知識。
```

## Q3 · 問答題

這是一題問答題或混合手寫題的題目描述？

```yaml
type: text
unit: day1.u-1
subQuestions:
  - id: q3-1
    q: 第一小題問題？
    a: 第一小題參考答案。
    rubric: |
      評分規準：
      - 得 3 分：回答完全符合參考答案要點。
      - 得 1 分：回答部分符合。
      - 得 0 分：未答或答非所問。
  - id: q3-2
    q: 第二小題問題？
    a: 第二小題參考答案。
    rubric: |
      評分規準：
      - 得 2 分：回答精確。
      - 得 0 分：回答有誤。
```
