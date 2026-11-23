// LeetCode 1614. Maximum Nesting Depth of the Parentheses
// Link: https://leetcode.com/problems/maximum-nesting-depth-of-the-parentheses/
// Difficulty: Easy
// Tags: string, stack
// Date: 260928
// Runtime: 0 ms (beats 100.00%) | Memory: 8.41 MB (beats 24.95%)

class Solution {
public:
    int maxDepth(string s) {
        int maxdepth{};
        int depth{};
        for(char c: s){
            depth += (c == '(') - (c == ')');
            maxdepth = max(maxdepth, depth);
        }
        return maxdepth;
    }
};
