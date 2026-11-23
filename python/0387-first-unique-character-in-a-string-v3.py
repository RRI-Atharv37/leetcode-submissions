# LeetCode 387. First Unique Character in a String
# Link: https://leetcode.com/problems/first-unique-character-in-a-string/
# Difficulty: Easy
# Tags: hash-table, string, counting
# Date: 261123
# Runtime: 70 ms (beats 61.37%) | Memory: 19.56 MB (beats 67.59%)

class Solution:
    def firstUniqChar(self, s: str) -> int:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - ord("a")] += 1
        for i, ch in enumerate(s):
            if counts[ord(ch)-ord("a")] == 1:
                return i
        return -1
