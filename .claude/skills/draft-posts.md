---
description: 翌日からN日分の投稿ドラフトを全プラットフォーム横断でバッチ生成する
argument-hint: [--days N] [--platforms threads,note,instagram,x]
---

# draft-posts

## 概要
ペルソナとプロダクト方針を参照し、翌日から N 日分の投稿ドラフトを各プラットフォームの文字数・トーンに合わせて生成し、`docs/drafts/<platform>/YYYY-MM-DD.md` に `approved: false` で保存する。CEO のレビュー・承認を経て初めて投稿される。

## 前提
- `docs/persona_v0.md`, `docs/product_v0_2.md`, `docs/sns_strategy_v0.md` が存在
- `docs/drafts/{threads,note,instagram,x}/` ディレクトリが存在
- 既存ドラフトを破壊しないこと

## 手順
1. 引数を解釈:
   - `--days N` 省略時は 7。
   - `--platforms` 省略時は `threads,note,instagram,x` 全て。
2. 参照ドキュメントを Read:
   - `docs/persona_v0.md`（ターゲット読者像）
   - `docs/product_v0_2.md`（サービス内容・価値提案）
   - `docs/sns_strategy_v0.md`（プラットフォーム別トーン・投稿頻度）
3. 既存ドラフトを Bash で確認: `ls docs/drafts/<platform>/ 2>/dev/null | sort | tail -5` を各プラットフォームで実行。最新日付と重複しないよう開始日を決定（基本は翌日 = 今日 + 1日）。
4. 各プラットフォームの制約に従い、N 日分のドラフトを生成:
   - **X**: 1日5本目安、140文字以内、ハッシュタグ最大2個、共感系・知見系・告知系を混ぜる
   - **Threads**: 1日5本目安、500文字以内、対話を誘発する問いかけや経験談中心
   - **note**: 1日2本（または週2本ペース）、1500〜3000字、ストーリー性のある長文
   - **Instagram**: 1日1本、キャプション最大2200字、画像必須（`image:` フィールドにプレースホルダー `TODO: docs/drafts/instagram/assets/YYYY-MM-DD.jpg` を記載）
5. 各ドラフトを Write で保存:
   - パス: `docs/drafts/<platform>/YYYY-MM-DD.md`（同一日に複数本ある場合は `YYYY-MM-DD-2.md`, `-3.md` と suffix）
   - **既存ファイルがあれば上書きせず suffix を付ける**（Bash の `ls` で事前確認）
   - frontmatter 例:
     ```yaml
     ---
     platform: threads
     date: 2026-05-15
     approved: false
     tags: [子育て, ワーママ]
     ---
     ```
6. 生成サマリーを表示:
   - 例: 「X 35本 / Threads 35本 / note 14本 / Instagram 7本 を `docs/drafts/` 配下に生成しました（5/15 〜 5/21）」
   - 生成パスのリスト（多い場合は件数のみでも可）
7. **必ず以下を CEO に案内**:
   - 「すべてのドラフトは `approved: false` です。内容をレビューし、投稿してよいものは `approved: true` に書き換えてください」
   - 「Instagram の `image:` はプレースホルダーです。実画像を `docs/drafts/instagram/assets/` に配置し、パスを更新してください」

## 失敗時の挙動
- **参照ドキュメント不存在**: 該当ファイル名を提示し「ペルソナ/プロダクト方針が読めません。先にドキュメントを整備してください」と表示。
- **ディレクトリ不存在**: Bash で `mkdir -p` で作成してから続行。
- **既存ファイル衝突**: 上書きせず suffix を付ける（手順5参照）。

## 関連
- 参照: `docs/persona_v0.md`, `docs/product_v0_2.md`, `docs/sns_strategy_v0.md`
- 出力: `docs/drafts/{threads,note,instagram,x}/`
- 設計: `docs/auto_posting_v0.md`
- 後続スキル: `/post-threads`, `/post-note`, `/post-instagram`, `/show-x-today`
