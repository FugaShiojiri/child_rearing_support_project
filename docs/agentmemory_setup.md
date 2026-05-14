---
tags: [infrastructure, agentmemory, setup]
status: active
date: 2026-05-14
related: [[VAULT_GUIDE]] [[knowledge_architecture]]
---

# agentmemory セットアップガイド

> **ひだまりこそだち の知識ベース3層構造のうち、Layer 3（AI セマンティック検索）** を担うコンポーネントの導入手順。
> リポジトリ: https://github.com/rohitg00/agentmemory（Apache-2.0、無料）

---

## 何ができるようになるか

- **論文・大量テキストの semantic 検索**: 「アタッチメント理論で〇〇に関する記述」のような曖昧クエリで該当箇所を即抽出
- **過去セッションの自動キャプチャ**: 12個のフックが Claude Code の作業を記録
- **メモリ階層**: Working → Episodic → Semantic → Procedural の4段階で自動整理
- **ハイブリッド検索**: BM25（キーワード）+ Vector（意味）+ Graph（関係）の融合
- **51個の MCP ツール** が Claude Code から使えるようになる

---

## 前提環境

| 項目 | 必要 | 現状 |
|---|---|---|
| Node.js | ≥20 | ✅ v24.14.1 |
| npm | あれば | ✅ 11.11.0 |
| ローカル埋め込みモデル | `all-MiniLM-L6-v2`（自動 DL、無料） | 初回起動時に取得 |
| LLM プロバイダ | **不要**（デフォルトでは LLM 呼び出しなし） | - |

---

## セットアップ手順（3 ステップ）

### Step 1: ワーカー起動

**専用のターミナルを1つ確保** して、以下を実行：

```bash
cd /home/fugashiojiri/child_rearing_support_project
npx @agentmemory/agentmemory
```

- 初回は依存ダウンロード（iii-engine v0.11.2 等、数十秒）
- ポート 3111 で REST API が起動
- **このターミナルは閉じない**（worker が止まると Claude Code から使えなくなる）

### Step 2: 動作確認

別のターミナルで：

```bash
npx @agentmemory/agentmemory doctor
```

✅ "Server reachable" になっていれば OK。

オプション: 動作デモを見る：
```bash
npx @agentmemory/agentmemory demo
```
→ サンプルセッションを seed して、semantic recall の動作を 30 秒で体験

### Step 3: Claude Code に MCP プラグインを登録（CEO 作業）

Claude Code セッション内で：

```
/plugin marketplace add rohitg00/agentmemory
```

これにより自動的に：
- 12 個のフック（PostToolUse 等で自動キャプチャ）
- 4 個のスキル
- 51 個の MCP ツール

が登録される。`.mcp.json` も自動配置される。

---

## 起動の永続化（推奨）

毎回手動でターミナルを開きたくない場合、以下のいずれか：

### 方法 A: systemd ユーザーサービス（WSL/Linux 推奨）

`~/.config/systemd/user/agentmemory.service` を作成：

```ini
[Unit]
Description=agentmemory worker

[Service]
ExecStart=/usr/bin/env npx @agentmemory/agentmemory
Restart=on-failure
WorkingDirectory=%h/child_rearing_support_project

[Install]
WantedBy=default.target
```

起動：
```bash
systemctl --user enable --now agentmemory
```

### 方法 B: tmux/screen で常駐

```bash
tmux new -d -s agentmemory 'cd ~/child_rearing_support_project && npx @agentmemory/agentmemory'
```

確認：
```bash
tmux ls
tmux attach -t agentmemory
```

### 方法 C: シンプルにバックグラウンド（セッション限定）

```bash
nohup npx @agentmemory/agentmemory > ~/.agentmemory.log 2>&1 &
disown
```

---

## 過去ログの取り込み（任意）

Claude Code の過去セッション JSONL を agentmemory に取り込んで、過去の会話を semantic 検索できる：

```bash
npx @agentmemory/agentmemory import-jsonl
```

デフォルトでは `~/.claude/projects` から取得。最大200ファイルまで。本プロジェクトは既にかなりの会話蓄積があるため、Phase 1 終了後にまとめて取り込むのも有効。

---

## 3層構造の使い分け

| Layer | 場所 | 用途 |
|---|---|---|
| **Memory** | `~/.claude/projects/.../memory/` | CEO の好み、確定事項、現状 |
| **docs/knowledge/** | `docs/knowledge/` | 整理されたノート、論文要約、Wiki-link で連携 |
| **agentmemory** | local SQLite + Vector DB | 論文本文、過去セッション、大量データの semantic 検索 |

論文を取り込む時の標準フロー：
1. PDF/テキストを取得
2. `docs/knowledge/papers/{topic}/{author_year}.md` に整理ページ作成（人間が読む用）
3. `agentmemory` MCP ツールで本文を ingest（AI 検索用）

---

## トラブルシューティング

### "iii.exe not found" (Windows/WSL)

```bash
# ~/.local/bin に PATH を通す
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### ポート 3111 が使用中

```bash
npx @agentmemory/agentmemory --port 3222
```
環境変数 `AGENTMEMORY_URL=http://localhost:3222` も設定。

### 動作が重い・ストレージ肥大化

- 自動圧縮を有効化（デフォルト OFF）:
  ```bash
  AGENTMEMORY_AUTO_COMPRESS=true npx @agentmemory/agentmemory
  ```
- 古いメモリは TTL で自動失効する設計

### Claude Code から MCP ツールが見えない

1. ワーカーが起動しているか: `npx @agentmemory/agentmemory status`
2. `.mcp.json` が配置されているか: `cat .mcp.json`
3. Claude Code を再起動

---

## セキュリティ・プライバシー

- すべてローカル（SQLite + 埋め込み）
- 外部 API を叩かないデフォルト設定
- `AGENTMEMORY_ALLOW_AGENT_SDK=true` は**設定しない**（再帰リスク #149）
- 本プロジェクトの方針「Claude Code Max 以外課金不可」と完全整合

---

## 関連ドキュメント

- [[knowledge_architecture]] — 3層構造の全体像
- [[VAULT_GUIDE]] — Obsidian Vault の運用ルール
- 公式: https://github.com/rohitg00/agentmemory
