from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "baking-104-mock-exam.md"
OUTPUT = ROOT / "content.md"

SOURCES = (
    "104 學年度商業類科學生技藝競賽【烘焙】職種【學科】模擬試卷；"
    "烘焙食品技術士技能檢定相關學科題庫；食品良好衛生規範準則；"
    "烘焙原料學、麵包與西點製程、營養計算、食品添加物、包裝保存與品質管制相關公開教學資料。"
)

REASONS = {
    1: "披薩餅皮需要足夠筋性支撐延展與咀嚼感，常用中筋與高筋麵粉搭配，兼顧成形性與脆韌口感。",
    2: "油脂每公克可提供 9 大卡，是三大營養素中熱量密度最高者。",
    3: "人造奶油與天然奶油在來源、風味、脂肪組成與加工方式不同；錯誤敘述通常混淆其原料來源或性質。",
    4: "蛋白發泡由起始擴展、濕性、硬性到乾性逐步形成，泡沫會由柔軟流動轉為尖峰直立。",
    5: "低成分重奶油蛋糕適合糖油拌合法，先打發油脂與糖包入空氣，再逐步乳化蛋液與粉類。",
    6: "活性麵筋粉或高筋麵粉能提升蛋白質與麵筋含量，使脆皮披薩麵糰更有筋性與韌度。",
    7: "黑糖、焦糖或未高度精製糖含較多糖蜜與色素風味物質，能增加特殊風味並加深色澤。",
    8: "蛋白在烘焙中屬韌性或結構性材料，受熱凝固後可支撐蛋糕、泡芙等產品組織。",
    9: "烘焙百分比以麵粉為 100%，奶粉 5kg / 麵粉 65kg = 7.69%，約為 7.7%。",
    10: "蛋糕包裝為延長保存常用脫氧劑、乾燥劑或防腐保鮮包材；題目正確選項符合延緩氧化或微生物生長的目的。",
    11: "蛋白、塔塔粉與細砂糖打發作為裝飾，屬蛋白霜飾，塔塔粉可穩定蛋白泡沫。",
    12: "標準量杯常以 1 杯約 240cc 計算，是烘焙配方常見容量換算。",
    13: "蛋白打至雪白尖峰挺立不下垂，屬硬性或乾性發泡階段，泡沫穩定且紋路明顯。",
    14: "雞蛋蛋白與蛋黃的 pH、凝固溫度與比例各有標準；錯誤選項通常在數值或性質上不符合蛋品原理。",
    15: "食品容器與器具應以清潔劑或合法方式洗滌並充分沖洗，目的在去除油污與食品殘渣。",
    16: "派皮油脂熔點約 40 至 42°C 較適合，能在操作時保持可塑性並在烘烤時形成酥鬆層次。",
    17: "中種法優點包含風味佳、老化較慢與發酵穩定；若選項描述不屬於中種法優點，即為答案。",
    18: "食品加工使用最多的溶劑是水，因其安全、便宜且能溶解多種食品成分。",
    19: "戚風蛋糕需要柔軟細緻組織，常用低筋麵粉，蛋白質約 8 至 9% 較適宜。",
    20: "酵母量 2 至 4% 時，一般麵糰基本發酵常約 1 至 3 小時，視溫度、糖量與配方而變動。",
    21: "烘焙油脂中合成抗氧化劑總量有法規限量，題目標準為 200ppm。",
    22: "中種法第一次攪拌的中種麵糰通常使用配方中大部分麵粉，約 70% 左右，以建立發酵風味與麵筋結構。",
    23: "機器皮帶運轉屬旋轉或捲入危害，操作時需避免手、衣物接近，並配置安全防護。",
    24: "蛋糕表面白色斑點常因砂糖顆粒太粗或未完全溶解，烤後在表面形成白點。",
    25: "鹽在蛋糕中可調味、平衡甜味並影響麵筋與蛋白質，但不是主要膨大來源。",
    26: "戚風蛋糕蛋白打發不足時支撐氣泡不足，成品容易體積小、組織粗或塌陷。",
    27: "穀類蛋白質常缺乏離胺酸，需搭配豆類等食物互補蛋白質品質。",
    28: "蛋糕配方中的奶粉通常歸為乾性材料或乳固形物，提供乳香、褐變與營養。",
    29: "依人體工學，超過約 25 公斤的重物應避免單人徒手搬運，以降低肌肉骨骼傷害風險。",
    30: "油脂熔點與飽和脂肪酸比例有關，氫化或動物性固態油脂通常熔點較高。",
    31: "油炸道納司油溫通常控制在約 180 至 190°C，能使外表定型上色且避免吸油過多。",
    32: "Ammonium bicarbonate 是碳酸氫銨，屬化學膨大劑，受熱會分解產生氣體。",
    33: "同樣烤模下，體積大、含水高或結構較密的蛋糕需要較長烤焙時間；題目正確選項符合熱傳較慢的產品。",
    34: "PS 是聚苯乙烯，常見於食品包裝或保麗龍相關材料，但耐熱性與使用條件需注意。",
    35: "硼砂進入人體後可轉為硼酸並蓄積，具有毒性，依法不得作為食品添加物使用。",
    36: "拉糖工藝需糖燈、剪刀、酒精燈或矽膠墊等工具；非相關工具即不是拉糖輔助工具。",
    37: "使用乾燥劑保存食品時，包材需低透濕性，才能阻止外界水氣進入並維持乾燥劑效果。",
    38: "烤酥性與油脂起酥能力、塑性和熔點有關；豬油或起酥油通常烤酥性較佳。",
    39: "1 卡定義為使 1 公克水升高 1°C 所需熱量，因此答案為 1°C。",
    40: "果糖甜度通常高於蔗糖、葡萄糖與乳糖，題列中最甜者為果糖。",
    41: "蛋塔、蘋果塔屬塔類或派塔類產品，以派皮或塔皮承裝餡料烘烤。",
    42: "6 磅約 2.72 公斤，雞蛋每公斤 45 元，約 122.4 元，取近似值 123 元。",
    43: "蛋黃含卵磷脂，是天然乳化劑，可幫助油水相混合並改善蛋糕組織。",
    44: "實際百分比總和 180%，麵糊總量 7.2kg，麵粉量為 7.2/1.8 = 4kg。",
    45: "奶油等乳脂類油脂在 35°C 易軟化、氧化或酸敗，保存時需低溫避光。",
    46: "蘇打餅乾含鹼性膨大劑或發酵調整，成品 pH 通常比一般奶油小西餅高。",
    47: "微波在食品上主要利用水分子等極性分子振動產熱，用於加熱或解凍。",
    48: "烘焙百分比永遠以麵粉為 100%，不受總百分比或麵粉實際重量影響。",
    49: "砂糖總量固定，原本每天 2kg 可用 20 天，總量 40kg；若每天 4kg，則可用 10 天。",
    50: "一顆蛋中蛋黃約三分之一、蛋白約三分之二；蛋黃占 20% 的說法不符合常見比例。"
}


def parse():
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    text = re.split(r"^###\s*(?:答案|參考答案|鈭)", text, maxsplit=1, flags=re.MULTILINE)[0]
    items = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        match = re.match(r"^\s*(\d+)\.\s*\*\*\(\s*([A-D])\s*\)\*\*\s*(.+)$", lines[i])
        if not match:
            i += 1
            continue
        no = int(match.group(1))
        answer = match.group(2)
        question = re.sub(r"\s+", " ", match.group(3).strip())
        options = []
        i += 1
        while i < len(lines):
            if re.match(r"^\s*\d+\.\s*\*\*\(", lines[i]):
                break
            opt = re.match(r"^\s*-\s*\(([A-D])\)\s*(.+)$", lines[i])
            if opt:
                options.append((opt.group(1), re.sub(r"\s+", " ", opt.group(2).strip())))
            i += 1
        items.append({"no": no, "answer": answer, "question": question, "options": options})
    return items


def unit_for(no):
    if no <= 15:
        return "day1.u-1"
    if no <= 30:
        return "day1.u-2"
    return "day1.u-3"


def analysis_for(item):
    answer_text = next(text for letter, text in item["options"] if letter == item["answer"])
    wrong = "、".join(f"{letter}. {text}" for letter, text in item["options"] if letter != item["answer"])
    return (
        f"本題答案為「{item['answer']}. {answer_text}」。{REASONS[item['no']]}"
        f"其他選項「{wrong}」不符合題幹所問的烘焙原理、營養換算、製程控制、原料功能或食品安全要求。"
        "作答時先抓題幹關鍵詞，再回到原料性質、配方百分比、溫度控制、食品法規或基本計算判斷。"
    )


def render_question(item):
    options = "\n".join(f"- ({letter}) {text}" for letter, text in item["options"])
    return f"""## Q{item['no']} 單選題
{item['question']}

{options}

```yaml
answer: {item['answer']}
unit: {unit_for(item['no'])}
explanation: |
  【答案】({item['answer']})
  【出處】{SOURCES}
  【AI 分析】
  {analysis_for(item)}
```
"""


def build_content(items):
    total = len(items)
    quiz = "\n".join(render_question(item) for item in items)
    return f"""# META

```yaml
title: 104 學年度烘焙職種學科模擬試卷
subtitle: 烘焙職種學科線上測驗
program: 全國高級中等學校學生技藝競賽烘焙職種
organizer: 104 學年度商業類科學生技藝競賽模擬試卷整理
dates: 104
location: 線上自我練習
format: 單選題線上測驗 / {total} 題
instructor: 烘焙職種學科題庫解析
storeKey: 104-baking-mock-progress-v1
timerSeconds: 3600
scorePerQuestion: 2
```

## 測驗目標

- 完成 104 學年度烘焙職種學科模擬試卷 {total} 題完整練習。
- 複習披薩麵糰、蛋白發泡、小西餅、戚風蛋糕、食品包裝、油脂、營養計算與食品安全。
- 每題提供答案、出處與 AI 分析，協助理解正確選項背後的烘焙學理與實務原因。

## 建議作答節奏

| 時間區間 | 題目範圍 | 複習重點 |
|---|---|---|
| 00:00 ~ 00:20 | Q1-Q15 | 麵粉油脂、蛋白發泡、糖類、蛋品與器具洗滌 |
| 00:20 ~ 00:40 | Q16-Q30 | 派皮油脂、中種法、戚風蛋糕、食品安全與搬運 |
| 00:40 ~ 01:00 | Q31-Q50 | 油炸、膨大劑、包材、熱量、乳化與烘焙百分比 |

---

# DAY1

```yaml
id: day1
n: 1
date: 104
title: 104 學年度烘焙職種學科模擬試卷
hours: 1.0
date_label: 104 學年度
hours_label: 1.0 小時 (60 分鐘)
learningGoal: 完成 104 學年度烘焙職種學科模擬試卷 50 題練習。
hero_title: 104 烘焙職種學科模擬試卷
hero_lead: 依模擬試卷整理 {total} 題單選題，搭配即時評分、作答紀錄與逐題詳解。
```

## 單元 1：基礎原料、發泡與配方換算
```yaml
id: u-1
subtitle: 第 1 題至第 15 題，每題 2 分
time: 00:00 ~ 00:20
```

### 學習重點

- 掌握披薩麵粉、油脂熱量、奶油比較、蛋白發泡階段與烘焙百分比。
- 複習蛋品、器具清潔、量杯容量與常見蛋糕裝飾霜飾。

## 單元 2：製程控制、食品安全與材料分類

```yaml
id: u-2
subtitle: 第 16 題至第 30 題，每題 2 分
time: 00:20 ~ 00:40
```

### 學習重點

- 判斷派皮油脂、中種法優點、戚風蛋糕粉類、酵母發酵時間與食品添加物限量。
- 理解機器安全、鹽的功能、穀類限制胺基酸、奶粉分類與人工搬運限制。

## 單元 3：油炸、包材、糖類與烘焙計算

```yaml
id: u-3
subtitle: 第 31 題至第 50 題，每題 2 分
time: 00:40 ~ 01:00
```

### 學習重點

- 複習道納司油溫、碳酸氫銨、PS 包材、硼砂、乾燥劑包裝與烤酥性。
- 能計算雞蛋價格、海綿蛋糕麵粉量、砂糖用量天數，並判斷蛋的比例。

---

# MATERIALS

- [MD] baking-104-mock-exam.md | 104 學年度烘焙職種學科模擬試卷原始試題

---

# PORTAL

```yaml
title: 線上考場入口
subtitle: 整合各年度技藝競賽與技能檢定學科測驗，支援計時、評分與詳解複習。
```

## 考科卡片

```yaml
id: exam-104-baking-mock
tag: 烘焙職種
title: 104 學年度烘焙職種學科模擬試卷
desc: 104 學年度烘焙職種學科模擬試卷，共 {total} 題，涵蓋披薩麵糰、蛋白發泡、小西餅、戚風蛋糕、食品包裝、油脂、營養計算與食品安全。
time: 60 分鐘
questions: 共 {total} 題
score: 滿分 100 分
href: 104-baking-mock/
btnText: 進入測驗
```

---

# QUIZ

{quiz}
"""


def main():
    items = parse()
    if len(items) != 50:
        raise SystemExit(f"Expected 50 questions, got {len(items)}")
    bad_options = [item["no"] for item in items if len(item["options"]) != 4]
    if bad_options:
        raise SystemExit(f"Questions with invalid option count: {bad_options}")
    OUTPUT.write_text(build_content(items), encoding="utf-8")
    print(f"Parsed {len(items)} questions -> {OUTPUT}")


if __name__ == "__main__":
    main()
