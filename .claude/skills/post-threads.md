---
description: Threads に承認済みドラフトを自動投稿する（approved gate 付き）
argument-hint: [--date YYYY-MM-DD]
---

# post-threads

## 概要
指定日（省略時は今日）の Threads ドラフトを読み込み、`approved: true` を確認した上で `scripts/post_threads.py` を実行して自動投稿する。投稿後、投稿 ID と URL を CEO に報告する。

## 前提
- `.env` に Threads API トークン（`THREADS_ACCESS_TOKEN`, `THREADS_USER_ID`）が設定済み
- `docs/drafts/threads/${date}.md` が存在し、frontmatter に `approved: true` が記載されている
- `scripts/post_threads.py` が動作する状態

## 手順
1. 引数 `--date` を解釈する。未指定なら今日の日付（`YYYY-MM-DD`）を使用。
2. Read ツールで `docs/drafts/threads/${date}.md` を読み込む。存在しなければ「ドラフトが見つかりません: docs/drafts/threads/${date}.md」と表示して終了。
3. frontmatter の `approved` フィールドを確認:
   - `approved: false` または未設定なら「未承認のため投稿しません。`approved: true` に変更してから再実行してください」と表示して終了。
   - `approved: true` なら次へ。
4. Bash で `python scripts/post_threads.py --date ${date} --commit` を実行する。
5. 標準出力から投稿 ID・URL・件数を抽出し、CEO に以下の形式で報告:
   - 投稿件数: N 件
   - 各投稿の ID と URL
   - 実行時刻

## 失敗時の挙動
- **401 / トークン期限切れ**: 「Threads アクセストークンが期限切れです。`scripts/refresh_threads_token.py` を実行してください」と案内。
- **ネットワークエラー (timeout / connection)**: 「ネットワークエラー。数分後に再実行してください」と案内。リトライは自動で行わない。
- **ドラフト不存在**: 上記手順2参照。
- **approved=false**: 上記手順3参照。
- **スクリプト非ゼロ終了**: stderr を引用して CEO に表示。

## 関連
- スクリプト: `scripts/post_threads.py`
- ドラフト: `docs/drafts/threads/`
- ログ: `docs/posted_log/threads.jsonl`
- 設計: `docs/auto_posting_v0.md`
