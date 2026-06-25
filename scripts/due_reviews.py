from __future__ import annotations

from common import emit_json, leetcode_url, load_questions, load_review_text, parse_date, review_rows, today


def main() -> None:
    today_d = today()
    _, problems = load_questions()
    problem_by_number = {str(problem.number): problem for problem in problems}
    due = []
    for row in review_rows(load_review_text()):
        try:
            if parse_date(row["next_review"]) <= today_d:
                problem = problem_by_number.get(row["number"])
                if problem:
                    row = {**row, "slug": problem.slug, "url": leetcode_url(problem)}
                due.append(row)
        except ValueError:
            continue
    due.sort(key=lambda row: row["next_review"])
    emit_json({"date": today_d.isoformat(), "due_reviews": due, "count": len(due)})


if __name__ == "__main__":
    main()
