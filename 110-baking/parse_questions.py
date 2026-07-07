from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "baking-110-official-exam.md"
OUTPUT = ROOT / "content.md"

TITLE = "110 學年度商業類學生技藝競賽烘焙職種學科正式試題"
STORE_KEY = "110-baking-progress-v1"
PORTAL_ID = "exam-110-baking"
HREF = "110-baking/"
MATERIAL = "baking-110-official-exam.md"

SOURCE_NOTE = (
    "110 學年度商業類學生技藝競賽烘焙職種學科正式試題與參考答案；"
    "烘焙食品技術士學科教材、烘焙原料學、麵包與西點製程、"
    "食品加工與食品安全衛生相關公開教學資料。"
)

TOPIC_HINTS = {
    "雞蛋": "雞蛋在烘焙中提供凝固、乳化、起泡與色澤；判斷時要看題目問的是蛋黃、蛋白或全蛋的主要功能。",
    "蛋白": "蛋白質受熱會凝固，攪拌可形成泡沫；油脂、溫度與酸鹼會影響泡沫穩定與產品體積。",
    "蛋黃": "蛋黃含卵磷脂與脂質，常提供乳化、柔軟口感與色澤，與純蛋白的起泡功能不同。",
    "糖": "糖在烘焙中影響甜味、保濕、上色、發酵可用性與結晶性；不同糖漿來源與製法會造成用途差異。",
    "油": "油脂能潤滑組織、阻礙部分麵筋形成並提供酥鬆或柔軟口感；不同油脂的熔點與可塑性不同。",
    "奶油": "奶油與相關油脂的判斷重點在來源、可塑性、乳化型態與是否適合裹入或打發。",
    "乾酪": "乾酪由牛乳蛋白凝乳、排乳清與熟成而成，與鮮奶、奶粉等乳製品製程不同。",
    "泡打粉": "泡打粉由鹼性膨鬆劑、酸性鹽與填充劑組成，遇水與加熱產生二氧化碳使產品膨大。",
    "膨脹": "化學膨大與酵母發酵都會產氣，但來源、反應條件與適用產品不同，須依題幹產品判斷。",
    "乳化": "乳化是使水相與油相穩定分散；蛋黃卵磷脂是烘焙中常見的天然乳化成分。",
    "巧克力": "調溫巧克力的核心在可可脂晶型控制；非調溫產品常以其他油脂系統取代或調整。",
    "台斤": "台制重量換算中一台斤為 600 公克，常用於原料採購與配方換算。",
    "吐司": "吐司入模與最後發酵高度會影響入爐膨脹、成品外形與組織，須控制到適當滿模程度。",
    "麵包": "麵包品質取決於麵筋網絡、酵母發酵、配方平衡、整形與烤焙條件。",
    "麵粉": "麵粉的蛋白質、灰分、粒度與筋性會影響吸水、顏色、麵筋形成與產品適性。",
    "麵筋": "麵筋含量與品質決定麵糰彈性、延展性與保氣能力；不同產品需要不同筋度。",
    "餅乾": "餅乾重點在低水分、糖油比例、成形方式與是否形成麵筋；不同類型口感差異很大。",
    "小西餅": "小西餅成形方式與麵糊性質相關，保存時須控制冷卻與防潮，避免回軟或變質。",
    "酵母": "酵母發酵將糖轉為二氧化碳、酒精與風味物質，主要應用於麵包類產品。",
    "發酵": "發酵控制重點為溫度、濕度、時間與麵糰狀態，會直接影響體積、組織與風味。",
    "鹽": "鹽能強化麵筋、調味並抑制微生物或酵母過度作用，因此不是單純讓麵糰柔軟。",
    "塔塔粉": "塔塔粉常用於穩定蛋白泡沫，其主要化學成分為酒石酸氫鉀。",
    "起酥油": "起酥油或裹入油脂要具備合適可塑性與熔點，才能形成層次並支撐產品結構。",
    "派": "派皮與酥皮類產品重點在低溫操作、油脂包覆與降低過度出筋，才能形成酥鬆層次。",
    "蛋糕": "蛋糕組織由打發、乳化、麵糊比重、麵粉筋性與烤焙膨脹共同決定。",
    "戚風": "戚風蛋糕依賴蛋白泡沫與麵糊乳化平衡，膨大劑選擇與拌合狀態會影響體積與底部狀況。",
    "磅蛋糕": "磅蛋糕屬重奶油蛋糕系統，重點在糖油拌合、乳化與麵糊比重。",
    "食品": "食品標示、保存與安全題須依衛生規範、保存條件、包材功能與禁止療效宣稱判斷。",
    "包裝": "包材選擇要考慮阻氧、阻濕、遮光、熱封性與印刷性；不同材質用途不同。",
    "烤爐": "烤爐與烘焙設備題須理解設備用途、容量限制與歷史或操作情境。",
}


def normalize(text):
    text = text.replace("，", ",")
    text = re.sub(r"\s+", " ", text.strip())
    return text.strip("。 ")


def parse_answer_table(text):
    answers = {}
    for no, answer in re.findall(r"\|\s*\*{0,2}(\d+)\*{0,2}\s*\|\s*([A-D])\s*", text):
        answers[int(no)] = answer
    return answers


def parse_items():
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    answer_table = parse_answer_table(text)
    if len(answer_table) != 50:
        raise SystemExit(f"Expected 50 answer-table entries, got {len(answer_table)}")

    pattern = re.compile(
        r"^\s*(\d+)\.\s*\*\*\(\s*([A-D])\s*\)\*\*\s*(.*?)(?=^\s*\d+\.\s*\*\*\(|\n---\n\s*### 二、|\Z)",
        re.M | re.S,
    )
    items = []
    for match in pattern.finditer(text):
        no = int(match.group(1))
        inline_answer = match.group(2)
        block = match.group(3).strip()

        option_matches = list(re.finditer(r"^\s*-\s*\(([A-D])\)\s*(.*?)\s*$", block, re.M))
        if len(option_matches) != 4:
            raise SystemExit(f"Question {no} expected 4 options, got {len(option_matches)}")

        question = normalize(block[: option_matches[0].start()])
        options = [(m.group(1), normalize(m.group(2))) for m in option_matches]

        table_answer = answer_table.get(no)
        if not table_answer:
            raise SystemExit(f"Question {no} missing answer in table")
        if table_answer != inline_answer:
            raise SystemExit(f"Question {no} answer mismatch: inline={inline_answer}, table={table_answer}")

        items.append({"no": no, "question": question, "options": options, "answer": table_answer})

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
    return (
        f"本題正答為（{item['answer']}）{answer_text}。{principle_for(item['question'])}"
        f"題幹的關鍵是「{item['question']}」，（{item['answer']}）能直接符合該原料、製程或品質條件。"
        f"其他選項如 {wrong}，雖可能是相關名詞或材料，但與題目指定條件不完全相符，因此不是最佳答案。"
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
organizer: 110 學年度商業類學生技藝競賽正式試題整理
dates: 110 學年度
location: 線上測驗
format: 單選題 / {total} 題
instructor: 烘焙職種學科題庫解析
storeKey: {STORE_KEY}
timerSeconds: 3600
scorePerQuestion: 2
```

## 測驗目標

- 完成 110 學年度商業類學生技藝競賽烘焙職種學科正式試題 {total} 題完整練習。
- 熟悉雞蛋與乳製品、糖油與膨鬆劑、麵包製程、餅乾與蛋糕、包裝保存、設備與食品安全等考點。
- 每題作答後閱讀 AI 分析，理解正確答案背後的烘焙學理與干擾選項差異。

## 建議作答節奏

| 時間區間 | 題目範圍 | 重點 |
|---|---|---|
| 00:00 ~ 00:20 | Q1-Q15 | 雞蛋、糖油、乳製品、膨鬆劑、吐司與麵粉基礎 |
| 00:20 ~ 00:40 | Q16-Q30 | 麵粉性質、餅乾成形、麵包與蛋糕製程、食品保存 |
| 00:40 ~ 01:00 | Q31-Q50 | 配方比例、戚風與磅蛋糕、設備包裝、烘焙趨勢與安全 |

---

# DAY1

```yaml
id: day1
n: 1
date: 110 學年度
title: 110 學年度烘焙職種學科正式試題
hours: 1.0
date_label: 110 學年度
hours_label: 1.0 小時（60 分鐘）
learningGoal: 完成 110 學年度商業類學生技藝競賽烘焙職種學科正式試題 {total} 題練習。
hero_title: 110 烘焙職種學科正式試題
hero_lead: 依正式試題與參考答案建置為線上測驗，每題 2 分，滿分 100 分。
```

## 單元 1：原料性質與麵包基礎

```yaml
id: u-1
subtitle: 第 1 題至第 15 題，每題 2 分
time: 00:00 ~ 00:20
```

### 學習重點

- 掌握雞蛋組成、蛋白質功能、糖油乳化、膨鬆劑與麵粉蛋白含量等基礎概念。

## 單元 2：製程控制與產品分類

```yaml
id: u-2
subtitle: 第 16 題至第 30 題，每題 2 分
time: 00:20 ~ 00:40
```

### 學習重點

- 熟悉麵粉吸水與筋性、餅乾成形、發酵性麵糰、蛋糕麵糊、食品保存與包材基礎。

## 單元 3：配方、設備與食品安全

```yaml
id: u-3
subtitle: 第 31 題至第 50 題，每題 2 分
time: 00:40 ~ 01:00
```

### 學習重點

- 釐清配方比例、蛋糕缺失、烘焙設備操作、包裝標示、地方特色與烘焙趨勢。

---

# MATERIALS

- [MD] {MATERIAL} | 110 學年度烘焙職種學科正式試題原始題本

---

# PORTAL

```yaml
title: 線上測驗入口
subtitle: 商業類技藝競賽正式試題練習
```

## 入口卡片

```yaml
id: {PORTAL_ID}
tag: 烘焙職種
title: 110 學年度烘焙職種學科正式試題
desc: 110 學年度商業類學生技藝競賽烘焙職種學科正式試題，共 {total} 題，涵蓋原料性質、麵包製程、餅乾蛋糕、食品保存、包裝設備與烘焙趨勢。
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
