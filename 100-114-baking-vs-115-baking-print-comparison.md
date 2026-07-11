# 100-114-baking-print vs 115-baking-b/c-print comparison

## Scope

- Base: `100-114-baking-print/data.js`, 847 questions.
- Candidate: `115-baking-b-print/data.js`, 731 questions.
- Candidate: `115-baking-c-print/data.js`, 513 questions.

## Method

- Each 100-114 question is compared against both 115 B and 115 C question banks.
- Matching uses normalized question text with bigram Dice similarity. Whitespace and common punctuation are ignored.
- Inclusion threshold: question similarity >= 90%.
- `same_option_set` means the four option texts match as a set, even if option order differs.
- `same_correct_text` compares the actual correct option text, not only the answer letter.

## Summary

- 100-114 questions above threshold: 68.
- Matched to 115 B: 0.
- Matched to 115 C: 68.
- Exact question text after normalization: 18.
- High similarity (95% <= score < 100%): 32.
- Possible similarity (90% <= score < 95%): 18.

## Comparison Table

| base_no | base_source | base_question | base_answer | matched_bank | matched_no | matched_source | matched_question | matched_answer | score | confidence | same_option_set | same_correct_text |
|---:|---|---|---|---|---:|---|---|---|---:|---|---|---|
| 83 | 101 學年度烘焙職種學科正式試卷 Q33 | 派皮堅韌不酥的原因為 | (C) | 115-baking-c-print | 329 | 工作項目 03：產品製作 Q140 | 派皮堅韌不酥的原因為？ | (B) | 94.7% | possible-similarity | no | yes |
| 86 | 101 學年度烘焙職種學科正式試卷 Q36 | 製作天使蛋糕擬降低蛋白之韌性可增加 | (C) | 115-baking-c-print | 339 | 工作項目 03：產品製作 Q150 | 製作天使蛋糕擬降低蛋白之韌性可增加 | (C) | 100.0% | exact-question | no | yes |
| 87 | 101 學年度烘焙職種學科正式試卷 Q37 | 下列蛋糕配方中何者宜使用高筋麵粉? | (B) | 115-baking-c-print | 9 | 工作項目 01：產品分類 Q9 | 下列蛋糕配方中何者宜使用高筋麵粉？ | (B) | 96.8% | high-similarity | no | yes |
| 90 | 101 學年度烘焙職種學科正式試卷 Q40 | 蛋糕表面有白色斑點是因為 | (B) | 115-baking-c-print | 385 | 工作項目 04：品質鑑定 Q18 | 蛋糕表面有白色斑點是因為？ | (A) | 95.7% | high-similarity | no | yes |
| 239 | 104 學年度烘焙職種學科正式試卷 Q39 | 依據食品衛生管理法規定,烘焙油脂中合成抗氧化劑的總量不得超過 | (C) | 115-baking-c-print | 106 | 工作項目 02：原料之選用 Q76 | 食品衛生管理法規定烘焙油脂中合成抗氧化劑的總量不得超過 | (B) | 90.9% | possible-similarity | no | yes |
| 260 | 104 學年度烘焙職種學科模擬試卷 Q10 | 蛋糕在包裝時為延長保存時間常使用: | (D) | 115-baking-c-print | 422 | 工作項目 05：烘品食品之包裝 Q5 | 蛋糕在包裝時為延長保存時間常使用？ | (D) | 96.8% | high-similarity | no | no |
| 274 | 104 學年度烘焙職種學科模擬試卷 Q24 | 蛋糕表面有白色斑點是因為: | (A) | 115-baking-c-print | 385 | 工作項目 04：品質鑑定 Q18 | 蛋糕表面有白色斑點是因為？ | (A) | 95.7% | high-similarity | no | yes |
| 296 | 104 學年度烘焙職種學科模擬試卷 Q46 | 蘇打餅乾成品的pH值比一般奶油小西餅為: | (A) | 115-baking-c-print | 317 | 工作項目 03：產品製作 Q128 | 蘇打餅乾成品的 pH 值比一般奶油小西餅為？ | (A) | 97.3% | high-similarity | no | yes |
| 354 | 106學年度烘焙職種學科模擬試卷 Q4 | 派皮自模型中取出易破碎原因為: | (C) | 115-baking-c-print | 193 | 工作項目 03：產品製作 Q4 | 派皮自模型中取出易破碎原因為？ | (C) | 96.3% | high-similarity | no | yes |
| 358 | 106學年度烘焙職種學科模擬試卷 Q8 | 重奶油蛋糕油脂的最低使用量為: | (D) | 115-baking-c-print | 235 | 工作項目 03：產品製作 Q46 | 重奶油蛋糕油脂的最低使用量為？ | (D) | 96.3% | high-similarity | no | no |
| 359 | 106學年度烘焙職種學科模擬試卷 Q9 | 標準土司麵包配方內水的用量應為: | (C) | 115-baking-c-print | 237 | 工作項目 03：產品製作 Q48 | 標準土司麵包配方內水的用量應為 | (C) | 100.0% | exact-question | no | no |
| 360 | 106學年度烘焙職種學科模擬試卷 Q10 | 奶油空心餅成型後應該 | (A) | 115-baking-c-print | 247 | 工作項目 03：產品製作 Q58 | 奶油空心餅成型後應該？ | (A) | 94.7% | possible-similarity | no | yes |
| 362 | 106學年度烘焙職種學科模擬試卷 Q12 | 麵包製程中之醒麵即是 | (C) | 115-baking-c-print | 258 | 工作項目 03：產品製作 Q69 | 麵包製程中之醒麵即是？ | (C) | 94.7% | possible-similarity | no | yes |
| 363 | 106學年度烘焙職種學科模擬試卷 Q13 | 奶油空心餅成品內部缺乏空囊是因為 | (A) | 115-baking-c-print | 270 | 工作項目 03：產品製作 Q81 | 奶油空心餅成品內部缺乏空囊是因為？ | (A) | 96.8% | high-similarity | no | yes |
| 370 | 106學年度烘焙職種學科模擬試卷 Q20 | 烤焙甜麵包時,若烤焙時間相同烤爐溫度太低會造成 | (C) | 115-baking-c-print | 337 | 工作項目 03：產品製作 Q148 | 烤焙甜麵包時，若烤焙時間相同烤爐溫度太低會造成 | (C) | 90.9% | possible-similarity | no | yes |
| 371 | 106學年度烘焙職種學科模擬試卷 Q21 | 製作天使蛋糕擬降低蛋白之韌性可增加 | (C) | 115-baking-c-print | 339 | 工作項目 03：產品製作 Q150 | 製作天使蛋糕擬降低蛋白之韌性可增加 | (C) | 100.0% | exact-question | no | yes |
| 373 | 106學年度烘焙職種學科模擬試卷 Q23；106學年度烘焙職種學科正式試卷 Q34 | 土司麵包的表皮性質應該是 | (B) | 115-baking-c-print | 388 | 工作項目 04：品質鑑定 Q21 | 土司麵包的表皮性質應該是？ | (B) | 95.7% | high-similarity | no | yes |
| 374 | 106學年度烘焙職種學科模擬試卷 Q24 | 評定白土司麵包的口感應 | (A) | 115-baking-c-print | 400 | 工作項目 04：品質鑑定 Q33 | 評定白土司麵包的口感應？ | (A) | 95.2% | high-similarity | no | yes |
| 375 | 106學年度烘焙職種學科模擬試卷 Q25；106學年度烘焙職種學科正式試卷 Q36 | 天使蛋糕顏色潔白、組織細膩乃因配方中添加了 | (D) | 115-baking-c-print | 410 | 工作項目 04：品質鑑定 Q43 | 天使蛋糕顏色潔白、組織細膩乃因配方中添加了 | (D) | 100.0% | exact-question | no | no |
| 377 | 106學年度烘焙職種學科模擬試卷 Q27 | 下列何者不是麵包包裝的最主要目的? | (D) | 115-baking-c-print | 423 | 工作項目 05：烘品食品之包裝 Q6 | 下列何者不是麵包包裝的最主要目的？ | (D) | 96.8% | high-similarity | no | no |
| 379 | 106學年度烘焙職種學科模擬試卷 Q29 | 下列數種包裝材料燃燒時最易產生濃煙是 | (D) | 115-baking-c-print | 446 | 工作項目 05：烘品食品之包裝 Q29 | 下列數種包裝材料燃燒時最易產生濃煙是？ | (D) | 97.1% | high-similarity | no | no |
| 385 | 106學年度烘焙職種學科模擬試卷 Q35 | 麵包放置一段時間後會變硬是因為 | (B) | 115-baking-c-print | 491 | 工作項目 06：食品之貯存 Q37 | 麵包放置一段時間後會變硬是因為 | (B) | 100.0% | exact-question | no | yes |
| 386 | 106學年度烘焙職種學科模擬試卷 Q36 | 冷凍食品之保存溫度為: | (D) | 115-baking-c-print | 492 | 工作項目 06：食品之貯存 Q38 | 冷凍食品之保存溫度為？ | (D) | 94.7% | possible-similarity | no | no |
| 403 | 106學年度烘焙職種學科正式試卷 Q3 | 下列烘焙用原料較不常使用的是 | (D) | 115-baking-c-print | 46 | 工作項目 02：原料之選用 Q16 | 下列烘焙用原料較不常使用的是？ | (D) | 96.3% | high-similarity | no | no |
| 407 | 106學年度烘焙職種學科正式試卷 Q7 | 乳化劑在麵包中的功能是: | (D) | 115-baking-c-print | 76 | 工作項目 02：原料之選用 Q46 | 乳化劑在麵包中的功能？ | (B) | 90.0% | possible-similarity | no | yes |
| 416 | 106學年度烘焙職種學科正式試卷 Q16 | 下列何者不是造成小西餅膨大之原因? | (C) | 115-baking-c-print | 222 | 工作項目 03：產品製作 Q33 | 下列何者不是造成小西餅膨大之原因？ | (C) | 96.8% | high-similarity | no | yes |
| 417 | 106學年度烘焙職種學科正式試卷 Q17 | 戚風類蛋糕其膨大的最主要因素是 | (A) | 115-baking-c-print | 233 | 工作項目 03：產品製作 Q44 | 戚風類蛋糕其膨大的最主要因素是？ | (A) | 96.6% | high-similarity | no | yes |
| 420 | 106學年度烘焙職種學科正式試卷 Q20 | 海綿蛋糕攪拌有冷攪拌法和熱攪拌法,熱攪拌法是先將蛋加溫至 | (C) | 115-baking-c-print | 254 | 工作項目 03：產品製作 Q65 | 海綿蛋糕攪拌有冷攪拌法和熱攪拌法，熱攪拌法是先將蛋加溫至？ | (C) | 90.9% | possible-similarity | no | no |
| 429 | 106學年度烘焙職種學科正式試卷 Q29 | 蘇打餅乾成品的 pH 值比一般奶油小西餅為 | (A) | 115-baking-c-print | 317 | 工作項目 03：產品製作 Q128 | 蘇打餅乾成品的 pH 值比一般奶油小西餅為？ | (A) | 97.3% | high-similarity | no | yes |
| 434 | 106學年度烘焙職種學科正式試卷 Q35 | 烘焙產品底部有黑色斑點原因是 | (A) | 115-baking-c-print | 399 | 工作項目 04：品質鑑定 Q32 | 烘焙產品底部有黑色斑點原因是？ | (A) | 96.3% | high-similarity | no | yes |
| 450 | 107 學年度烘焙職種學科正式試題 Q3 | 雞蛋及其相關產品所引起的食物中毒，是由下列何種菌造成？ | (C) | 115-baking-c-print | 508 | 工作項目 06：食品之貯存 Q54 | 雞蛋及其相關產品所引起的食物中毒，是由下列何種菌造成？ | (C) | 100.0% | exact-question | no | yes |
| 452 | 107 學年度烘焙職種學科正式試題 Q5 | 依 CNS 之標準，葡萄乾麵包應含葡萄乾量不少於麵粉的 | (A) | 115-baking-c-print | 239 | 工作項目 03：產品製作 Q50 | 依 CNS 之標準，葡萄乾麵包應含葡萄乾量不少於麵粉的 | (A) | 100.0% | exact-question | no | no |
| 454 | 107 學年度烘焙職種學科正式試題 Q7 | 下列包裝材料何者耐熱性最佳？ | (D) | 115-baking-c-print | 453 | 工作項目 05：烘品食品之包裝 Q36 | 下列包裝材料何者耐熱性最佳？ | (D) | 100.0% | exact-question | no | no |
| 455 | 107 學年度烘焙職種學科正式試題 Q8 | 餅乾麵糰在壓延成型時須考慮收縮比的產品為 | (B) | 115-baking-c-print | 25 | 工作項目 01：產品分類 Q25 | 餅乾麵糰在壓延成型時須考慮收縮比的產品為？ | (B) | 97.4% | high-similarity | no | yes |
| 457 | 107 學年度烘焙職種學科正式試題 Q10 | 下列何種產品之麵糰，其配方中糖油含量最低？ | (C) | 115-baking-c-print | 18 | 工作項目 01：產品分類 Q18 | 下列何種產品之麵糰，其配方中糖油含量最低？ | (A) | 100.0% | exact-question | no | yes |
| 458 | 107 學年度烘焙職種學科正式試題 Q11 | 酸性食品與低酸性食品之 pH 界限為 | (B) | 115-baking-c-print | 465 | 工作項目 06：食品之貯存 Q11 | 酸性食品與低酸性食品之 pH 界限為？ | (B) | 96.8% | high-similarity | no | yes |
| 459 | 107 學年度烘焙職種學科正式試題 Q12 | 海綿蛋糕配方中各項材料百分比加起來得 180%，已知麵糊總量為 9 公斤，其麵粉的用量應為 | (D) | 115-baking-c-print | 255 | 工作項目 03：產品製作 Q66 | 海綿蛋糕配方中各項材料百分比加起來得 180 ％，已知麵糊總量為 9 公斤，其麵粉的用量應為 | (D) | 96.3% | high-similarity | no | no |
| 460 | 107 學年度烘焙職種學科正式試題 Q13 | 小西餅配方中糖的用量比油多、油的用量比水多，麵糰較乾硬，須擀平或用模型壓出的產品是 | (D) | 115-baking-c-print | 28 | 工作項目 01：產品分類 Q28 | 小西餅配方中糖的用量比油多、油的用量比水多，麵糰較乾硬，須擀平或用模型壓出的產品是？ | (D) | 98.8% | high-similarity | no | no |
| 462 | 107 學年度烘焙職種學科正式試題 Q15 | 奶油空心餅成型後應該 | (A) | 115-baking-c-print | 247 | 工作項目 03：產品製作 Q58 | 奶油空心餅成型後應該？ | (A) | 94.7% | possible-similarity | no | yes |
| 466 | 107 學年度烘焙職種學科正式試題 Q19 | 小麥之橫斷面呈粉質狀者為何？ | (B) | 115-baking-c-print | 141 | 工作項目 02：原料之選用 Q111 | 小麥之橫斷面呈粉質狀者為何？ | (D) | 100.0% | exact-question | no | no |
| 467 | 107 學年度烘焙職種學科正式試題 Q20 | 製作轉化糖漿時，以下列何種酸水解得到之品質最佳？ | (D) | 115-baking-c-print | 131 | 工作項目 02：原料之選用 Q101 | 製作轉化糖漿時，以下列何種酸水解得到之品質最佳？ | (D) | 100.0% | exact-question | no | no |
| 468 | 107 學年度烘焙職種學科正式試題 Q21 | 評定白土司麵包的口感應 | (B) | 115-baking-c-print | 400 | 工作項目 04：品質鑑定 Q33 | 評定白土司麵包的口感應？ | (A) | 95.2% | high-similarity | no | yes |
| 469 | 107 學年度烘焙職種學科正式試題 Q22 | 冷凍蛋解凍後最好 | (A) | 115-baking-c-print | 487 | 工作項目 06：食品之貯存 Q33 | 冷凍蛋解凍後最好 | (A) | 100.0% | exact-question | no | yes |
| 470 | 107 學年度烘焙職種學科正式試題 Q23 | 沒有分析檢驗的情況下，下列何者不是由外觀判斷油炸油的劣化？ | (D) | 115-baking-c-print | 48 | 工作項目 02：原料之選用 Q18 | 沒有分析檢驗的情況下，下列何者不是由外觀判斷油炸油的劣化？ | (D) | 100.0% | exact-question | no | no |
| 472 | 107 學年度烘焙職種學科正式試題 Q25 | 若用快速酵母粉取代新鮮酵母時，快速酵母粉的用量應為新鮮酵母的___倍 | (B) | 115-baking-c-print | 53 | 工作項目 02：原料之選用 Q23 | 若用快速酵母粉取代新鮮酵母時，快速酵母粉的用量應為新鮮酵母的？ | (B) | 92.1% | possible-similarity | no | yes |
| 473 | 107 學年度烘焙職種學科正式試題 Q26 | 冷凍食品之保存溫度為 | (D) | 115-baking-c-print | 492 | 工作項目 06：食品之貯存 Q38 | 冷凍食品之保存溫度為？ | (D) | 94.7% | possible-similarity | no | no |
| 476 | 107 學年度烘焙職種學科正式試題 Q29 | 土司麵包的表面顏色太淺可能是 | (D) | 115-baking-c-print | 394 | 工作項目 04：品質鑑定 Q27 | 土司麵包的表面顏色太淺可能是？ | (D) | 96.3% | high-similarity | no | no |
| 477 | 107 學年度烘焙職種學科正式試題 Q30 | 下列何種糖，酵母醱酵產生二氧化碳及酒精之速率最慢？ | (D) | 115-baking-c-print | 154 | 工作項目 02：原料之選用 Q124 | 下列何種糖，酵母發酵產生二氧化碳及酒精之速率最慢？ | (D) | 91.7% | possible-similarity | no | no |
| 478 | 107 學年度烘焙職種學科正式試題 Q31 | 下列何種原料不是製作奶油布丁派餡之凝凍原料？ | (D) | 115-baking-c-print | 56 | 工作項目 02：原料之選用 Q26 | 下列何種原料不是製作奶油布丁派餡之凝凍原料？ | (D) | 100.0% | exact-question | no | no |
| 480 | 107 學年度烘焙職種學科正式試題 Q33 | 蛋白經攪拌後最易與其他原料拌合且進爐後膨脹力最好的階段是 | (B) | 115-baking-c-print | 256 | 工作項目 03：產品製作 Q67 | 蛋白經攪拌後最易與其他原料拌合且進爐後膨脹力最好的階段是？ | (B) | 98.2% | high-similarity | no | no |
| 481 | 107 學年度烘焙職種學科正式試題 Q34 | 配方中採用高筋麵粉，比較適合製作下列何種產品？ | (A) | 115-baking-c-print | 15 | 工作項目 01：產品分類 Q15 | 配方中採用高筋麵粉，比較適合製作下列何種產品？ | (C) | 100.0% | exact-question | no | yes |
| 482 | 107 學年度烘焙職種學科正式試題 Q35 | 雙皮水果派切開時派餡部分應 | (C) | 115-baking-c-print | 401 | 工作項目 04：品質鑑定 Q34 | 雙皮水果派切開時派餡部分應？ | (C) | 96.0% | high-similarity | no | yes |
| 487 | 107 學年度烘焙職種學科正式試題 Q40 | 要烤出一個組織細緻的蒸烤布丁，烤爐溫度宜選用 | (B) | 115-baking-c-print | 198 | 工作項目 03：產品製作 Q9 | 要烤出一個組織細緻的蒸烤布丁，烤爐溫度宜選用？ | (B) | 97.7% | high-similarity | no | no |
| 489 | 107 學年度烘焙職種學科正式試題 Q42 | 製作大量手工丹麥小西餅，粉與糖油拌勻時應留意 | (C) | 115-baking-c-print | 199 | 工作項目 03：產品製作 Q10 | 製作大量手工丹麥小西餅，粉與糖油拌勻時應留意？ | (A) | 97.7% | high-similarity | no | yes |
| 490 | 107 學年度烘焙職種學科正式試題 Q43 | 蛋白不易打發的原因繁多，下列何者並非其因素？ | (A) | 115-baking-c-print | 414 | 工作項目 04：品質鑑定 Q47 | 蛋白不易打發的原因繁多，下列何者並非其因素？ | (A) | 100.0% | exact-question | no | yes |
| 491 | 107 學年度烘焙職種學科正式試題 Q44 | 低成分重奶油蛋糕，採用何種攪拌方法為宜？ | (B) | 115-baking-c-print | 299 | 工作項目 03：產品製作 Q110 | 低成分重奶油蛋糕，採用何種攪拌方法為宜？ | (B) | 100.0% | exact-question | no | yes |
| 492 | 107 學年度烘焙職種學科正式試題 Q45 | 布丁蛋糕呈頂部高隆、中央部分裂開、四周收縮表示製作中 | (C) | 115-baking-c-print | 415 | 工作項目 04：品質鑑定 Q48 | 布丁蛋糕呈頂部高隆、中央部分裂開、四週收縮表示製作中？ | (C) | 90.2% | possible-similarity | no | yes |
| 494 | 107 學年度烘焙職種學科正式試題 Q47 | 利用糖油拌合法製作丹麥小西餅 (Danish Cookies) ，材料中的麵粉應在最後加入，輕輕拌勻，其主要的原因為 | (C) | 115-baking-c-print | 304 | 工作項目 03：產品製作 Q115 | 利用糖油拌合法製作丹麥小西餅 (Danish cookies) ，材料中的麵粉應在最後加入，輕輕拌勻，其主要的原因為？ | (C) | 95.2% | high-similarity | no | yes |
| 495 | 107 學年度烘焙職種學科正式試題 Q48 | 葡萄乾麵包切片時，葡萄乾易從麵包內掉落的原因是 | (B) | 115-baking-c-print | 404 | 工作項目 04：品質鑑定 Q37 | 葡萄乾麵包切片時，葡萄乾易從麵包內掉落的原因是？ | (B) | 97.8% | high-similarity | no | yes |
| 496 | 107 學年度烘焙職種學科正式試題 Q49 | 做蘋果派餡的膠凍原料，通常採用 | (A) | 115-baking-c-print | 86 | 工作項目 02：原料之選用 Q56 | 做蘋果派餡的膠凍原料，通常採用？ | (A) | 96.6% | high-similarity | no | yes |
| 533 | 108 學年度烘焙職種學科正式試題 Q36 | 為改善海綿蛋糕組織之韌性，在製作時可加入適量 | (B) | 115-baking-c-print | 208 | 工作項目 03：產品製作 Q19 | 為改善海綿蛋糕組織之韌性，在製作時可加入適量 | (A) | 100.0% | exact-question | no | yes |
| 584 | 109 學年度烘焙職種學科正式試題 Q37 | 一般烘焙人員所稱的 「 重曹 」 (baking soda)是指 | (C) | 115-baking-c-print | 73 | 工作項目 02：原料之選用 Q43 | 一般烘焙人員所稱的「重曹」 (baking soda) 是指？ | (B) | 98.0% | high-similarity | no | yes |
| 614 | 110 學年度烘焙職種學科正式試題 Q17 | 餅乾麵糰在攪拌終了階段不須產生麵筋的產品是? | (A) | 115-baking-c-print | 24 | 工作項目 01：產品分類 Q24 | 餅乾麵糰在攪拌終了階段不須產生麵筋的產品是？ | (A) | 97.6% | high-similarity | no | yes |
| 627 | 110 學年度烘焙職種學科正式試題 Q30 | 麵包可使用的防腐劑為? | (A) | 115-baking-c-print | 88 | 工作項目 02：原料之選用 Q58 | 麵包可使用的防腐劑為？ | (A) | 94.7% | possible-similarity | no | yes |
| 629 | 110 學年度烘焙職種學科正式試題 Q32 | 小麥胚乳的主要色素為? | (A) | 115-baking-c-print | 120 | 工作項目 02：原料之選用 Q90 | 小麥胚乳的主要色素為？ | (D) | 94.7% | possible-similarity | no | no |
| 634 | 110 學年度烘焙職種學科正式試題 Q37 | 麵粉貯藏之理想濕度為? | (C) | 115-baking-c-print | 483 | 工作項目 06：食品之貯存 Q29 | 麵粉貯藏之理想濕度為？ | (C) | 94.7% | possible-similarity | no | no |
| 646 | 110 學年度烘焙職種學科正式試題 Q49 | 為改善麵粉中澱粉之膠體性質及改良麵包之內部組織,一般可加入? | (A) | 115-baking-c-print | 340 | 工作項目 03：產品製作 Q151 | 為改善麵粉中澱粉之膠體性質及改良麵包之內部組織，一般可加入？ | (D) | 91.2% | possible-similarity | no | no |
| 732 | 112 學年度烘焙職種學科正式試題 Q35 | 派皮堅韌不酥的原因為何? | (A) | 115-baking-c-print | 329 | 工作項目 03：產品製作 Q140 | 派皮堅韌不酥的原因為？ | (B) | 90.0% | possible-similarity | no | yes |

## Notes

- This report identifies reused, lightly edited, or reordered questions by text similarity.
- For a stricter list, filter `confidence = exact-question` and `same_option_set = yes`.
- For answer-equivalent matches, also filter `same_correct_text = yes`.
