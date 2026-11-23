// LeetCode 724. Find Pivot Index
// Link: https://leetcode.com/problems/find-pivot-index/
// Difficulty: Easy
// Tags: array, prefix-sum
// Date: 260710
// Runtime: 0 ms (beats 100.00%) | Memory: 35.80 MB (beats 27.01%)

class Solution {
public:
    int pivotIndex(vector<int>& nums) {
        int n = nums.size();

        for(int i = 1; i < n; i++){
            nums[i] += nums[i-1];
        }

        for(int i = 0; i < n; i++){
            int left;
            if(i == 0){
                left = 0;
            } else{
                left = nums[i-1];
            }

            int right = nums[n-1] - nums[i];

            if(left == right) return i;
        }

        return -1;
    }
};
