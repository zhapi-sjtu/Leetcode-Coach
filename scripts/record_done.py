from __future__ import annotations

import re
from pathlib import Path

from common import (
    NOTES_DIR,
    REVIEW_FILE,
    add_days,
    find_problem,
    format_problem_row,
    load_questions,
    load_review_text,
    note_rel_path,
    read_text,
    update_activity,
    write_text,
)


def insert_review_row(text: str, row: str) -> str:
    marker = "|---|---|---|---|---|---|---|---|"
    index = text.find(marker)
    if index == -1:
        raise SystemExit("未找到复习表分隔行。")
    insert_at = text.find("\n", index) + 1
    if row in text:
        return text
    return text[:insert_at] + row + "\n" + text[insert_at:]


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="标记题目已完成，并安排阶段 0 复习。")
    parser.add_argument("--number", type=int, required=True)
    parser.add_argument("--title")
    parser.add_argument("--topic")
    parser.add_argument("--note", help="题解笔记路径。相对路径会从 data/ 目录解析。")
    args = parser.parse_args()

    lines, _ = load_questions()
    problem = find_problem(args.number)
    problem.title = args.title or problem.title
    problem.topic = args.topic or problem.topic
    lines[problem.line_index] = format_problem_row(problem, solved=True)
    from common import QUESTION_FILE

    write_text(QUESTION_FILE, "\n".join(lines).rstrip() + "\n")

    note = args.note or note_rel_path(problem.number, problem.title)
    note_display = f"[[{note}]]" if not note.startswith("[") else note
    row = f"| {problem.number} | {problem.title} | {problem.topic} | {note_display} | 0 | {add_days(3)} | 🌱 | 0 |"

    review_text = load_review_text()
    review_text = insert_review_row(review_text, row)
    review_text = update_activity(review_text, count_done=True)
    write_text(REVIEW_FILE, review_text)

    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    note_path = Path(note)
    if not note_path.is_absolute():
        note_path = REVIEW_FILE.parent / note_path
    if not note_path.exists():
        write_text(note_path, f"# {problem.number}. {problem.title}\n\n待补充：在这里粘贴最终复盘后的题解笔记。\n")

    print(f"已记录题目 {problem.number}。下次复习：{add_days(3)}")


if __name__ == "__main__":
    main()
