from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "baking-c-exam.md"
OUTPUT = ROOT / "content.md"

OPTION_MARKERS = [
    ("①", "A"), ("②", "B"), ("③", "C"), ("④", "D"),
    ("ロ", "A"), ("ヮ", "B"), ("ワ", "C"), ("ヰ", "D"),
]
ANSWER_LETTERS = {"1": "A", "2": "B", "3": "C", "4": "D"}

UNIT_TOPICS = {
    "01": ("day1.u-1", "產品分類"),
    "02": ("day1.u-2", "原料之選用"),
    "03": ("day1.u-3", "產品製作"),
    "04": ("day1.u-4", "品質鑑定"),
    "05": ("day1.u-5", "烘焙食品之包裝"),
    "06": ("day1.u-6", "食品之貯存"),
}

EXTRA_REASONS = {
    "表皮脆、內部軟": "硬式麵包的典型質地是外皮經高溫烘烤形成脆殼，內部仍保有柔軟組織與孔洞。",
    "天使蛋糕": "天使蛋糕主要靠蛋白泡沫形成體積，不使用油脂，才能維持潔白、輕盈與低脂特性。",
    "小西餅": "小西餅屬餅乾類產品，配方通常含油脂與糖，成品含水量低、口感酥鬆或脆硬。",
    "水果蛋糕": "水果蛋糕為高糖高油配方，糖除提供甜味外也有保濕、軟化與延長保存的作用。",
    "戚風蛋糕": "戚風蛋糕靠蛋白霜與液體油形成輕盈組織，麵糊比重低，烤後體積膨大。",
    "天使蛋糕": "塔塔粉可降低蛋白液 pH、穩定蛋白泡沫，特別適用於以蛋白為主要膨發來源的天使蛋糕。",
    "冰箱小西餅": "冰箱小西餅常用高油高糖配方，麵糰冷藏後切片成形；題示油脂 80%、糖 60% 符合此類產品特性。",
    "瑪琍餅乾": "瑪琍餅乾屬低油低糖餅乾，題示油脂與糖各 20% 較接近其配方結構。",
    "統粉": "統粉指小麥內胚乳整體磨出的麵粉，與全粒小麥粉含麩皮、胚芽不同。",
    "果糖": "常見糖類中果糖甜度高於蔗糖、麥芽糖與海藻糖，因此在同重量下甜味最強。",
    "丙酸鹽": "丙酸鹽可抑制黴菌生長，是麵包與糕餅類常見合法防腐用途之一。",
    "70%": "新鮮酵母含水量高，約 70%，因此保存性低於乾酵母，需冷藏並儘快使用。",
    "33%": "蛋黃含有較多脂質與乳化成分，脂肪約占蛋黃重量三分之一，是蛋糕乳化與增香的重要來源。",
    "總極性化合物": "油炸油劣變可用總極性化合物判斷，超過 25% 即應更換，避免品質與衛生風險。",
    "衛生福利部": "食品添加物品名、規格、使用範圍與限量由中央主管機關衛生福利部訂定。",
    "HACCP": "HACCP 是以危害分析與重要管制點為核心的食品安全管理制度，重點在預防而非事後檢驗。",
    "先進先出": "食品貯存須採先進先出，以降低逾期、變質與庫存交叉污染風險。",
    "10 ℃以下": "含奶油、布丁、果凍或餡料的蛋糕與派屬易腐敗食品，應低溫冷藏以抑制微生物繁殖。",
    "西點項": "比薩雖屬發酵麵糰製品，但題庫分類將歐美流行的比薩歸入西點項。",
    "鬆餅": "鬆餅以麵糊在烤盤或鬆餅機中加熱成形，不需像開口笑、沙其瑪或道納司經油炸製成。",
    "法國麵包": "法國麵包屬硬式麵包，配方較單純，外皮硬脆、內部有彈性與孔洞。",
    "海綿蛋糕": "海綿蛋糕常以全蛋加溫至約 40～43 ℃後打發，可降低蛋液黏度並提升起泡性。",
    "5~60 ℃": "5～60 ℃是食品安全常見危險溫度帶，微生物容易快速繁殖，食品不宜暴露超過 4 小時。",
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
        text = re.sub(r"[。．\s]+$", "", text)
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
    extra_reason = next((v for k, v in EXTRA_REASONS.items() if k in correct_name or k in stem), "")
    extra_sentence = f"具體來說，{extra_reason}" if extra_reason else ""
    negative_words = ("不屬", "不是", "不可", "不宜", "非", "錯誤", "何者不", "何者為非", "除外")
    formula_words = ("百分比", "比例", "成本", "售價", "損耗", "水分", "重量", "%", "幾")
    process_words = ("製作", "攪拌", "發酵", "烘烤", "包裝", "保存", "冷藏", "冷凍", "殺菌", "管制")

    if is_multiple:
        return (
            f"本題答案為「{correct_text}」。複選題的重點是逐項判斷每個敘述是否同時符合「{stem}」的條件；"
            f"正確選項「{correct_name}」都符合烘焙丙級題庫中的產品分類、配方特性、操作條件或衛生法規。"
            f"{extra_sentence}其餘選項（{wrong_text}）至少有一項在產品來源、製程條件、溫度時間、配方比例或法規要求上不符，"
            f"所以不能勾選。複習時建議把每一個正確選項拆成獨立規則，再用錯誤選項反向確認常見混淆點。"
        )

    if any(word in stem for word in negative_words):
        why = (
            f"本題答案為「{correct_text}」。題幹是否定式問法，應找出不符合分類、配方、製程或法規條件的排除項。"
            f"正確選項「{correct_name}」之所以正確，是因為它不屬於題幹所要求的標準範圍；{extra_sentence}"
            f"相對地，{wrong_text} 較符合題幹描述，所以不能選。"
        )
    elif any(word in stem for word in formula_words):
        why = (
            f"本題答案為「{correct_text}」。這類題目通常考烘焙百分比、原料比例、成本或品質數值；"
            f"正確選項「{correct_name}」與題幹的標準比例或數值最一致。{extra_sentence}"
            f"{wrong_text} 則是常見干擾值，若套回題幹條件，會造成配方平衡、製程判斷或成本計算不正確。"
        )
    elif any(word in stem for word in process_words):
        why = (
            f"本題答案為「{correct_text}」。題幹考的是烘焙製程或食品保存管理的因果關係；"
            f"正確選項「{correct_name}」能直接解釋產品體積、組織、口感、保存性或衛生安全的形成原因。"
            f"{extra_sentence}{wrong_text} 與題幹所要求的製程目的、溫度時間、包裝保存或衛生管制條件不完全相符。"
        )
    else:
        why = (
            f"本題答案為「{correct_text}」。判斷關鍵在於題幹「{stem}」要求的產品分類、原料性質、品質判定或衛生規範。"
            f"正確選項「{correct_name}」與該分類或規範最直接對應；{extra_sentence}"
            f"{wrong_text} 則屬於相近名詞、其他產品類別、不同原料功能或不符題幹條件的選項。"
        )

    return (
        f"{why} 本題屬於「{topic}」範圍，複習時可整理成「題幹條件 -> 正確答案 -> 排除理由」，"
        f"避免只背選項而無法判斷相似題。"
    )


def parse():
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    current_work = None
    current_topic = ""
    items = []

    for line in text.splitlines():
        section = re.match(r"^##\s*工作項目\s*(\d+)：(.+)$", line)
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
    multiple_total = sum(1 for item in items if item["multiple"])
    units = "\n".join(
        f"""
## 單元{int(work)}：{topic}

```yaml
id: u-{int(work)}
subtitle: 工作項目 {work}，共 {sum(1 for item in items if item["work"] == work)} 題
time: 自主練習
```

### 學習目標

- 熟悉「{topic}」在烘焙丙級學科中的常見考點。
- 能依據烘焙原料學、製程控制、品質鑑定、成本管理與食品衛生規範判斷正確答案。

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
            "勞動部勞動力發展署技能檢定中心，烘焙食品丙級技術士技能檢定學科測試參考資料；"
            "衛生福利部食品藥物管理署，食品安全衛生管理法及食品良好衛生規範準則；"
            "烘焙原料、產品製作、品質管制、包裝保存與成本計算相關公開教學資料。"
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
            f"""## Q{item["global_no"]} ｜ {heading}

工作項目 {item["work"]}「{item["topic"]}」第 {item["local_no"]} 題：
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
title: 烘焙丙級學科測試參考資料
subtitle: 115.07 題庫線上練習考場
program: 烘焙食品技術士技能檢定
organizer: 勞動部勞動力發展署技能檢定中心題庫整理
dates: 115.07
location: 線上測驗系統
format: 題庫自主練習 / 120 分鐘限時挑戰
instructor: 烘焙丙級學科輔助解析
storeKey: 115-baking-c-progress-v1
timerSeconds: 7200
```

## 學習目標

- 完成烘焙丙級學科測試參考資料 6 個工作項目的完整練習。
- 熟悉產品分類、原料選用、產品製作、品質鑑定、烘焙食品包裝與食品貯存。
- 透過逐題答案、出處與 AI 分析，建立可複習的錯題筆記。

## 考科時程

| 建議時間 | 考科單元 | 考核重點 |
|---|---|---|
| 00:00 ~ 00:30 | 工作項目 01-02 | 產品分類與原料選用 |
| 00:30 ~ 01:00 | 工作項目 03-04 | 產品製作與品質鑑定 |
| 01:00 ~ 01:30 | 工作項目 05 | 烘焙食品之包裝 |
| 01:30 ~ 02:00 | 工作項目 06 | 食品之貯存 |

---

# DAY1

```yaml
id: day1
n: 1
date: 115.07
title: 烘焙丙級學科題庫練習
hours: 2.0
date_label: 115.07
hours_label: 2.0 小時 (120分鐘)
learningGoal: 完成烘焙丙級學科 6 個工作項目的完整題庫練習。
hero_title: 烘焙丙級學科練習
hero_lead: 本題庫共 {total} 題，皆為單選題；系統以答對題數換算百分制。
```

{units}

---

# MATERIALS

- [MD] baking-c-exam.md | 烘焙丙級學科測試參考資料原始題庫

---

# PORTAL

```yaml
title: 學術能力模擬檢測入口
subtitle: 歡迎來到模擬考試線上平台。本系統已依照不同試題與科目分類，請點擊下方對應的卡片進入考場進行線上作答與評分。
```

## 考試卡片

```yaml
id: exam-115-baking-c
tag: 烘焙丙級
title: 烘焙丙級學科測試參考資料
desc: 115.07 版烘焙丙級學科題庫，共 {total} 題，涵蓋產品分類、原料選用、產品製作、品質鑑定、烘焙食品包裝與食品貯存。
time: 120 分鐘
questions: 共 {total} 題
score: 滿分 100 分
href: 115-baking-c/
btnText: 進入線上考場
```

---

# QUIZ

{"".join(quiz_blocks)}
"""


if __name__ == "__main__":
    items = parse()
    OUTPUT.write_text(build_content(items), encoding="utf-8")
    print(f"Parsed {len(items)} questions -> {OUTPUT}")
