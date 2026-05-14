---
tags: [meta, vault-guide]
description: ひだまりこそだち Vault の運用ルールと記法
---

# 📖 Vault 運用ガイド

> このリポジトリは **Obsidian Vault** として使えます。人間（CEO）と Claude Code が同じ Markdown ファイル群を共同編集する構成です。

---

## 🏗 アーキテクチャ

```
あなた（CEO）
  ├─→ Obsidian で .md を直接編集
  │
  └─→ Claude Code（AI オーケストレータ）に依頼
         └─→ Filesystem 経由で .md を読み書き
              ↓
         同じ Vault（child_rearing_support_project/）
              ↑
      Claude Code は Working Memory（~/.claude/projects/.../memory/）を別途保持
```

---

## 🚀 Obsidian の開き方（CEO 向け）

1. **Obsidian をインストール**（無料）: https://obsidian.md/download
2. Obsidian 起動 → `Open folder as vault`
3. 以下のパスを選択：
   - WSL: `\\wsl$\Ubuntu\home\fugashiojiri\child_rearing_support_project\`
   - Linux/Mac: `/home/fugashiojiri/child_rearing_support_project/`
4. 起点ノート: [[MOC]] を開く

---

## 📝 記法ルール

### Wiki-link（ノート間リンク）

```markdown
[[persona_v0]]                  ← ノートへ移動（自動補完）
[[product_v0_2|現行プロダクト仕様]]  ← エイリアス表示
[[education_theories/README]]    ← サブフォルダ内の場合
```

クリックで遷移、グラフビューで可視化、バックリンクが自動収集される。

### タグ

```markdown
#strategy #phase1 #brand
```

ファイル本文または front-matter に書く。Obsidian のタグペインで一覧。

### Front-matter（YAML メタデータ）

各ノートの先頭にこの形式で記述：

```markdown
---
tags: [strategy, phase1]
status: draft | approved | archived
date: 2026-05-14
related: [[persona_v0]] [[product_v0_2]]
---

# 本文
```

任意ですが、推奨。Obsidian の Dataview プラグインで一覧表化できる。

---

## 📁 推奨フォルダ構成

```
child_rearing_support_project/   ← Vault ルート
├── MOC.md                       ← 起点ノート（必ずここから開く）
├── VAULT_GUIDE.md               ← この文書
├── README.md                    ← プロジェクト概要
├── CLAUDE.md                    ← Claude Code 委譲ルール
├── docs/                        ← 戦略・設計・実行文書
│   ├── roadmap.md
│   ├── persona_v0.md
│   ├── product_v0_*.md
│   ├── phase1_*.md
│   ├── note/                    ← note プラットフォーム別アセット
│   ├── x/                       ← X プラットフォーム別アセット
│   ├── instagram/
│   ├── threads/
│   ├── knowledge/               ← ナレッジベース（教育理論等）
│   └── drafts/                  ← 投稿ドラフト置き場
├── assets/                      ← ロゴ・画像
├── scripts/                     ← Python 実装（Obsidian では参照のみ）
└── .obsidian/                   ← Obsidian 設定（一部 .gitignore）
```

---

## ✍️ 新規ノートの書き方

### 1. 新規ファイル作成時
- 場所: 内容に応じて適切なフォルダへ
  - 戦略 → `docs/`
  - SNS 別 → `docs/{platform}/`
  - 知識 → `docs/knowledge/{topic}/`
- ファイル名: スネークケース or kebab-case（例: `phase2_plan.md`）

### 2. 必ず冒頭に front-matter を入れる
```markdown
---
tags: [tag1, tag2]
status: draft
date: 2026-05-14
---
```

### 3. MOC への追加
新規ノートを作ったら [[MOC]] の該当セクションにリンクを追加すると、検索性が上がる。

---

## 🤖 Claude Code との協働

### CEO（人間）が編集する場合
- Obsidian で直接編集
- 変更は即座にディスクに反映される
- Claude Code が同じファイルを読みに行く時は、最新の編集が見える

### Claude Code が編集する場合
- セッションで「これを編集して」と依頼
- Read / Edit / Write ツールでファイル操作
- Obsidian 側もファイル変更を自動検知してリロード

### 衝突回避
- **同時に同じファイルを編集しない**（基本ルール）
- Obsidian で編集中は Claude Code に依頼しない
- 依頼直後は Obsidian の表示をリロードして最新を確認

---

## 🧠 Claude Code の Memory との関係

Claude Code には2層の記憶がある：

| 記憶層 | 保存場所 | 役割 |
|---|---|---|
| **Vault**（このリポジトリ） | `child_rearing_support_project/` | 全員で共有する正式ドキュメント |
| **Memory**（Claude 専用） | `~/.claude/projects/.../memory/` | Claude が次回セッションで思い出す個人的メモ |

→ Vault は「公式記録」、Memory は「Claude のメモ帳」。役割を分ける。

CEO が Obsidian で見るのは **Vault のみ**。Memory は Claude Code 内部の挙動。

---

## 🔌 推奨プラグイン（Phase 2 以降）

導入時期は CEO 判断。すべて無料：

- **Dataview** — ノートをデータベース的に検索・集計（タグや front-matter で）
- **Templater** — テンプレートからノート生成
- **Calendar** / **Daily Notes** — 日次振り返り
- **Excalidraw** — 図解作成

---

## 📊 グラフビュー活用

Obsidian の Graph View（左サイドバーの📊アイコン）で、Wiki-link で繋がったノートのネットワーク図が表示される。

- Phase 1 完了時点でグラフが密になっているか確認
- 孤立しているノートがあれば、MOC や関連ノートからリンクを追加
- カテゴリでフィルタ可能

---

## 🧹 メンテナンス

- **週次**: MOC を見直し、新規ノートへのリンクを追加
- **月次**: 不要ノートを `archive/` に移動（削除はしない、履歴として保持）
- **四半期**: タグの整理、用途不明タグの削除

---

## ❓ よくある質問

**Q. Vault と Git は両立する？**
A. はい。Vault は Markdown ファイル群なので、Git で完全に管理可能。.obsidian/ のうち workspace.json などは .gitignore 済み。

**Q. Obsidian なしでも使える？**
A. はい。すべて Markdown ファイルなので、VS Code / vim / 任意のテキストエディタでも編集可能。Obsidian はあくまで便利な UI。

**Q. Wiki-link は Markdown 標準ではないが？**
A. `[[]]` 記法は Obsidian / Roam Research 等で標準的。GitHub では表示されないが、リンク先のファイルパスは判別可能。`useMarkdownLinks: false` で `[[]]` を維持する設定。

**Q. 既存ファイルにすべて front-matter を追加すべき？**
A. 必須ではない。新規ノートから順次適用、既存は時間がある時にバックフィルで十分。
