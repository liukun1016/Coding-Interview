# -*- coding: utf-8 -*-
from collections import defaultdict,deque
import sys


def findLongestPalidrome(s):
    # 给一个字符串，求用其中字符组成的最长的回文字符串（如有多解，给一个答案即可）
    # 如"aabb"就是"abba","aabcbcd"就是"abcdcba"
    cc = defaultdict(int)
    for c in s:
        cc[c] += 1
    leftPart = []
    midChar = ''
    for c, count in cc.items():
        leftPart.append(c * (count / 2))
        if count % 2 != 0:
            # odd numbers count char, update midChar
            midChar = c
    return '{}{}{}'.format(''.join(leftPart), midChar, ''.join(leftPart[::-1]))

print findLongestPalidrome('aabb')
print findLongestPalidrome('aabbccddde')


def binary_tree_max_value_per_level(root):
    res = []
    if root:
        queue = deque([root])
        while queue:
            size = queue
            currMax = -sys.maxint
            while size:
                size -= 1
                node = queue.popleft()
                currMax = max(currMax, node.val)
            res.append(currMax)

    return res


def proudct_of_array_except_itself(nums):
    """
    https://leetcode.com/problems/product-of-array-except-self/description/
    可以用数组预处理的方式来计算，也可以节省空间，第一轮处理
         p:  1  n1  n1n2    n1n2n3
    output:  1  n1  n1n2    n1n2n3
    第二轮，逆序遍历
    output:  1       n1     n1n2    n1n2n3
         p:  n2n3n4  n3n4   n4      1
    output:  n2n3n4  n1n3n4 n1n2n4  n1n2n3

    """
    p = 1
    pei = []
    for n in nums:
        pei.append(p)
        p = p * n

    p = 1
    for i in xrange(len(nums)-1, -1, -1):
        pei[i] = pei[i] * p
        p = p * nums[i]

    return pei


def product2(nums):
    """
    nums:    n0         n1          n2          n3
    res:  n1n2n3    n0n2n3      n0n1n3      n0n1n2

    rolling product array, p1 and p2
    1st: l->r
    p1:      1           n0        n0n1      n0n1n2 (except n3)

    2nd: r->l
    p2:  n1n2n3        n2n3        n3     1

    res:  n1n2n3    n0n2n3      n0n1n3      n0n1n2
    output: p1[i] * p2[i] -> res[i]
    """
    p1 = [1]
    for i in xrange(len(nums) - 1):
        p1.append(p1[-1] * nums[i])

    from collections import deque
    p2 = deque([1])
    for i in xrange(len(nums) - 1, 0, -1):
        p2.appendleft(p2[-1] * nums[i])

    res = []
    for i in xrange(len(nums)):
        res.append(p1[i] * p2[i])

    return res, p1, p2


def trailing_zero(n):
    # https://leetcode.com/problems/factorial-trailing-zeroes/
    # Given an integer n, return the number of trailing zeroes in n!.
    # 前n个数，把所有5的倍数都提取出来 e.g 5\10\15，n!里面不会有trailing zero
    # 有多少个5的倍数，就有多少个trailing zero，所以就是找到前n个数当中，有多少个5的倍数
    # n! = x * (2 * 5 * m) - x 就是trailing zero前边的数字，m是最后的结果
    # 5! = 120, 10! = 362800, 15! = 1307674368000, 20! = 2432902008176640000
    M = 0
    while n > 0:
        n = n / 5
        M += n
    return M


def valid_palindrome(s):
    if not s:
        return True
    l, r = 0, len(s)-1
    while l < r:
        while l < r and not s[l].isalnum(): l += 1
        while l < r and not s[r].isalnum(): r -= 1
        if s[l].lower() != s[r].lower():
            return False
        l += 1
        r -= 1
    return True


class Solution(object):
    def validPalindromeOneDeletion(self, s):
        def is_palindrome(s, i, j):
            while i < j:
                if s[i] == s[j]:
                    i, j = i+1, j-1
                else:
                    return False
            return True

        left, right = 0, len(s)-1
        while left < right and s[left] == s[right]:
            left, right = left + 1, right - 1
        if left >= right:
            # 此时说明，所有的都检查完了，string已经是匹配的了
            return True
        # 否则，删除left，匹配剩下的s[left+1:right]，或者删除right，匹配剩下的s[left:right-1]
        return is_palindrome(s, left+1, right) or is_palindrome(s, left, right-1)


def squares_of_sorted_array(nums):
    """
    https://leetcode.com/problems/squares-of-a-sorted-array/
    两个指针，找到negative v.s. non negative，左边从右往左遍历，右边从左往右
    Use 2 pointers, [0...p1] all negaitive [p2...n-1] all non negative
    Merge sort the square of negative subarray v.s. non negative subarray
    """
    res = []
    p1 = 0
    while p1 < len(nums) and nums[p1] < 0:
        p1 += 1
    # now 0...p1-1 all negative, p1...n-1 all non negative
    p2, p1 = p1, p1 - 1
    while p1 >= 0 or p2 < len(nums):
        s1 = nums[p1] * nums[p1] if p1 >= 0 else float('inf')
        s2 = nums[p2] * nums[p2] if p2 < len(nums) else float('inf')
        if s1 > s2:
            res.append(s2)
            p2 += 1
        else:
            res.append(s1)
            p1 -= 1

    return res


def testSquare():
    nums = [
        [1, 2, 3, 4, 5],
        [-4, -2, 0, 3, 5],
        [-4, -3, -2, -1, 0],
    ]
    for num in nums:
        print squares_of_sorted_array(num)


def moveZeros(nums):
    # https://leetcode.com/problems/move-zeroes/
    # 2 pointers: 0...i -> all non zero values, i+1...j -> all zero values
    # j+1 not zero, swap it with i+1, then move j until a non zero value
    pass

