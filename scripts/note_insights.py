"""note ダッシュボード（PV/スキ/コメント）の読み取り専用集計。

note クリエイターダッシュボードの統計 API を、保存済みログインセッション
（``.auth/note_state.json``）の cookie で叩き、記事別・全体の数字を集計する。
**read-only**＝一切書き込まない（投稿・スキ・コメントはしない）。

マーケティングの観測ループ用。Threads 側の ``threads_insights.py`` と同じ役割を
note に対して担う（観測モード T106・KPI=note総ビュー 127→目標380〜640 の追跡）。

API: GET https://note.com/api/v1/stats/pv?filter=all&page=N&sort=pv
  data.total_pv / total_like / total_comment … 全体合計
  data.note_stats[] … 記事別 {key, name, read_count, like_count, comment_count}

使い方:
    python3 scripts/note_insights.py                 # 全期間（filter=all）
    python3 scripts/note_insights.py --json           # JSON 出力（機械処理用）

前提: 先に `python3 scripts/capture_note_session.py` でセッション取得済みであること。
"""
from __future__ import annotations

import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any

import click

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUTH_PATH = PROJECT_ROOT / ".auth" / "note_state.json"
STATS_API = "https://note.com/api/v1/stats/pv"

# KPI（this_week / backlog より）。観測モードの基準。
KPI_BASELINE = 127      # 6/10 No-Go判定時の総ビュー
KPI_TARGET_LOW = 380    # 目標レンジ下限（3倍）
KPI_TARGET_HIGH = 640   # 目標レンジ上限（5倍）
JUDGE_FLOOR = 50        # total views < 50 は時期尚早＝判定しない（T106）


def _cookie_header() -> str:
    if not AUTH_PATH.exists():
        raise click.ClickException(
            f"ログインセッションがありません: {AUTH_PATH}\n"
            "先に `python3 scripts/capture_note_session.py` を実行してください。"
        )
    state = json.loads(AUTH_PATH.read_text(encoding="utf-8"))
    cookies = state.get("cookies", [])
    return "; ".join(
        f"{c['name']}={c['value']}"
        for c in cookies
        if "note.com" in c.get("domain", "")
    )


def _get(url: str, cookie: str) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Cookie": cookie,
            "Accept": "application/json",
        },
    )
    try:
        raw = urllib.request.urlopen(req, timeout=30).read().decode()
    except urllib.error.HTTPError as e:  # noqa: BLE001
        raise click.ClickException(f"API エラー {e.code}: {url}") from e
    return json.loads(raw)


def fetch_stats(cookie: str) -> dict[str, Any]:
    """全ページの記事別統計を集約して返す。"""
    page = 1
    notes: list[dict[str, Any]] = []
    totals = {"pv": 0, "like": 0, "comment": 0}
    while True:
        d = _get(f"{STATS_API}?filter=all&page={page}&sort=pv", cookie)["data"]
        notes.extend(d.get("note_stats", []))
        # 合計は最終ページの値が全体合計（毎ページ同値）なので上書きでよい
        totals = {
            "pv": d.get("total_pv", 0),
            "like": d.get("total_like", 0),
            "comment": d.get("total_comment", 0),
        }
        if d.get("last_page", True):
            break
        page += 1
    notes.sort(key=lambda n: n.get("read_count", 0), reverse=True)
    return {"totals": totals, "notes": notes}


def main_impl(as_json: bool) -> None:
    cookie = _cookie_header()
    result = fetch_stats(cookie)
    if as_json:
        click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        return

    t = result["totals"]
    notes = result["notes"]
    click.echo("=== note インサイト（全期間・read-only） ===")
    click.echo(f"総PV {t['pv']} / 総スキ {t['like']} / 総コメント {t['comment']}  （公開{len(notes)}記事）")
    click.echo("")
    click.echo(f"{'PV':>5} {'スキ':>4} {'コメ':>4}  タイトル")
    click.echo("-" * 64)
    for n in notes:
        title = (n.get("name") or "").strip()
        if len(title) > 34:
            title = title[:33] + "…"
        click.echo(
            f"{n.get('read_count', 0):>5} {n.get('like_count', 0):>4} "
            f"{n.get('comment_count', 0):>4}  {title}"
        )

    # KPI 文脈
    click.echo("")
    pv = t["pv"]
    click.echo(
        f"KPI: 基準{KPI_BASELINE} → 目標{KPI_TARGET_LOW}〜{KPI_TARGET_HIGH}（3〜5倍）"
        f"／現在 {pv}"
    )
    if pv < JUDGE_FLOOR:
        click.echo(f"※ 総PV<{JUDGE_FLOOR} は時期尚早＝品質判定しない（観測モード T106）")
    else:
        delta = pv - KPI_BASELINE
        click.echo(f"※ 基準比 {'+' if delta >= 0 else ''}{delta}（目標下限まで残り {max(0, KPI_TARGET_LOW - pv)}）")


@click.command(help="note ダッシュボードの PV/スキ/コメントを集計する（read-only）。")
@click.option("--json", "as_json", is_flag=True, help="JSON で出力（機械処理用）。")
def main(as_json: bool) -> None:
    main_impl(as_json)


if __name__ == "__main__":
    main()
