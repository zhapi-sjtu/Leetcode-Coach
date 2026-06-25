from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
QUESTION_FILE = DATA_DIR / "_题单.md"
REVIEW_FILE = DATA_DIR / "_复习表.md"
NOTES_DIR = DATA_DIR / "题解"

DIFFICULTIES = {"简单", "中等", "困难", "Easy", "Medium", "Hard"}
HOT100_SLUGS = {
    1: "two-sum",
    2: "add-two-numbers",
    3: "longest-substring-without-repeating-characters",
    4: "median-of-two-sorted-arrays",
    5: "longest-palindromic-substring",
    11: "container-with-most-water",
    15: "3sum",
    17: "letter-combinations-of-a-phone-number",
    19: "remove-nth-node-from-end-of-list",
    20: "valid-parentheses",
    21: "merge-two-sorted-lists",
    22: "generate-parentheses",
    23: "merge-k-sorted-lists",
    24: "swap-nodes-in-pairs",
    25: "reverse-nodes-in-k-group",
    31: "next-permutation",
    32: "longest-valid-parentheses",
    33: "search-in-rotated-sorted-array",
    34: "find-first-and-last-position-of-element-in-sorted-array",
    35: "search-insert-position",
    39: "combination-sum",
    41: "first-missing-positive",
    42: "trapping-rain-water",
    45: "jump-game-ii",
    46: "permutations",
    48: "rotate-image",
    49: "group-anagrams",
    51: "n-queens",
    53: "maximum-subarray",
    54: "spiral-matrix",
    55: "jump-game",
    56: "merge-intervals",
    62: "unique-paths",
    64: "minimum-path-sum",
    70: "climbing-stairs",
    72: "edit-distance",
    73: "set-matrix-zeroes",
    74: "search-a-2d-matrix",
    75: "sort-colors",
    76: "minimum-window-substring",
    78: "subsets",
    79: "word-search",
    84: "largest-rectangle-in-histogram",
    94: "binary-tree-inorder-traversal",
    98: "validate-binary-search-tree",
    101: "symmetric-tree",
    102: "binary-tree-level-order-traversal",
    104: "maximum-depth-of-binary-tree",
    105: "construct-binary-tree-from-preorder-and-inorder-traversal",
    108: "convert-sorted-array-to-binary-search-tree",
    114: "flatten-binary-tree-to-linked-list",
    118: "pascals-triangle",
    121: "best-time-to-buy-and-sell-stock",
    124: "binary-tree-maximum-path-sum",
    128: "longest-consecutive-sequence",
    131: "palindrome-partitioning",
    136: "single-number",
    138: "copy-list-with-random-pointer",
    139: "word-break",
    141: "linked-list-cycle",
    142: "linked-list-cycle-ii",
    146: "lru-cache",
    148: "sort-list",
    152: "maximum-product-subarray",
    153: "find-minimum-in-rotated-sorted-array",
    155: "min-stack",
    160: "intersection-of-two-linked-lists",
    169: "majority-element",
    189: "rotate-array",
    198: "house-robber",
    199: "binary-tree-right-side-view",
    200: "number-of-islands",
    206: "reverse-linked-list",
    207: "course-schedule",
    208: "implement-trie-prefix-tree",
    215: "kth-largest-element-in-an-array",
    226: "invert-binary-tree",
    230: "kth-smallest-element-in-a-bst",
    234: "palindrome-linked-list",
    236: "lowest-common-ancestor-of-a-binary-tree",
    238: "product-of-array-except-self",
    239: "sliding-window-maximum",
    240: "search-a-2d-matrix-ii",
    279: "perfect-squares",
    283: "move-zeroes",
    287: "find-the-duplicate-number",
    295: "find-median-from-data-stream",
    300: "longest-increasing-subsequence",
    322: "coin-change",
    347: "top-k-frequent-elements",
    394: "decode-string",
    416: "partition-equal-subset-sum",
    437: "path-sum-iii",
    438: "find-all-anagrams-in-a-string",
    543: "diameter-of-binary-tree",
    560: "subarray-sum-equals-k",
    739: "daily-temperatures",
    763: "partition-labels",
    994: "rotting-oranges",
    1143: "longest-common-subsequence",
}


@dataclass
class Problem:
    number: int
    title: str
    topic: str
    difficulty: str
    slug: str
    solved: bool
    line_index: int


def today() -> date:
    return date.today()


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def add_days(days: int) -> str:
    return (today() + timedelta(days=days)).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def parse_problem_line(line: str, topic: str, line_index: int) -> Problem | None:
    match = re.match(r"^\s*- \[([ xX])\]\s*(\d+)\.\s*([^`]+?)(\s+`.*)?\s*$", line)
    if not match:
        return None
    checked, number, title, rest = match.groups()
    tags = re.findall(r"`([^`]+)`", rest or "")
    difficulty = next((tag for tag in tags if tag in DIFFICULTIES), "")
    number_int = int(number)
    slug = next((tag for tag in reversed(tags) if re.fullmatch(r"[a-z0-9-]+", tag)), "")
    slug = slug or HOT100_SLUGS.get(number_int, "")
    tag_topic = next((tag for tag in tags if tag not in DIFFICULTIES and tag != slug), "")
    return Problem(
        number=number_int,
        title=title.strip(),
        topic=tag_topic or topic,
        difficulty=difficulty,
        slug=slug,
        solved=checked.lower() == "x",
        line_index=line_index,
    )


def load_questions() -> tuple[list[str], list[Problem]]:
    if not QUESTION_FILE.exists():
        raise SystemExit(f"缺少题单文件：{QUESTION_FILE}")
    lines = read_text(QUESTION_FILE).splitlines()
    topic = ""
    problems: list[Problem] = []
    for index, line in enumerate(lines):
        heading = re.match(r"^##+\s+(.+?)\s*$", line)
        if heading:
            topic = heading.group(1).strip()
            topic = re.sub(r"^[一二三四五六七八九十百\d、.\s-]+", "", topic).strip()
        problem = parse_problem_line(line, topic, index)
        if problem:
            problems.append(problem)
    return lines, problems


def format_problem_row(problem: Problem, solved: bool | None = None) -> str:
    checked = "x" if (problem.solved if solved is None else solved) else " "
    tags = []
    if problem.difficulty:
        tags.append(problem.difficulty)
    if problem.topic:
        tags.append(problem.topic)
    if problem.slug:
        tags.append(problem.slug)
    suffix = " ".join(f"`{tag}`" for tag in tags)
    return f"- [{checked}] {problem.number}. {problem.title}" + (f" {suffix}" if suffix else "")


def load_review_text() -> str:
    if not REVIEW_FILE.exists():
        raise SystemExit(f"缺少复习台账：{REVIEW_FILE}")
    return read_text(REVIEW_FILE)


def frontmatter_value(text: str, key: str, default: str = "") -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*)$", text, flags=re.MULTILINE)
    if not match:
        return default
    return match.group(1).strip().strip('"')


def set_frontmatter_value(text: str, key: str, value: str | int) -> str:
    rendered = f'{key}: "{value}"' if isinstance(value, str) and value == "" else f"{key}: {value}"
    if re.search(rf"^{re.escape(key)}:\s*.*$", text, flags=re.MULTILINE):
        return re.sub(rf"^{re.escape(key)}:\s*.*$", rendered, text, count=1, flags=re.MULTILINE)
    return text.replace("---\n", f"---\n{rendered}\n", 1)


def update_activity(text: str, count_done: bool) -> str:
    today_s = today().isoformat()
    last = frontmatter_value(text, "last_active", "")
    streak_raw = frontmatter_value(text, "streak", "0") or "0"
    total_raw = frontmatter_value(text, "total_done", "0") or "0"
    streak = int(streak_raw)
    total_done = int(total_raw)

    if last == today_s:
        new_streak = streak
    elif last == (today() - timedelta(days=1)).isoformat():
        new_streak = streak + 1
    else:
        new_streak = 1

    text = set_frontmatter_value(text, "streak", new_streak)
    text = set_frontmatter_value(text, "last_active", f'"{today_s}"')
    if count_done:
        text = set_frontmatter_value(text, "total_done", total_done + 1)
    return text


def review_rows(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_section = False
    for line in text.splitlines():
        if line.startswith("## 待复习"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8 or cells[0] in {"题号", "---"}:
            continue
        rows.append(
            {
                "number": cells[0],
                "title": cells[1],
                "topic": cells[2],
                "note": cells[3],
                "stage": cells[4],
                "next_review": cells[5],
                "mastery": cells[6],
                "review_count": cells[7],
            }
        )
    return rows


def emit_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def leetcode_url(problem_or_number: Problem | int, slug: str = "") -> str:
    if isinstance(problem_or_number, Problem):
        number = problem_or_number.number
        slug = problem_or_number.slug
    else:
        number = problem_or_number
    resolved_slug = slug or HOT100_SLUGS.get(number, "")
    if not resolved_slug:
        return ""
    return f"https://leetcode.cn/problems/{resolved_slug}/description/"


def problem_payload(problem: Problem) -> dict[str, object]:
    return {
        "number": problem.number,
        "title": problem.title,
        "topic": problem.topic,
        "difficulty": problem.difficulty,
        "slug": problem.slug,
        "url": leetcode_url(problem),
    }


def find_problem(number: int) -> Problem:
    _, problems = load_questions()
    for problem in problems:
        if problem.number == number:
            return problem
    raise SystemExit(f"题号 {number} 未在题单中找到：{QUESTION_FILE}")


def note_rel_path(number: int, title: str) -> str:
    return f"题解/{number:04d}-{title}.md"


def arg_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    return parser
