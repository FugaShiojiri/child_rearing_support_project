---
title: "Screen Time at Age 1 Year and Communication and Problem-Solving Developmental Delay at 2 and 4 Years"
authors: ["Ippei Takahashi", "Taku Obara", "Mami Ishikuro", "Keiko Murakami", "Fumihiko Ueno", "Aoi Noda", "Genki Shinoda", "Tomomi Onuma", "Hisashi Kuribayashi", "Nobuo Yaegashi", "Shinichi Kuriyama"]
year: 2023
doi: "10.1001/jamapediatrics.2023.3057"
source: "JAMA Pediatrics"
source_url: "https://doi.org/10.1001/jamapediatrics.2023.3057"
openaccess_pdf_url: "https://jamanetwork.com/journals/jamapediatrics/articlepdf/2808593/jamapediatrics_takahashi_2023_oi_230047_1692626801.80966.pdf"

domain: D9_digital
sub_topics: ["screen_time", "developmental_delay", "Japanese_study", "TMM_birthree", "ASQ", "communication_delay", "problem_solving_delay", "dose_response"]
target_age: ["0-1", "1-3", "3-6"]
study_type: "longitudinal_cohort"
evidence_level: "high"
sample_size: 7097  # 母子ペア（東北メディカル・メガバンク）
sample_region: "日本（東北メディカル・メガバンク機構Birthree、宮城県中心）"

related_theories: ["[[harvard-cdc-framework]]", "[[executive-function]]", "[[sasaki-masami]]"]
related_research: ["[[research/D9_digital/madigan-2019-screen-time-developmental-screening]]", "[[research/D4_cognitive/kushima-2022-jecs-screen-time-autism]]", "[[research/D1_voice/madigan-2020-screen-language]]"]
matcher_axes: ["japan_screen_time", "1_year_screen_exposure", "developmental_delay_dose_response", "japan_evidence"]
note_potential: "very_high"

evidence_source: "abstract_only"
collected_via: "openalex"
collected_date: 2026-05-14
review_status: "collected"
ceo_note: "日本のTMM（東北メディカル・メガバンク）Birthreeコホート研究（JAMA Pediatrics、被引用91）。**1歳時のスクリーンタイム** と **2歳・4歳時の発達遅滞** の用量反応関係を日本で検証した重要論文。日本の家庭環境を反映した稀少な大規模縦断研究。Madigan 2019カナダ研究との対比に最適"
batch: PhaseC_sprint6

counterevidence_to: ["『日本の家庭環境ではスクリーンの影響は欧米と異なる』論", "『1歳時のスクリーンは2歳以降の発達と無関係』論"]
has_counterevidence: ["Orben & Przybylski 2019は『効果量は小さい』との反証", "観察研究で因果は確定しない"]
critique_included: true
cultural_caveat: "宮城県中心の日本人サンプル、東北震災後コホート。都市部の保育園利用児や祖父母同居家庭との差異は別途検証必要"
---

# 1歳時スクリーンタイムと2-4歳発達遅滞：日本TMM Birthreeコホート（Takahashi et al., 2023）

## 200-500字要約
**東北メディカル・メガバンク機構（TMM）三世代コホート（Birthree）** のデータを用いた、**日本で最大規模の縦断研究** の一つ（*JAMA Pediatrics*、被引用91）。N=7,097母子ペア。

**研究設計**: 
- **1歳時** にスクリーンタイム（TV・DVD・ゲーム・スマホ/タブレット）を親質問紙で測定
- **2歳時・4歳時** にASQ-3（Ages and Stages Questionnaire）日本語版で発達遅滞（コミュニケーション、粗大運動、微細運動、問題解決、対人）を評価

**主要発見**:
- 1歳時スクリーン1時間/日未満を基準として、用量依存的に発達遅滞リスクが上昇
- **1-2時間/日**: コミュニケーション遅滞OR=1.61、問題解決遅滞OR=1.46（2歳時）
- **2-4時間/日**: コミュニケーション遅滞OR=2.10、問題解決遅滞OR=1.61
- **4時間以上/日**: コミュニケーション遅滞OR=4.78（4歳時でも持続: OR=2.68）
- 効果は **コミュニケーション・問題解決** で顕著、粗大運動・微細運動・対人スキルへの影響は弱い
- 4歳時点でも持続する用量反応関係

**統制変数**: 母年齢、教育、世帯所得、産後うつ、配偶者状況、母乳/混合栄養、第一子か等を統制してもなお有意。

**日本サンプルの含意**: 添い寝率・家族同居率・保育園利用率が欧米と異なる日本でも、スクリーンタイムと発達遅滞の関連が確認された。

著者の解釈: 「**スクリーンタイムそのものが直接的に発達を阻害するというより、親子相互作用・対話・遊び時間の置き換え** が経路として有力」。

## キーフィンディング（3-5項目）
- 1歳時スクリーンタイムは2歳・4歳の **コミュニケーション・問題解決** 発達遅滞と用量依存的に関連
- 1日4時間以上で2歳時コミュニケーション遅滞リスクが **約5倍**
- 効果は4歳まで持続（OR=2.68）
- **日本サンプル** で確認された稀少な大規模エビデンス
- 経路は「親子相互作用の置き換え」が有力（直接効果ではない）

## ひだまりこそだち への示唆
- マッチャーでの使い方: 「1歳に動画を見せていいの？日本では？」相談 → 「**日本のTMM研究で、1歳時1時間以上のスクリーンが2-4歳の言語・問題解決発達遅滞リスクを上げる。完全禁止より代わりの遊び時間を確保**」
- note記事化のフック: 「日本7,000組の縦断研究：1歳の動画視聴が4歳まで影響？」「『1日何時間なら大丈夫』日本データの答え」
- 親への翻訳: 「**1歳までは特にスクリーン少なめ、その分の時間を対話・絵本・遊びに**。完全ゼロは目指さず、1時間以下を目安に」
- サービス設計示唆: **日本の親に直接当てはまるエビデンス** として強力。年齢別「代わりの活動メニュー」を提供。Madigan 2019カナダ研究と並列提示で説得力強化

## 関連理論との関係
- [[harvard-cdc-framework]]: Serve & Returnの機会が削られる現象の日本での実証
- [[executive-function]]: 問題解決能力（EFの一部）への用量依存的影響
- [[sasaki-masami]]: 「待つ・信じる・応える」の時間がスクリーンに奪われる現代的現象

## 留保・批判
- 観察研究のため **因果関係は未確定**（残存交絡：親の関わり方の質、SES、地域差等）
- スクリーンタイム測定は **親の自己報告** で測定誤差大
- スクリーン **内容・文脈・共視聴** を区別していない（量のみ）
- 宮城県中心、東北震災後コホートで、都市部・南日本との一般化に限界
- 効果量はORで示されるが、絶対リスク差は中程度（社会的影響を過大視しない）
- Orben & Przybylski派からは「効果量は些細」との立場あり
- 「親の罪悪感を煽る」研究としても作用しうる — 伝え方が重要

## 出典
- Takahashi, I., Obara, T., Ishikuro, M., Murakami, K., Ueno, F., Noda, A., Onuma, T., Shinoda, G., Orui, M., Iwama, N., Sugawara, J., Kuribayashi, H., Yaegashi, N., & Kuriyama, S. (2023). Screen Time at Age 1 Year and Communication and Problem-Solving Developmental Delay at 2 and 4 Years. *JAMA Pediatrics*, 177(10), 1039-1046.
- DOI: 10.1001/jamapediatrics.2023.3057
- 引用数: 91（2026年5月時点、近年論文ながら急速に引用増）
