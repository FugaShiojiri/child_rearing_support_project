"""
==============================================================================
Meta 長期トークン更新スクリプト
------------------------------------------------------------------------------
用途:
    Meta（Threads / Instagram）の長期アクセストークンは約60日で失効する。
    本スクリプトを月1回程度実行することで、現在のトークンを
    「同じ長期トークン」として更新（リフレッシュ）し、有効期限を延長する。

    参考: https://developers.facebook.com/docs/instagram-basic-display-api/guides/long-lived-access-tokens
    （Threads/Instagram Graph も同様のリフレッシュエンドポイントを提供）

前提:
    - `.env` に有効な長期 META_ACCESS_TOKEN が設定済み
    - 短期 → 長期の初回変換は別途 Meta for Developers の Graph Explorer
      または専用フローで取得しておくこと

実行例:
    # dry-run（リクエストは送らず、何をするか表示）
    python scripts/meta_token_refresh.py

    # 実行（API 呼び出し + .env 書き換え）
    python scripts/meta_token_refresh.py --commit

    # .env を書き換えず標準出力に新トークンを出すだけ
    python scripts/meta_token_refresh.py --commit --print-only

関連 .env キー:
    META_ACCESS_TOKEN  （読み込み + 書き換え対象）
==============================================================================
"""
from __future__ import annotations

import logging
import os
import re
import sys
from pathlib import Path

import click
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.lib.draft_loader import configure_logging  # noqa: E402


logger = logging.getLogger("meta_token_refresh")


REFRESH_ENDPOINT = "https://graph.threads.net/refresh_access_token"
# 互換: Instagram Graph 用 (https://graph.instagram.com/refresh_access_token)
# Threads 用エンドポイントを既定とする。


def refresh_token(current_token: str) -> dict:
    """Threads / Instagram の長期トークンをリフレッシュする。

    Args:
        current_token: 現在の長期アクセストークン。

    Returns:
        API レスポンス JSON（``access_token``, ``token_type``, ``expires_in``）。
    """
    import requests

    params = {
        "grant_type": "th_refresh_token",
        "access_token": current_token,
    }
    logger.info("リフレッシュリクエスト: %s", REFRESH_ENDPOINT)
    r = requests.get(REFRESH_ENDPOINT, params=params, timeout=30)
    logger.info("status=%s body=%s", r.status_code, r.text)
    r.raise_for_status()
    return r.json()


def update_env_file(env_path: Path, new_token: str) -> None:
    """``.env`` ファイル内の ``META_ACCESS_TOKEN`` を新トークンに置き換える。

    Args:
        env_path: 対象 ``.env`` のパス。
        new_token: 新しいアクセストークン。

    Raises:
        FileNotFoundError: ``.env`` が存在しないとき。
    """
    if not env_path.exists():
        raise FileNotFoundError(f".env が見つかりません: {env_path}")

    text = env_path.read_text(encoding="utf-8")
    pattern = re.compile(r"^META_ACCESS_TOKEN=.*$", re.MULTILINE)
    if pattern.search(text):
        new_text = pattern.sub(f"META_ACCESS_TOKEN={new_token}", text)
    else:
        # 行が無ければ末尾に追加
        sep = "" if text.endswith("\n") or text == "" else "\n"
        new_text = f"{text}{sep}META_ACCESS_TOKEN={new_token}\n"

    backup = env_path.with_suffix(env_path.suffix + ".bak")
    backup.write_text(text, encoding="utf-8")
    env_path.write_text(new_text, encoding="utf-8")
    logger.info("env 更新完了: %s (バックアップ: %s)", env_path, backup)


@click.command(help="Meta 長期アクセストークンを更新する。")
@click.option(
    "--commit",
    is_flag=True,
    default=False,
    help="このフラグを付けると実際に API を呼び .env を書き換える。",
)
@click.option(
    "--print-only",
    is_flag=True,
    default=False,
    help=".env を書き換えず標準出力にだけ新トークンを表示。",
)
def main(commit: bool, print_only: bool) -> None:
    """CLI エントリポイント。"""
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(env_path)
    configure_logging(os.environ.get("LOG_LEVEL"))

    current = os.environ.get("META_ACCESS_TOKEN", "").strip()
    if not current:
        raise click.ClickException(
            "META_ACCESS_TOKEN が未設定です。`.env` に現行トークンを設定してください。"
        )

    if not commit:
        click.echo("=== Meta token refresh (dry-run) ===")
        click.echo(f"現行トークン（先頭8文字）: {current[:8]}…")
        click.echo(f"リフレッシュエンドポイント: {REFRESH_ENDPOINT}")
        click.echo("実行するには --commit を付けてください。")
        return

    data = refresh_token(current)
    new_token = data.get("access_token")
    if not new_token:
        raise click.ClickException(f"新トークン取得失敗: {data}")
    expires_in = data.get("expires_in")

    click.echo("=== Meta token refresh 成功 ===")
    click.echo(f"新トークン（先頭8文字）: {new_token[:8]}…")
    if expires_in:
        days = int(expires_in) // 86400
        click.echo(f"有効期限: {expires_in}秒（約{days}日）")

    if print_only:
        click.echo("\n[--print-only] .env は書き換えません。")
        click.echo(new_token)
        return

    update_env_file(env_path, new_token)
    click.echo(f".env を更新しました: {env_path}")


if __name__ == "__main__":
    main()
