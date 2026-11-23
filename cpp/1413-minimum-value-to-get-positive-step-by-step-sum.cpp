// LeetCode 1413. Minimum Value to Get Positive Step by Step Sum
// Link: https://leetcode.com/problems/minimum-value-to-get-positive-step-by-step-sum/
// Difficulty: Easy
// Tags: array, prefix-sum
// Date: 260710
// Runtime: 0 ms (beats 100.00%) | Memory: 9.80 MB (beats 85.65%)

class Solution {
public:
    int minStartValue(vector<int>& nums) {
        int minValue = 0, sum = 0;
        for(int num: nums){
            sum += num;
            minValue = std::min(minValue, sum);
        }
        return std::max(1, 1-minValue);
    }
};
