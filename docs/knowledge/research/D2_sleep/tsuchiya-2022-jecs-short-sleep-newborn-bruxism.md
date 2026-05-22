---
title: "Prospective association of short sleep duration in newborns with bruxism behavior in children: The Japan Environment and Children's Study (JECS)"
authors: ["Masahiro Tsuchiya", "Shinobu Tsuchiya", "Haruki Momma", "Koh Mizuno", "Ryoichi Nagatomi", "Nobuo Yaegashi", "Takahiro Arima"]
year: 2022
doi: "10.1016/j.sleep.2022.07.018"
source: "Sleep Medicine"
source_url: "https://doi.org/10.1016/j.sleep.2022.07.018"
openaccess_pdf_url: null

domain: D2_sleep
sub_topics: ["jecs", "japan", "newborn_sleep_duration", "longitudinal_cohort", "bruxism", "early_life_sleep"]
target_age: ["0-2", "3-6"]
study_type: "prospective-cohort"
evidence_level: "moderate"
sample_size: 67923  # JECS本体は約10万妊娠だが本論文の解析対象児
sample_region: "日本全国（JECS 15地域、2011-2014 出生コホート）"

related_theories: ["[[bronfenbrenner-ecological]]", "[[harvard-cdc-framework]]"]
related_research: ["nakahara-2021-jecs-maternal-sleep-infant-development", "hayama-2007-japanese-4month-infant-night-waking", "chaput-2017-sleep-duration-health-indicators-early-years", "galland-2012-normal-sleep-patterns-infants-children"]
matcher_axes: ["short_sleep_japan", "newborn_sleep", "long_term_consequence"]
note_potential: high  # 日本最大コホートの新生児睡眠データを note 化できる

evidence_source: abstract_only
collected_via: openalex
collected_date: 2026-05-15
review_status: collected
ceo_note: "医療境界、CEO目視必須。JECS = 環境省主導の日本全国大規模出生コホート。新生児期睡眠と幼児期歯ぎしりの前向き関連という独自視点で、日本研究比率を一気に押し上げる重要論文。"

medical_caveat: true
clinical_advice_safe: false

counterevidence_to: []
has_counterevidence: []
critique_included: false
cultural_caveat: "日本全国コホート（JECS）のデータであり、日本文脈での外的妥当性は高い。ただし bruxism という臨床アウトカムの定義は親報告ベース、観察研究のため因果推論には注意。"

batch: PhaseC_sprint11
---

# 新生児期の短時間睡眠と小児期歯ぎしりの前向き関連：JECS

## 200-500字要約
本研究は、日本最大の出生コホート研究「子どもの健康と環境に関する全国調査（JECS）」のデータを用い、**新生児期（生後 1 ヶ月時点）の短時間睡眠が、幼児期の歯ぎしり（bruxism）行動と前向きに関連するか** を検討した観察研究です。JECS は環境省主導で 2011-2014 年に約 10 万妊娠を登録した日本初の全国規模出生コホートで、生後 1 ヶ月、6 ヶ月、1 歳、2 歳、3 歳と継続追跡しています。本研究では、新生児期に親報告で睡眠時間が短かった児（カットオフは論文内）と、3 歳・4 歳時点で歯ぎしり行動が観察された児の関連をロジスティック回帰で解析しました。結果、**新生児期に睡眠時間が短かった児は、その後の小児期に歯ぎしりを示すオッズが有意に高い** ことが示されました（オッズ比・信頼区間は論文内）。著者らは、新生児期の睡眠 - 覚醒制御の確立がその後の口腔・神経筋制御の発達と連動する可能性を示唆し、極めて早期の睡眠習慣支援の意義を提起しています。

## キーフィンディング（3-5項目）
- 知見1: 日本全国の JECS コホートにおいて、新生児期（生後 1 ヶ月）の短時間睡眠は小児期歯ぎしりと前向きに有意に関連した。
- 知見2: 大規模サンプル（数万人規模）と前向きデザインにより、新生児期睡眠の長期的影響を示した数少ない日本データである。
- 知見3: 共変量（出生体重、出産様式、母親の喫煙・年齢、世帯収入等）を調整後も関連は維持されたと報告されている。
- 知見4: 睡眠時間は親報告ベース、歯ぎしりも親観察ベースなので、客観的測定（actigraphy、ポリソムノグラフィ）とは異なる可能性。

## ひだまりこそだち への示唆（医療助言を避ける記述）
- **スタンス**: 日本の親に対し「赤ちゃんの睡眠時間は新生児期から大切」と説明できる、数少ない大規模日本データ。海外データに依存せず根拠を提示できる。
- マッチャーでの使い方: 「新生児の睡眠リズムが不安／よく起きる」マッチで、「日本の全国調査では新生児期の睡眠と後の口腔行動の関連が報告されている」と一次情報として参照。
- note 記事化のフック: 「JECS という日本全国 10 万人の研究では、新生児の睡眠時間が短いと数年後の歯ぎしりリスクが上がる可能性が報告されている」。
- 親への翻訳: 「研究では新生児期から睡眠リズムを整えることの長期的意義が示されています。ただし、これは個別診断ではなく集団レベルの傾向です」。

## 関連理論との関係
- [[bronfenbrenner-ecological]]: マイクロシステム（家庭の睡眠習慣）と児童発達のクロノシステム的（時間軸的）連関を示す典型例。
- [[harvard-cdc-framework]]: 「serve and return」以前の、生物学的サーカディアン基盤の早期確立の重要性を裏付ける。

## 留保・批判
- **個別判断は専門医に**: 個々の新生児の睡眠時間や歯ぎしりについては小児科・小児歯科に相談してください。
- 観察研究のため因果は確定できない。共変量で調整されているが残余交絡は否定できない。
- 親報告データであり、客観的測定とは乖離する可能性。
- bruxism は多因子性で、睡眠以外の要因（咬合、ストレス、神経発達特性）が重要な可能性。

## 出典
- Tsuchiya, M., Tsuchiya, S., Momma, H., Mizuno, K., Nagatomi, R., Yaegashi, N., & Arima, T. (2022). Prospective association of short sleep duration in newborns with bruxism behavior in children: The Japan Environment and Children's Study (JECS). *Sleep Medicine*, 100, 71-78. DOI: 10.1016/j.sleep.2022.07.018
- OpenAlex ID: W4289947805
- PMID: 36029753
