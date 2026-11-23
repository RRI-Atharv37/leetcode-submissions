# LeetCode 1446. Consecutive Characters
# Link: https://leetcode.com/problems/consecutive-characters/
# Difficulty: Easy
# Tags: string
# Date: 261119
# Runtime: 3 ms (beats 80.61%) | Memory: 19.07 MB (beats 88.02%)

class Solution:
    def maxPower(self, s: str) -> int:
        best = cur = 1
        for i in range(1, len(s)):
            if s[i] == s[i-1]:
                cur += 1
                best = max(best, cur)
            else:
                cur = 1
        return best
