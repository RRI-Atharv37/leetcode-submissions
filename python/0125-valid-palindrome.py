# LeetCode 125. Valid Palindrome
# Link: https://leetcode.com/problems/valid-palindrome/
# Difficulty: Easy
# Tags: two-pointers, string
# Date: 261123
# Runtime: 6 ms (beats 88.73%) | Memory: 19.55 MB (beats 70.94%)

class Solution:
    def isPalindrome(self, s: str) -> bool:
        clean = ""
        for ch in s:
            if ch.isalnum():
                clean += ch.lower()
        i,j = 0, len(clean) - 1
        while i < j:
            if not clean[i] == clean[j]:
                return False
            else:
                i += 1
                j -= 1
        return True
