from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "baking-106-official-exam.md"
OUTPUT = ROOT / "content.md"

SOURCES = (
    "全國高級中等學校106學年度商業類科學生技藝競賽【烘焙】職種【學科】正式試卷；"
    "烘焙食品技術士技能檢定相關學科題庫；食品良好衛生規範準則；"
    "麵包與西點製程、烘焙原料學、食品包裝保存、食品安全衛生、食品添加物與營業秘密相關公開教學資料。"
)

REASONS = {
    1: "派皮追求酥鬆口感，應避免麵筋過強，因此以低筋麵粉較適宜。",
    2: "無水奶油是由奶油去除水分與非脂固形物後取得，來源仍是乳脂。",
    3: "烘焙常用原料以麵粉、糖、油脂、蛋、乳品等為主；題目答案屬較不常作為烘焙主要原料者。",
    4: "鮮奶含水與乳固形物，60% 鮮奶換算成奶粉固形量通常高於 4% 脫脂奶粉，題目比較的是實際乳固形量。",
    5: "蛋白受熱凝固且能形成泡沫結構，在烘焙原料中屬於韌性或結構性材料。",
    6: "糖量由 2% 增至 4% 仍在酵母可利用範圍，通常不會抑制發酵，發酵時間可略縮短或差異不大。",
    7: "乳化劑可改善麵包柔軟度、延緩老化並穩定麵糰與氣泡，不是單純增加甜味或上色。",
    8: "油炸用油需高發煙點、氧化穩定、風味中性且耐反覆加熱，最適合食品工廠油炸作業。",
    9: "麵粉久存筋性受損時，可酌量加入活性麵筋或高筋性材料補強麵筋結構。",
    10: "乳化油適合改善麵包或蛋糕柔軟度，但不適合強調純油脂層次、風味或特殊質地的產品。",
    11: "穀類蛋白質缺乏離胺酸，添加奶粉可補充較完整的乳蛋白並提升營養價值。",
    12: "亮光糖漿主要由糖、水、葡萄糖漿或膠質等製成；與糖漿功能無關的原料即為錯誤選項。",
    13: "乳沫類蛋糕靠蛋液或蛋白打發包入空氣，最適合使用球狀打蛋器。",
    14: "直接法控制攪拌後麵糰溫度，主要與水溫、室溫、粉溫與摩擦熱有關，與題目答案所列因素無關。",
    15: "翻麵可排氣、均勻溫度、強化麵筋並重新分布酵母與養分；縮短或增加濕度不是其主要好處。",
    16: "小西餅膨大通常與膨大劑、打發或蒸氣有關；題目答案不是造成膨大的主要因素。",
    17: "戚風蛋糕主要靠蛋白泡沫受熱膨脹與凝固形成體積，是最關鍵的膨大來源。",
    18: "麵粉含水量低於標準 1% 時，配方水量約可增加 2%，以補足麵粉吸水差異。",
    19: "整形後丹麥或甜麵包冷藏需維持低溫，約 0 至 5°C 可延緩發酵並保持油脂層狀。",
    20: "海綿蛋糕熱拌法會先將蛋液加溫至約 35 至 43°C，以降低黏度、利於打發。",
    21: "天使蛋糕蛋白打至濕性發泡較具延展性，拌合後入爐膨脹能力較佳。",
    22: "蛋在牛奶雞蛋布丁餡中除提供風味，也靠蛋白質受熱凝固，使餡料成形並具稠度。",
    23: "酵母道納司需油炸成形，糖油量通常比甜麵包稍低，以利形狀完整並避免油炸過度上色或吸油。",
    24: "800 公克帶蓋土司以約 200°C 烤焙，常需 30 分鐘以上，才能使中心熟透並定型。",
    25: "法國麵包等硬式麵包需要蒸汽烤爐形成薄脆外皮與良好裂口。",
    26: "圓柱容積為半徑平方乘以圓周率再乘高度；直徑 22、高 5，約 3.14x11x11x5 = 1900 立方公分。",
    27: "50 至 100 公克甜麵包體積小，通常採較高溫、較短時間烤焙，以利上色且避免乾硬。",
    28: "戚風蛋糕蛋白與糖攪拌不足會造成支撐氣泡不足，成品體積小、組織粗或塌陷。",
    29: "蘇打餅乾含鹼性膨大劑或發酵調整，成品 pH 通常高於一般奶油小西餅。",
    30: "鬆餅或起酥類需高溫使水分快速汽化撐開層次，烤爐宜具足夠上、下火與穩定高溫。",
    31: "製作天使蛋糕增加糖可延緩蛋白凝固、穩定泡沫並降低韌性，使口感較柔軟。",
    32: "餐包製備水準可由表皮光滑、色澤均勻、薄而柔軟等外觀與表皮性質判斷。",
    33: "裹油麵包無層次常因包入油太軟、擀摺不當或發酵烤焙溫度不當；答案選項不是主要原因。",
    34: "土司麵包表皮應薄而柔軟、色澤均勻，過厚硬或粗糙代表製程控制不佳。",
    35: "烘焙產品底部黑點常因烤盤髒污、底火過強或焦屑沾附造成。",
    36: "天使蛋糕潔白細膩，因只用蛋白並可添加塔塔粉穩定泡沫、維持白色與細緻組織。",
    37: "食品包裝標示需依規定載明品名、內容物、有效日期等；不符強制標示要求者為錯誤。",
    38: "蛋糕包裝延長保存常使用脫氧劑，降低氧氣以延緩氧化與黴菌生長。",
    39: "鋁箔膠膜積層具有良好遮光、防濕與阻隔性，能保護食品免受光、氧與水氣影響。",
    40: "食品包裝材料必備安全、阻隔、保護與適用性；題目答案為不符合包裝材料基本要求的敘述。",
    41: "避免空氣造成食品品質劣變，最好使用真空包裝或脫氧方式，降低氧氣接觸。",
    42: "低溫貯藏食品包含冷藏與冷凍，利用低溫抑制微生物與酵素作用。",
    43: "砂糖溶液濃度越高，分子間作用與流動阻力越大，黏度會增加。",
    44: "食品加工使用最多的溶劑是水，安全、便宜且能溶解多種食品成分。",
    45: "酵母屬生物性膨大劑，不屬於化學膨脹劑；發粉、小蘇打等才是化學膨大劑。",
    46: "食品違法行為若涉及危害人體健康、摻偽或重大違反食安規定，可能處以刑罰。",
    47: "洗滌食品容器與器具應使用食品用清潔劑並充分沖洗，避免殘留污染。",
    48: "使用食品添加物應優先考慮安全性，再考量效果、成本與必要性。",
    49: "食品加工廠最普遍使用的消毒劑之一是氯系消毒劑，成本低且殺菌效果廣。",
    50: "受雇者在職務上研究或開發的營業秘密，原則上歸雇用人所有，除契約另有約定外。"
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
        f"其他選項「{wrong}」不符合題幹所問的烘焙原理、製程控制、原料功能、包裝保存、食品衛生或法規概念。"
        "作答時先抓題幹關鍵詞，再回到麵糰麵糊結構、溫度控制、烘焙百分比、保存條件或食品安全規範判斷。"
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
title: 106 學年度商業類科學生技藝競賽烘焙職種學科正式試卷
subtitle: 烘焙職種學科線上測驗
program: 全國高級中等學校學生技藝競賽烘焙職種
organizer: 106 學年度商業類科學生技藝競賽正式試卷整理
dates: 106
location: 線上自我練習
format: 單選題線上測驗 / {total} 題
instructor: 烘焙職種學科題庫解析
storeKey: 106-baking-progress-v1
timerSeconds: 3600
scorePerQuestion: 2
```

## 測驗目標

- 完成 106 學年度商業類科學生技藝競賽烘焙職種學科正式試卷 {total} 題完整練習。
- 複習派皮、乳品與乳化劑、麵包發酵、起酥與戚風蛋糕、包裝保存、食品安全、添加物與營業秘密。
- 每題提供答案、出處與 AI 分析，協助理解正確選項背後的烘焙學理與實務原因。

## 建議作答節奏

| 時間區間 | 題目範圍 | 複習重點 |
|---|---|---|
| 00:00 ~ 00:20 | Q1-Q15 | 派皮、乳品、乳化劑、麵粉筋性與麵包翻麵 |
| 00:20 ~ 00:40 | Q16-Q30 | 小西餅、戚風、丹麥、海綿蛋糕、土司與起酥 |
| 00:40 ~ 01:00 | Q31-Q50 | 天使蛋糕、包裝保存、低溫貯藏、添加物與法規 |

---

# DAY1

```yaml
id: day1
n: 1
date: 106
title: 106 學年度烘焙職種學科正式試卷
hours: 1.0
date_label: 106 學年度
hours_label: 1.0 小時 (60 分鐘)
learningGoal: 完成 106 學年度商業類科學生技藝競賽烘焙職種學科正式試卷 50 題練習。
hero_title: 106 烘焙職種學科正式試卷
hero_lead: 依正式試卷整理 {total} 題單選題，搭配即時評分、作答紀錄與逐題詳解。
```

## 單元 1：原料功能與麵包基礎
```yaml
id: u-1
subtitle: 第 1 題至第 15 題，每題 2 分
time: 00:00 ~ 00:20
```

### 學習重點

- 掌握派皮粉類、無水奶油、乳化劑、油炸用油、麵粉補強與麵包翻麵。

## 單元 2：產品製程與烤焙控制

```yaml
id: u-2
subtitle: 第 16 題至第 30 題，每題 2 分
time: 00:20 ~ 00:40
```

### 學習重點

- 複習小西餅膨大、戚風蛋糕、丹麥冷藏、海綿熱拌、布丁凝固、帶蓋土司與起酥烤焙。

## 單元 3：包裝保存、食品安全與法規

```yaml
id: u-3
subtitle: 第 31 題至第 50 題，每題 2 分
time: 00:40 ~ 01:00
```

### 學習重點

- 判斷天使蛋糕、餐包表皮、食品包裝標示、低溫保存、化學膨脹劑、添加物安全與營業秘密歸屬。

---

# MATERIALS

- [MD] baking-106-official-exam.md | 106 學年度烘焙職種學科正式試卷原始試題

---

# PORTAL

```yaml
title: 線上考場入口
subtitle: 整合各年度技藝競賽與技能檢定學科測驗，支援計時、評分與詳解複習。
```

## 考科卡片

```yaml
id: exam-106-baking
tag: 烘焙職種
title: 106 學年度烘焙職種學科正式試卷
desc: 106 學年度商業類科學生技藝競賽烘焙職種學科正式試卷，共 {total} 題，涵蓋派皮、乳品與乳化劑、麵包發酵、起酥與戚風蛋糕、包裝保存、食品安全、添加物與營業秘密。
time: 60 分鐘
questions: 共 {total} 題
score: 滿分 100 分
href: 106-baking/
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
