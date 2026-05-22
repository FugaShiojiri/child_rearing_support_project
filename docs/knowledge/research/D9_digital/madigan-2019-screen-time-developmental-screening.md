---
title: "Association Between Screen Time and Children's Performance on a Developmental Screening Test"
authors: ["Sheri Madigan", "Dillon T. Browne", "Nicole Racine", "Camille Mori", "Suzanne Tough"]
year: 2019
doi: "10.1001/jamapediatrics.2018.5056"
source: "JAMA Pediatrics"
source_url: "https://doi.org/10.1001/jamapediatrics.2018.5056"
openaccess_pdf_url: "https://jamanetwork.com/journals/jamapediatrics/articlepdf/2722666/jamapediatrics_madigan_2019_oi_180091.pdf"

domain: D9_digital
sub_topics: ["screen_time", "developmental_delay", "cognitive_development", "ASQ", "longitudinal_study", "directionality"]
target_age: ["1-3", "3-6"]
study_type: "longitudinal_cohort"
evidence_level: "high"
sample_size: 2441  # 母子ペア
sample_region: "カナダ（All Our Familiesコホート、カルガリー）"

related_theories: ["[[harvard-cdc-framework]]", "[[executive-function]]", "[[montessori]]"]
related_research: ["[[research/D1_voice/madigan-2020-screen-language]]", "[[research/D9_digital/takahashi-2023-jecs-screen-time-developmental-delay]]", "[[research/D4_cognitive/kushima-2022-jecs-screen-time-autism]]"]
matcher_axes: ["screen_time_24_36_60_months", "developmental_delay", "ASQ_screening", "longitudinal_evidence"]
note_potential: "very_high"

evidence_source: "abstract_only"
collected_via: "openalex"
collected_date: 2026-05-14
review_status: "collected"
ceo_note: "JAMA Pediatrics掲載のカナダ縦断研究（被引用681）。スクリーンタイムと発達遅滞の **時間的方向性** を示した稀少な縦断研究 — スクリーン → 発達遅滞 の方向は有意、逆向きは有意でない。因果関係への重要な示唆"
batch: PhaseC_sprint6

counterevidence_to: ["『発達遅滞の子がスクリーンを多用するだけで、スクリーン自体は害ではない』論", "『短期影響と長期影響は同じ』論"]
has_counterevidence: ["Orben & Przybylski 2019は『スクリーンと心理的wellbeingの関連は微弱』との反証"]
critique_included: true
cultural_caveat: "カナダ・カルガリーの中産階級主体サンプル。日本の生活様式（保育園利用率・添い寝率・通勤時スマホ使用等）とは異なる"
---

# 24-36-60か月時のスクリーンタイムと発達指標：縦断研究（Madigan et al., 2019）

## 200-500字要約
カナダ・カルガリーの **All Our Families** コホート研究の縦断データ（N=2,441母子ペア）を用い、**スクリーンタイムと幼児の発達指標** の関係を縦断的に検証した重要研究（JAMA Pediatrics、被引用681）。

**24, 36, 60か月時点** にスクリーンタイム（親報告、1日の平均時間）と **ASQ-3（Ages and Stages Questionnaire）** で発達指標（コミュニケーション、粗大運動、微細運動、問題解決、対人）を測定。

**結果**:
- 24か月時のスクリーンタイム → 36か月時のASQ低下（β = -0.08, p<.001）
- 36か月時のスクリーンタイム → 60か月時のASQ低下（β = -0.06, p<.001）
- **逆方向（発達遅滞 → 後のスクリーン増加）は有意でない**

**スクリーンタイムが発達遅滞の前駆指標** という時間的方向性を示した稀少な縦断研究。「スクリーンを多用する子はもともと発達が遅い」という逆因果説を弱める。

24か月児のスクリーン中央値は **2.4時間/日**（AAP推奨を大幅に上回る）。36か月児は **3.6時間/日**。

ただし観察研究で **絶対的な因果関係は確定しない**（残存交絡：親の関わり方・SES等）。サンプルもカナダ中産階級偏重。著者らも「**スクリーン使用そのものより、置き換えられる活動（読書・対話・遊び）の喪失** が問題」と示唆。

## キーフィンディング（3-5項目）
- 24-60か月の縦断データで、スクリーンタイム → 発達指標低下の **時間的方向性** を確認
- 逆方向（発達遅滞 → スクリーン増加）は有意でなく、逆因果説を部分的に反証
- カナダの実態として、24か月児で **1日2.4時間** （AAP推奨1時間を大幅超過）
- 影響領域: コミュニケーション・微細運動・問題解決で特に顕著
- 「**置き換えられる活動の喪失**」仮説：読書・対話・身体遊びの時間が削られることが本質か

## ひだまりこそだち への示唆
- マッチャーでの使い方: 「2-5歳のスクリーンタイムは本当に発達に影響する？」相談 → 「**カナダ2,441組の縦断研究では、スクリーン → 発達遅滞の方向に有意な関連。ただし因果ではなく、対話・遊びの時間が削られることが本質**」
- note記事化のフック: 「スクリーン2時間で本当に発達は遅れるのか：縦断研究の答え」「『見せている時間』より『見せていない時間に何をするか』」
- 親への翻訳: 「**スクリーンを減らすことより、減らした時間に対話・読書・遊びを足すこと** が大事」
- サービス設計示唆: スクリーンを減らすだけの罪悪感ベースの介入ではなく、「**代わりの活動メニュー**」を提供することが効果的

## 関連理論との関係
- [[harvard-cdc-framework]]: Serve & Return の機会が削られることが本質的悪影響
- [[executive-function]]: スクリーンによる受動消費はEF鍛錬を阻害
- [[montessori]]: 実物体験・自発的活動の重要性と整合

## 留保・批判
- 観察研究で因果関係は確定しない（残存交絡：親の関わり方の質・SES・親メンタル等）
- 効果量は **小から中**（β≈-0.06〜-0.08）、臨床的意義は限定的という解釈も可能
- ASQ-3は親報告のスクリーニングで、専門評価ではない
- カナダ中産階級コホートで一般化に限界
- スクリーンの **内容・文脈・共視聴** の質を区別していない（量のみ）
- Orben & Przybylski 2019などは「効果量は些細」との反証

## 出典
- Madigan, S., Browne, D., Racine, N., Mori, C., & Tough, S. (2019). Association Between Screen Time and Children's Performance on a Developmental Screening Test. *JAMA Pediatrics*, 173(3), 244-250.
- DOI: 10.1001/jamapediatrics.2018.5056
- 引用数: 681（2026年5月時点）
