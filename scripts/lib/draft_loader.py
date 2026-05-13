"""
==============================================================================
ひだまりこそだち 自動投稿 共通ヘルパー (draft_loader)
------------------------------------------------------------------------------
用途:
    docs/drafts/<platform>/ 以下の Markdown ドラフトファイルを読み込み、
    frontmatter と本文を分離し、approved=true のもののみを
    各プラットフォームの投稿スクリプトに渡す。

前提:
    - ドラフトファイルは YAML frontmatter 付き Markdown
    - パスは docs/drafts/<platform>/YYYY-MM-DD[-suffix].md
    - python-frontmatter ライブラリを利用

実行例:
    >>> from scripts.lib.draft_loader import load_drafts
    >>> drafts = load_drafts("threads", "2026-05-14")

関連 .env キー: なし（共通ライブラリ）
==============================================================================
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import frontmatter  # python-frontmatter
except ImportError:  # pragma: no cover
    frontmatter = None  # type: ignore[assignment]


logger = logging.getLogger(__name__)


# プロジェクトルート（このファイルは scripts/lib/draft_loader.py）
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
DRAFTS_ROOT: Path = PROJECT_ROOT / "docs" / "drafts"
POSTED_LOG_ROOT: Path = PROJECT_ROOT / "docs" / "posted_log"

SUPPORTED_PLATFORMS = ("x", "threads", "note", "instagram")
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-.+)?\.md$")


@dataclass
class Draft:
    """1件のドラフト（frontmatter + 本文 + パス）を表す。

    Attributes:
        frontmatter: YAML frontmatter を辞書化したもの。
        body: frontmatter を除いた本文（Markdown）。
        path: ファイルパス（絶対パス）。
    """

    frontmatter: dict[str, Any] = field(default_factory=dict)
    body: str = ""
    path: Path = field(default_factory=Path)

    @property
    def approved(self) -> bool:
        """approved フラグ。明示的に True のときのみ True を返す。"""
        return bool(self.frontmatter.get("approved", False)) is True

    @property
    def hashtags(self) -> list[str]:
        """ハッシュタグ配列。frontmatter に無ければ空リスト。"""
        tags = self.frontmatter.get("hashtags") or []
        if isinstance(tags, str):
            return [tags]
        return [str(t) for t in tags]

    @property
    def image(self) -> str | None:
        """画像パス or URL（Instagram 用、無ければ None）。"""
        v = self.frontmatter.get("image")
        return None if v in (None, "", "null") else str(v)

    @property
    def images(self) -> list[str]:
        """画像複数指定（Instagram カルーセル）。``images`` が無ければ ``image`` を1要素で返す。"""
        v = self.frontmatter.get("images")
        if isinstance(v, list) and v:
            return [str(x) for x in v if x]
        img = self.image
        return [img] if img else []


def parse_markdown_with_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Markdown テキストから frontmatter と本文を分離する。

    Args:
        text: ``---`` で囲まれた YAML frontmatter を含む Markdown テキスト。

    Returns:
        (frontmatter dict, body 文字列) のタプル。
        frontmatter が無い場合は空 dict と元テキストを返す。
    """
    if frontmatter is None:
        raise RuntimeError(
            "python-frontmatter が未インストールです。"
            "`pip install -r scripts/requirements.txt` を実行してください。"
        )
    post = frontmatter.loads(text)
    return dict(post.metadata), post.content


def load_drafts(platform: str, date: str) -> list[Draft]:
    """指定プラットフォーム・日付の承認済みドラフト一覧を返す。

    Args:
        platform: ``threads`` / ``note`` / ``instagram`` / ``x`` のいずれか。
        date: ``YYYY-MM-DD`` 形式の日付。

    Returns:
        approved=true のドラフトのみのリスト（昇順）。

    Raises:
        ValueError: platform が未対応のとき。
        FileNotFoundError: ドラフトフォルダが存在しないとき。
    """
    if platform not in SUPPORTED_PLATFORMS:
        raise ValueError(
            f"未対応プラットフォーム: {platform!r} "
            f"(対応: {', '.join(SUPPORTED_PLATFORMS)})"
        )
    _validate_date(date)

    folder = DRAFTS_ROOT / platform
    if not folder.exists():
        raise FileNotFoundError(f"ドラフトフォルダがありません: {folder}")

    all_drafts = _collect_drafts_for_date(folder, date)
    approved = [d for d in all_drafts if d.approved]

    logger.info(
        "drafts loaded: platform=%s date=%s total=%d approved=%d",
        platform,
        date,
        len(all_drafts),
        len(approved),
    )
    return approved


def _collect_drafts_for_date(folder: Path, date: str) -> list[Draft]:
    """指定フォルダ内の YYYY-MM-DD で始まるファイルを全て読み込む。

    Args:
        folder: 走査対象フォルダ。
        date: 日付（``YYYY-MM-DD``）。

    Returns:
        Draft のリスト（ファイル名昇順）。
    """
    drafts: list[Draft] = []
    for path in sorted(folder.glob(f"{date}*.md")):
        m = DATE_RE.match(path.name)
        if not m or m.group(1) != date:
            continue
        try:
            text = path.read_text(encoding="utf-8")
            fm, body = parse_markdown_with_frontmatter(text)
        except Exception as exc:  # noqa: BLE001
            logger.warning("ドラフト読み込み失敗 %s: %s", path, exc)
            continue
        drafts.append(Draft(frontmatter=fm, body=body.strip(), path=path))
    return drafts


def _validate_date(date: str) -> None:
    """日付文字列が ``YYYY-MM-DD`` 形式かをバリデーション。"""
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(
            f"--date は YYYY-MM-DD 形式で指定してください: {date!r}"
        ) from exc


def log_post(platform: str, result: dict[str, Any]) -> Path:
    """投稿結果を ``docs/posted_log/<platform>.jsonl`` に追記する。

    Args:
        platform: プラットフォーム名。
        result: 記録するレコード（dict）。
            最低限 ``date`` / ``post_id`` / ``draft_path`` を含めること。

    Returns:
        書き込んだログファイルのパス。
    """
    POSTED_LOG_ROOT.mkdir(parents=True, exist_ok=True)
    log_path = POSTED_LOG_ROOT / f"{platform}.jsonl"

    record = dict(result)
    record.setdefault("platform", platform)
    record.setdefault("posted_at", datetime.now(timezone.utc).isoformat())

    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    logger.info("投稿ログ追記: %s", log_path)
    return log_path


def configure_logging(level: str | None = None) -> None:
    """ルートロガーを最小構成でセットアップする。

    Args:
        level: ``DEBUG``/``INFO``/``WARNING``/``ERROR``。省略時は ``INFO``。
    """
    lv = (level or "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, lv, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def print_dry_run_notice() -> None:
    """dry-run モード時の案内メッセージを表示する。"""
    print(
        "\n[dry-run] 実投稿は行いませんでした。"
        "実投稿するには --commit を付けてください。\n"
    )


def truncate_for_log(text: str, limit: int = 80) -> str:
    """ログ出力用に長い文字列を切り詰める。"""
    text = text.replace("\n", " ")
    return text if len(text) <= limit else text[: limit - 1] + "…"
