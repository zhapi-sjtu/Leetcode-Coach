from __future__ import annotations

from common import emit_json, frontmatter_value, leetcode_url, load_questions, load_review_text, parse_date, problem_payload, review_rows, today


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="选择到期复习题和下一道未完成的 LeetCode 题。")
    parser.add_argument("--review-only", action="store_true")
    args = parser.parse_args()

    _, problems = load_questions()
    problem_by_number = {str(problem.number): problem for problem in problems}
    review_text = load_review_text()
    today_d = today()
    due = []
    for row in review_rows(review_text):
        try:
            if parse_date(row["next_review"]) <= today_d:
                problem = problem_by_number.get(row["number"])
                if problem:
                    row = {**row, "slug": problem.slug, "url": leetcode_url(problem)}
                due.append(row)
        except ValueError:
            continue
    due.sort(key=lambda row: row["next_review"])

    unsolved = [problem for problem in problems if not problem.solved]
    next_problem = None if args.review_only or not unsolved else unsolved[0]

    total = len(problems)
    solved = len([problem for problem in problems if problem.solved])
    payload = {
        "date": today_d.isoformat(),
        "streak": frontmatter_value(review_text, "streak", "0"),
        "total_done": frontmatter_value(review_text, "total_done", "0"),
        "solved_in_bank": solved,
        "total_in_bank": total,
        "due_reviews": due,
        "next_problem": None
        if next_problem is None
        else problem_payload(next_problem),
    }
    emit_json(payload)


if __name__ == "__main__":
    main()
