from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "baking-109-official-exam.md"
OUTPUT = ROOT / "content.md"

TITLE = "109 學年度商業類學生技藝競賽烘焙職種學科正式試題"
STORE_KEY = "109-baking-progress-v1"
PORTAL_ID = "exam-109-baking"
HREF = "109-baking/"
MATERIAL = "baking-109-official-exam.md"

SOURCE_NOTE = (
    "109 學年度商業類學生技藝競賽烘焙職種學科正式試題與答案卷；"
    "烘焙食品技術士學科教材、烘焙原料學、麵包與西點製程、食品加工與食品安全衛生相關公開教學資料。"
)

TOPIC_HINTS = {
    "乳沫": "乳沫類蛋糕主要靠蛋白泡沫或全蛋打發形成氣室，與麵糊類蛋糕以油脂乳化建立組織的原理不同。",
    "蛋白": "蛋白泡沫受油脂、溫度與攪拌狀態影響；油脂會干擾蛋白質展開與氣泡膜穩定。",
    "麵糰": "麵糰製程需同時控制水化、麵筋形成、溫度與攪拌程度，題目通常可由這些製程條件判斷。",
    "麵包": "麵包品質取決於麵筋網絡、酵母發酵、配方平衡與烤焙控制，答案需回到這些基本原理判斷。",
    "酵母": "酵母能發酵可利用糖類並產生二氧化碳與風味物質，糖類種類與溫度會影響發酵速度。",
    "發酵": "發酵條件需兼顧酵母活性與麵糰穩定，溫度、濕度與時間過度都會造成品質缺失。",
    "派": "派皮重點在油脂可塑性、低溫操作與降低出筋，才能形成酥鬆分層。",
    "蛋糕": "蛋糕組織由乳化、打發、麵糊比重與烤焙膨脹共同決定，需依蛋糕類型判斷。",
    "餅乾": "餅乾口感與麵粉筋性、糖油比例、水分及膨大劑有關，酥、脆、硬的來源不同。",
    "烘焙": "烘焙過程包含澱粉糊化、蛋白質凝固、糖褐變與水分蒸發，題目可由這些變化判斷。",
    "食品": "食品安全與食品加工題需依保存溫度、水活性、酸鹼值、標示與衛生規範判斷。",
    "包裝": "包裝材料需依阻氣、阻濕、耐熱、遮光與衛生安全性選用。",
    "冷凍": "冷凍與冷藏題的核心是抑制微生物與品質劣化，但不能把低溫視為完全殺菌。",
}

OPTION_TEXT_FIXES = {
    # The source markdown has OCR-damaged option labels in these questions.
    # Keep the corrections explicit so they can be checked against later errata.
    11: {"A": "無關"},
    16: {"C": "油脂", "D": "原始題本缺漏，非本題答案"},
    21: {"A": "2一4倍"},
    22: {"A": "低筋麵粉"},
    26: {"A": "50"},
    38: {"A": "水", "B": "油脂"},
}

QUESTION_TEXT_FIXES = {
    38: "調整麵包配方時，下列何者材料會使麵包麵糰較軟",
}


def normalize(text):
    text = text.replace("（", "(").replace("）", ")")
    text = text.replace("°", "°")
    text = text.replace("(Å)", "(A)").replace("(å)", "(A)").replace("(A•)", "(A)")
    return re.sub(r"\s+", " ", text.strip()).strip("。 ")


def parse_answer_table(text):
    answers = {}
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        for no, answer in re.findall(r"\|\s*(\d+)\s*\|\s*([A-D])\s*", line):
            answers[int(no)] = answer
    return answers


def is_question_line(line):
    return bool(re.match(r"^\(\)+\)?\s*\d+\s*\.?", line.strip()))


def split_question_blocks(text):
    blocks = []
    current = []
    for line in text.splitlines():
        if line.startswith("---") or line.lstrip().startswith("|"):
            break
        if is_question_line(line):
            if current:
                blocks.append(" ".join(current))
            current = [line.strip()]
        elif current and line.strip():
            current.append(line.strip())
    if current:
        blocks.append(" ".join(current))
    return blocks


def option_markers(rest):
    matches = []
    for match in re.finditer(r"(?i)(?:\(([A-D])\)|\b([A-D])\))", rest):
        letter = (match.group(1) or match.group(2)).upper()
        # Skip English abbreviations; option labels are followed by Chinese, number, or punctuation.
        tail = rest[match.end() : match.end() + 1]
        if tail and tail.isalpha() and tail.isascii():
            continue
        matches.append((letter, match.start(), match.end()))
    return matches


def parse_items():
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    answers = parse_answer_table(text)
    if len(answers) != 50:
        raise SystemExit(f"Expected 50 answer-table entries, got {len(answers)}")

    items = []
    for block in split_question_blocks(text):
        m = re.match(r"^\(\)+\)?\s*(\d+)\s*\.?\s*(.+)$", block)
        if not m:
            continue
        no = int(m.group(1))
        rest = normalize(m.group(2))
        markers = option_markers(rest)
        if not markers:
            raise SystemExit(f"Question {no} has no option markers")

        question = normalize(rest[: markers[0][1]])
        question = QUESTION_TEXT_FIXES.get(no, question)
        parsed = {}
        for idx, (letter, start, end) in enumerate(markers):
            next_start = markers[idx + 1][1] if idx + 1 < len(markers) else len(rest)
            parsed[letter] = normalize(rest[end:next_start].lstrip("* "))

        options = []
        for letter in "ABCD":
            value = parsed.get(letter, "")
            if not value:
                value = "（原始題本未清楚列出）"
            value = OPTION_TEXT_FIXES.get(no, {}).get(letter, value)
            options.append((letter, value))

        if no not in answers:
            raise SystemExit(f"Question {no} missing answer in table")
        items.append({"no": no, "question": question, "options": options, "answer": answers[no]})

    return items


def unit_for(no):
    if no <= 15:
        return "day1.u-1"
    if no <= 30:
        return "day1.u-2"
    return "day1.u-3"


def principle_for(question):
    for key, hint in TOPIC_HINTS.items():
        if key in question:
            return hint
    return "本題應回到烘焙原料功能、製程控制、食品安全或品質判定的基本原理判斷。"


def analysis_for(item):
    answer_text = next(text for letter, text in item["options"] if letter == item["answer"])
    wrong = "；".join(f"{letter}. {text}" for letter, text in item["options"] if letter != item["answer"])
    missing_note = ""
    if any("原始題本未清楚列出" in text for _, text in item["options"]):
        missing_note = " 本題原始題本有部分選項文字缺漏，已依可讀內容與答案表保留並標記。"
    return (
        f"本題正答為（{item['answer']}）{answer_text}。{principle_for(item['question'])}"
        f"題幹要求辨識最符合條件的選項，而（{item['answer']}）能直接對應題目中的關鍵條件。"
        f"其他選項如 {wrong}，與本題所問的原料功能、製程條件、保存安全或品質判定不完全相符，"
        f"因此不是最佳答案。{missing_note}"
    )


def render_question(item):
    options = "\n".join(f"- ({letter}) {text}" for letter, text in item["options"])
    return f"""## Q{item['no']}

{item['question']}

{options}

```yaml
answer: {item['answer']}
unit: {unit_for(item['no'])}
explanation: |
  【正確答案】({item['answer']})
  【文獻出處】{SOURCE_NOTE}
  【AI 分析】{analysis_for(item)}
```
"""


def build_content(items):
    total = len(items)
    quiz = "\n".join(render_question(item) for item in items)
    return f"""# META

```yaml
title: {TITLE}
subtitle: 烘焙職種學科線上正式考場
program: 商業類學生技藝競賽烘焙職種
organizer: 109 學年度商業類學生技藝競賽正式試題整理
dates: 109 學年度
location: 線上測驗
format: 單選題 / {total} 題
instructor: 烘焙職種學科題庫解析
storeKey: {STORE_KEY}
timerSeconds: 3600
scorePerQuestion: 2
```

## 測驗目標

- 完成 109 學年度商業類學生技藝競賽烘焙職種學科正式試題 {total} 題完整練習。
- 熟悉蛋糕與麵包製程、麵糰攪拌、酵母發酵、派皮與餅乾、食品包裝保存、烘焙原料與品質判定。
- 每題作答後閱讀 AI 分析，理解正確答案背後的烘焙原理與干擾選項差異。

## 建議作答節奏

| 時間區間 | 題目範圍 | 重點 |
|---|---|---|
| 00:00 ~ 00:20 | Q1-Q15 | 蛋糕分類、蛋白打發、麵糰攪拌與品質評定 |
| 00:20 ~ 00:40 | Q16-Q30 | 派皮、麵包製程、烘焙評分、食品與包裝保存 |
| 00:40 ~ 01:00 | Q31-Q50 | 比例換算、蛋糕配方、發酵條件、原料與食品安全 |

---

# DAY1

```yaml
id: day1
n: 1
date: 109 學年度
title: 109 學年度烘焙職種學科正式試題
hours: 1.0
date_label: 109 學年度
hours_label: 1.0 小時（60 分鐘）
learningGoal: 完成 109 學年度商業類學生技藝競賽烘焙職種學科正式試題 {total} 題練習。
hero_title: 109 烘焙職種學科正式試題
hero_lead: 依正式試題與答案卷整理為線上測驗，每題 2 分，滿分 100 分。
```

## 單元 1：蛋糕、蛋白打發與麵糰攪拌

```yaml
id: u-1
subtitle: 第 1 題至第 15 題，每題 2 分
time: 00:00 ~ 00:20
```

### 學習重點

- 判讀乳沫類與麵糊類蛋糕差異、蛋白泡沫、麵糰攪拌與麵包品質缺失。

## 單元 2：派皮、發酵、評分與保存

```yaml
id: u-2
subtitle: 第 16 題至第 30 題，每題 2 分
time: 00:20 ~ 00:40
```

### 學習重點

- 熟悉派皮材料、麵包發酵條件、烘焙評分、食品加工與包裝保存。

## 單元 3：比例換算、配方與食品安全

```yaml
id: u-3
subtitle: 第 31 題至第 50 題，每題 2 分
time: 00:40 ~ 01:00
```

### 學習重點

- 整合材料比例、蛋糕配方、酵母與膨大劑、最終發酵、包裝材料與品質判斷。

---

# MATERIALS

- [MD] {MATERIAL} | 109 學年度烘焙職種學科正式試題原始題本

---

# PORTAL

```yaml
title: 線上考場入口
subtitle: 技藝競賽學科測驗平台
```

## 入口卡片

```yaml
id: {PORTAL_ID}
tag: 烘焙職種
title: 109 學年度烘焙職種學科正式試題
desc: 109 學年度商業類學生技藝競賽烘焙職種學科正式試題，共 {total} 題，涵蓋蛋糕與麵包製程、麵糰攪拌、派皮與餅乾、食品保存、烘焙原料與品質判定。
time: 60 分鐘
questions: 共 {total} 題
score: 滿分 100 分
href: {HREF}
btnText: 進入測驗
```

---

# QUIZ

{quiz}
"""


def main():
    items = parse_items()
    if len(items) != 50:
        raise SystemExit(f"Expected 50 questions, got {len(items)}")
    actual = [item["no"] for item in items]
    expected = list(range(1, 51))
    if actual != expected:
        raise SystemExit(f"Unexpected question sequence: {actual}")
    OUTPUT.write_text(build_content(items), encoding="utf-8")
    print(f"Parsed {len(items)} questions -> {OUTPUT}")


if __name__ == "__main__":
    main()
