# 387. First Unique Character in a String

## Idea
Two passes: count every character, then return the first index whose count is 1.

## Attempts
| File | Counting structure | Runtime | Notes |
|---|---|---|---|
| [v1](../../python/0387-first-unique-character-in-a-string-v1.py) | `dict` with `if ch in counts` | 80 ms | Baseline. |
| [v2](../../python/0387-first-unique-character-in-a-string-v2.py) | `dict` with `counts.get(ch, 0) + 1` | 72 ms | Same idea, shorter and slightly faster. |
| [v3](../../python/0387-first-unique-character-in-a-string-v3.py) | `[0] * 26` indexed by `ord(ch) - ord("a")` | 70 ms | Fixed-size array; only valid because the input is lowercase letters. |

## Complexity
- Time: O(n)
- Space: O(1) — at most 26 distinct keys.

## Pitfalls
- The array version relies on the constraint "lowercase English letters"; the dict versions work for any characters.
