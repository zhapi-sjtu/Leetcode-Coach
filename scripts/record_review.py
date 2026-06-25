from __future__ import annotations

from common import REVIEW_FILE, add_days, load_review_text, today, update_activity, write_text


MASTERIES = {0: "🌱", 1: "🌿", 2: "🌳"}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="记录 LeetCode 复习结果。")
    parser.add_argument("--number", type=int, required=True)
    parser.add_argument("--result", choices=["pass", "fail"], required=True)
    args = parser.parse_args()

    text = load_review_text()
    lines = text.splitlines()
    changed = False
    graduated_row = None

    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8 or cells[0] != str(args.number):
            continue

        old_stage = int(cells[4])
        review_count = int(cells[7]) + 1
        if args.result == "fail":
            new_stage = 0
            cells[4] = "0"
            cells[5] = add_days(3)
            cells[6] = MASTERIES[0]
            cells[7] = str(review_count)
            lines[index] = "| " + " | ".join(cells) + " |"
        else:
            new_stage = old_stage + 1
            if new_stage >= 3:
                graduated_row = f"| {cells[0]} | {cells[1]} | {cells[2]} | {cells[3]} | {today().isoformat()} |"
                del lines[index]
            else:
                interval = 7 if new_stage == 1 else 15
                cells[4] = str(new_stage)
                cells[5] = add_days(interval)
                cells[6] = MASTERIES[new_stage]
                cells[7] = str(review_count)
                lines[index] = "| " + " | ".join(cells) + " |"
        changed = True
        break

    if not changed:
        raise SystemExit(f"题号 {args.number} 未在复习台账中找到。")

    text = "\n".join(lines).rstrip() + "\n"
    if graduated_row:
        marker = "|---|---|---|---|---|"
        marker_index = text.rfind(marker)
        insert_at = text.find("\n", marker_index) + 1
        text = text[:insert_at] + graduated_row + "\n" + text[insert_at:]

    text = update_activity(text, count_done=False)
    write_text(REVIEW_FILE, text)
    result_text = "通过" if args.result == "pass" else "未通过"
    print(f"已记录题目 {args.number} 的复习结果：{result_text}")


if __name__ == "__main__":
    main()
