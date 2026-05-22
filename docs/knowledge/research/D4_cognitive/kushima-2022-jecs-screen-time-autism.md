---
title: "Association Between Screen Time Exposure in Children at 1 Year of Age and Autism Spectrum Disorder at 3 Years of Age in the Japan Environment and Children's Study"
authors: ["Megumi Kushima", "Reiji Kojima", "Ryoji Shinohara", "Sayaka Horiuchi", "Sanae Otawa", "Tadao Ooka", "Yuka Akiyama", "Kunio Miyake", "Hiroshi Yokomichi", "Zentaro Yamagata"]
year: 2022
doi: "10.1001/jamapediatrics.2021.5778"
source: "JAMA Pediatrics"
source_url: "https://doi.org/10.1001/jamapediatrics.2021.5778"
openaccess_pdf_url: "https://jamanetwork.com/journals/jamapediatrics/articlepdf/2788488/jamapediatrics_kushima_2022_oi_210088_1648672925.06731.pdf"

domain: D4_cognitive
sub_topics: ["JECS", "screen_time", "autism_spectrum_disorder", "Japan_birth_cohort", "1_year_old", "boys_girls_difference"]
target_age: ["0-1", "3-4"]
study_type: "longitudinal_birth_cohort"
evidence_level: "high"  # N=84,030, JAMA Pediatrics
sample_size: 84030
sample_region: "日本（環境省 JECS 全国）"

related_theories: ["[[bronfenbrenner-ecological]]", "[[executive-function]]", "[[harvard-cdc-framework]]"]
related_research: ["[[research/D4_cognitive/madigan-2020-screen-use-language]]", "[[research/D4_cognitive/dowdall-2019-shared-book-reading-meta]]", "[[research/D7_parent_mental/matsumura-2019-jecs-education-ppd]]"]
matcher_axes: ["screen_time", "Japan_data", "JECS", "autism", "gender_difference"]
note_potential: "very_high"

batch: PhaseC_sprint3
evidence_source: "abstract_only"
collected_via: "openalex"
collected_date: 2026-05-14
review_status: "collected"
ceo_note: "**JECS の代表的子ども発達アウトカム論文**。山梨大学（山縣然太朗 PI）チーム。JAMA Pediatrics 掲載、被引用 105。1歳児スクリーンタイムが3歳児 ASD と関連、ただし男児のみ ── という重要な発見。スクリーン問題で日本データを語れる中核論文"

counterevidence_to: ["『スクリーンタイムと発達障害は無関係』論", "『ASD は完全に遺伝的』論"]
has_counterevidence: ["[[research/D4_cognitive/madigan-2020-screen-use-language]]"]  # 関連だが直接の反証ではない
critique_included: true
cultural_caveat: "日本全国出生コホート、N=84,030 ── 因果推論は限定、観察研究。ASD 診断は親報告ベース"
---

# 1歳児スクリーンタイムと3歳時の自閉スペクトラム症：JECS（Kushima et al., 2022）

## 200-500字要約
本論文は、**環境省「子どもの健康と環境に関する全国調査（JECS, Japan Environment and Children's Study）」** の N=84,030 大規模出生コホートを用い、**1歳時のスクリーンタイム曝露が3歳時の自閉スペクトラム症（ASD）診断と関連するか** を検証した日本発の重要な疫学研究です。山梨大学の山縣然太朗 PI チーム（Kushima 第一著者）による。
1歳時のスクリーンタイムを質問紙で測定（なし／1時間未満／1-2時間／2-4時間／4時間以上）、3歳時の ASD 診断を親報告で評価。多変量調整オッズ比で関連を推定。
結果、**男児では曝露量に応じて ASD オッズが直線的に増加** ── 4時間以上で OR=3.48（基準：1時間未満）。**女児では有意な関連は検出されず**。著者らは「**男児においてスクリーンタイムは ASD と関連がある**」と結論しつつ、**因果推論を厳格に避けた（逆方向の可能性：ASD 傾向の子が早期からスクリーンに惹かれる、を排除できない）**。引用数 105（2026-05時点、JAMA Pediatrics トップティア）。日本発の発達疫学論文の代表格。

## キーフィンディング（3-5項目）
- N=84,030 の大規模日本コホートで1歳時スクリーンタイムを系統的に評価
- 男児：4時間以上スクリーンで ASD オッズ 3.48 倍（vs 1時間未満）
- 女児：スクリーンタイムと ASD に有意な関連なし ── 明確な性差
- 著者らは因果と断定せず：「逆方向（ASD 傾向 → スクリーン愛好）」も論理的に可能
- JECS の発達アウトカム研究としてトップ被引用論文の一つ

## ひだまりこそだち への示唆
- マッチャーでの使い方: 「スクリーンタイムって本当に悪いの？」相談 → 「日本の N=8.4万コホートで、特に男児は4時間以上で ASD 関連リスクが3.5倍。ただし因果は不明、警戒は妥当」
- note記事化のフック: 「スマホ育児は ASD を増やすのか ── 日本 N=8.4万調査が示した『男児だけ』のリスク」「JECS が示す『1歳児スクリーン4時間』の境界線」
- 親への翻訳: 「1歳でスクリーン4時間以上は男児で ASD と関連あり、というデータがある（女児では関連なし）」「因果は不明だが、リスク回避の観点で1日1時間以下が目安」「ASD の原因はスクリーンだけではなく、スクリーンを減らせば ASD が防げるとは断定できない」
- ひだまりこそだち事業への示唆: 「日本データに基づくスクリーンタイム指針」を打ち出す根拠論文。男女差の視点は炎上回避にも有用

## 関連理論との関係
- [[bronfenbrenner-ecological]]: メディアという「マクロシステム」が「マイクロシステム（親子相互作用）」を圧迫する例
- [[executive-function]]: 早期スクリーンが実行機能発達を阻害する可能性（仮説）
- [[harvard-cdc-framework]]: 「serve & return」を阻害する画面メディアの位置づけ

## 留保・批判
- 観察研究で因果推論不可：RCT は倫理的に困難
- ASD 診断は親報告：臨床診断との誤差あり、信頼性は限定
- 逆方向の交絡：「ASD 傾向 → 早期スクリーン愛好」を排除できない（社会的サインへの反応性が低い児童は親もスクリーンに頼りがち）
- 男女差の生物学的解釈不明：男児のほうが ASD 自体多いことの統計学的人工性の可能性
- スクリーンの「内容」未測定：教育番組 vs 受動視聴の区別なし
- 1歳時測定の妥当性：1歳児のスクリーンタイムが3歳までに変化することは未調整

## 出典
- Kushima, M., Kojima, R., Shinohara, R., Horiuchi, S., Otawa, S., Ooka, T., Akiyama, Y., Miyake, K., Yokomichi, H., & Yamagata, Z. (2022). Association Between Screen Time Exposure in Children at 1 Year of Age and Autism Spectrum Disorder at 3 Years of Age in the Japan Environment and Children's Study. *JAMA Pediatrics*, 176(4), 384-391.
- DOI: 10.1001/jamapediatrics.2021.5778
- OpenAlex ID: W4210441228
- Cited by: 105 (2026-05時点)
- 所属：山梨大学 医学部 社会医学講座（山縣然太朗グループ）

## 関連日本研究
- JECS 公式：環境省「子どもの健康と環境に関する全国調査」全国 N=10万超出生コホート
- Yamagata 2012 双子研究（[[research/D3_parenting/yamagata-2012-japan-mz-twin-parenting]]）── 同じ山梨グループ
- Matsumura 2019 JECS（[[research/D7_parent_mental/matsumura-2019-jecs-education-ppd]]）── 同コホート別テーマ
