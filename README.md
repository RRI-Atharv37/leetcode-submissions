<div align="center">

# 🧩 LeetCode Submissions

*My LeetCode solutions in **C++** and **Python**.*

<!-- BADGES:START -->
![Solved: 12](https://img.shields.io/badge/Solved-12-blue?style=flat-square) ![Easy: 11](https://img.shields.io/badge/Easy-11-brightgreen?style=flat-square) ![Medium: 1](https://img.shields.io/badge/Medium-1-orange?style=flat-square) ![Hard: 0](https://img.shields.io/badge/Hard-0-red?style=flat-square) ![C++: 7](https://img.shields.io/badge/C%2B%2B-7-00599C?style=flat-square&logo=cplusplus&logoColor=white) ![Python: 6](https://img.shields.io/badge/Python-6-3776AB?style=flat-square&logo=python&logoColor=white)
<!-- BADGES:END -->

[📚 Full index](docs/INDEX.md) · [🏷️ By topic](docs/TOPICS.md) · [📝 Notes](docs/notes/)

</div>

---

<!-- STATS:START -->
## 📊 Progress

| Difficulty | Solved |
|---|---:|
| 🟢 Easy | 11 |
| 🟡 Medium | 1 |
| 🔴 Hard | 0 |

| Language | Problems | Submissions |
|---|---:|---:|
| C++ | 7 | 7 |
| Python | 6 | 8 |

**Top topics:** `string` (6) · `array` (4) · `hash-table` (3) · `prefix-sum` (3) · `linked-list` (2) · `counting` (1) — [all topics](docs/TOPICS.md)

### 🕒 Recent

| Date | Problem | Lang |
|---|---|---|
| 2026-11-23 | [387. First Unique Character in a String](https://leetcode.com/problems/first-unique-character-in-a-string/) | Python |
| 2026-11-23 | [242. Valid Anagram](https://leetcode.com/problems/valid-anagram/) | C++ + Python |
| 2026-11-23 | [125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Python |
| 2026-11-23 | [58. Length of Last Word](https://leetcode.com/problems/length-of-last-word/) | Python |
| 2026-11-19 | [1446. Consecutive Characters](https://leetcode.com/problems/consecutive-characters/) | Python |
<!-- STATS:END -->

---

## 🗂️ Layout

```text
cpp/      NNNN-slug.cpp           C++ solutions
python/   NNNN-slug.py            Python solutions (NNNN-slug-v2.py, ... for extra attempts)
docs/     INDEX.md, TOPICS.md     generated index and topic pages
          notes/                  optional write-ups (approach, complexity, mistakes)
tools/    scripts/, data/, tests/ helper scripts, problem metadata, C++ syntax-check shim
```

Every solution starts with a short header — problem, link, difficulty, topics, date (`yymmdd`), runtime and memory
(a snapshot from the day it was submitted; LeetCode's percentiles drift over time).

## 🛠️ Workflow

```bash
# add a solution (creates the file with its header and refreshes the index)
python tools/scripts/new.py 15 python --title "3Sum" --difficulty Medium --tags array,two-pointers,sorting

# paste your code into the new file, fill in runtime/memory, then
python tools/scripts/build_index.py     # regenerate README stats, INDEX.md, TOPICS.md
python tools/scripts/check.py           # syntax-check every solution
```

[`tools/data/problems.json`](tools/data/problems.json) is the single source of truth for titles, difficulty and tags:
edit it and re-run `build_index.py` to update the index pages *and* the matching header lines in every solution.
`build_index.py` also validates the repo (file names, slugs, dates, `-vN` numbering, note names) and stops on errors.

Optional: `pip install pre-commit && pre-commit install` keeps the generated files in sync on every commit,
and the GitHub Action runs `build_index.py --check` and `check.py` on every push and pull request.
Requires Python 3.8+ (and `g++` or `clang++` for the C++ check).

## 📄 License

[MIT](LICENSE) © Atharv Dewangan
