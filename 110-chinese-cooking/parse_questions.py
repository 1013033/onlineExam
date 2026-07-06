from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "course-package" / "materials" / "chinese-cooking-110-official-exam.md"
OUTPUT = ROOT / "content.md"

ANSWER_INDEX = {"A": 0, "B": 1, "C": 2, "D": 3}
UNIT_ID = "day1.u-1"
TOPIC = "110 學年度中餐烹飪正式試題"

SOURCES = (
    "110 學年度商業類學生技藝競賽中餐烹飪學科正式試題；"
    "勞動部勞動力發展署技能檢定中心中餐烹調相關學科題庫；"
    "衛生福利部食品藥物管理署食品安全衛生管理法、食品良好衛生規範準則與餐飲衛生公開資料。"
)

REASONS = {
    1: "技藝競賽進場規範重視衛生、安全與公平識別；制服不合規定表示未符合應試基本條件，因此不得進入或須離場。",
    2: "廚房地面常有水、油與熱湯汁，黑色工作安全皮鞋較能防滑、防護腳部並符合正式競賽服裝要求。",
    3: "廚師參與採購時要掌握蔬果季節性；盛產期食材通常品質穩定、價格合理，也較能反映菜餚風味。",
    4: "冷藏冷凍庫不可塞滿，約保留四成空間才利於冷空氣循環，使溫度快速回復並維持食品品質。",
    5: "糖醋瓦片魚需呈現酥脆片狀口感，魚片調味上漿後沾乾粉炸熟，才能形成外酥內熟且可掛糖醋汁的效果。",
    6: "爐台編號直接影響競賽公平與評分紀錄，發現不符時應立即告知現場裁判委員，由具裁決權者處理。",
    7: "麵糊加油可降低麵筋韌性並改善炸後表面質地，使外皮較鬆化酥脆，而不是柔軟或僵硬。",
    8: "圓糯米支鏈澱粉比例高、吸水後黏軟度較明顯；在相同加水量下，通常比尖糯米更軟黏。",
    9: "馬鈴薯發芽、變綠時茄靈毒素含量上升，食用可能造成中毒，因此發芽馬鈴薯不宜食用。",
    10: "香腸、火腿加硝主要是保色並抑制部分微生物，但必須符合食品添加物使用範圍與限量。",
    11: "生魚片風險評估重點是寄生蟲與污染來源；深海魚相對較少受淡水或近岸污染影響，較適合作為生食材料。",
    12: "發霉穀類常見風險是黃麴毒素，該毒素具肝毒性且耐熱，不能靠一般烹煮完全消除。",
    13: "A 型肝炎可經糞口途徑傳播，餐飲從業人員若感染，會增加食品污染風險，因此不得從事食品接觸工作。",
    14: "西湖醋魚與江浙、上海菜系文化關聯密切，特色是以魚、醋香與清鮮調味呈現地方風味。",
    15: "陶器使人類能盛水加熱，讓煮、燉、羹等加水烹調法成為可能，因此象徵加水烹調的開始。",
    16: "中餐廚房分工中，紅案多指處理葷食、切配與熱菜前處理的砧板工作，故對應砧櫈。",
    17: "佛跳牆是福建名菜，以多種乾貨與高湯燉煨聞名，代表閩菜講究湯鮮、料多與香氣融合的特色。",
    18: "競賽中離場會影響監督與公平，須經監評長准許且有人陪同；15 分鐘是題目規定的上限。",
    19: "抹布容易累積油脂與微生物，以 100℃ 沸水煮沸 5 分鐘可達基本熱消毒目的。",
    20: "乾米粉水分活性低，微生物較不易繁殖，所以比高水分食品耐保存；不是依靠大量防腐劑。",
    21: "油炸後濾除油渣可減少焦化物與劣變速度，再倒入乾淨容器保存，才能降低二次污染與油耗味。",
    22: "許多豆類含胰蛋白酶抑制物等抗營養因子，需加熱破壞後較安全、也較易消化。",
    23: "牛奶鈣含量高，但鐵含量相對不足；若只以牛奶補充礦物質，容易忽略鐵的攝取。",
    24: "鈉攝取過多會增加血容量與血壓負擔，是高血壓飲食控制的重要限制項目。",
    25: "木瓜等橙黃色蔬果含較多類胡蘿蔔素，可作為維生素 A 前驅物來源。",
    26: "胡蘿蔔立體切雕較適合冷盤，因冷盤展示時間較長且不會被熱湯、熱汁破壞造型。",
    27: "不鏽鋼耐腐蝕、易清潔、表面不易吸附污垢，是廚房工作檯常用且符合衛生需求的材質。",
    28: "盤飾是輔助菜餚美觀，不能喧賓奪主；用量超過主體會破壞菜餚比例與呈現重點。",
    29: "在四個選項中，馬鈴薯屬植物性食材，含膳食纖維；雞肉、魚肉與雞蛋幾乎不含膳食纖維。",
    30: "膽固醇只存在於動物性食品，奶油來自乳脂，含膽固醇；植物油如花生油、紅花子油與大豆油不含膽固醇。",
    31: "黃魚體色偏黃，常與年節喜慶、金黃色意象連結；題幹描述的產地與外觀都指向黃魚。",
    32: "排水溝採明溝時需加蓋且與地面平齊，可避免人員絆倒、器具卡住，也降低污染與病媒風險。",
    33: "廚師證照持有人每年需接受衛生講習，以維持食品安全知識與執業衛生觀念；題目指定為 8 小時。",
    34: "工作檯上方燈具加裝燈罩，可避免燈泡破裂時碎片落入食品，是食品作業場所常見衛生安全要求。",
    35: "金華火腿產自浙江金華，是中國傳統名火腿；江蘇、雲南則另有不同地方名產。",
    36: "傳統西湖醋魚多以草魚製作，重點在魚肉鮮嫩與醋汁調味，草魚是該菜常用魚種。",
    37: "乾鮑常以「頭」表示大小，即一斤約有幾顆；頭數越少通常個體越大。",
    38: "廚房常見油火與一般火災，乾粉滅火器適用範圍較廣，是廚房應備的基本滅火設備。",
    39: "鹽能凸顯與平衡多種味道，是調味基礎，因此有「百味之王」的稱呼。",
    40: "料清師傅負責掌控製備流程、出餐順序與最後把關，不一定親自切配烹調，是管理與協調角色。",
    41: "花椒具有去腥、增香、提鮮與解膩效果，常用於燒、滷、扣蒸、煨等料理，也帶有特殊麻香苦味。",
    42: "爆炒的技術重點是旺火、短時間與快速翻動，使食材迅速成熟並保持香氣與口感。",
    43: "蒸利用水蒸氣加熱，較少直接接觸油脂與大量湯水，能較好保留原料形態與營養。",
    44: "餐盤裝飾應選可食、潔淨、能塑形且不易污染菜餚的材料；硬脆瓜果與根莖類蔬菜較能符合這些條件。",
    45: "魚肚類乾貨多由魚膘乾製而成，泡發後呈膠質口感；不是魚腸、魚卵或一般魚腹肉。",
    46: "選購罐頭除了封罐完整，也要檢查標示清楚、無膨罐或變形，才能確認來源與保存狀態。",
    47: "竹製蒸籠吸濕性較佳，蒸氣凝結水較不易大量滴回食物表面，可保護成品外觀與口感。",
    48: "醬油膏比醬油濃稠，主要是加入澱粉形成稠度，並非單靠發酵時間或水分濃縮。",
    49: "老抽是深色醬油，常用於上色與增加醬香；與蒸魚醬油或淡色醬油的用途不同。",
    50: "刀工影響食材大小、厚薄與受熱速度，火候決定熟度與質地；兩者配合不好會直接影響成菜品質。",
}


def parse():
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    text = re.split(r"^###\s*二、", text, maxsplit=1, flags=re.MULTILINE)[0]
    items = []
    lines = text.splitlines()
    i = 0

    while i < len(lines):
        match = re.match(r"^\s*(\d+)\.\s*\*\*\(\s*([^)]+?)\s*\)\*\*\s*(.+)$", lines[i])
        if not match:
            i += 1
            continue

        number = int(match.group(1))
        answer_raw = match.group(2).strip()
        answer_letters = ["A", "B", "C", "D"] if "送分" in answer_raw else re.findall(r"[A-D]", answer_raw)
        question = match.group(3).strip()
        options = []
        i += 1

        while i < len(lines):
            if re.match(r"^\s*\d+\.\s*\*\*\(", lines[i]):
                break
            opt_match = re.match(r"^\s*-\s*[\(（]([A-D])[\)）]\s*(.+)$", lines[i])
            if opt_match:
                option_text = re.sub(r"[。．\s]+$", "", opt_match.group(2).strip())
                options.append((opt_match.group(1), option_text))
                i += 1
                continue
            i += 1

        items.append(
            {
                "global_no": number,
                "question": question,
                "options": options,
                "answer_raw": answer_raw,
                "answer_letters": answer_letters,
            }
        )

    return items


def analysis_for(item):
    answer_letters = item["answer_letters"]
    options = item["options"]
    correct_pairs = [(letter, text) for letter, text in options if letter in answer_letters]
    wrong_pairs = [(letter, text) for letter, text in options if letter not in answer_letters]
    correct_text = "、".join(f"{letter}. {text}" for letter, text in correct_pairs)
    wrong_text = "、".join(f"{letter}. {text}" for letter, text in wrong_pairs)
    reason = REASONS.get(
        item["global_no"],
        "本題可由題幹關鍵詞與中餐烹調、食品衛生或競賽規範的基本原則判斷；正確選項最符合題目所問的定義、用途或標準。",
    )

    if len(answer_letters) > 1:
        return (
            f"本題採複數給分，正確答案為「{correct_text}」。{reason}"
            f"其餘選項「{wrong_text}」不符合題幹限制或不是本題要判斷的重點。"
            "複習時可先抓題幹中的限定詞，再逐一排除與規範、食材特性或烹調原理不一致的敘述。"
        )

    return (
        f"本題答案為「{correct_text}」。{reason}"
        f"其他選項「{wrong_text}」雖可能與廚房作業或食材知識有關，但不是題幹所問的正確對應，"
        "因此作答時應回到題目中的關鍵條件判斷，而不是只憑字面相似度選擇。"
    )


def format_answer(answer_letters):
    indexes = [ANSWER_INDEX[letter] for letter in answer_letters]
    if len(indexes) == 1:
        return str(indexes[0])
    return "[" + ", ".join(str(i) for i in indexes) + "]"


def write_content(items):
    total = len(items)
    question_blocks = []
    for item in items:
        options_md = "\n".join(f"- ({letter}) {text}" for letter, text in item["options"])
        analysis = analysis_for(item)
        answer = format_answer(item["answer_letters"])
        question_blocks.append(
            f"""## Q{item['global_no']} ｜ 單選題

{item['question']}

{options_md}

```yaml
answer: {answer}
sourceUnit: {UNIT_ID}
explanation: |
  【答案】{"、".join(f"({letter})" for letter in item["answer_letters"])}
  【出處】{SOURCES}
  【AI 分析】
  {analysis}
```
"""
        )

    content = f"""# META

```yaml
title: 110 學年度中餐烹飪正式試題
subtitle: 商業類科學生技藝競賽線上練習考場
program: 商業類科學生技藝競賽中餐烹調
organizer: 110 學年度商業類學生技藝競賽正式試題整理
dates: 110
location: 線上測驗系統
format: 正式試題學科試卷 / {total} 題單選
instructor: 中餐烹調學科輔助解析
storeKey: 110-chinese-cooking-progress-v1
timerSeconds: 3600
scorePerQuestion: 2
```

## 學習目標

- 完成 110 學年度中餐烹飪正式試題 {total} 題完整練習。
- 熟悉競賽規範、食品衛生、食材特性、菜系文化、廚房安全與烹調技法。
- 透過逐題答案、出處與 AI 分析，理解每題正確答案的判斷理由。

## 考科時程

| 建議時間 | 考科單元 | 考核重點 |
|---|---|---|
| 00:00 ~ 00:15 | Q1-Q15 | 競賽規範、食品保存、食材安全與菜系文化 |
| 00:15 ~ 00:30 | Q16-Q30 | 廚房分工、營養素、盤飾與工作檯衛生 |
| 00:30 ~ 00:45 | Q31-Q40 | 廚房設備、證照衛生、地方名產與調味 |
| 00:45 ~ 01:00 | Q41-Q50 | 辛香料、烹調法、乾貨、罐頭與刀工火候 |

---

# MATERIALS

- [MD] chinese-cooking-110-official-exam.md | 110 學年度中餐烹飪正式試題原始試卷

---

# PORTAL

```yaml
title: 學術能力模擬檢測入口
subtitle: 歡迎來到模擬考試線上平台。本系統已依照不同試題與科目分類，請點擊下方對應的卡片進入考場進行線上作答與評分。
```

## 考試卡片

```yaml
id: exam-110-chinese-cooking
tag: 中餐烹調
title: 110 學年度中餐烹飪正式試題
desc: 110 學年度商業類學生技藝競賽中餐烹飪學科正式試題，共 {total} 題，涵蓋競賽規範、食品衛生、食材處理、米食點心、菜系文化與烹調技法。
time: 60 分鐘
questions: 共 {total} 題
score: 滿分 100 分
href: 110-chinese-cooking/
btnText: 進入線上考場
```

---

# QUIZ

{chr(10).join(question_blocks)}
"""
    OUTPUT.write_text(content, encoding="utf-8")


def main():
    items = parse()
    if len(items) != 50:
        raise SystemExit(f"Expected 50 questions, got {len(items)}")
    bad_options = [item["global_no"] for item in items if len(item["options"]) != 4]
    if bad_options:
        raise SystemExit(f"Questions with invalid option count: {bad_options}")
    write_content(items)
    print(f"Parsed {len(items)} questions -> {OUTPUT}")


if __name__ == "__main__":
    main()
