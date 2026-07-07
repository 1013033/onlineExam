from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "baking-107-official-exam.md"
OUTPUT = ROOT / "content.md"

TITLE = "107 學年度全國高級中等學校學生商業類技藝競賽烘焙職種學科正式試題"
STORE_KEY = "107-baking-progress-v1"
PORTAL_ID = "exam-107-baking"
HREF = "107-baking/"
MATERIAL = "baking-107-official-exam.md"

SOURCE_NOTE = (
    "107 學年度全國高級中等學校學生商業類技藝競賽烘焙職種學科正式試題；"
    "烘焙食品加工與烘焙食品技術士學科常用教材；食品良好衛生規範準則；"
    "烘焙原料學、麵包與西點製程、食品包裝保存與食品安全衛生相關公開教學資料。"
)

SPECIAL_NOTES = {
    33: "題本前標為 E，但題內註記說明原答案應為 B「溼性發泡」；本題依註記校正為 B。",
}

REASONS = {
    1: "油炸甜圈餅需要能承受油炸溫度、氧化安定性較佳且適合連續加熱的油脂，油炸油比一般沙拉油、豬油或奶油更符合用途。",
    2: "烤盤未滿時，以打溼白紙補足空盤處可降低局部空烤與熱分布不均；報紙有油墨與衛生疑慮，錫箔紙反射熱也會改變烤色。",
    3: "雞蛋與蛋製品最典型的食物中毒風險為沙門氏桿菌，常和蛋殼、蛋液污染或加熱不足有關。",
    4: "派皮與奶油底需要塑性佳、含水少的油脂形成酥鬆層次，無水奶油或精製豬油比含水奶油穩定。",
    5: "CNS 對葡萄乾麵包的葡萄乾含量有最低比例要求，題目所列正確門檻為麵粉量的 20%。",
    6: "轉化糖漿是蔗糖經酸或酵素水解後產生葡萄糖與果糖，因此原料是砂糖。",
    7: "鋁箔耐熱、阻光與阻隔性佳，比 PE、PP、PET 更能承受高溫或需要高阻隔的包裝情境。",
    8: "蘇打餅乾麵糰經壓延後容易因麵筋與層狀結構產生回縮，成型時需考慮收縮比。",
    9: "果糖是還原糖，較易參與梅納反應並促進烤焙著色；蔗糖需先分解才較明顯參與。",
    10: "蘇打餅乾屬發酵餅乾，糖油量低於蛋糕與高糖油小西點，配方重點在麵筋、發酵與壓延。",
    11: "食品酸鹼分類常以 pH 4.6 作為酸性與低酸性食品的界線，這也關係到肉毒桿菌風險控制。",
    12: "烘焙百分比總量 180% 對應麵糊總量 9 公斤，麵粉為基準 100%，9 ÷ 1.8 = 5 公斤。",
    13: "脆硬性小西餅糖多於油、油多於水，麵糰較乾硬，適合擀平或模型壓出。",
    14: "新鮮奶油需低溫冷藏以抑制微生物與油脂劣變，1~5°C 是較合適的冷藏範圍。",
    15: "奶油空心餅依靠高溫迅速產生水蒸氣膨脹形成空腔，成型後應立即進爐避免結構塌陷。",
    16: "全胚芽含脂質與酵素，長時間貯藏會促進脂肪水解，游離脂肪酸增加並造成酸敗風險。",
    17: "糖可保濕、助褐變與增添風味，但不能真正防止麵包老化變硬，只能延緩部分水分流失。",
    18: "產品品質鑑定著重外觀、體積、組織、口感與風味，價格屬市場因素，不是品質鑑定指標。",
    19: "小麥橫斷面呈粉質狀代表蛋白質較低、質地較軟，適合磨製低筋麵粉。",
    20: "酒石酸水解蔗糖製得轉化糖漿的品質較佳，較能符合烘焙糖漿風味與色澤需求。",
    21: "白土司屬主食麵包，口感應清淡並略帶鹹味，而非奶油、香草或焦糖等強烈風味。",
    22: "冷凍蛋解凍後微生物風險與品質劣化速度增加，最好在一天內使用完畢。",
    23: "油炸油劣化外觀可看顏色、黏度、泡沫與冒煙狀況；酸價需化學檢驗，不能靠外觀直接判斷。",
    24: "D.E. 值 30~50 的澱粉糖漿不是單一糖，而是糊精、麥芽糖與葡萄糖等不同鏈長糖類混合物。",
    25: "快速酵母含水少、活性濃度高，取代新鮮酵母時常用約三分之一用量。",
    26: "冷凍食品應在 -18°C 以下保存，以抑制微生物增殖並延緩品質劣化。",
    27: "砂糖吸濕性低於果糖、蜂蜜與轉化糖，因此較不易吸濕結塊。",
    28: "冰用量可由目標水溫、自來水溫與室溫差估算，題目條件計算結果最接近 54g。",
    29: "基本發酵過久會消耗可發酵糖並削弱烤焙膨脹與上色能力，使土司表面顏色偏淺。",
    30: "酵母利用麥芽糖需先經酵素分解，速度通常慢於葡萄糖、果糖與蔗糖。",
    31: "奶油布丁派餡的凝凍可來自蛋、動物膠或澱粉；奶油水不是凝凍原料。",
    32: "蛋糕出爐後放在乾燥陰涼處可降低水氣凝結與黴菌生長，熱而潮濕或混放舊品都會增加污染風險。",
    33: "蛋白打至溼性發泡時泡沫仍有延展性，最容易與其他原料拌合且入爐後膨脹佳；乾性發泡較易拌合不均或消泡。",
    34: "高筋麵粉蛋白質高、筋性強，適合需要麵筋骨架的法國麵包，不適合細緻低筋蛋糕。",
    35: "雙皮水果派切開時理想果餡應似流而不流，表示膠化與濃稠度適中。",
    36: "奶水屬蒸發乳類產品，固形物約為 12%，高於一般鮮乳但低於奶粉。",
    37: "鬆餅或起酥類膨大主要靠麵糰中水分受熱汽化形成水蒸氣，推開油脂隔層而產生層次。",
    38: "法國麵包需高溫烤焙形成脆皮、良好膨脹與色澤，常用約 230°C 的較高爐溫。",
    39: "新鮮酵母含水量高，常見水分約 65~70%，因此保存性較乾酵母差。",
    40: "蒸烤布丁需低溫緩慢凝固以保持細緻組織，150°C 比高溫烘烤更適合。",
    41: "圓柱體容積為 πr²h，直徑 22 公分半徑 11 公分，高 5 公分，約 3.14×11×11×5=1899.7 立方公分。",
    42: "大量手工丹麥小西餅混合粉與糖油時應分次攪拌，避免局部吸水、乾硬或拌合不均。",
    43: "蛋白不易打發常因蛋溫低、蛋不新鮮或容器沾油；高速攪拌本身不是主要阻礙因素。",
    44: "低成分重奶油蛋糕適合糖油拌合法，先將油脂與糖打發以包入空氣、建立細緻組織。",
    45: "布丁蛋糕頂部高隆、裂開且四周收縮，常見原因是爐溫太高導致表面過快凝固與膨脹破裂。",
    46: "天使蛋糕依靠蛋白泡沫攀附模壁膨脹，烤盤若擦油會降低附著力，影響高度與組織。",
    47: "糖油拌合法做丹麥小西餅時，麵粉最後輕拌可避免麵筋過度形成，維持酥鬆口感。",
    48: "葡萄乾未浸水會在麵包中吸水並與麵糰結合差，切片時容易掉落。",
    49: "蘋果派餡常用玉米澱粉作膠凍與增稠原料，使果餡加熱後形成適當濃稠度。",
    50: "中間發酵需兼顧酵母活性與麵糰穩定，約 28°C、75~80% 濕度較適合室內麵包製程控制。",
}


def normalize(text):
    return re.sub(r"\s+", " ", text.strip()).strip("。 ")


def parse_items():
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    rows = []
    for raw in text.splitlines():
        line = raw.strip()
        if not re.match(r"^\d+\.\s*\([A-E]\)", line):
            continue
        m = re.match(r"^(\d+)\.\s*\(([A-E])\)\s*(.+)$", line)
        if not m:
            continue

        no = int(m.group(1))
        inline_answer = m.group(2)
        rest = m.group(3)
        option_matches = list(re.finditer(r"\(([A-D])\)\s*", rest))
        if len(option_matches) != 4:
            raise SystemExit(f"Question {no} expected 4 options, got {len(option_matches)}")

        question = normalize(rest[: option_matches[0].start()])
        options = []
        for idx, opt in enumerate(option_matches):
            start = opt.end()
            end = option_matches[idx + 1].start() if idx + 1 < len(option_matches) else len(rest)
            value = normalize(rest[start:end])
            value = re.sub(r"\s*\(註：.*$", "", value).strip()
            options.append((opt.group(1), value))

        answer = inline_answer
        if no == 33:
            answer = "B"
        if answer not in "ABCD":
            raise SystemExit(f"Question {no} has unsupported answer {answer}")

        rows.append(
            {
                "no": no,
                "question": question,
                "options": options,
                "answer": answer,
                "inline_answer": inline_answer,
            }
        )
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
    note = f" {SPECIAL_NOTES[item['no']]}" if item["no"] in SPECIAL_NOTES else ""
    return (
        f"本題正答為（{item['answer']}）{answer_text}。{REASONS[item['no']]}{note}"
        f"其他選項如 {wrong}，雖然可能出現在相近的烘焙或食品加工情境，"
        f"但不符合本題指定的原料功能、製程條件、保存標準或食品安全判斷，因此不宜選用。"
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
organizer: 107 學年度全國高級中等學校學生商業類技藝競賽正式試題整理
dates: 107 學年度
location: 線上測驗
format: 單選題 / {total} 題
instructor: 烘焙職種學科題庫解析
storeKey: {STORE_KEY}
timerSeconds: 3600
scorePerQuestion: 2
```

## 測驗目標

- 完成 107 學年度全國高級中等學校學生商業類技藝競賽烘焙職種學科正式試題 {total} 題完整練習。
- 熟悉烘焙油脂、糖類、麵包與西點製程、食品包裝保存、食品安全、冷藏冷凍與品質判定。
- 每題作答後閱讀 AI 分析，理解正確答案為何成立，以及干擾選項與題意的差異。

## 建議作答節奏

| 時間區間 | 題目範圍 | 重點 |
|---|---|---|
| 00:00 ~ 00:20 | Q1-Q15 | 原料功能、包裝耐熱、梅納反應、配方百分比與基礎製程 |
| 00:20 ~ 00:40 | Q16-Q30 | 品質鑑定、酵母與糖類、油脂劣化、冷凍保存與麵包缺失 |
| 00:40 ~ 01:00 | Q31-Q50 | 派餡凝凍、蛋白打發、麵包蛋糕製程、發酵條件與衛生保存 |

---

# DAY1

```yaml
id: day1
n: 1
date: 107 學年度
title: 107 學年度烘焙職種學科正式試題
hours: 1.0
date_label: 107 學年度
hours_label: 1.0 小時（60 分鐘）
learningGoal: 完成 107 學年度全國高級中等學校學生商業類技藝競賽烘焙職種學科正式試題 {total} 題練習。
hero_title: 107 烘焙職種學科正式試題
hero_lead: 依正式試題整理為線上測驗，每題 2 分，滿分 100 分。
```

## 單元 1：原料功能、糖油與基礎製程

```yaml
id: u-1
subtitle: 第 1 題至第 15 題，每題 2 分
time: 00:00 ~ 00:20
```

### 學習重點

- 判讀油脂、糖類、包裝材料、食品酸鹼界線與配方百分比等基礎概念。

## 單元 2：品質鑑定、保存與麵包製程

```yaml
id: u-2
subtitle: 第 16 題至第 30 題，每題 2 分
time: 00:20 ~ 00:40
```

### 學習重點

- 熟悉產品品質判斷、麵粉與糖漿、冷凍保存、油炸油劣化與麵包發酵缺失。

## 單元 3：西點、蛋糕與發酵條件

```yaml
id: u-3
subtitle: 第 31 題至第 50 題，每題 2 分
time: 00:40 ~ 01:00
```

### 學習重點

- 整合派餡、蛋白打發、蛋糕攪拌、丹麥小西餅、麵包中間發酵與衛生保存條件。

---

# MATERIALS

- [MD] {MATERIAL} | 107 學年度烘焙職種學科正式試題原始題本

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
title: 107 學年度烘焙職種學科正式試題
desc: 107 學年度全國高級中等學校學生商業類技藝競賽烘焙職種學科正式試題，共 {total} 題，涵蓋烘焙原料、配方百分比、麵包與西點製程、食品包裝保存、食品安全與品質判定。
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
