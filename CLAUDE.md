# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

このファイルは Claude Code (claude.ai/code) がリポジトリ内で作業する際のガイダンスを提供します。

## プロジェクト概要

子育て支援を目的とした事業プロジェクト（child_rearing_support_project）。日本市場向け、個人/小規模チーム想定。サービス名は「ひだまりこそだち」。詳細な事業仮説・MVP方針は `ceo` エージェントが管理する。

**このリポジトリはコードベースであると同時に Obsidian Vault（Markdown 文書群）**であり、CEO（人間）は Obsidian で `.md` を直接閲覧・編集し、Claude Code は Filesystem 経由で同じファイルを読み書きする協働構成。成果物の中心は「コード」ではなく**戦略文書・知識ベース・SNS 投稿コンテンツ**。Python/Node スクリプトはそのコンテンツを配信・生成するための補助自動化。

## リポジトリ構成とアーキテクチャ（big picture）

全体像は1ファイルでは掴めないので、ここで俯瞰する。詳細記法・運用は `VAULT_GUIDE.md`、文書地図は `MOC.md` を参照。

### 3つの構成要素

1. **Obsidian Vault（`docs/` 中心の Markdown 群）＝正式記録・真実源**
   - リポジトリルートが Vault ルート。ノート間は `[[wiki-link]]` で連結し、各ノート先頭に YAML front-matter（`tags` / `status: draft|approved|archived` / `date`）を付ける。
   - `docs/` 直下 = 戦略・設計・実行文書（`roadmap.md` / `persona_v0.md` / `product_v0_*.md` / `phase1_*.md` / `phase2_plan_v0.md` / `monetization_roadmap_v0.md` / `web_only_strategy_v0.md` 等）。`_vN` サフィックスでバージョン管理し、旧版は消さず残す。
   - `docs/tasks/` = **タスクの真実源**（後述の「セッション開始時の同期」参照）。
   - `docs/{note,x,instagram,threads}/` = プラットフォーム別の投稿アセット・運用方針。
   - `docs/drafts/{platform}/YYYY-MM-DD.md` = 投稿ドラフト置き場（front-matter の `approved` フラグで投稿可否を制御）。

2. **知識ベース（`docs/knowledge/`・461ファイル規模）＝コンテンツの原料**
   - `education_theories/`（tier_s〜tier_c で重要度分類・`_matcher_views/` に横断ビュー）／`books/`（ジャンル別の育児書要約）／`research/`（D1〜D11 のテーマ別論文サマリ）。
   - これらは連載記事・有料単品記事・親向けガイドPDF の「素材」。`docs/matcher/`（axes/questions/scoring/recommendation）は MBTI 式の子育てタイプ診断ロジック設計。
   - 知識ベースの3層構造（Memory / docs/knowledge / agentmemory）の役割分担は `docs/knowledge_architecture.md` と memory `[[project-knowledge-architecture]]` に定義。

3. **自動化スクリプト（`scripts/`）＝配信・生成パイプライン**
   - Python（自動投稿・サムネ生成）と Node（リール動画生成）。`.claude/skills/` の各スキルがこれらを薄くラップし、Claude が「コマンド一発」で呼ぶ。

### コンテンツ配信パイプライン（最重要フロー）

**生成 → CEO目視承認 → 投稿**の3段で、承認ゲートを必ず通す設計：

1. **生成**: `draft-posts` スキル（or 手動執筆）が `docs/drafts/<platform>/YYYY-MM-DD.md` を **`approved: false`** で作成。
2. **承認**: CEO が内容を目視し front-matter を `approved: true` に変更（販売・配信コンテンツの CEO 目視は不可侵の制約）。
3. **投稿**: `post-note` / `post-threads` / `post-instagram` スキルが対応 Python スクリプトを呼ぶ。スクリプトは `approved: true` のみ処理し、`--commit` 無しは dry-run。
   - **note は「下書き保存」までで止め、公開ボタンは CEO が手動で押す**（Phase2 方針）。公式 API が無いため Playwright でブラウザ自動操作しており、note の UI 変更時はセレクター追従が必要。
   - Threads / Instagram は Meta Graph API。Instagram は画像を Cloudflare R2 にアップロードして公開 URL を得てから投稿（`scripts/lib/r2_uploader.py`）。

### スクリプト構成

- `scripts/post_{note,threads,instagram}.py` — プラットフォーム別自動投稿。`scripts/lib/draft_loader.py`（ドラフト読込）と `r2_uploader.py`（R2）を共有。
- `scripts/note_thumbnail.py` — note アイキャッチ（1280x670）を HTML/CSS → weasyprint → PyMuPDF で生成。ブランド配色・共通タグライン固定（memory `[[project-note-thumbnail]]`）。
- `scripts/reel_node/render_full.js` — Instagram 絵本リール動画のフレーム生成（@napi-rs/canvas + roughjs、色鉛筆タッチ）。`node render_full.js` で `frames_full/` に静止画を書き出し、後段で動画化。
- `scripts/meta_token_refresh.py` — Meta（Threads/Instagram）アクセストークンのリフレッシュ。
- `scripts/google_form_interview_v1.gs` — Phase1 インタビュー Google Form の GAS（Google 側に貼り付けて使用、ローカル実行なし）。
- 親向けガイドPDF は weasyprint + pydyf 0.10.0 + Noto Sans CJK JP で生成（成果物は `docs/parents_guides/*.pdf`、方針は memory `[[project-pdf-pipeline]]`）。

### テスト・ビルド・Lint について

**このリポジトリに自動テスト・ビルド・Lint の仕組みは無い**（コンテンツ事業のため）。投稿スクリプトの検証は `--commit` を付けない dry-run 実行が実質のテスト。知識ベースの整合性点検は `docs/knowledge_architecture.md` 記載の手動 Lint（リンク切れ・矛盾・陳腐化・孤立ページ）で、専用ツールは入れず Claude セッション内で実施する方針。

## よく使うコマンド

```bash
# Python 依存インストール（投稿・サムネ系）
pip install -r scripts/requirements.txt
playwright install chromium            # note 投稿に必要

# 環境変数: テンプレをコピーして実値を入れる（.env は .gitignore 済み）
cp .env.example .env

# 投稿スクリプト（--commit 無し = dry-run、付与 = 実投稿）
python scripts/post_note.py       --date YYYY-MM-DD            # 下書き保存(dry-run)
python scripts/post_note.py       --date YYYY-MM-DD --commit   # 実投稿（下書き保存まで・公開はCEO手動）
python scripts/post_note.py       --date YYYY-MM-DD --commit --headed   # セレクター確認用にブラウザ表示
python scripts/post_threads.py    --date YYYY-MM-DD --commit
python scripts/post_instagram.py  --date YYYY-MM-DD --commit
python scripts/meta_token_refresh.py        # Meta トークン更新

# note サムネ生成
python3 scripts/note_thumbnail.py --title 'タイトル' --series '連載「…」 第N回' --out assets/thumbnails/xxx.png

# Instagram 絵本リールのフレーム生成
cd scripts/reel_node && npm install && node render_full.js   # frames_full/ に出力
```

スキル経由（推奨・Claude が承認ゲートやメッセージ整形まで面倒を見る）: `/post-note`・`/post-threads`・`/post-instagram`・`/draft-posts`・`/show-x-today`（`.claude/skills/` 参照）。

## セッション開始時の同期（タスク管理・記憶）

### 記憶（ハイブリッド方針・2026-05-15 確定）

セッション横断の記憶は **agentmemory MCP を主**とするハイブリッド運用：

- **セッション開始時（必須）**: メインClaudeは agentmemory を `memory_recall`（必要に応じ `memory_smart_search`）で照会し、過去セッションの意思決定・経緯を把握してから作業に入る。**この照会を省略しない**（MCPは自動ロードされないため、照会忘れ＝記憶が実質使われない事故になる）。
- **保存の振り分け**:
  - **agentmemory MCP（主・大量横断）**: 日々の意思決定ログ・経緯・粒度の細かい履歴・調査メモは `memory_save` で蓄積。検索は `memory_smart_search`。
  - **ファイル `MEMORY.md` ＋ memory/（小・常時自動ロード）**: 「毎回必ず知っておくべき確定事項・フィードバック・現状」だけ薄く維持し、詳細は MCP へのポインタを置く。肥大化させない。
  - **docs/（中・人間が読む）**: 構造化された引用可能な知識・仕様。
- 詳細な振り分け基準は memory `[[project-knowledge-architecture]]` を参照。

### タスク管理

タスクの **単一の真実源** は `docs/tasks/backlog.md`、当週のビューは `docs/tasks/this_week.md`。

- **セッション開始時**: メインClaudeは `docs/tasks/this_week.md` → `docs/tasks/backlog.md` の順に Read し、現在の状況・優先タスクを把握してから作業に入る。
- **セッション開始時のリマインド（必須・通知方式=C 確定／ユーザー選択 2026-05-18）**: `this_week.md` の「📌 リマインダー：日付固定の手元作業」を確認し、**本日が期日 or 期日超過の未完(⬜)作業があれば、最初の応答の冒頭でユーザーに知らせる**（例:「本日5/21です。集客記事の note 入稿＋知人配布が今日の作業です」）。**期日超過分も必ず拾う**（その日に開かなくても、次に開いた時に取りこぼし作業を冒頭で知らせる）。期日のものが無ければ言及不要。
  - **通知方式は C（Claude Code 起動時の冒頭通知）でユーザー確定**。スケジュール自動プッシュ／Slack連携／モバイルアプリは**不採用**（無料・人手最小・追加ツール無しを優先）。`/schedule` の再試行・自動プッシュやSlack/モバイルの再提案は**しない**（ユーザーが再要望した場合のみ）。
- **セッション中/節目**: 作業の細かい分解は Claude Code のタスク機能（TaskCreate/TaskUpdate）で行い、完了・追加・中止が出たら `backlog.md`（必要なら `this_week.md`）へ差分反映する。`backlog.md` 以外を真実源にしない（二重管理の禁止）。
- **更新者**: タスクの起票・分解・更新・棚卸しは Claude（メイン/CEO）が担う。CEO本人の操作は週次レビュー回答と「終わった/やめた」の一言のみ（人手介入最小原則）。
- **週次**: 毎週金曜に CEO が `this_week.md` を翌週版へ再生成し、未消化を `backlog.md` の Next へ巻き戻す。見積合計が週15h（自己経営上限）を超えたら Later 送り。
- 閲覧は Obsidian（本リポジトリが Vault ルート）。運用ルール詳細は `docs/tasks/backlog.md` 末尾の「メンテナンス規約」。
- **閲覧強化（CEO決裁 2026-05-19）**: Obsidian プラグインは **Dataview のみ採用**（read-only ビュー）。真実源は `backlog.md` で**不変**（Dataview記法・メタデータ手入力はしない）。閲覧ビュー実体は `docs/tasks/board.md`（表示専用・編集禁止）と `this_week.md` の自動抽出ブロック。**Kanban 等の別ファイル板方式は二重管理になるため不採用**（オーナーが入れた obsidian-kanban は撤去済）。依存プラグインは Dataview 1本に固定し増やさない。新規ビューの作り込みは Phase1 完了後に再判断。
- **web完結シフト（CEO決裁 2026-05-28）**: 旧原則3「コミュニティはオフライン中心」を**撤回・書き換え**（オーナー知人/地域ネットワーク不在が判明・設計前提誤りはCEO責任引き受け＝[[project-distribution-reality]]）。当面のweb集客戦略は `docs/web_only_strategy_v0.md` を**正**とする（採用2本=note他クリエイター誠実接触+タグ最適化／不採用5本=X押し込み強化・Threads前倒し・創作大賞等）。Phase1 G1=20件厳格維持・6/4まで「学びの質」フェーズへ再定義。

## エージェント委譲ルール（最重要）

### ユーザー指示（2026-05-18・最優先）: 全件 CEO に回す

ユーザーは「**自分は CEO とのみ話す。全て CEO に回してほしい**」と明示。原則 **すべての判断・相談・要望は `ceo` SubAgent に委譲**し、メインClaude はその決裁の実装・整形・進捗反映に徹する。ユーザーへの応答は CEO の判断・方針を伝える形にする（メインClaude が独断で事業判断を返さない）。

- 例外（メインClaが直接処理してよい）: 純粋な技術実装・ファイル操作・調査・台帳/メモリ反映・CEO決裁の実行など「判断を伴わない作業」。判断が少しでも絡むものは CEO へ。
- 迷ったら CEO。CEO が「判断不要」と返せば即メインに戻るので過剰委譲のコストは低い。
- ユーザーが個別に「これは CEO 不要・直接やって」と言った場合のみ直接対応。

このプロジェクトでは **`ceo` SubAgent が事業統括者** として位置づけられている。以下のリクエストは、ユーザーが特に指示しなくても **常に `ceo` エージェントに委譲すること**：

- 事業戦略・ロードマップ・優先順位に関する判断
- 新機能・新規施策の方針決定（「次は何をすべきか」「これを作るべきか」）
- 要件定義・仕様策定（PRD作成、受け入れ基準の定義）
- 複数の専門領域にまたがる調整・意思決定
- ユーザーニーズ分析・ペルソナ定義
- 進捗報告・トレードオフ判断の依頼

委譲時は `Agent` ツールで `subagent_type: ceo` を指定する。同じ会話の文脈を継続する必要がある場合は、`SendMessage` で既存の agentId に送る。

### 委譲しない（メインClaudeが直接対応する）ケース

- 単純なファイル読み取り・grep・コード調査
- すでに方針が決まっているタスクの実装
- バグ修正・リファクタリング等の純粋な技術作業
- ユーザーが明示的に「CEOには聞かないで」と指示した場合

判断に迷ったら委譲する。CEOは「自分の判断不要」と判断したら即座にメインClaudeに戻すので、過剰委譲のコストは低い。

## エージェント定義の場所

- プロジェクト固有: `.claude/agents/`
- 現在定義済み: `ceo`（事業統括CEO、Opusモデル）

## ワークフロー

- `@claude` メンションで起動する GitHub Actions: `.github/workflows/claude.yml`
- 認証は `CLAUDE_CODE_OAUTH_TOKEN`（サブスクリプション認証）
