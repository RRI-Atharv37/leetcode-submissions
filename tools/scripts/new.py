"""Create a new solution file with a filled-in header, then refresh the index.

Examples:
    python tools/scripts/new.py 1 cpp --date 260709 --runtime 42 --runtime-beats 28.47 --memory 14.10 --memory-beats 74.26
    python tools/scripts/new.py 15 python --title "3Sum" --difficulty Medium --tags array,two-pointers,sorting

--title/--difficulty/--tags are only needed the first time a problem number is used
(to change them later, edit tools/data/problems.json and run build_index.py).
If the problem already has a file in that language, the old one becomes -v1 and the new one -v2 (and so on).
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date as _date

import build_index
import leet
from leet import DIFFICULTIES, LANGS, ROOT, Problem

ALIASES = {"cpp": "cpp", "c++": "cpp", "python": "python", "py": "python"}
STUBS = {
    "cpp": "class Solution {\npublic:\n};\n",
    "python": "class Solution:\n    pass\n",
}


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def lang_arg(s: str) -> str:
    try:
        return ALIASES[s.lower()]
    except KeyError:
        raise argparse.ArgumentTypeError(f"unknown language '{s}' (choose from {', '.join(ALIASES)})") from None


def date_arg(s: str) -> str:
    if leet.parse_date(s) is None:
        raise argparse.ArgumentTypeError(f"'{s}' is not a valid yymmdd date")
    return s


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("number", type=int)
    ap.add_argument("lang", type=lang_arg, metavar="{cpp,python}")
    ap.add_argument("--title")
    ap.add_argument("--slug")
    ap.add_argument("--difficulty", type=str.capitalize, choices=DIFFICULTIES)
    ap.add_argument("--tags", default="", help="comma separated, e.g. array,hash-table")
    ap.add_argument("--date", type=date_arg, default=_date.today().strftime("%y%m%d"), help="yymmdd (default: today)")
    ap.add_argument("--runtime")
    ap.add_argument("--runtime-beats")
    ap.add_argument("--memory")
    ap.add_argument("--memory-beats")
    a = ap.parse_args()
    if a.number < 1:
        ap.error("problem number must be positive")

    problems = leet.load_problems()
    p = problems.get(a.number)
    if p is None:
        if not (a.title and a.difficulty):
            ap.error(f"problem {a.number} is new: pass --title and --difficulty (and --tags)")
        slug = a.slug or slugify(a.title)
        if not leet.SLUG_RE.match(slug):
            ap.error(f"invalid slug '{slug}': pass --slug explicitly (copy it from the problem URL)")
        tags = list(dict.fromkeys(t for t in map(leet.normalize_tag, a.tags.split(",")) if t))
        p = Problem(a.number, a.title.strip(), slug, a.difficulty, tags)
        problems[a.number] = p
        leet.save_problems(problems)
        print(f"Added problem {p.number} to tools/data/problems.json")
    elif a.title or a.slug or a.difficulty or a.tags:
        print(f"Note: problem {p.number} already exists; --title/--slug/--difficulty/--tags were ignored "
              "(edit tools/data/problems.json to change them)")

    ext = LANGS[a.lang]["ext"]
    folder = ROOT / a.lang
    folder.mkdir(exist_ok=True)
    base = f"{p.number:04d}-{p.slug}"
    plain = folder / f"{base}.{ext}"
    versions = sorted(int(m.group(1)) for f in folder.glob(f"{base}-v*.{ext}")
                      if (m := re.fullmatch(rf"{re.escape(base)}-v(\d+)\.{ext}", f.name)))
    if plain.exists() and versions:
        sys.exit(f"Both {plain.name} and -vN files exist for problem {p.number}; rename {plain.name} first")
    if plain.exists():
        plain.rename(folder / f"{base}-v1.{ext}")
        print(f"Renamed {plain.name} -> {base}-v1.{ext}")
        target = folder / f"{base}-v2.{ext}"
    elif versions:
        target = folder / f"{base}-v{versions[-1] + 1}.{ext}"
    else:
        target = plain

    header = leet.render_header(p, a.lang, a.date, a.runtime, a.runtime_beats, a.memory, a.memory_beats)
    with open(target, "x", encoding="utf-8", newline="\n") as fh:  # "x": never overwrite
        fh.write(header + "\n" + STUBS[a.lang])
    print(f"Created {target.relative_to(ROOT).as_posix()}")
    return build_index.main([])


if __name__ == "__main__":
    sys.exit(main())
