# LeetCode 242. Valid Anagram
# Link: https://leetcode.com/problems/valid-anagram/
# Difficulty: Easy
# Tags: hash-table, string, sorting
# Date: 261123
# Runtime: 13 ms (beats 50.76%) | Memory: 19.35 MB (beats 72.18%)

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        counts = [0] * 26
        for i in range(len(s)):
            counts[ord(s[i]) - ord("a")] += 1
            counts[ord(t[i]) - ord("a")] -= 1
        return counts == [0] * 26
