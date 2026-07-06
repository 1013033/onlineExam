from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "chinese-cooking-b-exam.md"
OUTPUT = ROOT / "content.md"

OPTION_MARKERS = [
    ("ロ", "A"), ("ヮ", "B"), ("ワ", "C"), ("ヰ", "D"),
    ("①", "A"), ("②", "B"), ("③", "C"), ("④", "D"),
]
ANSWER_LETTERS = {"1": "A", "2": "B", "3": "C", "4": "D"}

EXTRA_REASONS = {
    "6%": "新鮮蛋氣室小、比重大，在適當濃度的鹽水中較容易下沉；題庫以 6% 鹽水作為判斷新鮮度的標準條件。",
    "鐵": "蛋黃中的鐵會和蛋白含硫胺基酸受熱分解產生的硫化氫反應，形成暗綠色的硫化鐵。",
    "卵磷脂": "卵磷脂具有親水端與親油端，能讓油脂分散在水相中，因此是蛋黃能乳化油脂的關鍵成分。",
    "果糖": "在常見食品糖類中，果糖相對甜度最高，高於蔗糖、葡萄糖與乳糖。",
    "醋": "酸性物質能促進蔗糖水解為葡萄糖與果糖，也就是轉化糖；轉化糖較不易再結晶。",
    "氯化鉀": "豆腐凝固常用硫酸鈣、氯化鎂或氯化鈣等鈣鎂鹽，氯化鉀不是製造豆腐的典型凝固劑。",
    "植物油氫化": "人造奶油是植物油經氫化或加工塑性化後製成，和直接從牛奶或動物脂肪分離不同。",
    "26%": "全脂奶粉保留乳脂肪，題庫採用的標準為脂肪含量約 26% 以上。",
    "油溫不夠高": "油炸時油溫不足會讓食物吸油、表面脫水不完全，成品就不易形成酥脆外殼。",
    "碳酸鈉": "食用鹼或鹼水常見主要成分為碳酸鈉，能提高 pH 並改變澱粉或蛋白質的質地。",
    "山葵": "真正的綠色芥末主要來自山葵根莖，和芥菜籽或其他辛香料不同。",
    "TQF": "TQF 是台灣優良食品驗證標章，購買加工食品或油品時可作為品質與安全管理參考。",
    "六大類": "國民健康署每日飲食指南將食物分為全穀雜糧、豆魚蛋肉、乳品、蔬菜、水果、油脂與堅果種子六大類。",
    "綠豆": "傳統冬粉主要以綠豆澱粉製成，因其澱粉特性可形成透明且耐煮的粉絲質地。",
}

UNIT_TOPICS = {
    "01": ("day1.u-1", "食物性質之認識"),
    "02": ("day1.u-2", "食物選購"),
    "03": ("day1.u-3", "食物貯藏"),
    "04": ("day1.u-4", "食物製備"),
    "05": ("day1.u-5", "排盤與裝飾"),
    "06": ("day1.u-6", "器具設備之認識"),
    "07": ("day1.u-7", "營養知識"),
    "08": ("day1.u-8", "成本控制"),
    "09": ("day1.u-9", "衛生知識"),
    "10": ("day1.u-10", "衛生法規"),
}


def split_options(raw):
    positions = []
    for marker, letter in OPTION_MARKERS:
        idx = raw.find(marker)
        if idx >= 0:
            positions.append((idx, marker, letter))
    positions.sort()
    if not positions:
        return raw.strip(), []

    question = raw[: positions[0][0]].strip()
    options = []
    for i, (idx, marker, letter) in enumerate(positions):
        start = idx + len(marker)
        end = positions[i + 1][0] if i + 1 < len(positions) else len(raw)
        text = raw[start:end].strip()
        text = re.sub(r"[。.\s]+$", "", text)
        options.append((letter, text))
    return question, options


def answer_to_yaml(answer):
    letters = [ANSWER_LETTERS[ch] for ch in answer if ch in ANSWER_LETTERS]
    if len(letters) == 1:
        return letters[0], f"({letters[0]})"
    return "[" + ", ".join(letters) + "]", "".join(f"({x})" for x in letters)


def analysis_for(topic, question, options, correct_letters, correct_text, is_multiple):
    stem = question.rstrip("。")
    wrong_options = [f"{letter}. {text}" for letter, text in options if letter not in correct_letters]
    wrong_text = "、".join(wrong_options)
    correct_names = [text for letter, text in options if letter in correct_letters]
    correct_name = "、".join(correct_names) or correct_text
    extra_reason = next((v for k, v in EXTRA_REASONS.items() if k in correct_name), "")
    extra_sentence = f"具體來說，{extra_reason}" if extra_reason else ""
    negative_words = ("不屬", "不是", "不可", "不宜", "錯誤", "何者不", "何者非", "除外")
    cause_words = ("因為", "由於", "原因", "為何", "來自", "產生")
    definition_words = ("是指", "稱為", "簡稱", "係", "屬於", "何種", "何者為")

    if is_multiple:
        return (
            f"本題答案為「{correct_text}」。題幹問的是「{stem}」，因此要逐一檢查每個選項是否同時符合"
            f"中餐烹調乙級學科的分類、操作條件、衛生規範或法規要求。正確選項「{correct_name}」之所以成立，"
            f"是因為它們都符合題幹指定的條件；其餘選項（{wrong_text}）則至少有一項概念、對象、時間、溫度、"
            f"用途或法規條件不符。複習時應把正確選項拆成獨立規則背誦，再用錯誤選項反向確認常見混淆點。"
        )

    if any(word in stem for word in negative_words):
        why = (
            f"本題答案為「{correct_text}」。題幹使用否定式問法，重點不是找最常見的項目，而是找出「不符合」"
            f"題幹分類、條件或規範的排除項。正確選項「{correct_name}」之所以正確，是因為它不屬於題幹所要求的"
            f"標準範圍；{extra_sentence}相對地，{wrong_text} 皆較符合題幹所描述的類別或實務規則，所以不能選。"
        )
    elif any(word in stem for word in cause_words):
        why = (
            f"本題答案為「{correct_text}」。題幹問的是形成原因或作用來源，因此要能說明「為什麼會發生題目中的"
            f"現象」。正確選項「{correct_name}」之所以正確，是因為它和題幹現象有直接因果關係；換句話說，"
            f"它才是造成該味道、質地、反應、變化或衛生結果的主要因素。{extra_sentence}{wrong_text} 雖可能與同章節相關，"
            f"但不能直接解釋題幹所描述的結果。"
        )
    elif any(word in stem for word in definition_words):
        why = (
            f"本題答案為「{correct_text}」。這類題目考的是名詞定義、食材分類或制度簡稱；正確選項「{correct_name}」"
            f"就是題幹概念在學科題庫中的標準名稱、標準分類或標準用途。{extra_sentence}{wrong_text} 屬於相近名詞、其他類別"
            f"或不同用途，與題幹定義不一致。"
        )
    else:
        why = (
            f"本題答案為「{correct_text}」。判斷關鍵在於題幹「{stem}」所要求的分類、用途、比例、流程或衛生條件。"
            f"正確選項「{correct_name}」與題幹要求最直接對應，因此是標準答案；{extra_sentence}{wrong_text} 則是常見混淆項，"
            f"通常在食材類別、加工方法、操作時機、溫度時間或衛生管理要求上與題幹條件不完全相符。"
        )

    return (
        f"{why} 本題屬於「{topic}」範圍，複習時可把它整理成「題幹條件 -> 正確選項 -> 排除其他選項」的筆記，"
        f"避免只背答案而無法應付相似題。"
    )


def parse():
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    current_work = None
    current_topic = ""
    items = []

    for line in text.splitlines():
        section = re.match(r"^## 工作項目\s*(\d+)：(.+)$", line)
        if section:
            current_work = section.group(1)
            current_topic = section.group(2).strip()
            continue

        match = re.match(r"^(\d+)\.\s*\((\d+)\)\s*(.+)$", line)
        if not match or not current_work:
            continue

        local_no = int(match.group(1))
        answer_raw = match.group(2)
        raw_question = match.group(3).strip()
        question, options = split_options(raw_question)
        yaml_answer, display_answer = answer_to_yaml(answer_raw)
        correct_letters = [ANSWER_LETTERS[ch] for ch in answer_raw if ch in ANSWER_LETTERS]
        correct_text = "、".join(
            f"{letter}. {text}" for letter, text in options if letter in correct_letters
        )
        unit_id, topic = UNIT_TOPICS.get(current_work, ("day1.u-1", current_topic))
        items.append(
            {
                "global_no": len(items) + 1,
                "work": current_work,
                "topic": topic,
                "local_no": local_no,
                "question": question,
                "options": options,
                "answer_raw": answer_raw,
                "yaml_answer": yaml_answer,
                "display_answer": display_answer,
                "correct_text": correct_text,
                "unit": unit_id,
                "multiple": len(correct_letters) > 1,
            }
        )
    return items


def build_content(items):
    total = len(items)
    units = "\n".join(
        f"""
## 單元{int(work)}：{topic}

```yaml
id: u-{int(work)}
subtitle: 工作項目 {work}，共 {sum(1 for item in items if item["work"] == work)} 題
time: 自主練習
```

### 學習目標

- 熟悉「{topic}」在中餐烹調乙級學科中的常見考點。
- 能依據食品科學、餐飲衛生與廚務管理原則判斷正確答案。

### 任務清單

- [d1-u{int(work)}-t1] 完成工作項目 {work} 題庫練習。
"""
        for work, (unit, topic) in UNIT_TOPICS.items()
    )

    quiz_blocks = []
    for item in items:
        heading = "複選題" if item["multiple"] else "單選題"
        options_md = "\n".join(f"- ({letter}) {text}" for letter, text in item["options"])
        source = (
            "勞動部勞動力發展署技能檢定中心，中餐烹調乙級技術士技能檢定學科測試參考資料；"
            "衛生福利部食品藥物管理署，食品安全衛生管理法及食品良好衛生規範準則；"
            "衛生福利部國民健康署，每日飲食指南與食品營養相關公開資料。"
        )
        analysis = analysis_for(
            item["topic"],
            item["question"],
            item["options"],
            [ANSWER_LETTERS[ch] for ch in item["answer_raw"] if ch in ANSWER_LETTERS],
            item["correct_text"],
            item["multiple"],
        )
        type_line = "type: multiple\n" if item["multiple"] else ""
        quiz_blocks.append(
            f"""## Q{item["global_no"]} · {heading}

工作項目 {item["work"]}「{item["topic"]}」原題號 {item["local_no"]}：

{item["question"]}

{options_md}

```yaml
{type_line}answer: {item["yaml_answer"]}
unit: {item["unit"]}
explanation: |
  【答案】{item["display_answer"]}
  【出處】{source}
  【AI 分析】
  {analysis}
```
"""
        )

    return f"""# META

```yaml
title: 中餐葷食乙級學科測試參考資料
subtitle: 115.07 題庫線上練習考場
program: 中餐烹調技術士技能檢定
organizer: 勞動部勞動力發展署技能檢定中心題庫整理
dates: 115.07
location: 線上測驗系統
format: 題庫自主練習 / 120 分鐘限時挑戰
instructor: 中餐烹調乙級學科輔助解析
storeKey: 115-chinese-cooking-b-progress-v2
timerSeconds: 7200
```

## 學習目標

- 完成中餐葷食乙級學科測試參考資料 10 個工作項目的完整練習。
- 熟悉食物性質、選購、貯藏、製備、排盤、器具設備、營養、成本、衛生與法規。
- 透過逐題答案、出處與 AI 分析，建立可複習的錯題筆記。

## 考科時程

| 建議時間 | 考科單元 | 考核重點 |
|---|---|---|
| 00:00 ~ 00:30 | 工作項目 01-03 | 食物性質、選購與貯藏 |
| 00:30 ~ 01:00 | 工作項目 04-06 | 食物製備、排盤裝飾與器具設備 |
| 01:00 ~ 01:30 | 工作項目 07-09 | 營養、成本控制與衛生知識 |
| 01:30 ~ 02:00 | 工作項目 10 | 衛生法規與 HACCP 管制 |

---

# DAY1

```yaml
id: day1
n: 1
date: 115.07
title: 中餐葷食乙級學科題庫練習
hours: 2.0
date_label: 115.07
hours_label: 2.0 小時 (120分鐘)
learningGoal: 完成中餐葷食乙級學科 10 個工作項目的完整題庫練習。
hero_title: 中餐葷食乙級學科練習
hero_lead: 本題庫共 {total} 題，包含單選與複選題；系統以百分制計分，複選題需完全答對才列為正確。
```

{units}

---

# MATERIALS

- [MD] chinese-cooking-b-exam.md | 中餐葷食乙級學科測試參考資料原始題庫

---

# PORTAL

```yaml
title: 學術能力模擬檢測入口
subtitle: 歡迎來到模擬考試線上平台。本系統已依照不同試題與科目分類，請點擊下方對應的卡片進入考場進行線上作答與評分。
```

## 考試卡片

```yaml
id: exam-115-chinese-cooking-b
tag: 中餐葷食乙級
title: 中餐葷食乙級學科測試參考資料
desc: 115.07 版中餐葷食乙級學科題庫，共 {total} 題，涵蓋食物性質、選購、貯藏、製備、排盤裝飾、器具設備、營養、成本控制、衛生知識與衛生法規。
time: 120 分鐘
questions: 共 {total} 題
score: 滿分 100 分
href: 115-chinese-cooking-b/
btnText: 進入線上考場
```

---

# QUIZ

{chr(10).join(quiz_blocks)}
"""


if __name__ == "__main__":
    parsed = parse()
    OUTPUT.write_text(build_content(parsed), encoding="utf-8")
    print(f"Parsed {len(parsed)} questions -> {OUTPUT}")
