from __future__ import annotations

from pathlib import Path

from common import QUESTION_FILE, load_questions, parse_problem_line, read_text, write_text


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="将 Markdown LeetCode 题单导入 data/_题单.md。")
    parser.add_argument("source", help="包含专题标题和清单行的 Markdown 文件。")
    args = parser.parse_args()

    source = Path(args.source)
    if not source.exists():
        raise SystemExit(f"源文件不存在：{source}")

    existing_lines, existing = load_questions()
    existing_numbers = {problem.number for problem in existing}
    imported_lines = read_text(source).splitlines()

    appended: list[str] = []
    current_topic = ""
    current_heading_added = False
    imported_count = 0
    skipped_count = 0

    for line in imported_lines:
        if line.startswith("##"):
            current_topic = line.strip()
            current_heading_added = False
            continue
        problem = parse_problem_line(line, current_topic.lstrip("# ").strip(), 0)
        if not problem:
            continue
        if problem.number in existing_numbers:
            skipped_count += 1
            continue
        if current_topic and not current_heading_added:
            appended.extend(["", current_topic])
            current_heading_added = True
        appended.append(line)
        existing_numbers.add(problem.number)
        imported_count += 1

    if imported_count:
        content = "\n".join(existing_lines).rstrip() + "\n" + "\n".join(appended).rstrip() + "\n"
        write_text(QUESTION_FILE, content)

    print(f"已导入 {imported_count} 道题，跳过 {skipped_count} 道重复题。")


if __name__ == "__main__":
    main()
