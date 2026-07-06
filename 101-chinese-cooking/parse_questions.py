from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "chinese-cooking-101-official-exam.md"
OUTPUT = ROOT / "content.md"

ANSWER_INDEX = {"A": 0, "B": 1, "C": 2, "D": 3}
UNIT_ID = "day1.u-1"
TOPIC = "101 學年度中餐烹調正式競賽學科"

EXTRA_REASONS = {
    "鹽": "鹽能強化食材本味、平衡甜酸苦味，是中餐調味中最基本且最常用的鹹味來源，因此稱為百味之首。",
    "119": "台灣火災、救護等緊急事故通報電話為 119；110 是警察報案專線。",
    "腿心肉": "和尚頭是豬後腿中的腿心肉，肉質較完整，常用於切片、切絲或炒製。",
    "腰內肉": "腰內肉活動量少、肌纖維細嫩，適合需要滑嫩口感的醬爆肉片。",
    "腰腹肉": "牛腩常指牛腹、腰腹附近帶筋膜與脂肪的部位，適合燉、燒等長時間加熱。",
    "維生素 B": "胚芽米保留胚芽，富含維生素 B 群，較白米有更高營養價值。",
    "香菇": "香菇含多醣體，如香菇多醣，常被作為菇類營養與機能性成分考點。",
    "豬蹄膀": "跟刀劈適合處理骨大、組織厚的食材，豬蹄膀需借助刀背與刀刃配合劈斷。",
    "江浙菜": "蔥燒鯽魚重視鮮甜、醬香與細緻火候，屬江浙菜常見代表菜。",
    "膠化作用": "米飯加熱吸水後澱粉顆粒膨潤、糊化並形成可食的飯粒質地，題庫以膠化作用作答。",
    "速發酵母": "速發酵母屬生物膨大來源，靠酵母發酵產生二氧化碳，不屬化學膨大劑。",
    "花青素": "花青素對酸鹼敏感，酸性偏紅、鹼性偏藍綠，因此最容易因 pH 改變而變色。",
    "豬肉": "清真飲食禁食豬肉及其相關製品，這是宗教飲食規範的基本原則。",
    "魷魚乾": "魷魚乾常以鹼水發使組織吸水膨潤、恢復脆彈口感。",
    "武火": "爆是短時間高溫快速加熱的技法，需用武火保持鑊氣與脆嫩口感。",
    "紅蔥頭": "油蔥酥是紅蔥頭切片油炸後形成的香料配料，常用於台式料理增香。",
    "麥芽糖": "麥芽糖主要由澱粉糖化製成，不以甘蔗為主要原料；冰糖、黑糖、二砂多由蔗糖製得。",
    "在來米粉": "粉蒸排骨中的蒸肉粉通常以米粉類製成，在來米粉能吸附醬汁並提供米香。",
    "花椒": "麻辣味中的「麻」主要來自花椒的麻感成分，辣味則主要來自辣椒。",
}


def split_options(raw):
    matches = list(re.finditer(r"\(([A-D])\)", raw))
    if not matches:
        return raw.strip(), []

    question = raw[: matches[0].start()].strip(" ：:，,")
    options = []
    for i, match in enumerate(matches):
        letter = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        text = raw[start:end].strip()
        options.append((letter, text))
    return question, options


def analysis_for(question, options, answer_letter):
    correct = next((text for letter, text in options if letter == answer_letter), "")
    wrong = "、".join(f"{letter}. {text}" for letter, text in options if letter != answer_letter)
    extra = next((v for k, v in EXTRA_REASONS.items() if k in correct or k in question), "")
    extra_sentence = f"具體來說，{extra}" if extra else ""
    negative_words = ("不屬", "不是", "不可以", "不適合", "錯誤", "不符合", "並非", "最不")
    cuisine_words = ("菜系", "菜餚", "清真", "客家", "古代", "別稱", "俗稱")
    food_safety_words = ("火災", "中毒", "溫度", "濕度", "冷藏", "冷凍", "熱藏", "HACCP", "衛生")

    if any(word in question for word in negative_words):
        why = (
            f"本題答案為「{answer_letter}. {correct}」。題幹是否定式問法，重點是找出不符合分類、用途或規範的排除項。"
            f"正確選項「{correct}」之所以成立，是因為它與題幹要求不相符；{extra_sentence}"
            f"相對地，{wrong} 較符合題幹所列的同類概念或實務規則，所以不能選。"
        )
    elif any(word in question for word in cuisine_words):
        why = (
            f"本題答案為「{answer_letter}. {correct}」。這類題目考的是中餐飲食文化、菜系典故、食材別稱或地方產品的對應關係。"
            f"正確選項「{correct}」與題幹所指的菜系、名稱或飲食規範直接對應；{extra_sentence}"
            f"{wrong} 則屬其他菜系、其他食材或不同文化脈絡。"
        )
    elif any(word in question for word in food_safety_words):
        why = (
            f"本題答案為「{answer_letter}. {correct}」。判斷關鍵在食品安全、廚房安全或保存條件的標準規範。"
            f"正確選項「{correct}」符合題幹要求的安全處置、溫度條件或衛生管理原則；{extra_sentence}"
            f"{wrong} 不是本題標準條件，實務上可能造成通報錯誤、保存不當或衛生風險。"
        )
    else:
        why = (
            f"本題答案為「{answer_letter}. {correct}」。判斷關鍵在題幹所問的食材部位、原料特性、烹調技法、調味功能或單位換算。"
            f"正確選項「{correct}」與該中餐學科概念最直接對應；{extra_sentence}"
            f"{wrong} 是相近但不符合題幹條件的干擾選項。"
        )

    return (
        f"{why} 複習時可把本題整理成「題幹關鍵詞 -> 正確對應 -> 排除其他選項」，"
        f"這樣遇到相似的食材、菜系或衛生安全題時比較不會只靠記憶猜答。"
    )


def parse():
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    items = []
    for line in text.splitlines():
        match = re.match(r"^(\d+)\.\s*\(([A-D])\)\s*(.+)$", line)
        if not match:
            continue
        number = int(match.group(1))
        answer_letter = match.group(2)
        raw = match.group(3).strip()
        question, options = split_options(raw)
        items.append(
            {
                "global_no": number,
                "question": question,
                "options": options,
                "answer_letter": answer_letter,
                "answer_index": ANSWER_INDEX[answer_letter],
                "correct_text": next(text for letter, text in options if letter == answer_letter),
            }
        )
    return items


def build_content(items):
    total = len(items)
    source = (
        "101 學年度商業類科學生技藝競賽中餐烹調學科正式試卷；"
        "勞動部勞動力發展署技能檢定中心中餐烹調相關學科題庫；"
        "衛生福利部食品藥物管理署食品安全衛生管理法、食品良好衛生規範準則與餐飲衛生公開資料。"
    )
    quiz_blocks = []
    for item in items:
        options_md = "\n".join(f"- ({letter}) {text}" for letter, text in item["options"])
        analysis = analysis_for(item["question"], item["options"], item["answer_letter"])
        quiz_blocks.append(
            f"""## Q{item["global_no"]} ｜ 單選題

101 學年度中餐烹調正式競賽學科第 {item["global_no"]} 題：
{item["question"]}

{options_md}

```yaml
answer: {item["answer_letter"]}
unit: {UNIT_ID}
explanation: |
  【答案】({item["answer_letter"]})
  【出處】{source}
  【AI 分析】
  {analysis}
```
"""
        )

    return f"""# META

```yaml
title: 101 學年度中餐烹調正式競賽學科試卷
subtitle: 商業類科學生技藝競賽線上練習考場
program: 商業類科學生技藝競賽中餐烹調
organizer: 101 學年度商業類科學生技藝競賽試題整理
dates: 101
location: 線上測驗系統
format: 正式競賽學科試卷 / 50 題單選
instructor: 中餐烹調學科輔助解析
storeKey: 101-chinese-cooking-progress-v1
timerSeconds: 3600
```

## 學習目標

- 完成 101 學年度中餐烹調正式競賽學科 50 題完整練習。
- 熟悉中餐食材部位、菜系文化、烹調技法、食品安全、廚房安全與基礎換算。
- 透過逐題答案、出處與 AI 分析，建立可複習的錯題筆記。

## 考科時程

| 建議時間 | 考科單元 | 考核重點 |
|---|---|---|
| 00:00 ~ 00:15 | Q1-Q15 | 調味、食材部位、營養與基礎安全 |
| 00:15 ~ 00:30 | Q16-Q30 | 飲食文化、菜系、發料、火候與單位換算 |
| 00:30 ~ 00:45 | Q31-Q40 | 食材別稱、米食、芡汁、地方飲食 |
| 00:45 ~ 01:00 | Q41-Q50 | 加工食材、地方名產、肉質變化與風味來源 |

---

# DAY1

```yaml
id: day1
n: 1
date: 101
title: 101 學年度中餐烹調正式競賽學科練習
hours: 1.0
date_label: 101
hours_label: 1.0 小時 (60分鐘)
learningGoal: 完成 101 學年度中餐烹調正式競賽學科 50 題單選練習。
hero_title: 101 中餐烹調正式競賽學科
hero_lead: 本試卷共 {total} 題，皆為單選題；系統以答對題數換算百分制。
```

## 單元1：101 學年度正式競賽學科題庫

```yaml
id: u-1
subtitle: 共 {total} 題
time: 自主練習
```

### 學習目標

- 熟悉 101 學年度中餐烹調正式競賽學科的常見考點。
- 能依據中餐食材知識、菜系文化、烹調原理與食品衛生安全判斷正確答案。

### 任務清單

- [d1-u1-t1] 完成 101 學年度正式競賽學科 50 題練習。

---

# MATERIALS

- [MD] chinese-cooking-101-official-exam.md | 101 學年度中餐烹調正式競賽學科原始試卷

---

# PORTAL

```yaml
title: 學術能力模擬檢測入口
subtitle: 歡迎來到模擬考試線上平台。本系統已依照不同試題與科目分類，請點擊下方對應的卡片進入考場進行線上作答與評分。
```

## 考試卡片

```yaml
id: exam-101-chinese-cooking
tag: 中餐烹調
title: 101 學年度中餐烹調正式競賽學科
desc: 101 學年度商業類科學生技藝競賽中餐烹調正式學科試卷，共 {total} 題，涵蓋食材部位、菜系文化、烹調技法、食品安全與地方飲食。
time: 60 分鐘
questions: 共 {total} 題
score: 滿分 100 分
href: 101-chinese-cooking/
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
