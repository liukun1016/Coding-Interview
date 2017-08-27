# -*- coding: utf-8 -*-

# Anagrams 元素出现次数一样，而且排序后也一定一样


def valid_anagram(s1, s2):
    # hash map O(N) 时间+空间
    # 排序，O(NlogN) 时间，O(N)空间（string immutable除非是char array）
    return sorted(s1) == sorted(s2)


# Given an array of strings, group anagrams together.
# https://leetcode.com/problems/group-anagrams
def group_anagrams_sort(str_list):
    # 排序后分组，O(N * M * logM)，M平均长度，N单词个数
    d = {}
    for s in str_list:
        sort = "".join(sorted(s))
        if sort in d:
            d[sort].append(s)
        else:
            d[sort] = list([s])
    return d.values()


def group_anagrams_prime(str_list):
    # 26个字母，每一个安排一个prime number，不同字母组合的乘积，肯定不一样
    # 所以算出所有str的素数乘积，乘积相等的就是anagrams，时间O(M * N)
    primes = [2, 3, 5, 7, 11 ,13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
              53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 107]
    ana_map = dict([])
    for s in str_list:
        product = 1
        for c in s:
            product *= primes[ord(c)-97]
        if product not in ana_map:
            ana_map[product] = list([])
        ana_map[product].append(s)
    return ana_map.values()


def test_group():
    str_list = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print group_anagrams_prime(str_list)
    print group_anagrams_sort(str_list)


class AnagramsWindow(object):
    def __init__(self, target):
        from collections import deque
        self.queue = deque([])
        self.target = {} # 需要比较的目标
        self.current = {} # 当前window所包含的char count map
        for c in target:
            self.target[c] = self.target.get(c, 0)+1 # char count
            self.current[c] = 0 # 初始化均为0
        self.total = len(target)
        # 这里的距离衡量的依据是，有几个char的数量是不等的，所以最多为keys的数量
        # 这一点和min substring window的概念有点像，都是找两个string之间的distance
        self.distance = self.distinct_keys = len(self.current.keys())

    def handle_change(self, c, is_remove):
        """
        如果c不在target中，删除或者新增c都不会改变距离，否则：
        删除c会把current map里面的count-1，反之新增会+1
        两种情况，都需要最后根据c在current和target中的count，来更新current与target的距离
        也就是当current[c] == target[c], distance需要-1，否则+1，但distance有上限
        """
        if c is not None and c in self.target:
            self.current[c] += -1 if is_remove else 1
            if self.current[c] == self.target[c]:
                self.distance -= 1
            else:
                # 距离最多为target中唯一char的数量
                self.distance = min(self.distinct_keys, self.distance + 1)

    def slide_right(self, new):
        self.queue.append(new)
        left = self.queue.popleft() if len(self.queue) == self.total+1 else None
        if left != new:
            # 相同则不需要改变，避免重复字符的情况，比如aaaa...a里面找aaa
            self.handle_change(left, True)
            self.handle_change(new, False)

    def is_anagram(self):
        return len(self.queue) == self.total and self.distance == 0


def substring_anagrams(s, p):
    # https://leetcode.com/problems/find-all-anagrams-in-a-string/description/
    # Given a string s and a non-empty string p, find all the start indices of p's anagrams in s.
    # 可以用暴力解法，但如果输入是：aaaa....a, p=aaa，那么会很费时，O(M * N)
    # O(N)解法，滑动窗口找距离，空间O(M)，时间O(N)
    res = []
    window = AnagramsWindow(p)
    for i, c in enumerate(s):
        window.slide_right(c)
        if window.is_anagram():
            res.append(i-len(p)+1) # 新加的是开始的index
    return res


test_list = [ ["abaacbabc", "abc"]
             ,["abcdebcafg", "abc"]
             ,["abab", "ab"]
             ,["aaaaaaaaa", "a"]
             ,["aaaaaaaaa", "aaa"]
             ,["aaaaaaaaa", "abc"]]

for test in test_list:
    print test, substring_anagrams(test[0], test[1])