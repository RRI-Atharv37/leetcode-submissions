# LeetCode 2. Add Two Numbers
# Link: https://leetcode.com/problems/add-two-numbers/
# Difficulty: Medium
# Tags: linked-list, math
# Date: 250612
# Runtime: 0 ms (beats 100.00%) | Memory: 17.71 MB (beats 100.00%)

class Solution:
    def addTwoNumbers(self, l1, l2):
        dummy_head = ListNode(0)
        current = dummy_head
        carry = 0

        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            total = val1 + val2 + carry
            carry = total // 10

            current.next = ListNode(total % 10)
            current = current.next

            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

        return dummy_head.next
