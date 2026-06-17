"""note コメント読取（read-only・投稿は一切しない）。

note コメント自動化（オーナー決裁 2026-06-17）の第1部品。保存済みセッション
（`.auth/note_state.json`・`capture_note_session.py` で取得）を使い、note の
内部 API からコメントを **読むだけ** 取得する。書き込み・投稿は一切行わない。

API 契約（2026-06-17 ネットワーク傍受で確定）:
    GET https://note.com/api/v3/notes/{key}/note_comments?per_page=50&page=N&order=newest
        -> {"data": [ ...ルートコメント... ]}   ※data は配列を直接返す
        ⚠️ 紛らわしい罠: `/notes/{key}/comments`（note_ 無し）は常に空を返す。
           本物は `note_comments`。記事 key（nXXXX）でアクセスできる（数値ID不要）。
    GET https://note.com/api/v2/current_user  -> 自分の user 情報

各コメントの主な構造:
    key                 コメントキー（返信先 parent_key に使う）
    comment             本文のリッチテキスト（root>element>text の入れ子。.value を連結）
    user                {key, urlname, nickname, profile_image_url}
    created_at          投稿日時
    like_count / is_creator_liked     スキ数 / 自分がスキ済みか
    reply_count                       返信数
    is_creator_replied                ★自分(クリエイター)が返信済みか → 未返信の抽出に使う
    latest_creator_reply              自分の最新返信（同じコメント構造）
    is_root                           ルートコメントか（返信でないか）

対象の指定:
    --url / --key を指定 → その記事のコメントを読む（競合接触 T070 の下調べ用）
    無指定               → 自分(hidamari_sodachi)の note 公開記事すべて
                          （クリエイターAPIで取得＝front-matter の記録漏れに依存しない）

使い方:
    python3 scripts/note_comments_read.py                 # 自分の公開記事全部
    python3 scripts/note_comments_read.py --unreplied     # 自分が未返信のものだけ
    python3 scripts/note_comments_read.py --url https://note.com/xxx/n/nXXXX
    python3 scripts/note_comments_read.py --key nXXXX --json
    python3 scripts/note_comments_read.py --key nXXXX --raw    # 1件目を生dump
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import click

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUTH_PATH = PROJECT_ROOT / ".auth" / "note_state.json"
COMMENTS_API = "https://note.com/api/v3/notes/{key}/note_comments"
CURRENT_USER_API = "https://note.com/api/v2/current_user"
MY_URLNAME = "hidamari_sodachi"


def key_from_url(url: str) -> str | None:
    """note 記事 URL から記事キー（n + 英数字）を取り出す。"""
    m = re.search(r"/n/(n[0-9a-z]+)", url)
    return m.group(1) if m else None


def extract_text(node: Any) -> str:
    """note コメントのリッチテキスト（root>element>text の入れ子）から本文を取り出す。"""
    if isinstance(node, dict):
        if node.get("type") == "text":
            return node.get("value", "")
        children = node.get("children", [])
        sep = "\n" if node.get("type") == "element" else ""
        return sep.join(extract_text(ch) for ch in children)
    if isinstance(node, list):
        return "\n".join(extract_text(ch) for ch in node)
    return ""


def fetch_my_articles(req, urlname: str = MY_URLNAME, max_pages: int = 5) -> list[dict[str, str]]:
    """note 本体（クリエイターAPI）から自分の公開記事を取得する。

    front-matter の published_url は記録漏れがあるため、真実源は note 本体。
    """
    arts: list[dict[str, str]] = []
    for page in range(1, max_pages + 1):
        r = req.get(
            f"https://note.com/api/v2/creators/{urlname}/contents?kind=note&page={page}",
            timeout=20000,
        )
        if r.status != 200:
            break
        conts = r.json().get("data", {}).get("contents", [])
        if not conts:
            break
        for n in conts:
            if n.get("key"):
                arts.append({"key": n["key"], "title": n.get("name", n["key"]), "file": "-"})
    return arts


def _require_session() -> None:
    if not AUTH_PATH.exists():
        raise click.ClickException(
            f"ログインセッションがありません: {AUTH_PATH}\n"
            "先に `python3 scripts/capture_note_session.py` を実行してください。"
        )


def fetch_note_comments(req, key: str, per_page: int = 50, max_pages: int = 20) -> dict[str, Any]:
    """1記事の全ルートコメントをページ送りで取得。"""
    rows: list[dict[str, Any]] = []
    for page in range(1, max_pages + 1):
        url = f"{COMMENTS_API.format(key=key)}?per_page={per_page}&page={page}&order=newest"
        r = req.get(url, timeout=20000)
        if r.status != 200:
            return {"error": f"status={r.status}", "comments": rows}
        data = r.json().get("data", [])
        if not data:
            break
        rows.extend(data)
        if len(data) < per_page:
            break
    return {"comments": rows}


def _parse(c: dict[str, Any]) -> dict[str, Any]:
    u = c.get("user") or {}
    reply = c.get("latest_creator_reply") or {}
    return {
        "comment_key": c.get("key"),
        "author_nickname": u.get("nickname"),
        "author_urlname": u.get("urlname"),
        "is_mine": (u.get("urlname") == MY_URLNAME),
        "body": extract_text(c.get("comment")).strip(),
        "created_at": c.get("created_at"),
        "like_count": c.get("like_count"),
        "is_creator_liked": c.get("is_creator_liked"),
        "reply_count": c.get("reply_count"),
        "is_creator_replied": c.get("is_creator_replied"),
        "my_reply": extract_text(reply.get("comment")).strip() if reply else "",
    }


@click.command(help="note のコメントを読むだけ取得する（投稿しない・read-only）。")
@click.option("--url", "urls", multiple=True, help="対象記事URL（複数可）")
@click.option("--key", "keys", multiple=True, help="対象記事キー nXXXX（複数可）")
@click.option("--unreplied", is_flag=True, help="自分が未返信のコメントだけ表示")
@click.option("--json", "as_json", is_flag=True, help="JSON で出力")
@click.option("--raw", is_flag=True, help="最初のコメントの全フィールドを生dump（構造確認用）")
def main(urls, keys, unreplied, as_json, raw) -> None:
    _require_session()
    from playwright.sync_api import sync_playwright

    explicit: list[dict[str, str]] = []
    for u in urls:
        k = key_from_url(u)
        explicit.append({"key": k, "title": u, "file": "-"}) if k else click.echo(
            f"[skip] URLからキー抽出不可: {u}", err=True
        )
    for k in keys:
        explicit.append({"key": k, "title": k, "file": "-"})

    results: list[dict[str, Any]] = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=str(AUTH_PATH))
        req = ctx.request
        # 無指定なら note 本体から自分の公開記事を取得（front-matter に依存しない）
        targets = explicit or fetch_my_articles(req)
        if not targets:
            b.close()
            raise click.ClickException("対象記事が取得できませんでした（セッション失効の可能性）。")
        for t in targets:
            res = fetch_note_comments(req, t["key"])
            parsed = [_parse(c) for c in res.get("comments", [])]
            if unreplied:
                parsed = [c for c in parsed if not c["is_creator_replied"] and not c["is_mine"]]
            results.append(
                {
                    "key": t["key"],
                    "title": t["title"],
                    "file": t["file"],
                    "count": len(parsed),
                    "error": res.get("error"),
                    "comments": parsed,
                    "_raw_first": (res.get("comments") or [None])[0] if raw else None,
                }
            )
        b.close()

    if as_json:
        click.echo(json.dumps(results, ensure_ascii=False, indent=2))
        return

    grand = 0
    for r in results:
        grand += r["count"]
        mark = f"[ERROR {r['error']}] " if r.get("error") else ""
        click.echo(f"\n■ {mark}{r['title']}  (key={r['key']}, file={r['file']})")
        click.echo(f"   ルートコメント {r['count']} 件" + ("（未返信のみ）" if unreplied else ""))
        for c in r["comments"]:
            who = "★自分" if c["is_mine"] else f"@{c['author_urlname']}({c['author_nickname']})"
            status = "✅返信済" if c["is_creator_replied"] else "🔴未返信"
            click.echo(f"   - [{who}] {status} ♥{c['like_count']} {c['created_at']}")
            click.echo(f"       {c['body'][:140].replace(chr(10), ' ')}")
            if c["my_reply"]:
                click.echo(f"       └ 自分の返信: {c['my_reply'][:100].replace(chr(10), ' ')}")
        if raw and r.get("_raw_first"):
            click.echo("   [--raw] 1件目の生フィールド:")
            for k, v in r["_raw_first"].items():
                vv = f"<dict keys={list(v.keys())}>" if isinstance(v, dict) else str(v)[:80]
                click.echo(f"       {k}: {vv}")
    click.echo(f"\n=== 合計 {grand} 件 / 対象 {len(results)} 記事 ===")


if __name__ == "__main__":
    main()
