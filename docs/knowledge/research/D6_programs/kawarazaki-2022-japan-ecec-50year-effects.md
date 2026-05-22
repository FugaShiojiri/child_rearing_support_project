---
title: "Early childhood education and care: effects after half a century and their mechanisms"
authors: ["Hikaru Kawarazaki"]
year: 2022
doi: "10.1007/s00148-022-00899-w"
source: "Journal of Population Economics"
source_url: "https://doi.org/10.1007/s00148-022-00899-w"
openaccess_pdf_url: "https://link.springer.com/content/pdf/10.1007/s00148-022-00899-w.pdf"

domain: D6_programs
sub_topics: ["Japan_ECEC", "long_term_effects", "income_effects", "labor_economics", "1960s_expansion", "universal_ECEC"]
target_age: ["3-4", "5-6"]
study_type: "quasi_experimental_long_run"
evidence_level: "high"  # 政策実験的、半世紀の追跡
sample_size: null  # 大規模行政データ
sample_region: "日本（1960s-1980s 出生コホート）"

related_theories: ["[[harvard-cdc-framework]]", "[[kurahashi-sozo]]", "[[highscope]]"]
related_research: ["[[research/D6_programs/heckman-2013-fostering-measuring-skills]]", "[[research/D6_programs/campbell-2002-abecedarian-young-adult]]", "[[research/D6_programs/muennig-2009-perry-37yr-followup]]", "[[research/D6_programs/van-huizen-2018-universal-ecec-meta]]", "[[research/D6_programs/fujisawa-2023-japan-ecers-quality]]"]
matcher_axes: ["Japan_ECEC", "long_term_outcomes", "income_inequality", "policy_evaluation"]
note_potential: "very_high"

batch: PhaseC_sprint3
evidence_source: "abstract_only"
collected_via: "openalex"
collected_date: 2026-05-14
review_status: "collected"
ceo_note: "**日本の保育所拡大の長期効果を Heckman 流の経済学手法で評価した稀少論文**。1960-80年代の保育所拡大政策を準実験として、50年後の所得を追跡。Perry/Abecedarian の日本版と位置づけられる重要論文。Journal of Population Economics 掲載"

counterevidence_to: ["『日本の保育所拡大は経済効果がない』論", "『ECEC 長期効果は米国限定』論"]
has_counterevidence: ["[[research/D6_programs/duncan-magnuson-2013-preschool-fadeout]]"]  # フェードアウト論への反証
critique_included: true
cultural_caveat: "1960s-80s の日本データで、現代の少子化期保育所への一般化には注意が必要"
---

# 日本の幼児教育・保育の半世紀後の効果とその機序（Kawarazaki, 2022）

## 200-500字要約
本論文は、河原崎光（UCL／IFS、ロンドン）による、**日本の1960s-80年代の保育所拡大政策を準実験的に利用し、50年後（50歳時点）の所得・教育達成への効果を測定した重要な経済学論文** です。Journal of Population Economics 掲載。
日本では1960-70年代の高度経済成長期に保育所が急速に拡大した。地域・時期によって保育所利用可能性に差が生じたことを **自然実験** として利用、保育所アクセス（intent-to-treat）と50年後アウトカム（所得、教育、労働参加）の関連を分析。
結果、**(1) 保育所アクセス → 50歳時所得の有意な上昇**。**(2) 効果は特に『初期不利層の女性』に集中** ── 低 SES 出身女性で最大。**(3) 機序は『労働参加の増加』ではなく『賃金水準の上昇』 ── これは教育達成の向上を介して**。**(4) 不利層以外への悪影響なし**。著者の結論：「**普遍的 ECEC は所得不平等を縮小する経済政策である**」。Perry Preschool / Abecedarian の日本版位置づけ。被引用 17 で発表3年で堅実な蓄積。

## キーフィンディング（3-5項目）
- 日本1960-80s 保育所拡大 → 50歳時所得が有意に上昇（特に女性）
- 効果は初期不利層（低 SES）に集中 ── ECEC は格差縮小機能を持つ
- 機序：労働参加ではなく賃金 ── 教育達成の向上を介して
- 不利層以外への悪影響なし ── 普遍的政策の合理性
- Perry Preschool / Abecedarian と整合する Japan エビデンス

## ひだまりこそだち への示唆
- マッチャーでの使い方: 「保育園に通わせる意味あるの？家庭保育のほうがいいって聞くけど」相談 → 「日本の半世紀データで、保育所は特に経済的に余裕がない家庭の子に長期的恩恵がある（Kawarazaki 2022）。フェードアウト論に対する日本からの反証」
- note記事化のフック: 「日本の保育所、50年追跡したら何が起きたか ── 経済学者が見つけた『見えない効果』」「保育園は早期教育のため？ いいえ、子の50歳後の所得のため」
- 親への翻訳: 「保育所通園は、特に共働きで頑張る家庭の子の将来の所得を上げる ── 日本データで確認された」「家庭保育 vs 保育園は『どちらが愛情深いか』の問題ではなく、両方とも子を支える別の道」「保育園を罪悪感なく利用してよい」
- ひだまりこそだち事業への示唆: 「保育園利用への罪悪感」を緩める根拠論文。共働き層へのメッセージ素材

## 関連理論との関係
- [[harvard-cdc-framework]]: 早期介入の累積効果論の日本での実証
- [[heckman-2013-fostering-measuring-skills]]: Heckman の人的資本形成論の日本版
- [[duncan-magnuson-2013-preschool-fadeout]]: フェードアウト論への部分的反証

## 留保・批判
- 1960-80s データ：当時の保育所と現代保育所の質は異なる
- ITT 推定：実際の保育所利用ではなく地域アクセスの効果
- アウトカムは所得・教育のみ：心理社会的・健康アウトカムは未測定
- 不利層への集中効果：効果ヘテロ性の解釈には注意
- 「保育の質」未測定：園による効果差は本研究では捉えきれない

## 出典
- Kawarazaki, H. (2022). Early childhood education and care: effects after half a century and their mechanisms. *Journal of Population Economics*, 36(4), 2725-2797.
- DOI: 10.1007/s00148-022-00899-w
- OpenAlex ID: W4293081973
- Cited by: 17 (2026-05時点)
- 所属：University College London / Institute for Fiscal Studies

## 関連日本研究
- 中室牧子 / 赤林英夫らによる日本の ECEC 経済学研究群
- Asai et al. 2015 ── 認可保育所のマザーズ労働効果
- 厚生労働省『保育所等関連状況取りまとめ』── 制度文脈
