---
tags: [moc, index]
description: ひだまりこそだち Vault の全体マップ。ここを起点に各ノートへ移動
---

# 🌅 ひだまりこそだち Vault

> 子育て支援サービス「ひだまりこそだち」の知識ベース。
> このノートを **Obsidian のトップ画面** として、必要な情報へ辿ってください。

---

## 📌 まず読むもの

- [[README]] — プロジェクト概要
- [[CLAUDE]] — Claude Code への委譲ルール
- [[VAULT_GUIDE]] — この Vault の使い方・記法ルール

---

## 🎯 事業戦略

- [[roadmap]] — 月¥30万までの4フェーズロードマップ
- [[persona_v0]] — 2ペルソナ（0-2歳 / 3-6歳）
- [[product_v0]] / [[product_v0_1]] / **[[product_v0_2]]** ← 現行仕様
- [[pre_phase1_decisions]] — 事前意思決定49項目

---

## 🏃 Phase 1 実行

- [[phase1_sprint]] — 4週間スプリント計画
- [[phase1_go_nogo]] — Go/No-Go 契約書（CEO 署名待ち）
- [[ceo_self_management_v0]] — CEO 自己経営（CEO 記入待ち）
- [[interview_form_v0]] — Google Form 設計

---

## 🌿 ブランド・アイデンティティ

- [[service_name_candidates_v3]] — 命名旅程（最終: ひだまりこそだち）
- [[handle_availability_hidamari_kosodachi]] — 商標・ハンドル空き調査
- [[sns_profile_common]] — SNS 共通指針
- [[auto_posting_v0]] — 自動投稿パイプライン

---

## 💬 SNS 別アセット

### note
- [[note/profile_v0]] — プロフィール3版
- [[note/manifesto_v0]] — マニフェスト記事（投稿準備済）

### X (Twitter)
- [[x/profile_v0]] — プロフィール
- [[x/opening_posts_v0]] — オープニング5本

### Instagram
- [[instagram/profile_v0]] — プロフィール

### Threads
- [[threads/profile_v0]] — プロフィール

### 戦略
- [[sns_strategy_v0]] — 集客チャネル戦略

---

## 📚 ナレッジベース

- **[[knowledge_architecture]] — 3層構造の全体像**（Memory + docs/knowledge + agentmemory）
- [[agentmemory_setup]] — agentmemory MCP セットアップ手順
- [[education_theories/README|世界の教育理論一覧]] — Day 1 完了済（20理論 + 補助9件）
- _Day 2-7 で各理論の詳細ページを追加予定_
- _今後: docs/knowledge/papers/ に海外論文の整理ページ_

---

## 🤖 Claude Code 構成

### エージェント
- [[ceo|CEO エージェント定義]]

### スキル
- [[skills/README|スキル一覧]]
- [[post-threads]] / [[post-note]] / [[post-instagram]] — 自動投稿
- [[show-x-today]] — X 手動投稿支援
- [[draft-posts]] — バッチドラフト生成

### スクリプト
- `scripts/post_threads.py` / `scripts/post_note.py` / `scripts/post_instagram.py`
- `scripts/lib/draft_loader.py` / `scripts/lib/r2_uploader.py`
- `scripts/meta_token_refresh.py`

---

## 🎨 ブランド資産

- `assets/logo/mark_v0_a_sun_sprout.svg` — 採用ロゴ（太陽 + 親子3株）
- `assets/logo/mark_v0_b_engawa.svg` — 候補B（縁側）
- `assets/logo/mark_v0_c_hi_monogram.svg` — 候補C（モノグラム）

---

## 📋 タグ索引

- `#strategy` — 事業戦略系
- `#brand` — ブランディング系
- `#phase1` — Phase 1 実行系
- `#sns` — SNS 運用系
- `#knowledge` — ナレッジベース
- `#decision-log` — 意思決定記録
- `#draft` — ドラフト状態
- `#approved` — 承認済み

---

## 🕒 タイムライン

- 2026-05-13: プロジェクト立ち上げ、戦略文書一式作成、SNS アカウント開設
- 2026-05-14: ロゴ確定、自動投稿実装、Vault 化、ナレッジ蓄積開始
- _Phase 1 完了予定: 2026-06-10_
