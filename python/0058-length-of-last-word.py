# LeetCode 58. Length of Last Word
# Link: https://leetcode.com/problems/length-of-last-word/
# Difficulty: Easy
# Tags: string
# Date: 261123
# Runtime: 0 ms (beats 100.00%) | Memory: 19.05 MB (beats 88.62%)

class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        i = len(s) - 1
        while i >= 0 and s[i] == " ":
            i -= 1
        end = i
        while i >= 0 and s[i] != " ":
            i -= 1
        return end - i
