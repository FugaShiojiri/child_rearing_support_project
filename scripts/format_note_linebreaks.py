#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""note記事本文を読みやすい改行に整形する（文字は変えず、改行のみ挿入）。

オーナー指示(2026-06-17): note公開時はモバイルで読みやすいよう改行を調整する。
そのスタイルを記事ファイル側にあらかじめ反映し、コピペで済むようにする。

スタイル:
  - 句点(。！？)ごとに改行。
  - 1文が長い場合は読点(、)でも分割し、1行を短く保つ（既定 25 字超で分割）。
  - 括弧「」（）『』の内側、および **太字** スパンの内側では改行しない
    （マーカーが行をまたいで壊れるのを防ぐ）。
対象範囲:
  「## 記事本文（ここから下を note へ）」〜「出典（軽い参照）」の手前まで。
  見出し(#)・空行・区切り(---)・front-matter・ドラフトメモは触らない。
  リード(> )と箇条書き(- )は接頭辞を保って分割（箇条書きの継続行は2字インデント）。

使い方:
  python3 scripts/format_note_linebreaks.py docs/note/articles/07_series06_montessori.md [...]
  ※ 元に戻すなら git checkout -- <file>。1行あたりの長さは LIMIT で調整。
"""
import sys

OPEN = "「（『"
CLOSE = "」）』"
ENDERS = "。！？!?"
LIMIT = 25  # この長さを超えていれば読点でも改行


def break_text(s):
    lines, cur, depth, emph = [], "", 0, False
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if ch == "*" and i + 1 < n and s[i + 1] == "*":  # **太字** トグル
            cur += "**"
            emph = not emph
            i += 2
            continue
        cur += ch
        if ch in OPEN:
            depth += 1
        elif ch in CLOSE:
            depth = max(0, depth - 1)
        if depth == 0 and not emph:
            if ch in ENDERS:
                lines.append(cur)
                cur = ""
            elif ch == "、" and len(cur) >= LIMIT:
                lines.append(cur)
                cur = ""
        i += 1
    if cur:
        lines.append(cur)
    return [l for l in lines if l != ""]


def process_body_line(line):
    if line.strip() == "" or line.strip() == "---" or line.lstrip().startswith("#"):
        return [line]
    if line.startswith("> "):
        parts = break_text(line[2:])
        return ["> " + parts[0]] + ["> " + p for p in parts[1:]]
    if line.startswith("- "):
        parts = break_text(line[2:])
        return ["- " + parts[0]] + ["  " + p for p in parts[1:]]
    return break_text(line)


def main(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    out, in_body = [], False
    for line in lines:
        if line.strip() == "## 記事本文（ここから下を note へ）":
            in_body = True
            out.append(line)
            continue
        if in_body and "出典（軽い参照）" in line:
            in_body = False
        out.extend(process_body_line(line) if in_body else [line])
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"{path}: {len(lines)} -> {len(out)} 行")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python3 scripts/format_note_linebreaks.py <article.md> [...]")
    for p in sys.argv[1:]:
        main(p)
