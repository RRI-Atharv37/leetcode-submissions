// LeetCode 303. Range Sum Query - Immutable
// Link: https://leetcode.com/problems/range-sum-query-immutable/
// Difficulty: Easy
// Tags: array, design, prefix-sum
// Date: 260710
// Runtime: 3 ms (beats 75.61%) | Memory: 23.99 MB (beats 43.83%)

class NumArray {
public:
    vector<int> prefixSum;

    NumArray(vector<int>& nums) {
        if(nums.empty()) return;

    //     prefixSum.push_back(0);
    //     int sum = 0;
    //     for(int num: nums){
    //         sum += num;
    //         prefixSum.push_back(sum);
    //     }
    // }
        int n = nums.size();
        prefixSum.resize(n + 1, 0);
        for(int i = 0; i < n; i++){
            prefixSum[i+1] = prefixSum[i]+nums[i];
        }
    }

    int sumRange(int left, int right) {
        return prefixSum[right+1] - prefixSum[left];
    }
};

/**
 * Your NumArray object will be instantiated and called as such:
 * NumArray* obj = new NumArray(nums);
 * int param_1 = obj->sumRange(left,right);
 */
