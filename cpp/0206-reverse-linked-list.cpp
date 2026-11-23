// LeetCode 206. Reverse Linked List
// Link: https://leetcode.com/problems/reverse-linked-list/
// Difficulty: Easy
// Tags: linked-list
// Date: 261001
// Runtime: 0 ms (beats 100.00%) | Memory: 13.32 MB (beats 53.95%)

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode *cur, *prev, *next;
        cur = head;
        prev = nullptr;
        while(cur!=nullptr){
            next = cur->next;
            cur->next=prev;
            prev=cur;
            cur=next;
        }
        return prev;
    }
};
