---
tags: [operations, auto-posting, setup, runbook]
status: active
date: 2026-06-12
related: [[auto_posting_v0]] [[CLAUDE]]
---

# 自動投稿セットアップ手順書（Threads / Instagram）

> **これは「あとで一人で進める」ための手順書**。上から順にやればOK。
> スクリプト・依存・ヘルパーは**すべて準備済み**。残るは Meta のトークン取得（人手作業・1回限り）だけ。
> **まず STEP1（Threads）だけ通す**のが推奨（圧倒的に簡単・FBページもR2も審査も不要・戦略上の主役チャネル）。Instagram は後日でよい。
> 詰まったら、その画面のスクショを Claude に貼れば、その時点のUIに合わせて案内する。

---

## 全体像（自動化されても承認ゲートは残る）

```
[Claudeが下書き生成] → docs/drafts/<platform>/YYYY-MM-DD.md (approved: false)
        ↓ オーナーが内容を目視 → approved: true に変更
[投稿コマンド1発]    → Threads / Instagram に投稿
```

自動化されるのは「投稿の手作業」だけ。内容のオーナー目視は維持される。

## 現在の状態（2026-06-12）

| 項目 | 状態 |
|---|---|
| スクリプト本体（Threads/IG） | ✅ 完成・現行API準拠・dry-run検証済 |
| Python依存 | ✅ インストール済 |
| ID取得ヘルパー `scripts/meta_setup_ids.py` | ✅ 作成・動作確認済 |
| トークン更新 `scripts/meta_token_refresh.py` | ✅ 既存 |
| テスト用Threads下書き | ✅ `docs/drafts/threads/2026-06-15.md`（承認済み・投稿待ち） |
| **`.env`（Meta/R2 認証情報）** | ⬜ **これだけ残っている＝この手順書で埋める** |

**Claude に丸投げできる部分**：`.env`の作成、`meta_setup_ids.py`によるID取得、dry-run/本投稿の実行は、トークンさえ取れれば Claude がセッションで代行できる。**オーナーがやるのは「Metaコンソールでトークンを取る」ところだけ**。

---

# 【STEP 1】Threads API（所要 約20〜30分・アプリ審査不要）

## ① Metaアプリを作る
1. https://developers.facebook.com/ に、Threadsに紐づくアカウントでログイン
2. 右上「マイアプリ」→「**アプリを作成**」
3. ユースケースで「**Threads API を利用**」を選択 → アプリ名（例: `hidamari-posting`）を付けて作成

## ② Threads権限を設定
1. 左メニュー「**ユースケース**」→ Threadsのユースケースを「カスタマイズ」
2. 権限に **`threads_basic`** と **`threads_content_publish`** を追加
3. 「**Threads testers**」に自分のThreadsアカウントを追加
4. スマホのThreadsアプリ側で承認：設定 → アカウント → ウェブサイトの許可（招待）→ 承認

## ③ アクセストークンを取得
1. ユースケース設定内の「**トークンを生成**」（または Graph API Explorer）で、上の2権限を付けたトークンを発行
2. 短期トークンなら**長期（60日）に交換** … 参考: https://developers.facebook.com/docs/threads/get-started/long-lived-tokens

## ④ `.env` にトークンを記入
- `.env` が無ければ `cp .env.example .env`（または Claude に「.env作って」と頼む）
- 記入：
  ```
  META_ACCESS_TOKEN=（取得した長期トークン）
  ```

## ⑤ ユーザーIDを自動取得（手でAPIを叩かなくてよい）
```bash
python scripts/meta_setup_ids.py
```
→ 表示された `META_THREADS_USER_ID=xxxxx` の行を `.env` にコピペ
（※ Claudeにこのコマンドを実行してもらってもよい）

## ⑥ テスト投稿
承認済みドラフト（6/15の赤ちゃん返り）で：
```bash
python scripts/post_threads.py --date 2026-06-15            # dry-run（投稿されない・本文確認）
python scripts/post_threads.py --date 2026-06-15 --commit   # 実投稿
```
→ Threadsに出れば完成。`docs/posted_log/threads.jsonl` に記録が残る。

> **トークンは60日で失効**。月1回 `python scripts/meta_token_refresh.py --commit` を実行（Claudeがセッションで実行してもよい）。

---

# 【STEP 2】Instagram API（Threadsが回ってから・約1〜1.5時間）

> 手数が多い（プロアカウント化＋FBページ連携＋画像の公開URL化）。急がない。

## ① アカウント側の準備
1. Instagramを「**プロアカウント（ビジネス or クリエイター）**」に切替（個人アカウントはAPI投稿不可）
2. **Facebookページ**を1つ作り、IGと連携（IG設定 → ページをリンク）

## ② Metaアプリに Instagram を追加
1. STEP1のアプリに「**Instagram Graph API**」と「**Facebookログイン**」を追加
2. 権限：`instagram_basic` / `instagram_content_publish` / `pages_show_list` / `pages_read_engagement` / `business_management`
3. 自分のアカウントへの投稿は**開発モードで可**（他人のアカウントに使う時だけ審査が要る）
4. トークン発行 → 長期化 → `.env` の `META_ACCESS_TOKEN` を更新
5. ```bash
   python scripts/meta_setup_ids.py
   ```
   → `META_INSTAGRAM_BUSINESS_ID=xxxxx` を `.env` にコピペ

## ③ 画像ホスティング（Cloudflare R2・無料枠10GB）
Instagram APIは「公開URLの画像」しか受け付けないため、生成画像をR2に上げてURL化する。
1. https://dash.cloudflare.com/ → R2 → バケット作成（例: `hidamari-kosodachi-images`）→ 公開アクセス有効化
2. R2 APIトークン作成 → `.env` に記入：
   ```
   R2_ACCOUNT_ID=...
   R2_ACCESS_KEY_ID=...
   R2_SECRET_ACCESS_KEY=...
   R2_BUCKET_NAME=hidamari-kosodachi-images
   R2_PUBLIC_URL=https://（公開URLのベース）
   ```
3. テスト：
   ```bash
   # docs/drafts/instagram/YYYY-MM-DD.md に image: パス と approved: true
   python scripts/post_instagram.py --date YYYY-MM-DD            # dry-run
   python scripts/post_instagram.py --date YYYY-MM-DD --commit   # 実投稿
   ```

---

## つまずいたら

- **トークン系エラー（`OAuthException` 等）** → 権限不足 or 失効。`python scripts/meta_setup_ids.py` の出力を Claude に貼れば原因を切り分ける。
- **Threadsトークンと Instagram(FB Graph)トークンが別アプリに分かれる**ことがある。その場合は各トークンで `meta_setup_ids.py` を2回実行し、解決できたIDだけ採用。
- **Metaコンソールの画面が手順書と違う** → UIは時期で変わる。詰まった画面のスクショを Claude に渡せば、その時点のUIで案内する。

## 再開するときの最短ルート

1. STEP1 ①〜③でトークンを取る（ここだけ人手）
2. Claudeに「Threadsトークン取れた。.env作ってセットアップして」と言う
3. あとは Claude が `.env`作成 → ID取得 → テスト投稿まで実行する
