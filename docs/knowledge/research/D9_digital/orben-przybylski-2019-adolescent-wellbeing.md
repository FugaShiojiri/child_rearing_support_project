---
title: "The association between adolescent well-being and digital technology use"
authors: ["Amy Orben", "Andrew K. Przybylski"]
year: 2019
doi: "10.1038/s41562-018-0506-1"
source: "Nature Human Behaviour"
source_url: "https://doi.org/10.1038/s41562-018-0506-1"
openaccess_pdf_url: "https://www.nature.com/articles/s41562-018-0506-1"

domain: D9_digital
sub_topics: ["digital_technology", "adolescent_wellbeing", "effect_size", "specification_curve_analysis", "researcher_degrees_of_freedom", "counter_evidence"]
target_age: ["6+"]
study_type: "specification_curve_analysis"
evidence_level: "high"
sample_size: 355358  # 3つの大規模代表性データセット
sample_region: "米国・英国（YRBS, MTF, MCS）"

related_theories: ["[[harvard-cdc-framework]]"]
related_research: ["[[research/D9_digital/twenge-2017-depression-suicide-screen-time]]", "[[research/D9_digital/aap-chassiakos-2016-children-adolescents-digital-media]]"]
matcher_axes: ["screen_time_effect_size", "adolescent_wellbeing", "research_methodology", "counter_evidence"]
note_potential: "very_high"

evidence_source: "abstract_only"
collected_via: "openalex"
collected_date: 2026-05-14
review_status: "collected"
ceo_note: "Orben & Przybylski（Oxford）の代表反証論文（Nature Human Behaviour、被引用1,381）。Twenge 2017と同じデータを **specification curve analysis** で再分析し、『効果量はジャガイモを食べることと同程度に些細』と結論。デジタル悲観論への科学的カウンターパンチ。両論併記の中核文献"
batch: PhaseC_sprint6

counterevidence_to: ["『スクリーンタイムが青少年メンタルを悪化させる』論", "Twenge 2017の強い主張", "AAP 2016の厳格な時間制限根拠"]
has_counterevidence: ["Twenge 2017は『スマホ普及と青少年メンタル悪化』を強調", "Lin 2016 等の小規模研究は強い悪影響を示す"]
critique_included: true
cultural_caveat: "米国・英国データ。日本ではTikTok普及が後発のため、最新動向を反映しない部分あり。ただし方法論的批判は普遍的に妥当"
---

# 青少年の主観的幸福度とデジタル技術使用の関連：効果量は些細（Orben & Przybylski, 2019）

## 200-500字要約
Oxford大学のAmy Orben & Andrew Przybylskiによる、**デジタルスクリーンタイムと青少年メンタルヘルスの関連の効果量** を厳密に検証した重要論文（*Nature Human Behaviour*、被引用1,381）。

**Twenge 2017 が用いた3つの大規模データセット（YRBS、MTF、MCS）計約35万人** を、**specification curve analysis** という新手法で再分析。この手法では、研究者の自由度（変数選択・統制変数・分析モデル）を全て探索し、可能なすべての組み合わせの効果量を提示する。

**主要発見**:
- スクリーンタイムと青少年wellbeingの **負の関連** は確かに存在するが、効果量は **r ≈ -0.035〜-0.05**（非常に小さい）
- この効果量は「**ジャガイモを食べる頻度（r=-0.034）**」「眼鏡をかけること（r=-0.035）」と同程度
- **朝食を抜くこと（r=-0.044）、いじめ被害（r=-0.187）** などの方がはるかに大きな負の効果
- 研究者の分析選択次第で効果量が大きく変動（researcher degrees of freedom問題）
- Twenge 2017の「3時間閾値」「強い因果主張」は **過大解釈** と批判

**結論**: 「**デジタル技術が青少年メンタルを破壊している**」という一般的言説は科学的に支持されない。スクリーンタイムは青少年wellbeingの **0.4%以下** しか説明しない。**親の関わり・睡眠・いじめ・SES** の方がはるかに重要な要因。

**方法論的革新**: specification curve analysisは「p-hacking」「cherry-picking」を防ぐ手法として広く採用されるようになった。

## キーフィンディング（3-5項目）
- スクリーンタイムと青少年wellbeingの関連は **存在するが効果量は些細**（r ≈ -0.04）
- 「ジャガイモを食べる頻度」や「眼鏡をかけること」と同程度の効果
- **いじめ被害・睡眠不足・朝食欠食** の方がはるかに大きな悪影響
- スクリーンタイムは青少年wellbeingの分散の **0.4%未満** しか説明しない
- specification curve analysisで研究者の恣意的選択を排除すると効果は縮小

## ひだまりこそだち への示唆
- マッチャーでの使い方: 「『スマホで子のメンタルが壊れる』というニュースが不安」相談 → 「**最新の厳密研究では効果量は些細、ジャガイモを食べる頻度と同程度。いじめ・睡眠・親子関係の方がはるかに重要**」
- note記事化のフック: 「『スマホが子のメンタルを壊す』は本当か：Oxfordの再分析が示す驚き」「効果量を正しく読むと見える世界」
- 親への翻訳: 「**スクリーンタイムへの過度な不安は無用、本当に大事なのは睡眠・いじめ対策・対話**。スマホは諸要因のひとつに過ぎない」
- サービス設計示唆: 親の罪悪感を煽る「スクリーン警鐘コンテンツ」を控え、**睡眠・対話・運動など本当に効く要因にフォーカス** したコンテンツを優先

## 関連理論との関係
- [[harvard-cdc-framework]]: Serve & Returnの質・量の方がスクリーンタイムより重要、と整合

## 留保・批判
- **観察研究の限界は同じ**（因果関係未確定）
- 「**平均的効果量**」を見ており、特定のサブグループ（既に脆弱な子・依存傾向）への強い影響は埋もれる可能性
- スクリーンタイムの **量のみ** で内容・文脈を区別していない（質の悪い使い方が混ざる）
- Twenge派からの再反論あり: 「2010年以降の縦断的変化を捉えきれていない」
- 「効果量小=対策不要」ではなく、**人口レベルでは小さくても個別ケアは別** の議論

## 出典
- Orben, A., & Przybylski, A. K. (2019). The association between adolescent well-being and digital technology use. *Nature Human Behaviour*, 3(2), 173-182.
- DOI: 10.1038/s41562-018-0506-1
- 引用数: 1,381（2026年5月時点）
