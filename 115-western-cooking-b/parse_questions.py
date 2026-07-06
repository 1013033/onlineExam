from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "western-cooking-b-exam.md"
OUTPUT = ROOT / "content.md"

OPTION_MARKERS = [
    ("ロ", "A"), ("ヮ", "B"), ("ワ", "C"), ("ヰ", "D"),
    ("①", "A"), ("②", "B"), ("③", "C"), ("④", "D"),
]
ANSWER_LETTERS = {"1": "A", "2": "B", "3": "C", "4": "D"}

EXTRA_REASONS = {
    "肉質的脂肪多寡": "Marbling 是肌肉間細小脂肪分布，脂肪分布越明顯，肉質通常越多汁、風味越佳。",
    "番紅花": "Bouillabaisse 是法式普羅旺斯海鮮湯，番紅花是其代表性香料，能提供金黃色澤與特殊香氣。",
    "荳蔻粉": "西餐中洋芋與奶油、乳製品搭配時常用 nutmeg 增香，能提升澱粉類與白醬料理的溫暖辛香。",
    "提高發煙點溫度": "澄清奶油去除水分與乳固形物後較不易焦化，因此比一般奶油更適合較高溫烹調。",
    "雞胸肉": "Fricassee 是白色燉煮法，常用雞肉等嫩質白肉，以低溫燉煮並搭配白色醬汁。",
    "帕瑪森": "Parmesan 含水量低、熟成時間長，質地堅硬，屬硬質乳酪。",
    "松露": "松露因產量稀少、採集困難且香氣特殊，是西餐中價格昂貴的高級食材。",
    "禽肉、畜肉、蛋及蛋製品": "沙門氏菌常與禽畜肉、蛋及蛋製品污染相關，未充分加熱或交叉污染會提高風險。",
    "成立食品安全管制小組": "HACCP 系統的建立需先成立管制小組，才能進行危害分析、決定重要管制點與矯正措施。",
    "物理性": "食品危害分析通常包含物理性、生物性與化學性危害；物理性危害如異物、碎片等。",
    "生物性": "生物性危害包含病原菌、病毒、寄生蟲等，屬 HACCP 必須評估的食品安全風險。",
    "化學性": "化學性危害包含清潔劑殘留、農藥、重金屬或添加物使用不當等風險。",
}

UNIT_TOPICS = {
    "02": ("day1.u-2", "食物的性質及選購"),
    "03": ("day1.u-3", "食物貯存"),
    "04": ("day1.u-4", "食物製備"),
    "05": ("day1.u-5", "器皿與盤飾"),
    "06": ("day1.u-6", "設備與器具"),
    "07": ("day1.u-7", "營養知識"),
    "08": ("day1.u-8", "成本控制"),
    "09": ("day1.u-9", "安全措施"),
    "10": ("day1.u-10", "衛生知識"),
    "11": ("day1.u-11", "衛生法規"),
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
            f"西餐烹調乙級學科的分類、操作條件、衛生規範或法規要求。正確選項「{correct_name}」之所以成立，"
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

- 熟悉「{topic}」在西餐烹調乙級學科中的常見考點。
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
            "勞動部勞動力發展署技能檢定中心，西餐烹調乙級技術士技能檢定學科測試參考資料；"
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
title: 西餐烹調乙級學科測試參考資料
subtitle: 115.07 題庫線上練習考場
program: 西餐烹調技術士技能檢定
organizer: 勞動部勞動力發展署技能檢定中心題庫整理
dates: 115.07
location: 線上測驗系統
format: 題庫自主練習 / 120 分鐘限時挑戰
instructor: 西餐烹調乙級學科輔助解析
storeKey: 115-western-cooking-b-progress-v1
timerSeconds: 7200
```

## 學習目標

- 完成西餐烹調乙級學科測試參考資料 10 個工作項目的完整練習。
- 熟悉食物性質與選購、貯存、製備、器皿盤飾、設備器具、營養、成本、安全、衛生與法規。
- 透過逐題答案、出處與 AI 分析，建立可複習的錯題筆記。

## 考科時程

| 建議時間 | 考科單元 | 考核重點 |
|---|---|---|
| 00:00 ~ 00:30 | 工作項目 02-03 | 食物性質、選購與貯存 |
| 00:30 ~ 01:00 | 工作項目 04-06 | 食物製備、器皿盤飾與設備器具 |
| 01:00 ~ 01:30 | 工作項目 07-09 | 營養、成本控制與安全措施 |
| 01:30 ~ 02:00 | 工作項目 10-11 | 衛生知識、衛生法規與 HACCP 管制 |

---

# DAY1

```yaml
id: day1
n: 1
date: 115.07
title: 西餐烹調乙級學科題庫練習
hours: 2.0
date_label: 115.07
hours_label: 2.0 小時 (120分鐘)
learningGoal: 完成西餐烹調乙級學科 10 個工作項目的完整題庫練習。
hero_title: 西餐烹調乙級學科練習
hero_lead: 本題庫共 {total} 題，包含單選與複選題；系統以百分制計分，複選題需完全答對才列為正確。
```

{units}

---

# MATERIALS

- [MD] western-cooking-b-exam.md | 西餐烹調乙級學科測試參考資料原始題庫

---

# PORTAL

```yaml
title: 學術能力模擬檢測入口
subtitle: 歡迎來到模擬考試線上平台。本系統已依照不同試題與科目分類，請點擊下方對應的卡片進入考場進行線上作答與評分。
```

## 考試卡片

```yaml
id: exam-115-western-cooking-b
tag: 西餐烹調乙級
title: 西餐烹調乙級學科測試參考資料
desc: 115.07 版西餐烹調乙級學科題庫，共 {total} 題，涵蓋食物性質及選購、貯存、製備、器皿盤飾、設備器具、營養、成本控制、安全措施、衛生知識與衛生法規。
time: 120 分鐘
questions: 共 {total} 題
score: 滿分 100 分
href: 115-western-cooking-b/
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
