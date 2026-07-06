from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "chinese-cooking-103-official-exam.md"
OUTPUT = ROOT / "content.md"

ANSWER_INDEX = {"A": 0, "B": 1, "C": 2, "D": 3}
UNIT_ID = "day1.u-1"
TOPIC = "103 學年度中餐烹調正式競賽學科"

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
    "沙茶醬": "廣東料理常見柱侯醬、京都醬與蠔油汁；沙茶醬較常見於閩南、潮汕及台灣火鍋、沙茶料理脈絡。",
    "雞、豬": "雞肉常見沙門氏菌風險，豬肉則需注意旋毛蟲等寄生蟲風險，因此兩者都應充分煮熟。",
    "順丁烯二酸": "黑心珍珠粉圓事件與順丁烯二酸化製澱粉相關，長期攝取可能增加腎臟負擔。",
    "鋁": "部分含鋁膨鬆劑若攝取過量，可能造成健康疑慮，因此烘焙與食品添加物題常考含鋁膨鬆劑。",
    "猴頭菇": "猴頭菇為傳統珍貴菇菌食材，常被列入中國山珍類考點。",
    "小排": "無錫排骨、粉蒸排骨多取帶骨且肉質適合蒸、燒的豬小排。",
    "吉利丁": "吉利丁由動物膠原蛋白製成，並非植物性食材；瓊脂、海茸、髮菜則屬藻類或植物性來源。",
    "黃豆": "沙拉油在台灣市售常見大豆沙拉油，主要原料為黃豆。",
    "小茴香": "小茴香籽外觀細長，形似稻粒，是常見辛香料辨識題。",
    "鹽": "鹽可影響麵筋蛋白形成並增強麵糰筋性，使麵筋更有彈性與延展性。",
    "糖": "煙燻時糖受熱焦化並產生煙燻色澤與香氣，是煙燻材料中重要來源。",
    "16-18℃、50-60%": "乾料庫房宜維持低溫、低濕與通風，避免乾貨受潮、發霉或蟲害。",
    "200 燭光以上": "料理台與工作檯需有足夠照度，才能降低切割、加熱與操作錯誤風險。",
    "綠豆": "雞絲拉皮的拉皮多由綠豆澱粉製成，成品質地透明滑韌。",
    "澄粉": "水晶粉常指澄粉，即小麥澱粉，可形成透明或半透明質地。",
    "醋": "醋中的酸可促進部分礦物質溶出與吸收，因此常用來輔助鈣質利用。",
    "龍眼": "龍眼為台灣夏季盛產水果；檸檬也可在夏季盛產，因此原試題標示 B 或 D。",
    "360 元": "6 台斤為 3.6 公斤，每公斤 100 元，總價為 3.6 × 100 = 360 元。",
    "腹部": "魚類脂肪常集中於腹部，腹肉油脂含量較高，口感也較肥美。",
    "材料": "八珍是傳統料理中對八種珍貴食材或材料的總稱，重點在食材組合而非調味或火候。",
    "楊桃": "楊桃切開後酚類物質易與氧氣接觸並受酵素作用而褐變。",
    "黃麴毒素": "發霉穀類可能產生黃麴毒素，具肝毒性與致癌風險，不宜食用。",
    "濃厚蛋白量較多者": "新鮮蛋的濃厚蛋白比例較高，蛋白較黏稠，氣室較小。",
    "長糯米": "油飯常用長糯米，蒸煮後口感較 Q、粒粒分明，適合拌炒油飯配料。",
    "絲瓜": "絲瓜為台灣夏季常見盛產蔬菜，適合夏季料理與湯品。",
    "40～60％": "乾貨庫房需控制相對濕度，約 40～60% 可降低受潮、發霉與蟲害風險。",
    "脂肪": "膽汁能乳化脂肪，幫助脂肪及脂溶性維生素消化吸收。",
    "維生素B2": "維生素 B2 缺乏常見症狀包括口角炎、舌炎等黏膜問題。",
    "肉毒桿菌": "肉毒桿菌可產生強烈神經毒素，屬毒素型食物中毒的重要代表。",
    "正壓": "廚房清潔區宜維持正壓，避免較髒區域空氣流入造成污染。",
    "魯菜": "孔府菜源自山東曲阜孔府宴飲系統，屬魯菜代表。",
    "包心白": "台灣滷白菜常用包心白菜，葉片厚實、耐煮且能吸收湯汁。",
    "雲林": "雲林大埤等地以酸菜聞名，是台灣酸菜相關地方特產考點。",
    "綠豆": "冬粉主要由綠豆澱粉製成，透明且耐煮，是常見粉絲類食材。",
    "腐竹": "豆腐筋即腐竹，是豆漿加熱後表面凝結的豆皮乾製品。",
    "10 天、20 天": "牛肉屠宰後需經適當熟成，使肌肉蛋白分解、肉質變嫩；不同教材可能採約 10 天或 20 天作為標準，因此原卷標示 B 或 C。",
    "半磅水": "半磅約 227 公克，較 1 杯水、7 兩水與 9 盎司水都輕。",
}


def split_options(raw):
    circled = {"①": "A", "②": "B", "③": "C", "④": "D"}
    matches = []
    for match in re.finditer(r"\(([A-D])\)|[①②③④]", raw):
        letter = match.group(1) if match.group(1) else circled[match.group(0)]
        matches.append((match.start(), match.end(), letter))
    if not matches:
        return raw.strip(), []

    question = raw[: matches[0][0]].strip(" ：:，,")
    options = []
    for i, (marker_start, marker_end, letter) in enumerate(matches):
        start = marker_end
        end = matches[i + 1][0] if i + 1 < len(matches) else len(raw)
        text = raw[start:end].strip()
        text = re.sub(r"[。．\s]+$", "", text)
        options.append((letter, text))
    return question, options


def analysis_for(question, options, answer_letters):
    correct_pairs = [(letter, text) for letter, text in options if letter in answer_letters]
    correct_text = "、".join(f"{letter}. {text}" for letter, text in correct_pairs)
    correct_names = "、".join(text for _, text in correct_pairs)
    wrong = "、".join(f"{letter}. {text}" for letter, text in options if letter not in answer_letters)
    extra = next((v for k, v in EXTRA_REASONS.items() if k in correct_names or k in question), "")
    extra_sentence = f"具體來說，{extra}" if extra else ""
    negative_words = ("不屬", "不是", "不可以", "不適合", "錯誤", "不符合", "並非", "最不")
    cuisine_words = ("菜系", "菜餚", "清真", "客家", "古代", "別稱", "俗稱")
    food_safety_words = ("火災", "中毒", "溫度", "濕度", "冷藏", "冷凍", "熱藏", "HACCP", "衛生")

    if len(answer_letters) > 1:
        return (
            f"本題答案為「{correct_text}」。原試卷標示可接受多個答案，代表題幹條件與選項事實存在一個以上可成立的對應。"
            f"正確選項「{correct_names}」都符合題幹所問的季節、食材或學科分類；{extra_sentence}"
            f"{wrong} 則不符合本題標準。複習時應同時記住題庫答案與背後條件，避免只背單一選項。"
        )

    if any(word in question for word in negative_words):
        why = (
            f"本題答案為「{correct_text}」。題幹是否定式問法，重點是找出不符合分類、用途或規範的排除項。"
            f"正確選項「{correct_names}」之所以成立，是因為它與題幹要求不相符；{extra_sentence}"
            f"相對地，{wrong} 較符合題幹所列的同類概念或實務規則，所以不能選。"
        )
    elif any(word in question for word in cuisine_words):
        why = (
            f"本題答案為「{correct_text}」。這類題目考的是中餐飲食文化、菜系典故、食材別稱或地方產品的對應關係。"
            f"正確選項「{correct_names}」與題幹所指的菜系、名稱或飲食規範直接對應；{extra_sentence}"
            f"{wrong} 則屬其他菜系、其他食材或不同文化脈絡。"
        )
    elif any(word in question for word in food_safety_words):
        why = (
            f"本題答案為「{correct_text}」。判斷關鍵在食品安全、廚房安全或保存條件的標準規範。"
            f"正確選項「{correct_names}」符合題幹要求的安全處置、溫度條件或衛生管理原則；{extra_sentence}"
            f"{wrong} 不是本題標準條件，實務上可能造成通報錯誤、保存不當或衛生風險。"
        )
    else:
        why = (
            f"本題答案為「{correct_text}」。判斷關鍵在題幹所問的食材部位、原料特性、烹調技法、調味功能或單位換算。"
            f"正確選項「{correct_names}」與該中餐學科概念最直接對應；{extra_sentence}"
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
        match = re.match(r"^(\d+)\.\s*\(([A-D](?:或[A-D])*)\)\s*(.+)$", line)
        if not match:
            continue
        number = int(match.group(1))
        answer_raw = match.group(2)
        answer_letters = re.findall(r"[A-D]", answer_raw)
        raw = match.group(3).strip()
        question, options = split_options(raw)
        items.append(
            {
                "global_no": number,
                "question": question,
                "options": options,
                "answer_raw": answer_raw,
                "answer_letters": answer_letters,
                "answer_yaml": answer_letters[0] if len(answer_letters) == 1 else "[" + ", ".join(answer_letters) + "]",
                "display_answer": "".join(f"({letter})" for letter in answer_letters),
                "multiple": len(answer_letters) > 1,
                "correct_text": "、".join(text for letter, text in options if letter in answer_letters),
            }
        )
    return items


def build_content(items):
    total = len(items)
    source = (
        "103 學年度商業類科學生技藝競賽中餐烹調學科正式試卷；"
        "勞動部勞動力發展署技能檢定中心中餐烹調相關學科題庫；"
        "衛生福利部食品藥物管理署食品安全衛生管理法、食品良好衛生規範準則與餐飲衛生公開資料。"
    )
    quiz_blocks = []
    for item in items:
        options_md = "\n".join(f"- ({letter}) {text}" for letter, text in item["options"])
        analysis = analysis_for(item["question"], item["options"], item["answer_letters"])
        type_line = "type: multiple\n" if item["multiple"] else ""
        quiz_blocks.append(
            f"""## Q{item["global_no"]} ｜ {"複選題" if item["multiple"] else "單選題"}

103 學年度中餐烹調正式競賽學科第 {item["global_no"]} 題：
{item["question"]}

{options_md}

```yaml
{type_line}answer: {item["answer_yaml"]}
unit: {UNIT_ID}
explanation: |
  【答案】{item["display_answer"]}
  【出處】{source}
  【AI 分析】
  {analysis}
```
"""
        )

    return f"""# META

```yaml
title: 103 學年度中餐烹調正式競賽學科試卷
subtitle: 商業類科學生技藝競賽線上練習考場
program: 商業類科學生技藝競賽中餐烹調
organizer: 103 學年度商業類科學生技藝競賽試題整理
dates: 103
location: 線上測驗系統
format: 正式競賽學科試卷 / 50 題單選
instructor: 中餐烹調學科輔助解析
storeKey: 103-chinese-cooking-progress-v1
timerSeconds: 3600
```

## 學習目標

- 完成 103 學年度中餐烹調正式競賽學科 50 題完整練習。
- 熟悉中餐食材部位、菜系文化、烹調技法、食品安全、廚房安全與基礎換算。
- 透過逐題答案、出處與 AI 分析，建立可複習的錯題筆記。

## 考科時程

| 建議時間 | 考科單元 | 考核重點 |
|---|---|---|
| 00:00 ~ 00:15 | Q1-Q15 | 食材特性、鮮度、營養與菜系基礎 |
| 00:15 ~ 00:30 | Q16-Q30 | 麵點、漲發、毒素、清潔區與地方物產 |
| 00:30 ~ 00:45 | Q31-Q40 | 粉類、豆製品、酒糟調味、菜系與粥品 |
| 00:45 ~ 01:00 | Q41-Q50 | 清潔設備、地方特產、勾芡、度量衡與古籍 |

---

# DAY1

```yaml
id: day1
n: 1
date: 103
title: 103 學年度中餐烹調正式競賽學科練習
hours: 1.0
date_label: 103
hours_label: 1.0 小時 (60分鐘)
learningGoal: 完成 103 學年度中餐烹調正式競賽學科 50 題練習。
hero_title: 103 中餐烹調正式競賽學科
hero_lead: 本試卷共 {total} 題，多數為單選題；第 34 題依原卷標示可接受 B 或 C，系統以答對題數換算百分制。
```

## 單元1：103 學年度正式競賽學科題庫

```yaml
id: u-1
subtitle: 共 {total} 題
time: 自主練習
```

### 學習目標

- 熟悉 103 學年度中餐烹調正式競賽學科的常見考點。
- 能依據中餐食材知識、菜系文化、烹調原理與食品衛生安全判斷正確答案。

### 任務清單

- [d1-u1-t1] 完成 103 學年度正式競賽學科 50 題練習。

---

# MATERIALS

- [MD] chinese-cooking-103-official-exam.md | 103 學年度中餐烹調正式競賽學科原始試卷

---

# PORTAL

```yaml
title: 學術能力模擬檢測入口
subtitle: 歡迎來到模擬考試線上平台。本系統已依照不同試題與科目分類，請點擊下方對應的卡片進入考場進行線上作答與評分。
```

## 考試卡片

```yaml
id: exam-103-chinese-cooking
tag: 中餐烹調
title: 103 學年度中餐烹調正式競賽學科
desc: 103 學年度商業類科學生技藝競賽中餐烹調正式學科試卷，共 {total} 題，涵蓋食材特性、菜系文化、食品安全、庫房管理、地方特產與度量衡。
time: 60 分鐘
questions: 共 {total} 題
score: 滿分 100 分
href: 103-chinese-cooking/
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
