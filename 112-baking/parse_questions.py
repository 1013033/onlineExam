from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "baking-112-official-exam.md"
OUTPUT = ROOT / "content.md"

TITLE = "112 學年度商業類學生技藝競賽烘焙職種學科正式試題"
STORE_KEY = "112-baking-progress-v1"
PORTAL_ID = "exam-112-baking"
HREF = "112-baking/"
MATERIAL = "baking-112-official-exam.md"

SOURCE_NOTE = (
    "112 學年度商業類學生技藝競賽烘焙職種學科正式試題與更正版參考答案；"
    "烘焙食品技術士學科教材、烘焙原料學、麵包與西點製程、"
    "食品加工與食品安全衛生相關公開教學資料。"
)

TOPIC_HINTS = {
    "轉化糖": "轉化糖漿與翻糖等糖製品的判斷重點在原料、結晶性、可塑性與裝飾用途。",
    "液蛋": "液蛋衛生標準重點在原料蛋完整性、殺菌或未殺菌產品的微生物限量與食安規範。",
    "鮮奶油": "鮮奶油須分辨動物性與植物性來源、打發性、適口性與配方用途。",
    "攪拌機": "攪拌設備需受容量限制；投料過量會影響攪拌效率、設備負荷與產品品質。",
    "裹油": "裹油麵包或起酥產品靠油脂包入與折疊形成層次，麵糰與油脂硬度需匹配。",
    "穀物": "全穀與穀物添加標示需依規定比例判斷，不同宣稱有不同最低含量要求。",
    "戚風": "戚風蛋糕依賴蛋白泡沫與中空或活動烤模支撐，烤模選擇會影響脫模與結構。",
    "麵包": "麵包品質取決於麵筋網絡、發酵程度、整形、蒸氣或噴水與烘烤條件。",
    "吐司": "吐司最後發酵、出爐冷卻與切片溫度會影響體積、組織、切面與包裝品質。",
    "麵粉": "麵粉依小麥品種、蛋白質含量、筋度與用途區分，高低筋適合的產品不同。",
    "牛角": "牛角麵包重點在包油硬度、折疊冷藏鬆弛與層次控制，操作溫度尤其重要。",
    "貝果": "貝果需經熱水或煮料處理，使表皮定型並形成特殊咀嚼感。",
    "小布利": "小布利麵包需控制攪拌、發酵、整形圈數與表面裝飾，避免層次與外觀失準。",
    "全穀": "全穀食品宣稱須符合全穀成分比例與標示原則，百分比是判斷關鍵。",
    "冷凍": "液體蛋冷凍前需防止蛋白質變性，常以糖類等保護性配方改善凍藏品質。",
    "海藻糖": "海藻糖甜度較低，具有抑制澱粉老化、保濕與延長保存期等應用特性。",
    "乳製品": "乳製品替代需依水分、乳固形物與脂肪比例換算，不能只看重量相等。",
    "蛋糕": "蛋糕膨大來自空氣、水蒸氣、膨大劑與蛋白結構，不同材料對膨大貢獻不同。",
    "塔": "塔皮需控制低筋麵粉、糖油拌合法、鬆弛與戳孔，避免收縮或膨脹。",
    "鬆餅": "鬆餅或酥皮類產品的膨大受包油、折疊、鬆弛、切割與油脂熔點影響。",
    "披薩": "披薩餅皮筋度、發酵、麵粉配比與烤焙條件會決定厚薄、韌性與酥脆度。",
    "道納司": "道納司配方接近甜麵包，但油炸與糖油比例會影響口感、體積與吸油。",
    "布丁": "蒸烤布丁需要控制蛋乳混合溫度與隔水烘烤溫度，使凝固細緻不粗糙。",
    "油脂": "油脂在烘焙中提供潤滑、酥鬆、光澤與保濕，但不是蛋糕膨大的直接氣體來源。",
    "中種": "中種法主麵糰與中種麵糰原料分工不同，酵母通常已在中種階段使用。",
    "甘納許": "甘納許由巧克力與鮮奶油等組成，是被覆蛋糕和內餡常用材料。",
    "麵筋粉": "麵筋粉可提高麵糰筋度與韌性，常用於需要咀嚼性或支撐性的產品。",
}


def normalize(text):
    text = text.replace("，", ",")
    text = re.sub(r"\s+", " ", text.strip())
    return text.strip("。 ")


def parse_answer_value(raw):
    raw = raw.strip().replace(" ", "")
    if "或" in raw:
        return raw.split("或")
    if "、" in raw:
        return raw.split("、")
    return raw


def answer_for_yaml(answer):
    if isinstance(answer, list):
        return "[" + ", ".join(answer) + "]"
    return answer


def answer_label(answer):
    if isinstance(answer, list):
        return " 或 ".join(f"({letter})" for letter in answer)
    return f"({answer})"


def parse_answer_table(text):
    answers = {}
    pattern = r"\|\s*\*{0,2}(\d+)\*{0,2}\s*\|\s*([A-D](?:\s*[或、]\s*[A-D])?)\s*"
    for no, answer in re.findall(pattern, text):
        answers[int(no)] = parse_answer_value(answer)
    return answers


def parse_items():
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    answer_table = parse_answer_table(text)
    if len(answer_table) != 50:
        raise SystemExit(f"Expected 50 answer-table entries, got {len(answer_table)}")

    pattern = re.compile(
        r"^\s*(\d+)\.\s*\*\*\(\s*([A-D](?:\s*[或、]\s*[A-D])?)\s*\)\*\*\s*(.*?)(?=^\s*\d+\.\s*\*\*\(|\n---\n\s*### 二、|\Z)",
        re.M | re.S,
    )
    items = []
    for match in pattern.finditer(text):
        no = int(match.group(1))
        inline_answer = parse_answer_value(match.group(2))
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
    answer_letters = item["answer"] if isinstance(item["answer"], list) else [item["answer"]]
    answer_text = " 或 ".join(
        f"({letter}){text}" for letter, text in item["options"] if letter in answer_letters
    )
    wrong = "；".join(f"{letter}. {text}" for letter, text in item["options"] if letter not in answer_letters)
    return (
        f"本題正答為{answer_label(item['answer'])}{answer_text}。{principle_for(item['question'])}"
        f"題幹的關鍵是「{item['question']}」，{answer_label(item['answer'])}能直接符合該原料、製程或品質條件。"
        f"其他選項如 {wrong}，雖可能是相關名詞或材料，但與題目指定條件不完全相符，因此不是最佳答案。"
    )


def render_question(item):
    options = "\n".join(f"- ({letter}) {text}" for letter, text in item["options"])
    return f"""## Q{item['no']}

{item['question']}

{options}

```yaml
answer: {answer_for_yaml(item['answer'])}
unit: {unit_for(item['no'])}
explanation: |
  【正確答案】{answer_label(item['answer'])}
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
organizer: 112 學年度商業類學生技藝競賽正式試題整理
dates: 112 學年度
location: 線上測驗
format: 單選題 / {total} 題
instructor: 烘焙職種學科題庫解析
storeKey: {STORE_KEY}
timerSeconds: 3600
scorePerQuestion: 2
```

## 測驗目標

- 完成 112 學年度商業類學生技藝競賽烘焙職種學科正式試題 {total} 題完整練習。
- 熟悉液蛋衛生、鮮奶油、裹油麵包、全穀標示、乳製品換算、塔皮鬆餅、披薩、布丁與蛋糕膨大等考點。
- 每題作答後閱讀 AI 分析，理解正確答案背後的烘焙學理與干擾選項差異。

## 建議作答節奏

| 時間區間 | 題目範圍 | 重點 |
|---|---|---|
| 00:00 ~ 00:20 | Q1-Q15 | 糖、液蛋、鮮奶油、設備、裹油麵包與麵粉分類 |
| 00:20 ~ 00:40 | Q16-Q30 | 全穀標示、液蛋冷凍、乳製品換算、鮮奶油與麵糊乳化 |
| 00:40 ~ 01:00 | Q31-Q50 | 塔皮鬆餅、披薩、道納司、布丁、油脂、吐司與蛋糕裝飾 |

---

# DAY1

```yaml
id: day1
n: 1
date: 112 學年度
title: 112 學年度烘焙職種學科正式試題
hours: 1.0
date_label: 112 學年度
hours_label: 1.0 小時（60 分鐘）
learningGoal: 完成 112 學年度商業類學生技藝競賽烘焙職種學科正式試題 {total} 題練習。
hero_title: 112 烘焙職種學科正式試題
hero_lead: 依正式試題與更正版參考答案建置為線上測驗，每題 2 分，滿分 100 分。
```

## 單元 1：原料、設備與麵包基礎

```yaml
id: u-1
subtitle: 第 1 題至第 15 題，每題 2 分
time: 00:00 ~ 00:20
```

### 學習重點

- 掌握轉化糖、液蛋衛生、鮮奶油、攪拌容量、裹油麵包、全穀添加與烤模刀具等基礎。

## 單元 2：標示、乳製品與乳化麵糊

```yaml
id: u-2
subtitle: 第 16 題至第 30 題，每題 2 分
time: 00:20 ~ 00:40
```

### 學習重點

- 熟悉全穀宣稱、冷凍液蛋、海藻糖、乳製品代換、打發鮮奶油、麵糊乳化與膨大原理。

## 單元 3：產品製程、包裝與品質缺失

```yaml
id: u-3
subtitle: 第 31 題至第 50 題，每題 2 分
time: 00:40 ~ 01:00
```

### 學習重點

- 釐清塔皮、鬆餅、披薩、道納司、布丁、油脂、吐司冷卻、發酵缺失與蛋糕裝飾材料。

---

# MATERIALS

- [MD] {MATERIAL} | 112 學年度烘焙職種學科正式試題原始題本

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
title: 112 學年度烘焙職種學科正式試題
desc: 112 學年度商業類學生技藝競賽烘焙職種學科正式試題，共 {total} 題，涵蓋液蛋衛生、裹油麵包、全穀標示、乳製品換算、塔皮鬆餅、披薩布丁與蛋糕膨大。
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
