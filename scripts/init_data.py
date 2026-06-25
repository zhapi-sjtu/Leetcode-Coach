from __future__ import annotations

from pathlib import Path

from common import DATA_DIR, NOTES_DIR, QUESTION_FILE, REVIEW_FILE, write_text


QUESTION_TEMPLATE = """---
tags:
  - leetcode
  - 题单
title: LeetCode 刷题教练题单
---

# LeetCode 刷题教练题单

## 哈希

- [ ] 1. 两数之和 `简单` `哈希` `two-sum`
- [ ] 49. 字母异位词分组 `中等` `哈希` `group-anagrams`
"""


REVIEW_TEMPLATE = """---
tags:
  - leetcode
  - 复习表
title: LeetCode 刷题教练复习台账
streak: 0
last_active: ""
total_done: 0
---

# LeetCode 刷题教练复习台账

## 待复习 / 进行中

| 题号 | 题名 | 专题 | 笔记 | 阶段 | 下次复习 | 掌握度 | 复习次数 |
|---|---|---|---|---|---|---|---|

## 已毕业

| 题号 | 题名 | 专题 | 笔记 | 毕业日期 |
|---|---|---|---|---|
"""


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    if not QUESTION_FILE.exists():
        write_text(QUESTION_FILE, QUESTION_TEMPLATE)
        print(f"已创建 {QUESTION_FILE}")
    else:
        print(f"已存在 {QUESTION_FILE}")
    if not REVIEW_FILE.exists():
        write_text(REVIEW_FILE, REVIEW_TEMPLATE)
        print(f"已创建 {REVIEW_FILE}")
    else:
        print(f"已存在 {REVIEW_FILE}")


if __name__ == "__main__":
    main()
