from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "chinese-cooking-100-official-exam.md"
OUTPUT = ROOT / "content.md"

ANSWER_INDEX = {"A": 0, "B": 1, "C": 2, "D": 3}
SOURCES = (
    "全國高級中等學校100學年度商業類科學生技藝競賽中餐烹飪職種學科正式試卷；"
    "中餐烹調技術士技能檢定相關學科題庫；"
    "食品良好衛生規範準則與中餐食材、菜系、烹調技法、食品衛生相關公開教學資料。"
)

REASONS = {
    1: "廚房工作檯面需有足夠照度，才能安全辨識食材、刀工與污染狀況；題庫標準答案 C 對應 200 燭光。",
    2: "1 磅約為 454 公克，是餐飲與烘焙常用重量換算；其他台兩、杯量或磅盎司換算不符標準。",
    3: "羹類通常以羹碗或深盤呈現，不是最適合放湯碗；其他餐具與菜餚搭配較符合中餐出菜邏輯。",
    4: "北平鍋典型特徵為單柄長把，便於翻鍋；玻璃導熱、生熟鐵導熱與熟鐵色澤敘述皆不正確。",
    5: "不銹鋼主要由鐵、鉻、鎳等組成以提升耐蝕性，鎘不是不銹鋼的主要材質。",
    6: "它似蜜為北京名菜，傳統以羊里肌等嫩羊肉切片調味炒製，呈甜香滑嫩口感。",
    7: "叉燒肉常選梅花肉，肥瘦適中且適合醃烤；其他菜餚與食材部位配對不正確。",
    8: "沖菜是以芥菜類加工或調味形成的食品，不屬油菜類；菜籽、菜苔與菜心則與油菜類關聯較高。",
    9: "百合食用部位為鱗莖，不是球莖；蓮藕、山藥與韭黃配對較符合植物部位分類。",
    10: "此題原資料列為送分，表示正式答案不採單一選項計分；系統接受任一選項作答。",
    11: "台語市仔常指蟹類，是中餐水產食材別稱題的常見考點。",
    12: "生蛋最常見風險為沙門氏菌污染，因此蛋品生食需特別注意來源與衛生。",
    13: "本題答案依原正式資料為奇異果；漿果分類在植物學與食品分類中易有差異，作答以正式答案為準。",
    14: "蝦餃皮以澄粉等澱粉或麵粉類材料製作，屬麵粉類製品範圍；粄條與芋圓來源不同。",
    15: "雲林西螺等地以蔭油、黑豆醬油聞名，是台灣地方調味品產地常見題。",
    16: "螞蟻上樹主要由絞肉與冬粉構成，肉末附著在冬粉上形成菜名意象。",
    17: "稻作文化在中國長江流域有早期發展，題庫指定湖南為稻米栽培源起相關答案。",
    18: "莧菜偏好溫暖季節，冬季產量相對較少；白菜、包心菜、菠菜較常見於冷涼季節。",
    19: "壽司飯需黏性與粒形適中，台灣常以蓬萊米等粳米系統製作。",
    20: "糙米保留麩皮與胚芽，膳食纖維含量高於胚芽米、精白米與糯米。",
    21: "銀芽為綠豆芽，並非黃豆製品；納豆、素雞與素食人造肉可歸於黃豆或豆製品範圍。",
    22: "大薄片為雲南菜常見風味菜餚，常以豬肉薄片搭配酸辣調味。",
    23: "宋嫂魚羹、醃篤鮮、道口燒雞分別可對應杭州、上海與河南；九轉大腸為魯菜，不是湖南菜。",
    24: "清炒、紅燒與醬爆多不以勾芡作為必要條件；滑溜通常重視上漿與芡汁滑嫩感。",
    25: "花青素在酸性環境中較能維持紅紫色，醋可降低 pH 並幫助保色。",
    26: "此題原資料列為送分，表示正式答案不採單一選項計分；系統接受任一選項作答。",
    27: "紫蘇常用於蟹類料理，可增香、去腥並平衡寒涼感，是蒸蟹常見搭配。",
    28: "雪蛤與干貝較不適合單純冷水發，常需較細緻或加熱處理；竹笙、蜇皮發製方式不同。",
    29: "魚肚又稱廣肚，可水發，來源為魚鰾；題庫指定錯誤敘述為漲發時不可加鹼。",
    30: "吉利炸使用麵包粉等方式形成外層，與西式酥炸方式最接近。",
    31: "焗為廣東菜常見技法，利用密閉或高溫使食材受熱成熟並保留香氣。",
    32: "麻辣豆魚主要用腐衣，醃篤鮮常用百頁結；合菜戴帽與炸響鈴的配對在題目中不正確。",
    33: "珍珠丸子常歸為湘菜特色，以糯米裹肉丸蒸製，外觀似珍珠。",
    34: "酒釀使用圓糯米，海產粥常用粳米；珍珠丸子與蘿蔔糕配對在題目中不採為正確組合。",
    35: "動物屠宰後肌肉糖原轉為乳酸，pH 會下降；其餘肉質熟成、加熱保水與肉色來源敘述不正確。",
    36: "芫爆菜式的關鍵香氣來自芫荽，也就是香菜，能凸顯墨魚鮮味。",
    37: "粉皮多由綠豆澱粉製成，口感滑嫩，常用於雞絲拉皮等涼菜。",
    38: "瓦焗的瓦指陶罐或陶製容器，藉其蓄熱與密閉性完成焗製。",
    39: "蘋果屬溫帶水果，適宜低溫貯藏，通常可比鳳梨、香瓜、檸檬使用更低儲存溫度。",
    40: "冰糖能在紅燒中增加甜味、亮澤與醬色光感，使蹄膀表面更光亮。",
    41: "米酒的主要酒精成分是乙醇，甲醇、丙醇、丁醇不是一般食用酒的主要成分。",
    42: "紅燒色澤主要來自醬油中的胺基酸褐變與焦糖色，也可搭配糖色，但題目主因為醬油。",
    43: "粉心麵粉筋性約介於高低筋之間，找不到時可用中筋麵粉較接近替代。",
    44: "水果入菜常搭配嫩薑，能提香、去生味並平衡水果甜酸。",
    45: "虎掌肉指豬前腳部位，因形似虎掌而得名，常用於滷、燒等料理。",
    46: "排骨飯使用帶骨豬排多取大排，肉片帶骨且適合醃炸或煎炸。",
    47: "蔬菜苦味常來自植物鹼等苦味成分，不是薑酚、蒜類硫化物或草酸本身。",
    48: "鳳眼糕以台南等地較具代表性，題目中配對台中市不符合。",
    49: "三星蔥產於宜蘭三星，為台灣著名地方農產。",
    50: "四川大紅袍是花椒品種或稱名，具有麻香，是川菜重要辛香料。",
}


def split_options(text):
    matches = list(re.finditer(r"\(([A-D])\)", text))
    if len(matches) == 0:
        return text.strip(), []
    question = text[: matches[0].start()].strip()
    options = []
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        option_text = text[match.end() : end].strip()
        options.append((match.group(1), option_text))
    return question, options


def parse_answer(answer):
    answer = answer.strip()
    if "送分" in answer:
        return ["A", "B", "C", "D"]
    return re.findall(r"[A-D]", answer)


def parse():
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    items = []
    row_re = re.compile(r"^\|\s*\*\*(\d+)\*\*\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$")
    for line in text.splitlines():
        match = row_re.match(line)
        if not match:
            continue
        no = int(match.group(1))
        answer_letters = parse_answer(match.group(2))
        question, options = split_options(match.group(3).strip())
        if no == 1 and not options:
            options = [("A", "50 燭光"), ("B", "100 燭光"), ("C", "200 燭光"), ("D", "500 燭光")]
        items.append({"no": no, "answer_letters": answer_letters, "question": question, "options": options})
    return items


def unit_for(no):
    if no <= 15:
        return "day1.u-1"
    if no <= 30:
        return "day1.u-2"
    return "day1.u-3"


def answer_yaml(letters):
    indexes = [ANSWER_INDEX[x] for x in letters]
    if len(indexes) == 1:
        return letters[0]
    return "[" + ", ".join(str(i) for i in indexes) + "]"


def answer_display(letters):
    return "、".join(f"({letter})" for letter in letters)


def analysis_for(item):
    letters = item["answer_letters"]
    correct = [(letter, text) for letter, text in item["options"] if letter in letters]
    wrong = [(letter, text) for letter, text in item["options"] if letter not in letters]
    correct_text = "、".join(f"{letter}. {text}" for letter, text in correct) or "送分"
    wrong_text = "、".join(f"{letter}. {text}" for letter, text in wrong)
    reason = REASONS[item["no"]]
    if len(letters) > 1:
        return (
            f"本題為送分題，系統接受任一選項。{reason}"
            "複習時仍建議理解題目爭議所在，避免遇到修正版或相似題時只依賴送分結果。"
        )
    return (
        f"本題答案為「{correct_text}」。{reason}"
        f"其他選項「{wrong_text}」雖可能與中餐食材、菜系、器具或烹調法有關，"
        "但不符合題幹指定的正確配對、食材來源、衛生風險或製程原理。"
        "作答時應先抓住題幹關鍵詞，再用中餐學理與食品衛生規範排除干擾選項。"
    )


def render_question(item):
    options = "\n".join(f"- ({letter}) {text}" for letter, text in item["options"])
    type_line = "type: multiple\n" if len(item["answer_letters"]) > 1 else ""
    return f"""## Q{item['no']} ｜ 單選題

{item['question']}

{options}

```yaml
{type_line}answer: {answer_yaml(item["answer_letters"])}
unit: {unit_for(item["no"])}
explanation: |
  【答案】{answer_display(item["answer_letters"])}
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
title: 100 學年度中餐烹飪職種學科正式試卷
subtitle: 商業類科學生技藝競賽線上練習考場
program: 商業類科學生技藝競賽中餐烹飪職種
organizer: 100 學年度商業類科學生技藝競賽正式試卷整理
dates: 100
location: 線上測驗系統
format: 正式試題學科試卷 / {total} 題單選
instructor: 中餐烹飪職種學科輔助解析
storeKey: 100-chinese-cooking-progress-v1
timerSeconds: 3600
scorePerQuestion: 2
```

## 學習目標

- 完成 100 學年度中餐烹飪職種學科正式試卷 {total} 題完整練習。
- 熟悉廚房衛生與器具、食材別稱與分類、菜系代表菜、烹調技法、肉品與米食知識。
- 透過逐題答案、出處與 AI 分析，理解每題正確答案的學理依據與排除理由。

## 考科時程

| 建議時間 | 考科單元 | 考核重點 |
|---|---|---|
| 00:00 ~ 00:20 | Q1-Q15 | 廚房衛生、器具、重量換算、食材部位與地方產物 |
| 00:20 ~ 00:40 | Q16-Q30 | 米食、豆製品、菜系、乾貨漲發與烹調技法 |
| 00:40 ~ 01:00 | Q31-Q50 | 菜餚配對、肉品、調味、麵粉、蔬菜苦味與地方名產 |

---

# DAY1

```yaml
id: day1
n: 1
date: 100
title: 100 學年度中餐烹飪職種學科正式試卷
hours: 1.0
date_label: 100 學年度
hours_label: 1.0 小時 (60分鐘)
learningGoal: 完成 100 學年度商業類科學生技藝競賽中餐烹飪職種學科正式試卷 50 題練習。
hero_title: 100 中餐烹飪職種學科正式試卷
hero_lead: 本試卷共 {total} 題，其中第 10、26 題依原始資料為送分題；系統接受任一選項作答。
```

## 單元1：廚房衛生、器具與食材基礎

```yaml
id: u-1
subtitle: 第 1 題至第 15 題，每題 2 分
time: 00:00 ~ 00:20
```

### 學習目標

- 熟悉廚房照度、器具材質、重量容積換算與餐具使用。
- 掌握肉品、蔬果、醬油與水產別稱的基礎考點。

## 單元2：米食豆製品、菜系與烹調技法

```yaml
id: u-2
subtitle: 第 16 題至第 30 題，每題 2 分
time: 00:20 ~ 00:40
```

### 學習目標

- 分辨米種、豆製品、地方菜系與乾貨發製方式。
- 理解花青素保色、蛋液爭議題、辛香料與油炸技法。

## 單元3：菜餚配對、肉品調味與地方食材

```yaml
id: u-3
subtitle: 第 31 題至第 50 題，每題 2 分
time: 00:40 ~ 01:00
```

### 學習目標

- 熟悉焗、瓦焗、紅燒、芫爆與珍珠丸子等中餐技法與菜系歸屬。
- 掌握肉品部位、調味來源、粉類替代、地方伴手禮與辛香料。

---

# MATERIALS

- [MD] chinese-cooking-100-official-exam.md | 100 學年度中餐烹飪職種學科正式試卷原始試題

---

# PORTAL

```yaml
title: 學術能力模擬檢測入口
subtitle: 歡迎來到模擬考試線上平台。本系統已依照不同試題與科目分類，請點擊下方對應的卡片進入考場進行線上作答與評分。
```

## 考試卡片

```yaml
id: exam-100-chinese-cooking
tag: 中餐烹調
title: 100 學年度中餐烹飪職種學科正式試卷
desc: 100 學年度商業類科學生技藝競賽中餐烹飪職種學科正式試卷，共 {total} 題，涵蓋廚房衛生、食材別稱、菜系代表菜、烹調技法、肉品部位、調味與地方名產。
time: 60 分鐘
questions: 共 {total} 題
score: 滿分 100 分
href: 100-chinese-cooking/
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
    bad_options = [item["no"] for item in items if len(item["options"]) not in (0, 4)]
    if bad_options:
        raise SystemExit(f"Questions with invalid option count: {bad_options}")
    OUTPUT.write_text(build_content(items), encoding="utf-8")
    print(f"Parsed {len(items)} questions -> {OUTPUT}")


if __name__ == "__main__":
    main()
