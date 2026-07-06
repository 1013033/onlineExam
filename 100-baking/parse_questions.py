from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "baking-100-official-exam.md"
OUTPUT = ROOT / "content.md"

SOURCES = (
    "全國高級中等學校100學年度商業類科學生技藝競賽【烘焙】職種【學科】正式試卷；"
    "烘焙食品技術士技能檢定相關學科題庫；"
    "食品良好衛生規範準則與烘焙原料、製程、包裝保存、品質管制相關公開教學資料。"
)

REASONS = {
    1: "糖會提高餅乾配方中固形物與玻璃化程度，降低成品水分活性，使小西餅口感更脆硬。",
    2: "一英吋約 2.54 公分，12 吋約 30.48 公分，傳統換算可近似為 30 公分與 1 尺。",
    3: "華氏轉攝氏公式為 (F-32)*5/9，400°F 約為 204.4°C，最接近 205°C。",
    4: "天然酵母麵包通常發酵時間長、風味與保存性佳，但不必然代表利潤高，利潤仍受成本、售價與產能影響。",
    5: "法國麵包需蒸氣幫助表皮延展與形成脆殼；帶蓋土司在模具中烘烤，通常不需爐內噴水。",
    6: "巧克力含可可脂，替代可可粉時需折算脂肪含量；20% 巧克力約需調整 10% 油性較符合配方平衡。",
    7: "戚風蛋糕出爐倒扣可防止組織因重力塌陷，腳架能保持通風與支撐高度。",
    8: "高筋麵粉蛋白質較高，能增加麵糊支撐性，使擠花紋路烘烤後較不易消失。",
    9: "全麥麵包主要原料是全麥粉，含麩皮、胚芽與胚乳，與低筋麵粉或粉心粉不同。",
    10: "真空包裝可降低氧氣與黴菌生長機會，延緩紅豆沙發霉與氧化劣變。",
    11: "中成分重奶油蛋糕以麵粉為 100% 基準，糖、蛋、奶油依配方比例排列，正確順序為麵粉大於糖、蛋、奶油。",
    12: "白油氫化程度高、熔點與發煙點較高，適合較高溫操作且穩定性高。",
    13: "全穀類保留胚芽與麩皮，維生素 B 群含量通常高於精製穀粉與多數蔬果。",
    14: "比容積為模具體積除以麵糰重量，20*11*11/560 約為 4.3。",
    15: "切蛋糕捲需用熱水加熱刀具並以消毒毛巾擦乾，可降低沾黏、保持切面整齊並兼顧衛生。",
    16: "牛角麵包壓延需讓包入油保持可塑而不融化，室溫約 15~20°C 較適合。",
    17: "奶油布丁餡儲存主要受澱粉回凝、溫度與蛋白質變性影響，pH 並非題目列出的主要不包含因素。",
    18: "裝飾鮮奶油蛋糕屬高水分、高營養且易腐敗食品，應於 7°C 以下冷藏販售。",
    19: "聚乙烯 PE 熱封性佳、耐熱約 85°C，但表面能低，直接印刷較困難。",
    20: "戚風蛋糕通常先處理蛋黃糊再打蛋白霜，且蛋白不可混入蛋黃；題目問何者為非，故選蛋白先攪拌。",
    21: "麵粉 3000g，蛋水合計 62% 為 1860g，扣除蛋 340g，需加水 1520g。",
    22: "海綿蛋糕通常需較高烤溫以快速定型與形成體積，相較重奶油、水果與天使蛋糕更高。",
    23: "甜麵包糖量高，糖會造成滲透壓抑制酵母作用；若發酵時間相同需增加酵母量。",
    24: "鬆餅類起酥產品需高溫讓水分迅速汽化推開層次並固定油脂，故用 220~240°C。",
    25: "奶油空心餅扁平常與蛋量太多、糊化不足或液體油過多有關；蛋量太少可酌量增加 NH3 的說法不正確。",
    26: "椰子油飽和度高，氧化安定性較好，較能減少油耗味並延長小西餅保存。",
    27: "可頌麵包為層酥麵糰，包入大量油脂以形成層次，油量高於一般甜麵包、吐司與法國麵包。",
    28: "麵糊類蛋糕攪拌過發會破壞組織或使麵筋、氣泡狀態不穩，冷卻切片容易鬆散。",
    29: "麵糊 1600g 加 8% 損耗需約 1728g；全蛋佔總百分比 286/695，約為 711g，最接近 716g。",
    30: "中種法先發酵部分麵糰，可改善麵筋成熟、風味與保水，使麵包柔軟且有 Q 勁。",
    31: "新鮮酵母含水量高、活性易衰退，通常冷藏於 4~7°C 保存。",
    32: "法國麵包基本材料為麵粉、酵母、鹽與水；選項中以酵母、鹽、麵粉最符合核心材料。",
    33: "鹽主要調味與調節麵筋、發酵，不能作為小西餅膨大來源；小蘇打、發粉與打入空氣均可膨鬆。",
    34: "美式派皮採切拌法，先將油脂與麵粉切成小粒，再加水拌合，避免出筋並形成酥鬆口感。",
    35: "脫氧劑可降低包裝內氧氣，抑制氧化與部分微生物，延長蛋糕保存時間。",
    36: "杏仁薄餅含水量低，冷卻後密封即可；裝袋後冷藏易吸濕回軟，故為非。",
    37: "尼龍積層具有較佳耐熱與阻隔性，可用於食品蒸煮包裝。",
    38: "油炸甜甜圈需使用適合油炸且口感穩定的油炸油，較能維持外觀、吸油量與風味。",
    39: "新鮮酵母用量約為乾酵母或快速酵母的 3 倍，1.5% 快速酵母約換算為 4.5% 新鮮酵母。",
    40: "罐頭經密封與殺菌，保存期限通常比麵粉、油脂與水果更久。",
    41: "烘焙百分比以麵粉為 100%，蛋 385g / 麵粉 500g = 77%。",
    42: "乳酪主要成分包含水分、蛋白質與脂質，脂質是影響風味與口感的重要成分。",
    43: "奶酪常用明膠等動物膠作為膠凍原料，使乳液凝固成柔軟膠體。",
    44: "40 公斤為 40000g，每粒 40g 共 1000 粒；每分鐘 40 粒需 25 分鐘。",
    45: "派皮整形防黏常用高筋麵粉，較不易被麵糰吸收並能降低黏附。",
    46: "葡萄乾未先泡水會吸收麵包水分且與麵糰結合較差，切片時容易掉落。",
    47: "膠凍原料太多會使布丁凝膠過硬，冷卻收縮後容易龜裂。",
    48: "奶油易受溫度影響軟化與氧化，不適合放在 20°C、60%RH 的常溫乾燥區長期保存。",
    49: "香辛料芳香成分易揮發與氧化，採購量不宜過多，最好約 3 個月內用完。",
    50: "麵粉蛋白質下降時吸水量通常降低，原水量 62% 可調降約 2%，故為 60%。",
}


def parse():
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    text = re.split(r"^###\s*二、", text, maxsplit=1, flags=re.MULTILINE)[0]
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
            opt = re.match(r"^\s*-\s*[\(（]([A-D])[\)）]\s*(.+)$", lines[i])
            if opt:
                text_value = re.sub(r"[。．\s]+$", "", re.sub(r"\s+", " ", opt.group(2).strip()))
                options.append((opt.group(1), text_value))
            i += 1

        items.append({"no": no, "answer": answer, "question": question, "options": options})

    return items


def unit_for(no):
    if no <= 15:
        return "day1.u-1"
    if no <= 30:
        return "day1.u-2"
    return "day1.u-3"


def topic_for(no):
    if no <= 15:
        return "烘焙基礎、原料換算與產品特性"
    if no <= 30:
        return "製程控制、配方計算與產品保存"
    return "包裝保存、品質管制、成本與原料應用"


def analysis_for(item):
    answer_text = next(text for letter, text in item["options"] if letter == item["answer"])
    wrong = "、".join(f"{letter}. {text}" for letter, text in item["options"] if letter != item["answer"])
    return (
        f"本題答案為「{item['answer']}. {answer_text}」。{REASONS[item['no']]}"
        f"其他選項「{wrong}」雖可能與烘焙原料、製程或保存條件有關，"
        "但不符合題幹指定的主要原因、標準換算、產品特性或衛生保存要求。"
        "作答時應先抓住題幹中的產品、溫度、比例或否定問法，再用烘焙原理排除干擾選項。"
    )


def render_question(item):
    options = "\n".join(f"- ({letter}) {text}" for letter, text in item["options"])
    return f"""## Q{item['no']} ｜ 單選題

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
title: 100 學年度商業類科學生技藝競賽烘焙職種學科正式試卷
subtitle: 烘焙職種學科正式試卷線上考場
program: 商業類科學生技藝競賽烘焙職種
organizer: 100 學年度商業類科學生技藝競賽正式試卷整理
dates: 100
location: 線上測驗系統
format: 正式試題學科試卷 / {total} 題單選
instructor: 烘焙職種學科輔助解析
storeKey: 100-baking-progress-v1
timerSeconds: 3600
scorePerQuestion: 2
```

## 學習目標

- 完成 100 學年度商業類科學生技藝競賽烘焙職種學科正式試卷 {total} 題完整練習。
- 熟悉烘焙原料功能、烤焙溫度換算、配方百分比、產品製作、包裝保存與品質判斷。
- 透過逐題答案、出處與 AI 分析，理解每題正確答案的烘焙學理與排除理由。

## 考科時程

| 建議時間 | 考科單元 | 考核重點 |
|---|---|---|
| 00:00 ~ 00:20 | Q1-Q15 | 烘焙基礎、原料換算與產品特性 |
| 00:20 ~ 00:40 | Q16-Q30 | 製程控制、配方計算與產品保存 |
| 00:40 ~ 01:00 | Q31-Q50 | 包裝保存、品質管制、成本與原料應用 |

---

# DAY1

```yaml
id: day1
n: 1
date: 100
title: 100 學年度烘焙職種學科正式試卷
hours: 1.0
date_label: 100 學年度
hours_label: 1.0 小時 (60分鐘)
learningGoal: 完成 100 學年度商業類科學生技藝競賽烘焙職種學科正式試卷 50 題練習。
hero_title: 100 烘焙職種學科正式試卷
hero_lead: 本試卷共 {total} 題，皆為單選題；系統以答對題數換算百分制。
```

## 單元1：烘焙基礎、原料換算與產品特性

```yaml
id: u-1
subtitle: 第 1 題至第 15 題，每題 2 分
time: 00:00 ~ 00:20
```

### 學習目標

- 掌握烘焙材料功能、度量衡與烤溫換算。
- 理解餅乾、土司、法國麵包、戚風蛋糕與奶油蛋糕的基礎特性。

## 單元2：製程控制、配方計算與產品保存

```yaml
id: u-2
subtitle: 第 16 題至第 30 題，每題 2 分
time: 00:20 ~ 00:40
```

### 學習目標

- 熟悉麵糰壓延、冷藏保存、烤溫控制與麵包發酵法。
- 能運用烘焙百分比與損耗概念進行配方計算。

## 單元3：包裝保存、品質管制、成本與原料應用

```yaml
id: u-3
subtitle: 第 31 題至第 50 題，每題 2 分
time: 00:40 ~ 01:00
```

### 學習目標

- 判斷酵母保存、派皮製作、食品包裝材料與原料保存條件。
- 理解乳酪、動物膠、分割效率、香辛料與麵粉蛋白質對成品的影響。

---

# MATERIALS

- [MD] baking-100-official-exam.md | 100 學年度烘焙職種學科正式試卷原始試題

---

# PORTAL

```yaml
title: 學術能力模擬檢測入口
subtitle: 歡迎來到模擬考試線上平台。本系統已依照不同試題與科目分類，請點擊下方對應的卡片進入考場進行線上作答與評分。
```

## 考試卡片

```yaml
id: exam-100-baking
tag: 烘焙職種
title: 100 學年度烘焙職種學科正式試卷
desc: 100 學年度商業類科學生技藝競賽烘焙職種學科正式試卷，共 {total} 題，涵蓋烘焙原料功能、配方計算、產品製作、烤焙控制、包裝保存與品質判斷。
time: 60 分鐘
questions: 共 {total} 題
score: 滿分 100 分
href: 100-baking/
btnText: 進入線上考場
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
