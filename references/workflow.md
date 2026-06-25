# 工作流

## 开始刷题

当用户说“开始刷题”“今天刷什么”“下一题”“规划刷题”等类似表达时使用。

运行：

```bash
python -B scripts/pick_next.py
```

按下面结构回答：

```text
连续打卡 N 天 ｜ 已完成 X/Y

今日复习：
- ...

今日新题：
- 题号. 题名 ｜ 专题 ｜ 难度
- 做题链接：<url>

建议顺序：
1. 先复习到期题
2. 再做今日新题
```

除非用户主动要求，否则不要提前讲解新题。

展示新题或复习题时，必须包含脚本返回的 `url` 字段。默认使用力扣通用题目页链接，例如：

```text
https://leetcode.cn/problems/two-sum/description/
```

## 完成一题后的复盘

当用户说“做完了”“AC了”“复盘这题”，或直接贴出代码时使用。

必须按这个顺序执行：

1. 确认题号、题名和专题。
2. 如果用户还没提供 AC 的 Python 代码，要求用户贴出代码。
3. 根据 `strict-questioning.md` 和 `python-checklist.md` 提出严格追问。
4. 等待用户回答。
5. 如果回答含糊、错误或缺少关键点，继续追问。
6. 只有当用户能讲清楚思路后，才写题解笔记。
7. 运行 `record_done.py`。

示例：

```bash
python -B scripts/record_done.py --number 1 --title "两数之和" --topic "哈希" --note "data/题解/0001-两数之和.md"
```

## 复习旧题

当用户说“复习”“考考我”“旧题”，或询问到期复习时使用。

必须按这个顺序执行：

1. 检查到期复习题。
2. 选择一道到期题。
3. 在打开笔记前，先让用户回忆解法。
4. 将用户回答与笔记对照。
5. 标记通过或未通过。

命令：

```bash
python -B scripts/pick_next.py --review-only
python -B scripts/record_review.py --number 1 --result pass
python -B scripts/record_review.py --number 1 --result fail
```

## 导入题目

以 Markdown 作为主要导入格式。

```bash
python -B scripts/import_markdown_questions.py path/to/questions.md
```

导入后运行：

```bash
python -B scripts/pick_next.py
```
