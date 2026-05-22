---
title: "Increases in Depressive Symptoms, Suicide-Related Outcomes, and Suicide Rates Among U.S. Adolescents After 2010 and Links to Increased New Media Screen Time"
authors: ["Jean M. Twenge", "Thomas E. Joiner", "Megan L. Rogers", "Gabrielle N. Martin"]
year: 2017
doi: "10.1177/2167702617723376"
source: "Clinical Psychological Science"
source_url: "https://doi.org/10.1177/2167702617723376"
openaccess_pdf_url: "https://journals.sagepub.com/doi/10.1177/2167702617723376"

domain: D9_digital
sub_topics: ["adolescent_depression", "suicide", "smartphone_use", "social_media", "generational_trend", "screen_time_dose_response"]
target_age: ["6+"]
study_type: "cross_sectional_national_survey"
evidence_level: "moderate"
sample_size: 506820  # 米国全国調査3つの統合
sample_region: "米国（Monitoring the Future, YRBSS, NSDUH）"

related_theories: ["[[harvard-cdc-framework]]", "[[bowlby-attachment]]"]
related_research: ["[[research/D9_digital/orben-przybylski-2019-adolescent-wellbeing]]", "[[research/D9_digital/aap-chassiakos-2016-children-adolescents-digital-media]]", "[[research/D2_sleep/carter-2016-portable-screen-devices-sleep-meta-analysis]]"]
matcher_axes: ["adolescent_mental_health", "smartphone_depression", "social_media_risk", "generational_trends"]
note_potential: "high"

evidence_source: "abstract_only"
collected_via: "openalex"
collected_date: 2026-05-14
review_status: "collected"
ceo_note: "Twenge（『iGen』著者）の代表論文。スマホ普及（2010年以降）と米国青少年のメンタル悪化を結びつけた最影響論文（被引用1,634）。後にOrben & Przybylski 2019で『効果量は些細』と反証されたが、社会的議論を引き起こした重要文献。両論併記必須"
batch: PhaseC_sprint6

counterevidence_to: ["『スマホ普及と若者のメンタル悪化は無関係』論", "『SNSは中立的なツール』論"]
has_counterevidence: ["**Orben & Przybylski 2019**は『効果量はジャガイモを食べることと同程度に些細』と反証", "Etchells 2016は『デジタル悲観論』を批判"]
critique_included: true
cultural_caveat: "米国データのみ。日本の青少年（LINE中心、TikTok・Instagram比較的後発）への適用は要検証"
---

# 2010年以降の米国青少年の抑うつ・自殺増加とスクリーンタイム（Twenge et al., 2017）

## 200-500字要約
San Diego州立大学のJean Twenge（『iGen』『Generations』著者）による、**米国青少年のメンタルヘルス悪化とスマホ普及の関連** を示した代表論文（*Clinical Psychological Science*、被引用1,634）。

**3つの米国全国調査**（Monitoring the Future、YRBSS、NSDUH）から **計約50万人** の青少年データを統合分析。

**主要発見**:
- **2010年以降**、米国13-18歳の抑うつ症状・自殺念慮・自殺率が急増（2010年がスマホ所有率50%超のターニングポイント）
- **新メディアスクリーンタイム（SNS・スマホ・ゲーム）** が多い青少年ほど抑うつ・自殺関連アウトカムが高い
- **非スクリーン活動**（対面交流・運動・宗教活動・宿題）が多い青少年ほどメンタルが良好
- 1日 **3時間以上** の電子機器使用で自殺リスク要因が約35%増（OR ≈ 1.35）
- **女子・10代後半** で効果が強い
- 経済要因・テスト成績変化では説明できない

著者の結論: 「**スマホ・SNSの普及が現代青少年メンタル危機の主要因の一つ**」。AAPガイドラインに準じた使用制限を強く推奨。

ただし観察研究で **因果は確定しない**。後にOrben & Przybylski 2019が同データを再分析し「**効果量はジャガイモを食べる頻度と同程度に些細**」と反証、激しい論争を呼んだ。

## キーフィンディング（3-5項目）
- 2010年以降、米国青少年の抑うつ・自殺関連アウトカムが急増（スマホ普及と同時期）
- 1日3時間以上の電子機器使用で自殺リスク要因が35%増
- **女子・10代後半** で影響が顕著
- 対面交流・運動・宗教活動など **非スクリーン活動** はメンタル保護的
- 経済要因・学業ストレス変化では説明困難

## ひだまりこそだち への示唆
- マッチャーでの使い方: 「思春期の子のスマホ使用が心配」相談 → 「**Twengeの研究は『スマホ普及と青少年メンタル悪化の同時期性』を示すが、Orben らの反証もあり因果は議論中。ただし対面交流・運動を保つことの保護効果は確実**」
- note記事化のフック: 「スマホ世代（iGen）のメンタル危機：因果か相関か」「思春期の子のスマホとの距離感、研究はこう言う」
- 親への翻訳: 「**スマホ使用そのものより、対面交流・運動・睡眠が削られることが本質。完全禁止より置き換え活動を提案**」
- サービス設計示唆: 思春期前後の親向けに **両論併記コンテンツ**（Twenge派 vs Orben派）。「3時間ルール」は参考目安として提示

## 関連理論との関係
- [[harvard-cdc-framework]]: 思春期も Serve & Return（対話・接触）が必要、SNSはこれを置き換えない
- [[bowlby-attachment]]: 思春期のアタッチメント対象（同輩・親）への影響経路

## 留保・批判
- **最大の批判**: Orben & Przybylski 2019 が同データを再分析し、効果量r ≈ -0.03〜-0.05 と **極めて些細** であることを示した
- 観察研究で逆因果（メンタル悪化 → スクリーン増加）排除できない
- 「2010年以降の増加」は他要因（リーマンショック後の経済不安、政治極化、薬物依存等）でも説明可能
- 米国データのみで日本・東アジアへの適用は要慎重
- Twenge自身が「スマホ悪影響論」のスポークスパーソンで、選択的引用バイアスの指摘あり
- 「3時間閾値」は事後分析で恣意的に決められた可能性

## 出典
- Twenge, J. M., Joiner, T. E., Rogers, M. L., & Martin, G. N. (2018). Increases in Depressive Symptoms, Suicide-Related Outcomes, and Suicide Rates Among U.S. Adolescents After 2010 and Links to Increased New Media Screen Time. *Clinical Psychological Science*, 6(1), 3-17.
- DOI: 10.1177/2167702617723376
- 引用数: 1,634（2026年5月時点）
