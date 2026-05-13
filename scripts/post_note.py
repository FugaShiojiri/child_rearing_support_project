"""
==============================================================================
note 自動投稿スクリプト（下書き保存まで）
------------------------------------------------------------------------------
用途:
    docs/drafts/note/YYYY-MM-DD*.md のうち approved=true のものを
    Playwright で note にログインし、新規記事として **下書き保存** する。
    公開はしない（Phase 2 方針：CEO が note 上で最終確認→手動公開）。

前提:
    - note 公式 API が存在しないためブラウザ自動化（Playwright）で代替
    - 2026-05時点の note UI 前提でセレクターを記述。UI 変更時は要追従
    - ヘッドレス実行を前提。デバッグ時は --headed で headed モードに
    - 本文1行目を ``# タイトル`` として扱い、それ以外を本文へ流し込む
    - ボット判定回避: 1日数本に抑制し、ステップ間に 3 秒のウェイト

実行例:
    # dry-run（実投稿なし）
    python scripts/post_note.py --date 2026-05-14

    # 実投稿（下書き保存）
    python scripts/post_note.py --date 2026-05-14 --commit

    # ブラウザ表示モード（セレクター確認用）
    python scripts/post_note.py --date 2026-05-14 --commit --headed

関連 .env キー:
    NOTE_EMAIL
    NOTE_PASSWORD
    LOG_LEVEL (optional)
==============================================================================
"""
from __future__ import annotations

import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

import click
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.lib.draft_loader import (  # noqa: E402
    Draft,
    configure_logging,
    load_drafts,
    log_post,
    print_dry_run_notice,
    truncate_for_log,
)


logger = logging.getLogger("post_note")


NOTE_LOGIN_URL = "https://note.com/login"
NOTE_NEW_NOTE_URL = "https://note.com/notes/new"
STEP_WAIT_SEC = 3.0  # ボット判定回避用のウェイト


def split_title_and_body(md: str) -> tuple[str, str]:
    """Markdown 本文の先頭 ``# タイトル`` 行をタイトルとして分離する。

    Args:
        md: ドラフトの本文（frontmatter は除去済み）。

    Returns:
        ``(title, body_without_title)`` のタプル。
        ``#`` タイトル行が無い場合は最初の非空行をタイトル化。
    """
    lines = md.splitlines()
    title = ""
    body_start = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            continue
        if s.startswith("# "):
            title = s.lstrip("# ").strip()
        else:
            title = s
        body_start = i + 1
        break
    body = "\n".join(lines[body_start:]).strip()
    return title or "（無題）", body


def post_draft_to_note(
    draft: Draft,
    *,
    email: str,
    password: str,
    headed: bool = False,
) -> dict[str, Any]:
    """Playwright で note にログインして下書き保存する。

    2026-05時点の note UI に依存するため、セレクター変更時は要追従。

    Args:
        draft: 対象ドラフト。
        email: note のログインメール。
        password: note のログインパスワード。
        headed: True なら headed モード（デバッグ用）。

    Returns:
        ``{"post_id": ..., "draft_url": ...}`` を含む辞書。
    """
    # 遅延 import（dry-run で playwright 未導入でも動くように）
    from playwright.sync_api import sync_playwright

    title, body = split_title_and_body(draft.body)
    logger.info("note 下書き作成 title=%s body_len=%d", title, len(body))

    result: dict[str, Any] = {"post_id": None, "draft_url": None}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()
        try:
            # --- ログイン (2026-05時点の note UI) ---
            logger.info("ログイン画面へ遷移")
            page.goto(NOTE_LOGIN_URL, wait_until="domcontentloaded")
            page.wait_for_selector(
                "input[type='email'], input[name='login']", timeout=15000
            )
            email_input = page.locator(
                "input[type='email'], input[name='login']"
            ).first
            email_input.fill(email)
            page.locator("input[type='password']").first.fill(password)
            time.sleep(STEP_WAIT_SEC)
            # ログインボタン（テキスト or type=submit）
            page.locator(
                "button[type='submit'], button:has-text('ログイン')"
            ).first.click()
            page.wait_for_load_state("networkidle", timeout=30000)
            time.sleep(STEP_WAIT_SEC)

            # --- 新規記事作成画面へ ---
            logger.info("新規記事作成画面へ遷移")
            page.goto(NOTE_NEW_NOTE_URL, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle", timeout=30000)
            time.sleep(STEP_WAIT_SEC)

            # --- タイトル入力（2026-05時点の note UI: contenteditable の見出し領域） ---
            title_selector = (
                "textarea[placeholder*='タイトル'], "
                "[contenteditable='true'][aria-label*='タイトル'], "
                "[contenteditable='true'][placeholder*='タイトル']"
            )
            page.wait_for_selector(title_selector, timeout=20000)
            page.locator(title_selector).first.click()
            page.keyboard.type(title, delay=15)
            time.sleep(STEP_WAIT_SEC)

            # --- 本文入力 ---
            body_selector = (
                "[contenteditable='true'][aria-label*='本文'], "
                "[contenteditable='true'][data-placeholder*='本文'], "
                "div[role='textbox']"
            )
            page.locator(body_selector).first.click()
            # 改行を含めて入力
            for line in body.split("\n"):
                page.keyboard.type(line, delay=10)
                page.keyboard.press("Enter")
            time.sleep(STEP_WAIT_SEC)

            # --- 下書き保存 ---
            # 2026-05時点では「保存」または「下書き保存」ボタンが存在
            save_btn = page.locator(
                "button:has-text('下書き保存'), "
                "button:has-text('保存'), "
                "button[aria-label*='保存']"
            ).first
            save_btn.click()
            page.wait_for_load_state("networkidle", timeout=30000)
            time.sleep(STEP_WAIT_SEC)

            # URL から post_id 抽出（/notes/<id>/edit の形）
            current_url = page.url
            result["draft_url"] = current_url
            parts = [p for p in current_url.split("/") if p]
            for i, part in enumerate(parts):
                if part == "notes" and i + 1 < len(parts):
                    result["post_id"] = parts[i + 1]
                    break

            logger.info("下書き保存完了 url=%s", current_url)
        finally:
            context.close()
            browser.close()

    return result


def _get_required_env(name: str) -> str:
    """必須環境変数を取得。未設定なら案内付きエラー。"""
    v = os.environ.get(name, "").strip()
    if not v:
        raise click.ClickException(
            f"環境変数 {name} が未設定です。`.env` を作成し値を入れてください。"
        )
    return v


@click.command(help="note に承認済みドラフトを下書き保存する。")
@click.option("--date", required=True, help="対象日付（YYYY-MM-DD）")
@click.option(
    "--commit",
    is_flag=True,
    default=False,
    help="このフラグを付けると下書き保存を実行。無いと dry-run。",
)
@click.option(
    "--headed",
    is_flag=True,
    default=False,
    help="ブラウザを表示モードで起動（デバッグ用）。",
)
def main(date: str, commit: bool, headed: bool) -> None:
    """CLI エントリポイント。"""
    load_dotenv(PROJECT_ROOT / ".env")
    configure_logging(os.environ.get("LOG_LEVEL"))

    drafts = load_drafts("note", date)
    if not drafts:
        all_path = (PROJECT_ROOT / "docs" / "drafts" / "note").glob(f"{date}*.md")
        if any(all_path):
            click.echo(f"承認済みドラフトなし (date={date})")
        else:
            click.echo(f"該当ドラフトなし (date={date})")
        return

    click.echo(f"=== note 下書き保存 {len(drafts)}件 (date={date}, commit={commit}) ===")

    if not commit:
        for i, d in enumerate(drafts, 1):
            title, body = split_title_and_body(d.body)
            click.echo(f"\n--- [{i}/{len(drafts)}] {d.path.name} ---")
            click.echo(f"title: {title}")
            click.echo(f"body  : {truncate_for_log(body, 200)}")
            click.echo(f"({len(body)}文字)")
        print_dry_run_notice()
        return

    email = _get_required_env("NOTE_EMAIL")
    password = _get_required_env("NOTE_PASSWORD")

    success = 0
    for i, d in enumerate(drafts, 1):
        logger.info("[%d/%d] 下書き保存開始 path=%s", i, len(drafts), d.path.name)
        try:
            r = post_draft_to_note(
                d, email=email, password=password, headed=headed
            )
            log_post(
                "note",
                {
                    "date": date,
                    "draft_path": str(d.path.relative_to(PROJECT_ROOT)),
                    "post_id": r.get("post_id"),
                    "draft_url": r.get("draft_url"),
                },
            )
            success += 1
            click.echo(f"[OK] {d.path.name} -> {r.get('draft_url')}")
        except Exception as exc:  # noqa: BLE001
            logger.exception("下書き保存失敗: %s", d.path)
            click.echo(f"[FAIL] {d.path.name}: {exc}", err=True)

    click.echo(f"\n完了: {success}/{len(drafts)} 件成功")


if __name__ == "__main__":
    main()
