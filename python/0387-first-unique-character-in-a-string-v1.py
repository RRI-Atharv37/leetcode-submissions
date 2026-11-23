# LeetCode 387. First Unique Character in a String
# Link: https://leetcode.com/problems/first-unique-character-in-a-string/
# Difficulty: Easy
# Tags: hash-table, string, counting
# Date: 261123
# Runtime: 80 ms (beats 28.28%) | Memory: 19.52 MB (beats 67.59%)

class Solution:
    def firstUniqChar(self, s: str) -> int:
        counts = {}
        for ch in s:
            if ch in counts:
                counts[ch] += 1
            else:
                counts[ch] = 1
        for i, ch in enumerate(s):
            if counts[ch] == 1:
                return i
        return -1
