// LeetCode 242. Valid Anagram
// Link: https://leetcode.com/problems/valid-anagram/
// Difficulty: Easy
// Tags: hash-table, string, sorting
// Date: 260709
// Runtime: 7 ms (beats 10.43%) | Memory: 9.63 MB (beats 67.89%)

class Solution {
public:
    bool isAnagram(string s, string t) {
        std::sort(s.begin(), s.end());
        std::sort(t.begin(), t.end());
        return s == t;
    }
};
