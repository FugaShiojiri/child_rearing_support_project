"""
==============================================================================
Meta ID 取得ヘルパー（初回セットアップ用・読み取り専用）
------------------------------------------------------------------------------
用途:
    `.env` に長期 META_ACCESS_TOKEN を入れた後、本スクリプトを実行すると、
    投稿スクリプトに必要な以下の ID を Meta API から自動取得して表示する：
      - META_THREADS_USER_ID        （Threads 投稿に必要）
      - META_INSTAGRAM_BUSINESS_ID  （Instagram 投稿に必要）

    表示された行を `.env` にコピペすればセットアップ完了。
    Graph API Explorer を手で叩く必要をなくすためのもの（読み取りのみ・無害）。

前提:
    - `.env` に長期 META_ACCESS_TOKEN が設定済み
    - Threads 用と Instagram(Facebook Graph) 用でトークンが別アプリの場合がある。
      その場合は各トークンで2回実行し、解決できた ID だけ採用すればよい。

実行例:
    python scripts/meta_setup_ids.py

関連 .env キー:
    META_ACCESS_TOKEN（読み込みのみ）
==============================================================================
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

import click
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.lib.draft_loader import configure_logging  # noqa: E402


logger = logging.getLogger("meta_setup_ids")

THREADS_ME = "https://graph.threads.net/v1.0/me"
GRAPH_ME_ACCOUNTS = "https://graph.facebook.com/v20.0/me/accounts"


def fetch_threads_user_id(token: str) -> str | None:
    """Threads ユーザー ID を取得する。失敗時は None。"""
    import requests

    try:
        r = requests.get(
            THREADS_ME,
            params={"fields": "id,username", "access_token": token},
            timeout=30,
        )
        if not r.ok:
            logger.warning("Threads /me 失敗: status=%s body=%s", r.status_code, r.text)
            return None
        data = r.json()
        uid = data.get("id")
        if uid:
            click.echo(f"  Threads: @{data.get('username', '?')} (id={uid})")
        return uid
    except Exception as exc:  # noqa: BLE001
        logger.warning("Threads ID 取得でエラー: %s", exc)
        return None


def fetch_instagram_business_id(token: str) -> str | None:
    """Facebook ページに紐づく Instagram Business アカウント ID を取得。失敗時 None。"""
    import requests

    try:
        r = requests.get(
            GRAPH_ME_ACCOUNTS,
            params={
                "fields": "name,instagram_business_account",
                "access_token": token,
            },
            timeout=30,
        )
        if not r.ok:
            logger.warning(
                "Graph /me/accounts 失敗: status=%s body=%s", r.status_code, r.text
            )
            return None
        pages = r.json().get("data", [])
        for page in pages:
            iba = page.get("instagram_business_account")
            if iba and iba.get("id"):
                click.echo(
                    f"  Instagram: page='{page.get('name', '?')}' "
                    f"ig_business_id={iba['id']}"
                )
                return iba["id"]
        logger.warning(
            "Instagram Business アカウントに紐づくページが見つかりません。"
            "IGをプロアカウント化し Facebook ページに連携済みか確認してください。"
        )
        return None
    except Exception as exc:  # noqa: BLE001
        logger.warning("Instagram ID 取得でエラー: %s", exc)
        return None


@click.command(help="Meta トークンから Threads/Instagram の ID を取得して表示する。")
def main() -> None:
    """CLI エントリポイント（読み取り専用）。"""
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(env_path)
    configure_logging(os.environ.get("LOG_LEVEL"))

    token = os.environ.get("META_ACCESS_TOKEN", "").strip()
    if not token:
        raise click.ClickException(
            "META_ACCESS_TOKEN が未設定です。`.env` に長期トークンを入れてから実行してください。"
        )

    click.echo("=== Meta ID 取得（読み取り専用）===")
    click.echo("解決できた ID:")
    threads_id = fetch_threads_user_id(token)
    ig_id = fetch_instagram_business_id(token)

    click.echo("\n--- `.env` にコピペする行 ---")
    if threads_id:
        click.echo(f"META_THREADS_USER_ID={threads_id}")
    else:
        click.echo("# META_THREADS_USER_ID=（このトークンでは取得できず）")
    if ig_id:
        click.echo(f"META_INSTAGRAM_BUSINESS_ID={ig_id}")
    else:
        click.echo("# META_INSTAGRAM_BUSINESS_ID=（このトークンでは取得できず）")

    if not threads_id and not ig_id:
        click.echo(
            "\n両方とも取得できませんでした。トークンの権限/種類を確認してください"
            "（Threads と Instagram でアプリ・トークンが分かれている場合あり）。"
        )


if __name__ == "__main__":
    main()
