# Hidamari Kosodachi 自動投稿スキル

ひだまりこそだちプロジェクトの SNS 投稿パイプラインを Claude Code Skills として実装したもの。バッチ生成 → CEO レビュー → 承認 → 投稿の流れを slash command で操作する。

## 利用可能なスキル

| コマンド | 用途 | 自動化レベル |
|---|---|---|
| `/draft-posts --days 7` | 7日分のドラフトを全プラットフォーム横断で生成 | 自動 |
| `/show-x-today` | 今日の X 投稿（承認済み）を表示してコピペ準備 | 表示のみ |
| `/post-threads --date YYYY-MM-DD` | Threads に自動投稿 | 自動 |
| `/post-note --date YYYY-MM-DD` | note に下書き保存（公開は手動） | 半自動 |
| `/post-instagram --date YYYY-MM-DD` | Instagram に自動投稿（R2 経由） | 自動 |

## 標準ワークフロー

1. **バッチ生成（週次）**: 日曜夜などに `/draft-posts --days 7` を実行し、翌週1週間分のドラフトを生成する。すべて `approved: false` で保存される。
2. **CEO レビュー**: `docs/drafts/<platform>/YYYY-MM-DD.md` を開き、内容を確認・修正する。OK なものは frontmatter の `approved: true` に書き換える。Instagram は `image:` を実画像パスに差し替える。
3. **投稿（日次）**:
   - 朝: `/show-x-today` で X 投稿候補を表示し、スマホで手動コピペ。
   - 任意のタイミング: `/post-threads --date 2026-05-14` で Threads に自動投稿。
   - note 公開日: `/post-note --date 2026-05-14` で下書き保存 → note 上で最終確認して手動公開。
   - Instagram: `/post-instagram --date 2026-05-14` で自動投稿。
4. **ログ確認**: `docs/posted_log/<platform>.jsonl` に投稿履歴が追記される（X のみ手動）。

## プラットフォーム別の方針

| プラットフォーム | 投稿方式 | 理由 |
|---|---|---|
| X | 手動コピペ（`show-x-today` で支援） | API 課金回避 |
| Threads | API 自動投稿 | 無料 API あり |
| note | Playwright で下書き保存のみ | API なし・誤公開リスク回避 |
| Instagram | Meta Graph API + R2 | 画像配信に public URL が必要 |

## 注意事項

- **approved gate**: すべての自動投稿スキルは `approved: true` のドラフトのみを処理する。`false` または未設定は投稿されない。
- **dry-run**: 各スクリプトは `--commit` フラグなしで実行すると dry-run になる（実投稿しない）。スキルは原則 `--commit` 付きで呼ぶ。デバッグ時は手動で `--commit` を外して `python scripts/post_<platform>.py --date YYYY-MM-DD` を実行。
- **トークン更新**: Threads / Meta のアクセストークンは長期トークン（60日）。期限切れ前に再発行が必要。401 / 190 エラー時の対処は各スキルの「失敗時の挙動」を参照。
- **note UI 変更**: note は公式 API がなく Playwright によるブラウザ操作のため、UI 変更でセレクターが壊れる可能性がある。失敗時は `scripts/post_note.py` のセレクター定義を更新する。
- **画像準備**: Instagram の画像は `docs/drafts/instagram/assets/YYYY-MM-DD.jpg` に CEO が事前配置する。`draft-posts` はプレースホルダーのみ生成。
- **重複投稿防止**: 投稿スクリプトは `docs/posted_log/<platform>.jsonl` を読み、同一日付・同一本文の重複投稿をスキップする（実装は `scripts/lib/draft_loader.py` 参照）。

## 関連ドキュメント

- 設計書: `docs/auto_posting_v0.md`
- ペルソナ: `docs/persona_v0.md`
- プロダクト方針: `docs/product_v0_2.md`
- SNS 戦略: `docs/sns_strategy_v0.md`
