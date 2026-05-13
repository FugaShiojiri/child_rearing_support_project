# Claude Code 自動投稿パイプライン 設計書 v0

> ステータス: 設計書（実装前レビュー要）
> 対象: note / X (Twitter) / Instagram / Threads の半自動投稿
> 作成日: 2026-05-14
> 参照: 各実装記事（末尾「参考記事」参照）

---

## ゴール

ひだまりこそだち の毎日のお題と SNS 投稿を、**Claude Code から半自動で配信できる状態** にする。

- **半自動 = 「Claude Code が生成 → CEO が目視レビュー → 承認分のみ自動投稿」**
- 全自動は採用しない（プロジェクト原則「販売コンテンツは CEO 目視確認」と整合）

---

## 設計原則

### プロジェクト制約との整合

| 原則 | 本設計での対応 |
|---|---|
| **Claude Code Max 以外は課金不可** | X API 無料枠 / note Playwright / Threads API / Meta API / 無料画像ホスティング を採用 |
| **販売コンテンツは CEO 目視確認** | 全プラットフォームで「承認ステップ」を必須化 |
| **人手介入最小化** | 生成・整形・スケジューリングは自動化、承認のみ人間 |
| **配信主軸 note** | note 投稿を最優先プラットフォームとして実装 |

### 共通アーキテクチャ

```
┌──────────────────────┐
│ Claude Code セッション│
│ (バッチで月90本生成) │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ docs/drafts/         │
│ - YYYY-MM-DD.md      │
│ - frontmatter で     │
│   approved: false    │
└──────────┬───────────┘
           ▼
   ┌─── CEO レビュー ───┐
   │  approved: true に  │
   │  変更（承認）       │
   └─────────┬───────────┘
             ▼
┌──────────────────────────────┐
│ /post スキル実行             │
│ approved 一覧から            │
│ プラットフォーム別投稿       │
└──┬───────┬─────────┬─────────┘
   │       │         │
   ▼       ▼         ▼
 note    X       Threads/IG
 (PW)  (API)     (API)
```

---

## プラットフォーム別実装

### 1. X (Twitter)

**手法**: X API 無料枠 + OAuth 2.0 PKCE 認証

| 項目 | 内容 |
|---|---|
| API | https://developer.x.com/ で取得 |
| 無料枠 | **月1,500投稿まで無料** |
| 認証 | OAuth 2.0 PKCE（`tweet.write` スコープ） |
| トークン管理 | macOS Keychain（または `.env` + .gitignore） |
| 必要ライブラリ | `tweepy` または直接 curl/requests |
| 鍵更新 | アクセストークンは長期有効、初回認証時のみブラウザフロー |

**実装ファイル構成**:
```
.claude/skills/post-x.md       ← Claude Code スキル定義
scripts/post_x.py              ← Python 投稿スクリプト
scripts/x_auth.py              ← OAuth 認証フロー
.env                           ← API キー（.gitignore 対象）
```

**運用フロー**:
1. CEO が初回認証（1回だけ・5分）
2. Claude Code: ドラフト生成 → `docs/drafts/x/YYYY-MM-DD.md` に保存
3. CEO: ドラフトをレビュー、`approved: true` 設定
4. `/post-x` コマンド実行 → 承認分のみ自動投稿

**コスト**: ¥0

---

### 2. note

**手法**: Playwright (ブラウザ自動操作) — note 公式 API が存在しないため

| 項目 | 内容 |
|---|---|
| ライブラリ | Playwright（Python or Node.js） |
| 認証 | note のメール+パスワードを `.env` に格納（または macOS Keychain） |
| MCP | Playwright MCP を `~/.claude/mcp/` に登録すれば Claude Code から直接操作可能 |
| 投稿先 | **下書き保存** を基本（公開は CEO が手動で実行） |
| 注意点 | note の UI 変更でセレクター追従が必要・ボット判定回避のため間隔3秒 |

**実装ファイル構成**:
```
.claude/skills/post-note.md
scripts/post_note.py           ← Playwright で下書き作成
scripts/note_articles/         ← マニフェスト・お題記事のソース
.env                           ← note ログイン情報
```

**運用フロー**:
1. Claude Code: 記事ドラフト生成 → `docs/drafts/note/YYYY-MM-DD.md`
2. CEO: ドラフトをレビュー、`approved: true` 設定
3. `/post-note` 実行 → Playwright が note にログイン → **下書き保存**
4. CEO が note 上で最終確認 → 手動で公開

**注意**:
- 完全自動公開ではなく **下書き保存まで** が安全
- note の利用規約上、ブラウザ自動化はグレー → 1日数本程度に抑える
- バッチで10本超を一気に投稿するとボット判定リスク

**コスト**: ¥0

---

### 3. Threads

**手法**: Meta Threads API（2024年6月一般公開）

| 項目 | 内容 |
|---|---|
| API | https://developers.facebook.com/docs/threads |
| 無料枠 | **完全無料** |
| 認証 | Meta for Developers でアプリ登録 → アクセストークン |
| トークン有効期限 | 約60日（更新スクリプトを cron 化推奨） |
| Instagram 連動 | Instagram Business アカウントと同じ Meta インフラ |

**実装ファイル構成**:
```
.claude/skills/post-threads.md
scripts/post_threads.py
scripts/meta_token_refresh.py  ← 60日ごとのトークン更新
.env
```

**運用フロー**:
1. Claude Code: スレッド草案生成 → `docs/drafts/threads/YYYY-MM-DD.md`
2. CEO: レビュー、承認
3. `/post-threads` 実行 → API 経由で投稿

**コスト**: ¥0

---

### 4. Instagram

**手法**: Meta Graph API + 無料画像ホスティング

| 項目 | 内容 |
|---|---|
| API | Meta Graph API（Threads と同じインフラ） |
| 前提 | **Instagram Business アカウントへ切替必須**（個人アカウントでは投稿不可） |
| Facebook Page 連携 | 必須（Meta 仕様） |
| 審査 | アプリ審査が必要（標準的な権限なら数日〜2週間） |
| 画像ホスティング | shiftb.dev は AWS S3（数百円/月）使用 → **本プロジェクトは課金不可方針のため代替必須** |

**画像ホスティングの無料代替**:
| 候補 | 無料枠 | 適合性 |
|---|---|---|
| **Cloudflare R2** | 10GB ストレージ + 10GB egress/月 | ◎ 推奨 |
| **GitHub Pages** | 公開リポジトリの静的ファイル | ◎ 1日数枚なら十分 |
| **Imgur API** | レート制限あり | △ 商用利用要確認 |
| **Cloudinary** | 無料枠 25GB ストレージ | ○ |

→ **推奨: Cloudflare R2 無料枠**（10GB は1日数枚で何年も持つ）。次点で GitHub Pages（既にリポジトリあり、追加コストゼロ）

**実装ファイル構成**:
```
.claude/skills/post-instagram.md
.claude/skills/feed-design.md   ← Pencil MCP or Canva 連携でデザイン生成
scripts/post_instagram.py       ← Meta Graph API ラッパー（3段階呼び出し）
scripts/upload_image.py         ← R2 or GitHub Pages へアップロード
.env
```

**Meta Graph API の3段階処理**:
1. 各画像コンテナ作成（POST /{account_id}/media、is_carousel_item:true）
2. カルーセルコンテナ生成（POST /{account_id}/media、children配列指定）+ ポーリング
3. 公開実行（POST /{account_id}/media_publish）

**運用フロー**:
1. Claude Code: キャプション＋画像コンセプト生成
2. 画像生成（Pencil MCP / Canva 手動 / その他）
3. CEO: 画像＋キャプションをレビュー、承認
4. `/post-instagram` 実行 → 画像 R2 アップロード → Meta API 投稿

**注意**:
- Instagram は **Phase 3 後半まで保留** が SNS 戦略 v0 の方針
- 実装着手は Phase 3 着手前に再判断

**コスト**: ¥0（R2 無料枠内）

---

## Claude Code スキル化のパターン

各プラットフォーム向けスキルは以下のフォーマットで `.claude/skills/` 配下に置く：

```markdown
---
description: X (Twitter) に承認済みドラフトを自動投稿する
argument-hint: [YYYY-MM-DD]（省略時は今日の日付）
---

# Post to X

## 手順

1. `docs/drafts/x/${ARG:-$(date +%Y-%m-%d)}.md` を読む
2. frontmatter の `approved: true` のもののみ対象
3. Bash で `python scripts/post_x.py` を実行
4. 投稿結果を `docs/posted_log/x.jsonl` に追記
5. CEO に「N件投稿しました」と報告

## 失敗時の挙動
- API エラー時は `docs/posted_log/x_errors.jsonl` に記録
- アクセストークン期限切れ時は再認証フローを案内
```

---

## ドラフトファイルの標準フォーマット

`docs/drafts/{platform}/YYYY-MM-DD.md`:

```markdown
---
platform: x | note | threads | instagram
date: 2026-05-14
approved: false        # CEO が true に変更すると投稿対象に
scheduled_at: 19:30    # 投稿時刻（オプション、Phase 2 で対応）
hashtags: [こそだち, 育児記録]
image: assets/2026-05-14.png  # Instagram のみ
---

# Post Body

ここに投稿本文（X: 280字以内、Threads: 500字以内、note: 制限なし）
```

---

## 実装ロードマップ

### Phase 1 (Week 2-3): 基盤整備

- [ ] `.claude/skills/` フォルダ作成
- [ ] X API キー取得（CEO 作業 30分）
- [ ] Meta for Developers アプリ登録（CEO 作業 30分）
- [ ] `.env` テンプレート作成（`.gitignore` 設定）
- [ ] ドラフト用フォルダ `docs/drafts/{x,note,threads,instagram}/` 作成
- [ ] `scripts/` フォルダ作成

### Phase 2 (Week 3-4): X / Threads 実装（先行）

- [ ] `scripts/post_x.py` 実装
- [ ] `.claude/skills/post-x.md` 作成
- [ ] `scripts/post_threads.py` 実装
- [ ] `.claude/skills/post-threads.md` 作成
- [ ] CEO 承認フロー（approved: true 一覧）の検証
- [ ] 月3本程度で試験運用

### Phase 3 (Week 5-): note 実装

- [ ] Playwright インストール
- [ ] `scripts/post_note.py` 実装（下書き保存まで）
- [ ] `.claude/skills/post-note.md` 作成
- [ ] note UI セレクター追従の監視運用
- [ ] β期間中は1日1〜2本に抑制

### Phase 4 (Phase 3 後半): Instagram 実装

- [ ] Instagram Business アカウント切替（CEO 作業）
- [ ] Facebook Page 作成
- [ ] Meta Graph API アプリ審査申請
- [ ] Cloudflare R2 セットアップ
- [ ] `scripts/post_instagram.py` 実装
- [ ] `.claude/skills/post-instagram.md` 作成

---

## リスクと対策

| リスク | 対策 |
|---|---|
| X API 無料枠超過 | 月1,500投稿の上限を Phase 1 で計測、超えそうなら配信頻度調整 |
| Meta トークン60日失効 | `meta_token_refresh.py` を月1回 cron 実行、CEO にリマインド通知 |
| note UI 変更でセレクター破綻 | Playwright を `headless=False` で月1回手動確認、CI/CD に組み込まない |
| ブラウザ自動化のボット判定 | 1日数本に抑制、間隔3秒以上、ユーザーエージェント設定 |
| Instagram アプリ審査落ち | Phase 3 着手前に申請、落ちたら手動投稿で対応継続 |
| API キー流出 | `.env` を必ず `.gitignore`、macOS Keychain 推奨 |
| 誤投稿 | CEO の `approved: true` 承認を必須化、投稿前に dry-run モード |

---

## セキュリティ

- すべての API キーは `.env` または macOS Keychain 経由で参照
- `.gitignore` で機密ファイルを除外
- 投稿スクリプトは **dry-run モード**（実投稿せずプレビューのみ）を必ず実装
- 投稿ログ `docs/posted_log/` には実投稿日時のみ記録、内容は drafts/ にすでにあるため二重保存しない

---

## 参考記事

1. **X (Twitter) 自動投稿**: https://nexa-corp.jp/claude-code-tweet-auto-draft-x/
   - X API + OAuth 2.0 PKCE + Cloudflare Workers Tweet Composer
   - SKILL.md パターンの実装例

2. **note 自動投稿（uravation）**: https://uravation.com/media/claude-code-note-auto-post/
   - Playwright + Claude API（Python パイプライン）
   - 下書き保存方式

3. **note 自動投稿（hirosuke_0520）**: https://note.com/hirosuke_0520/n/n8ed734a89ee6
   - Playwright MCP + `~/.claude/commands/` スキル
   - Gemini API でサムネイル生成

4. **Instagram 自動投稿**: https://shiftb.dev/articles/instagram-automation-claude-code
   - Meta Graph API + Pencil MCP + AWS S3
   - カルーセル投稿の3段階処理

---

## ユーザー確認事項

1. **Instagram の画像ホスティング**: Cloudflare R2 or GitHub Pages のどちらにするか
2. **Threads と X の優先順位**: SNS 戦略 v0 では「X 主軸 / Threads 補助」だが、自動投稿はどちらから着手するか
3. **note 投稿の自動公開可否**: 下書き保存までに留めるか、CEO 承認後の自動公開まで踏み込むか
4. **Phase 1 中の試験運用本数**: 月何本までで上限設定するか

## 次のアクション候補

- [ ] 本設計書を PR → マージ
- [ ] Phase 2 着手前に `.claude/skills/` の雛形を準備
- [ ] X API キーの取得（CEO 30分）
- [ ] Meta for Developers アプリ登録（CEO 30分）
