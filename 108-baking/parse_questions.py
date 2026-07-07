from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "baking-108-official-exam.md"
OUTPUT = ROOT / "content.md"

TITLE = "108 學年度全國高級中等學校學生商業類技藝競賽烘焙職種學科正式試題"
STORE_KEY = "108-baking-progress-v1"
PORTAL_ID = "exam-108-baking"
HREF = "108-baking/"
MATERIAL = "baking-108-official-exam.md"

SOURCE_NOTE = (
    "108 學年度全國高級中等學校學生商業類技藝競賽烘焙職種學科正式試題；"
    "烘焙食品技術士學科教材、烘焙原料學、麵包與西點製程、食品加工與食品安全衛生相關公開教學資料。"
)

REASONS = {
    1: "麵糰攪拌不足時麵筋未充分擴展，通常造成體積小、組織粗糙、顆粒與條紋明顯；不會讓麵包體積變大。",
    2: "麵糰攪拌溫度偏高會加速麵筋形成與酵素、酵母作用，較快到達擴展階段，但也可能使麵糰過熱而品質不穩。",
    3: "攪拌主要功能是水化、拌合與發展麵筋；麵粉糖化屬澱粉酵素分解或加熱變化，不是攪拌本身的主要功能。",
    4: "擴展階段麵糰表面較光滑、有彈性與延展性，但薄膜仍容易斷裂，尚未達完成階段的充分延展。",
    5: "酵母最容易直接利用葡萄糖，發酵速度快於需先分解的砂糖、麥芽糖或不易利用的乳糖。",
    6: "麵包外部評定包含體積、表皮色澤與表皮質地；組織與結構屬內部評定項目。",
    7: "鬆餅麵糰筋性過強時可用酸性材料如檸檬汁調整麵筋，使麵糰較柔軟、便於壓延與操作。",
    8: "反式脂肪酸常見於部分氫化或反芻動物脂肪；選項中牛油較可能含有天然反式脂肪酸。",
    9: "天使蛋糕靠蛋白泡沫膨脹，通常打至濕性發泡以兼顧泡沫穩定與拌合延展性。",
    10: "麵包品質鑑定中內部組織、紋理、顏色與口感占比高，題目所列正確比例為 70%。",
    11: "快性發粉反應快速，適合需要快速膨脹的產品，如道納司；餅乾或油條常另有不同膨大系統。",
    12: "小麥麵粉蛋白質中麩胺酸含量高，是麵筋蛋白胺基酸組成的重要特色。",
    13: "派用油脂需較高融點與良好可塑性，45~48°C 的硬脂能維持派皮層次並減少操作時融化。",
    14: "水果派餡常以玉米澱粉糊化增稠，形成透明、可切而不過度流動的膠凍狀態。",
    15: "冷凍戚風派餡需要低溫下穩定凝結，動物膠適合形成柔軟膠體並維持冷凍派餡結構。",
    16: "鬆餅加冰水可使油脂與麵糊硬度接近、降低黏手並利於操作；它不是為了讓麵糰吸水較少。",
    17: "麵粉筋性主要取決於蛋白質含量與品質，蛋白質越高越能形成較強麵筋網絡。",
    18: "燙麵麵糰黏手主因是澱粉受熱糊化，吸水膨潤後使麵糰黏性提高。",
    19: "小麥磨粉前調濕可使麩皮韌化、胚乳較易粉碎，目的是讓麩皮易於剝離並提升製粉效率。",
    20: "油酥製作時油脂包覆麵粉並破壞麵筋形成，使筋性降低，形成酥鬆層次。",
    21: "蛋黃酥油皮豬油越多，油脂縮短麵筋並潤滑組織，口感越酥。",
    22: "油酥由低筋麵粉與油脂組成，重點是低筋、低水與高油脂，以避免出筋。",
    23: "蔥油餅常以燙麵或半燙麵製作，使麵糰柔軟、有延展性並保有層次。",
    24: "酵母菌發酵可產生二氧化碳使組織鬆軟，同時形成酒精、有機酸與香氣物質。",
    25: "烘焙食品受熱時糖與胺基化合物發生梅納反應，形成金黃色澤與烘焙香氣。",
    26: "小蘇打受熱或遇酸會釋放二氧化碳，是化學膨脹劑的膨大來源。",
    27: "氣體溶解性隨溫度升高而降低屬物理變化；二氧化碳生成、澱粉糊化和麵筋凝固都涉及化學或結構變化。",
    28: "澱粉破碎程度會大幅影響麵粉吸水，破損澱粉越多越容易吸水。",
    29: "麵筋彈性主要來自穀蛋白，醇溶蛋白則較影響延展性。",
    30: "雙皮派需較高溫使派皮迅速定型、著色並呈現鮮明色澤，題目所列最適溫度為 212°C。",
    31: "一磅約等於 454 公克，是烘焙秤量常用換算值。",
    32: "小蘇打粉即碳酸氫鈉，可作為烘焙膨脹劑；氫氧化鈉、氯化鈉與硼砂不適合此用途。",
    33: "麵包入爐初期受熱時氣體膨脹、酵母最後活化與水蒸氣形成，使體積主要在前十分鐘膨脹。",
    34: "麵包老化與澱粉回凝有關，糊化後的 α-澱粉逐漸轉為較有序的 β-澱粉狀態。",
    35: "蛋白在約 17~22°C 較利於打發，過冷泡沫形成慢，過熱則穩定性下降。",
    36: "蛋黃含乳化劑與脂質，可改善海綿蛋糕組織韌性，使口感較柔軟細緻。",
    37: "水果蛋糕屬重奶油蛋糕系統，通常以重奶油麵糊承載果乾與較高比例油糖。",
    38: "小西餅脆硬性主要由糖貢獻，糖能降低水活性、促進脆性並影響烤後硬度。",
    39: "發粉是碳酸氫鈉與酸性鹽類及填充物的混合膨大劑，受水與熱作用產生二氧化碳。",
    40: "麵糰發酵完成溫度若過高，乳酸菌或酸性代謝增加，易產生大量乳酸並影響風味與筋性。",
    41: "酥鬆餅乾需低筋麵粉降低麵筋形成，使口感鬆脆。",
    42: "可可粉是風味與色澤材料，不是膨脹劑；小蘇打、阿摩尼亞與發粉都能產氣膨大。",
    43: "烘焙百分比以麵粉為 100%，不論其他材料多少，題中低筋麵粉的百分比即為 100%。",
    44: "酵母為單細胞微生物，可發酵產生二氧化碳與香氣，但不能行光合作用。",
    45: "派皮用冰水可降低麵糰溫度，防止整形時油脂融化，維持酥鬆層次。",
    46: "奶油空心餅使用高筋麵粉是為了形成韌性與延展性承受蒸氣膨脹；麵筋脆弱易破裂不是目的。",
    47: "磅蛋糕傳統一磅材料為雞蛋、奶油、麵粉與糖；奶水不是四項基本一磅材料。",
    48: "高成分烘焙產品指糖與油脂含量高，配方會影響攪拌、乳化與烤焙結構。",
    49: "磅蛋糕麵糊比重較高，常見範圍約 0.83~0.85；比重過低或過高都會影響組織。",
    50: "新鮮蛋白 pH 約 7.6，貯藏後二氧化碳逸散，pH 會上升到約 9~9.6。",
}


def normalize(text):
    return re.sub(r"\s+", " ", text.strip()).strip("。 ")


def parse_items():
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    rows = []
    for raw in text.splitlines():
        line = raw.strip()
        if not re.match(r"^\d+\.\s*\([A-D]\)", line):
            continue
        m = re.match(r"^(\d+)\.\s*\(([A-D])\)\s*(.+)$", line)
        if not m:
            continue
        no = int(m.group(1))
        answer = m.group(2)
        rest = m.group(3)
        option_matches = list(re.finditer(r"\(([A-D])\)\s*", rest))
        if len(option_matches) != 4:
            raise SystemExit(f"Question {no} expected 4 options, got {len(option_matches)}")
        question = normalize(rest[: option_matches[0].start()])
        options = []
        for idx, opt in enumerate(option_matches):
            start = opt.end()
            end = option_matches[idx + 1].start() if idx + 1 < len(option_matches) else len(rest)
            options.append((opt.group(1), normalize(rest[start:end])))
        rows.append({"no": no, "question": question, "options": options, "answer": answer})
    return rows


def unit_for(no):
    if no <= 15:
        return "day1.u-1"
    if no <= 30:
        return "day1.u-2"
    return "day1.u-3"


def analysis_for(item):
    answer_text = next(text for letter, text in item["options"] if letter == item["answer"])
    wrong = "；".join(f"{letter}. {text}" for letter, text in item["options"] if letter != item["answer"])
    return (
        f"本題正答為（{item['answer']}）{answer_text}。{REASONS[item['no']]}"
        f"其他選項如 {wrong}，雖可能與烘焙原料、製程或食品加工概念相近，"
        f"但不符合題幹指定條件或正確學理判斷，因此不是本題最佳答案。"
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
program: 商業類科學生技藝競賽烘焙職種
organizer: 108 學年度全國高級中等學校學生商業類技藝競賽正式試題整理
dates: 108 學年度
location: 線上測驗
format: 單選題 / {total} 題
instructor: 烘焙職種學科題庫解析
storeKey: {STORE_KEY}
timerSeconds: 3600
scorePerQuestion: 2
```

## 測驗目標

- 完成 108 學年度全國高級中等學校學生商業類技藝競賽烘焙職種學科正式試題 {total} 題完整練習。
- 熟悉麵糰攪拌、酵母與糖類、派與蛋糕製程、油酥與中式麵食、食品膨脹劑、澱粉與蛋白質特性。
- 每題作答後閱讀 AI 分析，理解正確答案背後的烘焙原理與干擾選項差異。

## 建議作答節奏

| 時間區間 | 題目範圍 | 重點 |
|---|---|---|
| 00:00 ~ 00:20 | Q1-Q15 | 麵糰攪拌、酵母糖類、麵包品質、派餡與膠凍原料 |
| 00:20 ~ 00:40 | Q16-Q30 | 麵粉筋性、油酥與燙麵、烘焙膨脹、澱粉與麵筋蛋白 |
| 00:40 ~ 01:00 | Q31-Q50 | 換算、膨脹劑、蛋糕麵糊、烘焙百分比、蛋白與發酵控制 |

---

# DAY1

```yaml
id: day1
n: 1
date: 108 學年度
title: 108 學年度烘焙職種學科正式試題
hours: 1.0
date_label: 108 學年度
hours_label: 1.0 小時（60 分鐘）
learningGoal: 完成 108 學年度全國高級中等學校學生商業類技藝競賽烘焙職種學科正式試題 {total} 題練習。
hero_title: 108 烘焙職種學科正式試題
hero_lead: 依正式試題整理為線上測驗，每題 2 分，滿分 100 分。
```

## 單元 1：麵糰攪拌、酵母糖類與派餡

```yaml
id: u-1
subtitle: 第 1 題至第 15 題，每題 2 分
time: 00:00 ~ 00:20
```

### 學習重點

- 判讀麵糰攪拌階段、酵母糖類利用、麵包品質評定與派餡膠凍原理。

## 單元 2：麵粉、油酥與烘焙變化

```yaml
id: u-2
subtitle: 第 16 題至第 30 題，每題 2 分
time: 00:20 ~ 00:40
```

### 學習重點

- 熟悉麵粉筋性、燙麵糊化、油酥製作、膨脹原理、澱粉破碎與麵筋蛋白特性。

## 單元 3：膨脹劑、蛋糕與發酵控制

```yaml
id: u-3
subtitle: 第 31 題至第 50 題，每題 2 分
time: 00:40 ~ 01:00
```

### 學習重點

- 整合重量換算、食品膨脹劑、蛋糕組織、烘焙百分比、酵母特性與蛋白 pH。

---

# MATERIALS

- [MD] {MATERIAL} | 108 學年度烘焙職種學科正式試題原始題本

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
title: 108 學年度烘焙職種學科正式試題
desc: 108 學年度全國高級中等學校學生商業類技藝競賽烘焙職種學科正式試題，共 {total} 題，涵蓋麵糰攪拌、烘焙原料、派與蛋糕製程、食品膨脹劑、麵粉蛋白與發酵控制。
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
