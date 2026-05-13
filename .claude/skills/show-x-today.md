---
description: 今日（または指定日）の承認済み X ドラフトをコピペ用に整形表示する
argument-hint: [--date YYYY-MM-DD]
---

# show-x-today

## 概要
X（旧 Twitter）は API 課金を回避するため自動投稿せず、CEO が手動でコピペ運用する。本スキルは指定日のドラフト（複数ファイル対応）を読み込み、`approved: true` のものだけをコピーしやすい形式で順次表示する。スクリプトは呼ばない（Read のみ）。

## 前提
- `docs/drafts/x/${date}.md` または `docs/drafts/x/${date}-*.md` が存在
- 各ドラフトの frontmatter に `approved: true/false` が記載

## 手順
1. 引数 `--date` を解釈。未指定なら今日。
2. Bash で `ls docs/drafts/x/${date}*.md 2>/dev/null` を実行して該当ファイルを列挙。0件なら「指定日の X ドラフトはありません」と表示して終了。
3. 各ファイルを Read で読み込み、frontmatter の `approved` を確認。`true` のみフィルタ。
4. approved=true が 0 件なら「承認済みの X ドラフトはありません」と表示して終了。
5. 各投稿を順次、以下のフォーマットで **コピーしやすい形** で表示（コードブロックや枠で囲まない、プレーンテキスト）:

```
────────────────────────────
[1/N] ${ファイル名}
────────────────────────────
（本文をそのまま出力）

ハッシュタグ: #xxx #yyy（frontmatter にあれば）
文字数: NN / 140
```

6. 全件表示後、CEO に以下を案内:
   - 「上記をスマホまたは PC で X にコピペして投稿してください」
   - 「投稿後にログとして残したい場合は、`docs/posted_log/x.jsonl` に手動で追記するか、別途 `mark-x-posted` スキル（未実装）で対応してください」

## 失敗時の挙動
- **ドラフトなし**: 上記手順2参照。
- **全件 approved=false**: 上記手順4参照。
- **frontmatter パース失敗**: 該当ファイル名を提示し「frontmatter の YAML が不正です」と表示。スキップして残りを処理。

## 関連
- ドラフト: `docs/drafts/x/`
- ログ（手動更新）: `docs/posted_log/x.jsonl`
- 設計: `docs/auto_posting_v0.md`
