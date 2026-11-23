"""Shared helpers for the LeetCode repo scripts."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "tools" / "data" / "problems.json"
NOTES = ROOT / "docs" / "notes"

LANGS = {
    "cpp": {"name": "C++", "ext": "cpp", "comment": "//"},
    "python": {"name": "Python", "ext": "py", "comment": "#"},
}
DIFFICULTIES = ["Easy", "Medium", "Hard"]
DIFF_EMOJI = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FILE_RE = re.compile(r"^(\d{4})-([a-z0-9-]+?)(?:-v(\d+))?\.(cpp|py)$")
NOTE_RE = re.compile(r"^(\d{4})-([a-z0-9-]+)\.md$")
DATE_RE = re.compile(r"Date:\s*(\d{6})\b")
STAT_RE = re.compile(
    r"Runtime:\s*(\S+) ms \(beats (\S+?)%\)\s*\|\s*Memory:\s*(\S+) MB \(beats (\S+?)%\)"
)
# The first lines of every header mirror problems.json; build_index.py keeps them in sync.
SYNCED_PREFIXES = ("LeetCode ", "Link: ", "Difficulty: ", "Tags: ")


@dataclass
class Problem:
    number: int
    title: str
    slug: str
    difficulty: str
    tags: list = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"https://leetcode.com/problems/{self.slug}/"


@dataclass
class Submission:
    number: int
    slug: str
    lang: str
    version: int | None
    path: str  # repo-relative, posix style
    date: str | None
    runtime: str | None
    runtime_beats: str | None
    memory: str | None
    memory_beats: str | None


def normalize_tag(tag: str) -> str:
    return re.sub(r"[\s_]+", "-", tag.strip().lower())


def parse_date(yymmdd: str) -> datetime | None:
    """Parse a yymmdd string; None if it isn't a real calendar date."""
    try:
        return datetime.strptime(yymmdd, "%y%m%d")
    except (TypeError, ValueError):
        return None


def pretty_date(yymmdd: str | None) -> str:
    d = parse_date(yymmdd) if yymmdd else None
    return d.strftime("%Y-%m-%d") if d else (yymmdd or "?")


def load_problems() -> dict[int, Problem]:
    items = json.loads(DATA.read_text(encoding="utf-8"))
    problems: dict[int, Problem] = {}
    errors = []
    for item in items:
        p = Problem(**item)
        where = f"tools/data/problems.json: problem {p.number}"
        if p.number in problems:
            errors.append(f"{where} is listed twice")
        if p.difficulty not in DIFFICULTIES:
            errors.append(f"{where} has difficulty '{p.difficulty}' (expected one of {DIFFICULTIES})")
        if not SLUG_RE.match(p.slug):
            errors.append(f"{where} has an invalid slug '{p.slug}'")
        bad_tags = [t for t in p.tags if t != normalize_tag(t) or not t]
        if bad_tags:
            errors.append(f"{where} has non-normalized tags {bad_tags} (use lowercase-with-dashes)")
        problems[p.number] = p
    if errors:
        fail(errors)
    return problems


def save_problems(problems: dict[int, Problem]) -> None:
    items = [
        {"number": p.number, "title": p.title, "slug": p.slug, "difficulty": p.difficulty, "tags": p.tags}
        for _, p in sorted(problems.items())
    ]
    DATA.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("[\n")
        fh.write(",\n".join("  " + json.dumps(i, ensure_ascii=False) for i in items))
        fh.write("\n]\n")


def fail(errors: list[str]) -> None:
    print("Problems found:", *errors, sep="\n  - ")
    raise SystemExit(1)


def _clean(v: str | None) -> str | None:
    return None if v in (None, "?") else v


def split_file(text: str) -> tuple[str, str]:
    """Split a solution file into (header, body) at the first blank line."""
    text = text.replace("\r\n", "\n")
    head, _, body = text.partition("\n\n")
    return head, body


def parse_header(head: str) -> dict:
    out = {"date": None, "runtime": None, "runtime_beats": None, "memory": None, "memory_beats": None}
    m = DATE_RE.search(head)
    if m:
        out["date"] = m.group(1)
    m = STAT_RE.search(head)
    if m:
        out["runtime"], out["runtime_beats"], out["memory"], out["memory_beats"] = (_clean(g) for g in m.groups())
    return out


def render_header(p: Problem, lang: str, date: str, runtime=None, runtime_beats=None,
                  memory=None, memory_beats=None) -> str:
    c = LANGS[lang]["comment"]
    q = lambda v: "?" if v is None else v  # noqa: E731
    return (
        f"{c} LeetCode {p.number}. {p.title}\n"
        f"{c} Link: {p.url}\n"
        f"{c} Difficulty: {p.difficulty}\n"
        f"{c} Tags: {', '.join(p.tags)}\n"
        f"{c} Date: {date}\n"
        f"{c} Runtime: {q(runtime)} ms (beats {q(runtime_beats)}%) | "
        f"Memory: {q(memory)} MB (beats {q(memory_beats)}%)\n"
    )


def sync_header(text: str, p: Problem, lang: str) -> str | None:
    """Return `text` with the problems.json-derived header lines refreshed,
    or None if the file doesn't start with the expected header lines."""
    c = LANGS[lang]["comment"]
    lines = text.replace("\r\n", "\n").split("\n")
    n = len(SYNCED_PREFIXES)
    if len(lines) < n or any(not lines[i].startswith(f"{c} {pre}") for i, pre in enumerate(SYNCED_PREFIXES)):
        return None
    lines[:n] = render_header(p, lang, "").split("\n")[:n]
    return "\n".join(lines)


def scan(problems: dict[int, Problem]) -> tuple[list[Submission], list[str]]:
    subs: list[Submission] = []
    errors: list[str] = []
    for lang, info in LANGS.items():
        folder = ROOT / lang
        if not folder.is_dir():
            continue
        for f in sorted(folder.iterdir()):
            if not f.is_file():
                continue
            m = FILE_RE.match(f.name)
            rel = f.relative_to(ROOT).as_posix()
            if not m or m.group(4) != info["ext"]:
                errors.append(f"{rel}: bad file name (expected NNNN-slug[-vN].{info['ext']})")
                continue
            num, slug, ver = int(m.group(1)), m.group(2), m.group(3)
            p = problems.get(num)
            if p is None:
                errors.append(f"{rel}: problem {num} missing from tools/data/problems.json")
                continue
            if p.slug != slug:
                errors.append(f"{rel}: slug '{slug}' != '{p.slug}' in tools/data/problems.json")
                continue
            text = f.read_text(encoding="utf-8")
            if sync_header(text, p, lang) is None:
                errors.append(f"{rel}: header must start with the LeetCode/Link/Difficulty/Tags lines")
            meta = parse_header(split_file(text)[0])
            if meta["date"] is None:
                errors.append(f"{rel}: header has no 'Date: yymmdd' line")
            elif parse_date(meta["date"]) is None:
                errors.append(f"{rel}: 'Date: {meta['date']}' is not a valid yymmdd date")
            subs.append(Submission(num, slug, lang, int(ver) if ver else None, rel, **meta))
    subs.sort(key=lambda s: (s.number, s.lang, s.version or 0))

    # A problem's files in one language must be either a single plain file or all -vN, with unique N.
    groups: dict[tuple[int, str], list[Submission]] = {}
    for s in subs:
        groups.setdefault((s.number, s.lang), []).append(s)
    for (num, lang), group in groups.items():
        versions = [s.version for s in group]
        if len(group) > 1 and None in versions:
            errors.append(f"{lang}/{num:04d}-*: mixes an unversioned file with -vN files; rename it to -v1")
        elif len(set(versions)) != len(versions):
            errors.append(f"{lang}/{num:04d}-*: duplicate version numbers {versions}")

    if NOTES.is_dir():
        for f in sorted(NOTES.glob("*.md")):
            if f.name.startswith("_") or f.name == "README.md":
                continue
            m = NOTE_RE.match(f.name)
            rel = f.relative_to(ROOT).as_posix()
            if not m:
                errors.append(f"{rel}: bad note name (expected NNNN-slug.md)")
            elif int(m.group(1)) not in problems or problems[int(m.group(1))].slug != m.group(2):
                errors.append(f"{rel}: doesn't match a problem in tools/data/problems.json")
    return subs, errors
