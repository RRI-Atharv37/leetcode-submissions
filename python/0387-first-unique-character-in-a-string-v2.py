# LeetCode 387. First Unique Character in a String
# Link: https://leetcode.com/problems/first-unique-character-in-a-string/
# Difficulty: Easy
# Tags: hash-table, string, counting
# Date: 261123
# Runtime: 72 ms (beats 53.72%) | Memory: 19.64 MB (beats 38.93%)

class Solution:
    def firstUniqChar(self, s: str) -> int:
        counts = {}
        for ch in s:
            counts[ch] = counts.get(ch, 0) + 1
        for i, ch in enumerate(s):
            if counts[ch] == 1:
                return i
        return -1
