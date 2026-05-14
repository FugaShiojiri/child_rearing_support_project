---
tags: [meta, knowledge, architecture]
status: active
date: 2026-05-14
related: [[VAULT_GUIDE]] [[agentmemory_setup]]
---

# 知識ベース 3層アーキテクチャ

> ひだまりこそだち プロジェクトの知識を「**スケールに応じた3つの層**」で管理する設計。
> CEO 確定（2026-05-14）。

---

## 全体像

```
┌──────────────────────────────────────────────────┐
│                                                  │
│    あなた（CEO）                                 │
│       ↕                                          │
│    Obsidian（人間の編集 UI）                     │
│       ↕                                          │
│   ┌──────────────────────────────────────┐       │
│   │ Layer 2: docs/knowledge/             │       │
│   │ （整理されたノート、Wiki-link 化）   │       │
│   └────────┬─────────────────────────────┘       │
│            ↕  Read/Write                         │
│   ┌────────────────────────────────────────────┐ │
│   │    Claude Code（AI オーケストレータ）      │ │
│   └───┬──────────────────────────────────────┬─┘ │
│       ↕                                      ↕   │
│  ┌──────────────────────┐  ┌──────────────────┐  │
│  │ Layer 1: Memory      │  │ Layer 3:         │  │
│  │ ~/.claude/projects/  │  │ agentmemory MCP  │  │
│  │ .../memory/          │  │ (SQLite+Vector)  │  │
│  │                      │  │                  │  │
│  │ CEO の好み・確定事項 │  │ 論文本文・大量   │  │
│  │ （小・常駐）         │  │ データ（大・検索）│ │
│  └──────────────────────┘  └──────────────────┘  │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 各層の役割

### Layer 1: Memory（小・常駐）

| 項目 | 内容 |
|---|---|
| 場所 | `~/.claude/projects/-home-fugashiojiri-child-rearing-support-project/memory/` |
| 形式 | Markdown ファイル（frontmatter 付き） |
| サイズ目安 | 1ファイル数百字、合計 <50KB |
| 読み込み | Claude Code セッション開始時に自動 |
| 適した内容 | CEO の好み、プロジェクト現状、確定事項、フィードバック |
| 編集者 | Claude が自動更新、CEO が直接編集することもある |

**保存判断**: 「次回セッションで思い出すべき短い事実」のみ。長文・参考資料は入れない。

### Layer 2: docs/knowledge/（中・人間が読む）

| 項目 | 内容 |
|---|---|
| 場所 | `docs/knowledge/` 配下（Vault 内） |
| 形式 | Markdown、Wiki-link 化、frontmatter 推奨 |
| サイズ目安 | 1ノート 1000〜5000字、合計 数MB |
| 読み込み | Claude は Read tool で必要時に参照、Obsidian で人間が読む |
| 適した内容 | 教育理論の整理ページ、論文要約・引用集、ペルソナ示唆 |
| 編集者 | CEO と Claude の両方 |

**保存判断**: 「人間が読めて、引用可能で、構造化された知識」

**現状の主要コンテンツ**:
- [[education_theories/README|教育理論一覧]] - 主要20件 + 補助9件

**今後の予定**:
- `docs/knowledge/education_theories/{theory}.md` - 親和性◎理論の詳細
- `docs/knowledge/papers/{topic}/{author_year}.md` - 論文の整理ページ
- `docs/knowledge/research/` - 実験・調査結果のまとめ

### Layer 3: agentmemory（大・AI 検索）

| 項目 | 内容 |
|---|---|
| 場所 | local SQLite + Vector DB（agentmemory worker が管理） |
| 形式 | 構造化されたメモリレコード（自動圧縮対応） |
| サイズ目安 | 数百MB 〜 数GB（論文蓄積想定） |
| 読み込み | Claude が MCP ツール経由で semantic 検索 |
| 適した内容 | 論文本文、実験データ詳細、過去セッション自動キャプチャ |
| 編集者 | Claude が自動管理、CEO は import コマンドで投入 |

**保存判断**: 「全文検索が必要で、Obsidian で読むには量が多すぎるデータ」

**セットアップ**: [[agentmemory_setup]] 参照

---

## 海外論文の取り込み標準フロー

CEO 確定方針：情報蓄積を進める中で、以下の二重保管を標準にする。

```
論文 PDF/テキスト発見
       ↓
┌──────────────────────────────────────┐
│ Step 1: 整理ページを作成 (Layer 2)   │
│ docs/knowledge/papers/                │
│   {topic}/{author_year}.md           │
│                                       │
│ - タイトル・著者・年・出典           │
│ - 要旨（500-1000字）                 │
│ - 「ひだまりこそだち への示唆」      │
│ - 関連 Wiki-link                     │
│                                       │
│ → 人間が読めて、引用できる         │
└──────────────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ Step 2: 本文を ingest (Layer 3)      │
│ agentmemory MCP ツールで本文投入     │
│                                       │
│ - 全文を semantic 検索可能化         │
│ - 過去セッションとの関連も自動抽出   │
│                                       │
│ → AI が必要時に該当箇所を抽出     │
└──────────────────────────────────────┘
```

---

## どこに何を書くかの判断フロー

```
新しい情報が出てきた
       ↓
[Q1] 短い事実 or 設定？
  Yes → Layer 1 (memory) ✓
  No ↓
       ↓
[Q2] 人間が後で読みたい構造化情報？
  Yes → Layer 2 (docs/knowledge/) ✓
  Maybe → Layer 2 + Layer 3 の両方
  No ↓
       ↓
[Q3] 大量の本文・データ？
  Yes → Layer 3 (agentmemory) ✓
  No → どこにも書かない（一時的な情報）
```

---

## アンチパターン（避けるべきこと）

❌ **Memory に論文本文を入れる** → サイズ過大で毎セッションのトークン消費爆発

❌ **agentmemory のみで知識管理** → 人間が読めない、Obsidian で確認できない

❌ **docs/knowledge/ に大量論文本文を直接置く** → grep ベースの検索で苦戦、Git 容量肥大

❌ **3層に同じ情報を重複保存** → 更新時の同期負担、矛盾の温床

✅ **正しい運用**: 整理（Layer 2）+ 本文（Layer 3）の二重保管、Layer 1 は最小限

---

## 関連ドキュメント

- [[VAULT_GUIDE]] - Obsidian Vault の使い方
- [[agentmemory_setup]] - Layer 3 のセットアップ手順
- [[education_theories/README]] - Layer 2 の代表例
- [[MOC]] - Vault 全体マップ
