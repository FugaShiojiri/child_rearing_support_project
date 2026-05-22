---
title: "Patterns of Mobile Device Use by Caregivers and Children During Meals in Fast Food Restaurants"
authors: ["Jenny Radesky", "Caroline J. Kistin", "Barry Zuckerman", "Katie Nitzberg", "Jamie Gross"]
year: 2014
doi: "10.1542/peds.2013-3703"
source: "Pediatrics"
source_url: "https://doi.org/10.1542/peds.2013-3703"
openaccess_pdf_url: "https://publications.aap.org/pediatrics/article/133/4/e843/32925"

domain: D9_digital
sub_topics: ["parental_smartphone_use", "observational_study", "meal_interaction", "child_attention_seeking", "naturalistic_observation", "technoference"]
target_age: ["1-3", "3-6", "6+"]
study_type: "naturalistic_observation"
evidence_level: "moderate"
sample_size: 55  # 親子組
sample_region: "米国（ボストン地域のファストフード店）"

related_theories: ["[[bowlby-attachment]]", "[[harvard-cdc-framework]]", "[[sasaki-masami]]"]
related_research: ["[[research/D9_digital/mcdaniel-radesky-2017-technoference-child-behavior]]", "[[research/D9_digital/aap-chassiakos-2016-children-adolescents-digital-media]]"]
matcher_axes: ["parental_smartphone", "meal_time_distraction", "naturalistic_observation", "child_attention_seeking"]
note_potential: "very_high"

evidence_source: "abstract_only"
collected_via: "openalex"
collected_date: 2026-05-14
review_status: "collected"
ceo_note: "Radesky（Michigan）の博士論文に基づく自然観察研究（Pediatrics、被引用458）。ファストフード店で **55組の親子を匿名観察** し、親のスマホ使用と子の反応を詳細記録。質的研究の代表として頻繁に引用される。technoference研究の起点"
batch: PhaseC_sprint6

counterevidence_to: ["『食事中のスマホ使用は子に影響しない』論"]
has_counterevidence: ["小サンプル質的研究のため一般化に限界"]
critique_included: true
cultural_caveat: "米国ファストフード店という公共空間特有の文脈。日本の家庭食卓・回転寿司・ファミレス等での観察は別途必要"
---

# ファストフード店での親子食事と親のモバイル機器使用：自然観察（Radesky et al., 2014）

## 200-500字要約
Boston University のJenny Radesky（後にMichigan大、AAPテクニカルレポート共著者）による、**親子の食事中の親のスマホ使用パターン** を自然観察した質的研究（*Pediatrics*、被引用458）。

**研究方法**: 大都市圏のファストフード店15軒で、**親子55組（子は乳幼児〜学齢期）** を匿名観察。観察者は近くで食事しながらメモを取る。親のスマホ使用と、子の反応・親の応答を詳細記録。

**主要発見**:
- **55組中40組（73%）** の親が食事中に何らかのモバイル機器を使用
- うち **16組** は食事の大半をスマホに没頭（顔がほぼ画面に向きっぱなし）
- **親が没頭中、子は親の注意を引こうとして声を出す・物を投げる・席を立つ** などのエスカレーション行動を示す
- 親はこれらに **「うるさい・止めて」と苛立った反応** を返すパターン頻発
- 一部の親は、子が話しかけても返事をせず画面を見続けた
- **食事中に高度な親子対話が生まれる場面はスマホ非使用の組に集中**

**質的所見**: 親のスマホ使用は、(1) 完全没頭型、(2) 断続的チェック型、(3) 子と一緒に画面を見る型、(4) ほぼ未使用型 に類型化された。完全没頭型では、子からの **bid for attention（注意要求）** が無視され、エスカレートし、最終的に親が叱責するパターン。

**理論的含意**: 親のスマホ使用が **still-face状態を作り出す**、技術的中断（technoference）の初期実証。後続のMcDaniel & Radesky 2017の定量研究につながった。

## キーフィンディング（3-5項目）
- ファストフード店の **73%の親** が食事中にモバイル機器を使用、29%が大半没頭
- 親が没頭中、子は **注意要求行動をエスカレート** （声・動作・小道具）
- 親は子のエスカレーションに **苛立った反応** を返すパターンが頻発
- スマホ非使用組では **高度な対話・教育的やりとり** が観察された
- 自然観察で見えた、**「公共空間での親子関係の質」** の変化

## ひだまりこそだち への示唆
- マッチャーでの使い方: 「子の癇癪が外出時に増える」相談 → 「**自然観察研究では、親の食事中スマホ使用と子の注意要求エスカレーションが関連。外食時こそスマホを置く時間に**」
- note記事化のフック: 「ファミレスで観察された55組の親子：親のスマホと子の癇癪の見えない連鎖」「『うるさい』と叱る前に：子の bid for attention を読む」
- 親への翻訳: 「**食事中はスマホを置く** という小さな習慣で、外食時の子の癇癪が減る可能性。子の声がうるさく感じる時こそ、画面から目を上げる」
- サービス設計示唆: 「食事中noスマホ」習慣化チャレンジ、外出時のスマホ使用ルール提案

## 関連理論との関係
- [[bowlby-attachment]]: 子の bid for attention は安全基地確認行動の一種
- [[harvard-cdc-framework]]: Serve & Return が成立しない場面の累積
- [[sasaki-masami]]: 「応える」が失われ、子が「うるさい」と否定される現代的構図

## 留保・批判
- **N=55の質的観察研究**、定量的一般化は不可
- ファストフード店という特定環境（騒音多・公共・他客の目）
- 観察者効果の可能性（観察されている自覚で行動が変わる）
- 米国都市部のみ、日本のような「子連れ外食文化が異なる」環境への一般化は要慎重
- 親のスマホ使用の **理由** （仕事の緊急対応・育児情報検索・パートナーとの連絡等）は記録されない
- 親に罪悪感を与える危険、「スマホ＝悪」の単純化は避けるべき

## 出典
- Radesky, J. S., Kistin, C. J., Zuckerman, B., Nitzberg, K., Gross, J., Kaplan-Sanoff, M., Augustyn, M., & Silverstein, M. (2014). Patterns of Mobile Device Use by Caregivers and Children During Meals in Fast Food Restaurants. *Pediatrics*, 133(4), e843-e849.
- DOI: 10.1542/peds.2013-3703
- 引用数: 458（2026年5月時点）
