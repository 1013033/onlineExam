from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "baking-105-official-exam.md"
OUTPUT = ROOT / "content.md"

SOURCES = (
    "全國高級中等學校105學年度商業類科學生技藝競賽【烘焙】職種【學科】正式試題；"
    "烘焙食品技術士技能檢定相關學科題庫；食品良好衛生規範準則；"
    "烘焙原料學、麵包與西點製程、食品衛生消毒、包裝保存、食品添加物與品質管制相關公開教學資料。"
)

REASONS = {
    1: "奶油空心餅在爐內出油，常因燙麵糊化不足或麵糊乳化不良，油脂未被澱粉與蛋液結構吸收而析出。",
    2: "巧克力戚風蛋糕顏色加深，來自可可粉與鹼性材料作用；鹼性環境會使可可色澤更深。",
    3: "餐包用奶粉通常屬全脂或脫脂奶粉分類中的乳製品乾料，主要提供乳香、乳糖與蛋白質。",
    4: "奶酥麵包適合使用中等硬度、礦物質適中的水質；過硬或過軟都會影響麵筋、發酵與口感。",
    5: "戚風蛋糕出爐後表面立即收縮，多因烘烤不足或結構未完全定型，冷卻時支撐力不夠而回縮。",
    6: "蛋白含水量約 88% 左右，剩餘主要為蛋白質與少量礦物質，故選 88%。",
    7: "有香味、有顏色且不含水的烘焙油脂，通常指經調製或具風味的純油脂，而非含水乳化油脂。",
    8: "蒸發奶水是濃縮乳，固形物含量較鮮乳高，常約 26% 左右。",
    9: "奶油海綿蛋糕中的奶油量過高會破壞泡沫結構，實務上通常控制在約 40% 至 50% 以內。",
    10: "丹麥麵包與鬆餅需要裹入油具可塑性與延展性，片狀瑪琪琳或專用裹入油最適合形成層次。",
    11: "巧克力丹麥小西餅屬層狀起酥類產品，需採摺疊或裹油類拌合法形成層次。",
    12: "檸檬布丁派皮配方仍以麵粉為烘焙百分比 100% 的基準，其他材料相對麵粉計算。",
    13: "奶油空心餅蛋量較多時，麵糊較稀且蒸氣膨脹較強，成品外殼通常較薄。",
    14: "蛋白打至濕性發泡時仍具延展性，較容易和其他材料拌合，入爐後膨脹較佳；過乾易結塊破泡。",
    15: "麵糊類小西餅提高脆性常增加糖量，糖能降低水分活性、削弱麵筋並促進酥脆口感。",
    16: "蛋糕配方總百分比 360%，麵糊總量 5400g，麵粉量為 5400/3.6 = 1500g。",
    17: "麵糰彈性主要來自麥穀蛋白，延展性主要來自麥膠蛋白，兩者共同形成麵筋特性。",
    18: "天使蛋糕需大量蛋白泡沫支撐，通常打至濕性至接近硬性發泡，便於拌合且能維持膨脹。",
    19: "抹布煮沸殺菌需足夠時間，100°C 煮沸 5 分鐘以上可有效降低微生物污染。",
    20: "奶油大理石蛋糕若要組織細膩，使用麵粉油脂拌合法可抑制麵筋過度形成並改善組織。",
    21: "Ganache 主要由巧克力與鮮奶油乳化而成，比例與溫度控制會影響口感、光澤與凝固狀態。",
    22: "鋁箔具有良好的遮光、防水與氣體阻隔性，適合需要避光防潮的食品包裝。",
    23: "粗糙未精製穀類保留麩皮與胚芽，除醣類、蛋白質外，也提供膳食纖維、礦物質與維生素。",
    24: "蛋糕包裝延長保存常使用脫氧劑或保鮮包材，以降低氧化與黴菌生長。",
    25: "牛奶含水分、蛋白質、脂肪、乳糖與礦物質，但不含題列中某些非乳品主要成分。",
    26: "瑪琍餅乾屬韌性餅乾，麵糰需攪拌至適當麵筋發展，才能擀壓成薄片並保持形狀。",
    27: "纖維素主要存在於植物細胞壁，未精製穀類或麩皮含量最高。",
    28: "烘焙食品包裝應保護品質、防潮防氧並符合標示；與此原則相反者為錯誤敘述。",
    29: "塔塔粉是酸性鹽類，主要成分為酒石酸氫鉀，用於穩定蛋白泡沫與調整酸鹼。",
    30: "食鹽加倍會抑制酵母發酵並強化麵筋，使正常基本發酵後高度降低。",
    31: "蛋糕發粉是化學膨大劑，受熱或遇水反應產生二氧化碳，使蛋糕膨脹。",
    32: "植物性液態油通常不飽和脂肪酸較高；題列中不飽和脂肪酸最豐富者為答案。",
    33: "乳沫類蛋糕的膨鬆主要來自蛋或蛋白打發所形成的泡沫結構。",
    34: "巧克力融化溫度過高會油水分離或失去光澤，通常不宜超過約 50°C。",
    35: "巧克力融化後降溫再回溫，使可可脂形成穩定晶型，稱為調溫。",
    36: "比重越低代表含氣量越高，天使蛋糕等蛋白泡沫類蛋糕麵糊通常最輕。",
    37: "乳化劑能幫助油水均勻分散、穩定氣泡並改善蛋糕體積與組織。",
    38: "泡芙內部缺乏空囊常因麵糊太乾、加蛋不足或爐溫控制不當，蒸氣不足以撐開空腔。",
    39: "鬆餅或起酥類裹入油量高，常接近麵糰油脂層需求；足量裹入油可形成體積大、層次多的產品。",
    40: "蛋糕夾餡奶油霜需均勻打發與乳化，使用槳狀拌打器較能控制質地並避免過度打入大氣泡。",
    41: "小麥胚芽約占小麥粒 2% 左右，含油脂、維生素與酵素，易氧化酸敗。",
    42: "蛋糕表面白色斑點常因砂糖顆粒太粗或未完全溶解，烤後殘留形成白點。",
    43: "低酸性食品通常指 pH 大於 4.6；pH 4.6 是微生物控制與罐頭食品分類的重要界線。",
    44: "使用食品添加物應優先考慮安全性，確認合法、必要且不超量，才符合食品衛生原則。",
    45: "若小西餅要金黃色澤，可使用蛋黃或含蛋黃材料，因蛋黃促進上色並增加金黃色調。",
    46: "餅乾用麵粉酸度偏高時，可提高小蘇打等鹼性材料用量以中和酸度並改善色澤與膨鬆。",
    47: "麵糊類蛋糕的打發主要來自油脂與糖拌打包入空氣，並靠乳化維持麵糊穩定。",
    48: "糖量占烘焙百分比 20% 以上者屬甜麵包等高成分麵包，風味甜且上色較深。",
    49: "砂糖由 3% 增至 6% 在一般範圍內可供酵母利用，通常發酵時間不會增加，可能略縮短或差異不大。",
    50: "巧克力慕斯常用明膠等動物膠作凝結材料，使泡沫乳化體冷卻後定型。"
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
        f"其他選項「{wrong}」不符合題幹所問的烘焙原理、製程控制、原料功能、食品衛生或包裝保存要求。"
        "作答時先抓題幹關鍵詞，再回到麵糊麵糰結構、烘焙百分比、溫度條件、食品法規或材料特性判斷。"
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
title: 105 學年度商業類科學生技藝競賽烘焙職種學科正式試題
subtitle: 烘焙職種學科線上測驗
program: 全國高級中等學校學生技藝競賽烘焙職種
organizer: 105 學年度商業類科學生技藝競賽正式試題整理
dates: 105
location: 線上自我練習
format: 單選題線上測驗 / {total} 題
instructor: 烘焙職種學科題庫解析
storeKey: 105-baking-progress-v1
timerSeconds: 3600
scorePerQuestion: 2
```

## 測驗目標

- 完成 105 學年度商業類科學生技藝競賽烘焙職種學科正式試題 {total} 題完整練習。
- 複習空心餅、戚風蛋糕、丹麥與小西餅、麵包製程、食品衛生、包裝保存、乳製品與巧克力製品。
- 每題提供答案、出處與 AI 分析，協助理解正確選項背後的烘焙學理與實務原因。

## 建議作答節奏

| 時間區間 | 題目範圍 | 複習重點 |
|---|---|---|
| 00:00 ~ 00:20 | Q1-Q15 | 空心餅、戚風、乳製品、丹麥與小西餅 |
| 00:20 ~ 00:40 | Q16-Q30 | 烘焙百分比、土司麵糰、衛生殺菌、包裝保存 |
| 00:40 ~ 01:00 | Q31-Q50 | 發粉、油脂、巧克力調溫、食品添加物與慕斯 |

---

# DAY1

```yaml
id: day1
n: 1
date: 105
title: 105 學年度烘焙職種學科正式試題
hours: 1.0
date_label: 105 學年度
hours_label: 1.0 小時 (60 分鐘)
learningGoal: 完成 105 學年度商業類科學生技藝競賽烘焙職種學科正式試題 50 題練習。
hero_title: 105 烘焙職種學科正式試題
hero_lead: 依正式試題整理 {total} 題單選題，搭配即時評分、作答紀錄與逐題詳解。
```

## 單元 1：蛋糕、西點與基礎原料
```yaml
id: u-1
subtitle: 第 1 題至第 15 題，每題 2 分
time: 00:00 ~ 00:20
```

### 學習重點

- 掌握奶油空心餅、戚風蛋糕、乳製品、丹麥裹入油、小西餅脆性與烘焙百分比基準。

## 單元 2：製程控制、衛生與包裝

```yaml
id: u-2
subtitle: 第 16 題至第 30 題，每題 2 分
time: 00:20 ~ 00:40
```

### 學習重點

- 複習蛋糕配方換算、土司麵筋蛋白、抹布煮沸殺菌、Ganache、包裝材料與食鹽對發酵的影響。

## 單元 3：食品添加物、巧克力與成品判斷

```yaml
id: u-3
subtitle: 第 31 題至第 50 題，每題 2 分
time: 00:40 ~ 01:00
```

### 學習重點

- 判斷發粉、油脂不飽和度、巧克力融化與調溫、乳化劑、泡芙空囊、食品添加物安全與慕斯凝結材料。

---

# MATERIALS

- [MD] baking-105-official-exam.md | 105 學年度烘焙職種學科正式試題原始試題

---

# PORTAL

```yaml
title: 線上考場入口
subtitle: 整合各年度技藝競賽與技能檢定學科測驗，支援計時、評分與詳解複習。
```

## 考科卡片

```yaml
id: exam-105-baking
tag: 烘焙職種
title: 105 學年度烘焙職種學科正式試題
desc: 105 學年度商業類科學生技藝競賽烘焙職種學科正式試題，共 {total} 題，涵蓋空心餅、戚風蛋糕、丹麥與小西餅、麵包製程、食品衛生、包裝保存、乳製品與巧克力製品。
time: 60 分鐘
questions: 共 {total} 題
score: 滿分 100 分
href: 105-baking/
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
