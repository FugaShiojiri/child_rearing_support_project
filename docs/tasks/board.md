---
tags: [tasks, view, readonly]
status: view-only
updated_by: メインClaude
related: [[backlog]] [[this_week]]
---

# タスクボード（見るだけのページ）

> **このページは「見るだけ」です。ここを編集しないでください。**
> タスクの本当の中身（真実源）は [[backlog]]（`docs/tasks/backlog.md`）にあり、Claude が管理します。
> ここは backlog.md の内容を **Dataview プラグインで見やすく表示しているだけ** です（自動更新・手入力不要）。
> Dataview が有効でないと下の表は「コードのまま」表示されます。その場合は [[this_week]] の📌の「Dataview有効化」を一度だけ実施してください（5/21 以降でOK）。

---

## ① あなた（オーナー）がやる未完タスク

> 担当が `user`（あなた本人＝承認・入稿・配布など委譲不可のもの）で、まだ終わっていないもの。**普段見るのはここだけでOK。**

```dataview
TASK
FROM "docs/tasks/backlog.md"
WHERE !completed AND contains(text, "｜ user ｜")
SORT text ASC
```

---

## ② 全体ざっくり件数

```dataview
TABLE WITHOUT ID
  length(filter(file.tasks, (t) => !t.completed)) AS "未完",
  length(filter(file.tasks, (t) => t.completed)) AS "完了",
  length(filter(file.tasks, (t) => !t.completed AND contains(t.text, "｜ user ｜"))) AS "うち・あなた担当(未完)"
FROM "docs/tasks/backlog.md"
```

---

## ③ 未完タスク一覧（backlog 全体・参考）

> Claude 担当も含む全未完。普段は見なくて構いません（進捗が気になる時の参考）。

```dataview
TASK
FROM "docs/tasks/backlog.md"
WHERE !completed
SORT text ASC
```

---

## ④ 最近やったこと（完了・直近）

```dataview
TASK
FROM "docs/tasks/backlog.md"
WHERE completed
SORT text DESC
LIMIT 15
```

---

> 表が崩れて見える / 仕様を変えたい時は Claude に一言。レイアウトは Claude が調整します（あなたの作業は不要）。
