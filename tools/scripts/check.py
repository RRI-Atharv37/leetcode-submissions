"""Syntax-check every solution: Python is byte-compiled, C++ is compiled with -fsyntax-only
against tests/shim.hpp (which provides LeetCode's usual headers, ListNode and TreeNode)."""
from __future__ import annotations

import shutil
import subprocess
import sys

from leet import ROOT


def main() -> int:
    failures = 0
    checked = 0

    for f in sorted((ROOT / "python").glob("*.py")):
        try:
            compile(f.read_text(encoding="utf-8"), str(f), "exec")
            checked += 1
        except SyntaxError as e:
            failures += 1
            print(f"FAIL {f.relative_to(ROOT).as_posix()}: {e}")

    cxx = shutil.which("g++") or shutil.which("clang++")
    cpp_files = sorted((ROOT / "cpp").glob("*.cpp"))
    if cpp_files and not cxx:
        print("SKIP C++ checks: no g++/clang++ found on PATH")
    elif cxx:
        shim = ROOT / "tools" / "tests" / "shim.hpp"
        for f in cpp_files:
            r = subprocess.run([cxx, "-std=c++17", "-fsyntax-only", "-include", str(shim), str(f)],
                               capture_output=True, text=True)
            if r.returncode:
                failures += 1
                print(f"FAIL {f.relative_to(ROOT).as_posix()}:\n{r.stderr.strip()}")
            else:
                checked += 1

    print(f"{checked} files OK, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
