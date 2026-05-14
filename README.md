---
tags: [meta, readme]
description: ひだまりこそだち プロジェクトのエントリーポイント
---

# ひだまりこそだち（hidamari kosodachi）

> 「ひだまり」（陽の当たる温かい場所）と「こそだち」（子育ち＋子育て）を重ねた合成造語。
> 温かい陽だまりのような場所で、親子が自分のペースで育つ ― 0〜6歳児の保護者向け子育て支援サービス。

---

## 🗺️ ナビゲーション

このリポジトリは **Obsidian Vault** としても機能します。

- **全体マップ**: [[MOC|MOC（Map of Content）]]
- **Vault の使い方**: [[VAULT_GUIDE]]
- **Claude Code への委譲ルール**: [[CLAUDE]]

---

## 📌 主要ドキュメント

| 領域 | ファイル |
|---|---|
| 事業戦略 | [[docs/roadmap]] |
| ペルソナ | [[docs/persona_v0]] |
| プロダクト仕様 | [[docs/product_v0_2]] |
| Phase 1 計画 | [[docs/phase1_sprint]] |
| Go/No-Go 契約 | [[docs/phase1_go_nogo]] |

詳しい全体像は [[MOC]] を参照してください。

---

## 🚀 開発・運用

- **Python スクリプト**: `scripts/` 配下に自動投稿実装（Threads / note / Instagram）
- **Claude Code スキル**: `.claude/skills/` 配下に投稿コマンド群
- **環境変数**: `.env.example` をコピーして `.env` を作成
- **依存インストール**: `pip install -r scripts/requirements.txt`

---

## 📜 制約

このプロジェクトの設計・運用は以下の原則に従う：

- 課金は **Claude Code Max のみ**（他の有料 SaaS は不採用）
- 人手介入を最小化（自動化前提）
- 販売・配信コンテンツは CEO が目視確認
- 公的資料（文科省・こども家庭庁等）を引用ベースに使用

詳細: [[CLAUDE]] / [[docs/pre_phase1_decisions]]

---

## 🤖 Generated with Claude Code

このリポジトリは [Claude Code](https://claude.com/claude-code) を活用して構築しています。
