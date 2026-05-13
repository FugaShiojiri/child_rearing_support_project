---
description: note に承認済みドラフトを下書き保存する（公開は手動）
argument-hint: [--date YYYY-MM-DD]
---

# post-note

## 概要
指定日（省略時は今日）の note ドラフトを読み込み、`approved: true` を確認した上で `scripts/post_note.py` を実行して **下書き保存のみ** を行う。公開操作は CEO が note 上で手動実施する。

## 前提
- `.env` に note ログイン情報（`NOTE_EMAIL`, `NOTE_PASSWORD`）が設定済み
- Playwright が利用可能（`pip install -r scripts/requirements.txt` 済み）
- `docs/drafts/note/${date}.md` が存在し、frontmatter に `approved: true` が記載

## 手順
1. 引数 `--date` を解釈。未指定なら今日。
2. Read で `docs/drafts/note/${date}.md` を読み込む。存在しなければ「ドラフトが見つかりません」と表示して終了。
3. frontmatter の `approved` を確認:
   - `false` / 未設定 → 「未承認のため投稿しません」と表示して終了。
   - `true` → 次へ。
4. Bash で `python scripts/post_note.py --date ${date} --commit` を実行する。
5. **必ず以下のメッセージを CEO に表示**:
   - 「note に下書き保存しました。note 上で最終確認してから手動で公開してください」
   - 下書き URL（スクリプト出力から抽出）
   - タイトル・本文文字数

## 失敗時の挙動
- **note ログイン失敗**: 「note ログインに失敗しました。`.env` の `NOTE_EMAIL` / `NOTE_PASSWORD` を確認してください。2段階認証が有効な場合は手動投稿に切り替えてください」と案内。
- **UI セレクター変更検知**: スクリプトが「セレクターが見つからない」エラーを返した場合、「note の UI が変更された可能性があります。`scripts/post_note.py` のセレクター定義を更新する必要があります」と案内。
- **ドラフト不存在 / approved=false**: 上記参照。
- **タイムアウト**: 「note の読み込みが遅延しています。再実行してください」と案内。

## 関連
- スクリプト: `scripts/post_note.py`
- ドラフト: `docs/drafts/note/`
- ログ: `docs/posted_log/note.jsonl`
- 設計: `docs/auto_posting_v0.md`
