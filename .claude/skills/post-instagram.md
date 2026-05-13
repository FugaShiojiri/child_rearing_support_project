---
description: Instagram に承認済みドラフトを自動投稿する（R2 経由で画像配信）
argument-hint: [--date YYYY-MM-DD]
---

# post-instagram

## 概要
指定日（省略時は今日）の Instagram ドラフトを読み込み、`approved: true` と画像パスを確認した上で `scripts/post_instagram.py` を実行する。画像を Cloudflare R2 にアップロードし、Meta Graph API でフィード投稿する。

## 前提
- `.env` に Meta Graph API トークン（`META_ACCESS_TOKEN`, `IG_USER_ID`）と R2 認証情報（`R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`, `R2_PUBLIC_BASE_URL`）が設定済み
- `docs/drafts/instagram/${date}.md` が存在し、frontmatter に `approved: true` と `image: <path>` が記載
- 画像ファイルがローカルに存在（推奨: `docs/drafts/instagram/assets/`）

## 手順
1. 引数 `--date` を解釈。未指定なら今日。
2. Read で `docs/drafts/instagram/${date}.md` を読み込む。存在しなければ「ドラフトが見つかりません」と表示して終了。
3. frontmatter を検証:
   - `approved` が `true` でなければ「未承認のため投稿しません」と表示して終了。
   - `image` キーが無い、または指定パスのファイルが存在しない場合「画像が指定されていません」または「画像ファイルが見つかりません: ${image_path}」と表示して終了。
4. Bash で `python scripts/post_instagram.py --date ${date} --commit` を実行する。スクリプト内部の流れは:
   - 画像を R2 にアップロード（public URL を取得）
   - Meta Graph API `/media` でコンテナ作成 → `/media_publish` で公開
5. 結果を CEO に報告:
   - Instagram 投稿 URL（permalink）
   - 投稿 ID
   - キャプション先頭 50 文字
   - R2 上の画像 URL

## 失敗時の挙動
- **R2 アップロード失敗**: 「R2 へのアップロードに失敗しました。`.env` の R2 認証情報とバケット名を確認してください」と案内。
- **Meta API レート制限 (429 / OAuthException code=4)**: 「Meta API のレート制限です。1時間後に再実行してください」と案内。
- **トークン期限切れ (190)**: 「Meta アクセストークンが期限切れです。Meta Developer Console で長期トークンを再発行してください」と案内。
- **画像形式エラー**: Instagram は JPEG 必須。PNG の場合は変換が必要な旨を案内。
- **ドラフト不存在 / approved=false / 画像なし**: 上記手順参照。

## 関連
- スクリプト: `scripts/post_instagram.py`
- ドラフト: `docs/drafts/instagram/`
- ログ: `docs/posted_log/instagram.jsonl`
- 設計: `docs/auto_posting_v0.md`
