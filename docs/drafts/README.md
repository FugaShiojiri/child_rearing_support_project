# ドラフト投稿フォルダ

> 各 SNS プラットフォーム別の投稿ドラフト置き場。Claude Code がここに生成し、CEO が承認したものだけが自動投稿される。

---

## フォルダ構成

```
docs/drafts/
├── x/         ← X (Twitter) 投稿ドラフト
├── threads/   ← Threads 投稿ドラフト
├── note/      ← note 記事ドラフト
└── instagram/ ← Instagram 投稿ドラフト
```

---

## ファイル命名規則

```
YYYY-MM-DD[-suffix].md
```

例:
- `2026-05-14.md` — その日の標準ドラフト
- `2026-05-14-morning.md` — 朝の投稿
- `2026-05-14-evening.md` — 夜の投稿

---

## ドラフトファイルの標準フォーマット

```markdown
---
platform: x          # x | threads | note | instagram
date: 2026-05-14     # YYYY-MM-DD（必須）
approved: false      # CEO が true に変更すると投稿対象になる
scheduled_at: "19:30" # 投稿時刻（オプション、Phase 2 で対応）
hashtags:            # オプション、配列で複数可
  - こそだち
  - 育児記録
image: null          # Instagram のみ、画像パス or URL
---

# Post Body

ここに投稿本文（プラットフォーム別の文字数制限を守る）:
- X: 280字以内
- Threads: 500字以内
- note: 制限なし
- Instagram: 2,200字以内（キャプション）
```

---

## CEO の承認フロー

1. Claude Code がドラフトを生成（`approved: false` で保存）
2. CEO が内容をレビュー
3. 投稿してよい場合: `approved: false` を `approved: true` に変更
4. 該当プラットフォームの投稿スキルを実行（例: `/post-x`）
5. スクリプトが `approved: true` のドラフトのみ拾って投稿

---

## 安全装置

- **デフォルト dry-run**: スクリプトは `--commit` フラグなしでは実投稿しない
- **CEO 目視確認**: `approved: false` のままなら絶対に投稿されない
- **二重承認**: スクリプトは最終確認プロンプトを表示（オプション）

---

## 投稿ログ

実投稿後は `docs/posted_log/{platform}.jsonl` に追記される。
このログは `.gitignore` 対象（プライバシー・本番運用記録のため）。
