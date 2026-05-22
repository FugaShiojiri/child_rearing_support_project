---
title: "Sleep duration and incidence of obesity in infants, children, and adolescents: a systematic review and meta-analysis of prospective studies"
authors: ["Michelle A. Miller", "Marlot Kruisbrink", "Joanne Wallace", "Chen Ji", "Francesco P. Cappuccio"]
year: 2018
doi: "10.1093/sleep/zsy018"
source: "SLEEP"
source_url: "https://doi.org/10.1093/sleep/zsy018"
openaccess_pdf_url: "https://academic.oup.com/sleep/article-pdf/41/4/zsy018/24611450/zsy018.pdf"

domain: D2_sleep
sub_topics: ["sleep_duration", "obesity", "BMI", "longitudinal_meta_analysis", "physical_health"]
target_age: ["0-2", "3-4", "5-6", "school", "adolescent"]
study_type: "systematic-review-meta-analysis"
evidence_level: "high"
sample_size: 75499  # 42研究の合計対象者数（infancy 14738 + early childhood 31104 + middle childhood 3005 + adolescence 26652）
sample_region: "国際（前向きコホート研究42本のメタ分析）"

related_theories: ["[[harvard-cdc-framework]]", "[[executive-function]]"]
related_research: ["chaput-2017-sleep-duration-health-indicators-early-years", "janssen-2019-screen-time-sleep-under5s-meta-analysis"]
matcher_axes: ["sleep_duration", "obesity_risk", "child_health"]
note_potential: medium

evidence_source: abstract_only
collected_via: openalex
collected_date: 2026-05-14
review_status: collected
ceo_note: "医療境界、CEO目視必須。睡眠時間と肥満リスクの大規模メタ分析。『短い睡眠=肥満』と短絡せず、リスク要因の一つであることを丁寧に伝える。"

medical_caveat: true
clinical_advice_safe: false

counterevidence_to: []
has_counterevidence: []
critique_included: false
cultural_caveat: "メタ分析対象研究は欧米中心。日本人小児の睡眠時間は欧米より短い傾向が他研究で示されており、相対リスクの絶対量は文化圏で異なる可能性。"

batch: PhaseA_D2
---

# 乳幼児・小児・思春期における睡眠時間と肥満発症の系統的レビューおよびメタ分析

## 200-500字要約
本論文は、生後 0 歳から思春期までの睡眠時間と肥満発症の前向き関連を、42 本の前向きコホート研究（追跡期間 ≥1 年）のメタ分析として統合したものです。研究では、年齢区分別に短時間睡眠と肥満／過体重リスクの関連が解析され、**乳児期（infancy）で相対リスク 1.40（95% CI 1.19-1.65）、幼児期（early childhood）で 1.57（1.40-1.76）、学童期（middle childhood）で 2.23（2.18-2.27）、思春期で 1.30（1.11-1.53）** と、いずれの年齢区分でも短時間睡眠が肥満リスクと有意に関連することが報告されました。また、睡眠時間 1 時間あたりの BMI z スコア変化は -0.03（-0.04 から -0.01）、BMI 換算で -0.03 kg/m²（同様の幅）と、量反応関係も観察されました。著者らは、睡眠時間は乳児期から思春期まで肥満リスクの独立した因子・マーカーとなる可能性があり、公衆衛生上の介入対象として注目されると結論しています。

## キーフィンディング（3-5項目）
- 知見1: 42 本の前向き研究（合計約 75,499 人）のメタ分析。
- 知見2: 短時間睡眠は全年齢区分で肥満リスクと有意に関連（RR 1.30-2.23）。
- 知見3: 学童期で関連が最も強く（RR 2.23）、乳児期から思春期まで一貫した方向性。
- 知見4: 睡眠時間 1 時間あたり BMI z スコア -0.03、BMI -0.03 kg/m² の量反応関係。
- 知見5: 著者らは睡眠時間を「肥満リスク因子もしくはマーカー」として公衆衛生介入の対象に位置づける。

## ひだまりこそだち への示唆（医療助言を避ける記述）
- **スタンス**: 「子どもの睡眠時間と健康」を扱う際の量的根拠。ただし「短い睡眠 → 肥満」と短絡せず、睡眠は複数のリスク因子の一つであることを丁寧に伝える。
- マッチャーでの使い方: 「寝る時間が遅くて心配」マッチで、睡眠時間と健康指標の量反応関係を提示するクッションに使う。CEO 目視前提、`clinical_advice_safe: false`。
- note 記事化のフック: 「子どもの睡眠時間と健康──大規模研究が見たもの」。Galland 2012（参照値）と本論文（健康関連）を組み合わせた記事。
- 親への翻訳: 「研究では、子どもの睡眠時間が短いことと将来の肥満リスクには弱から中程度の関連が報告されています。ただし睡眠は数あるリスク因子の一つで、『何時間以上寝れば安全』という閾値があるわけではなく、家庭全体の生活リズムや食事・運動と合わせて考えることが大切です」。

## 関連理論との関係
- [[harvard-cdc-framework]]: 安定した睡眠は serve-and-return と発達基盤を支える健康指標として位置づけられる。
- [[executive-function]]: 睡眠不足は実行機能低下と関連することが他研究で報告されており、肥満と並ぶアウトカムの一つ。

## 留保・批判
- **個別判断は専門医に**: 個別の肥満・睡眠障害・成長遅延が懸念される場合は小児科医による評価が必要です。
- 観察研究の限界: メタ分析対象は前向きコホートで、ランダム化試験ではない。逆因果（肥満傾向の児は睡眠が短い）を完全に排除できない。
- サンプル限界: 欧米サンプル中心で、日本を含む東アジア圏のデータは少なめ。
- 量反応関係の臨床的意義: 睡眠 1 時間あたり BMI z スコア -0.03 は統計的に有意だが、個別判断の閾値設定には別途検討が必要。

## 出典
- Miller, M. A., Kruisbrink, M., Wallace, J., Ji, C., & Cappuccio, F. P. (2018). Sleep duration and incidence of obesity in infants, children, and adolescents: a systematic review and meta-analysis of prospective studies. *SLEEP*, 41(4), zsy018. DOI: 10.1093/sleep/zsy018
- OpenAlex ID: W2785146914
