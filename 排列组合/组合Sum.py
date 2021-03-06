# -*- coding: utf-8 -*-


def combination_sum_reusable(candidates, target):
    # https://leetcode.com/problems/combination-sum/description/
    # 所有数字为正，且可以有无穷多个，但是结果不能有重复的，candidates是一个list
    def dfs(res, candidates, path, target):
        if target == 0:  # 找到一个path为结果
            res.append(path)
        elif target > 0:
            for i, x in enumerate(candidates):
                if x <= target:  # smart search
                    # this guarantee path node is appended in increasing order
                    dfs(res, candidates[i:], path + [x], target - x)

    if not candidates or not target:
        return []
    res, path = [], []
    # Use DFS to record results
    dfs(res, sorted(candidates), path, target)
    return res


def combination_sum_no_reuse(candidates, target):
    # https://leetcode.com/problems/combination-sum-ii/description/
    # 所有数字为正，但是只能用一个，但是结果不能有重复的，candidates是一个list
    def dfs(res, candidates, path, target):
        if target == 0:  # 找到一个path为结果
            res.append(path)
        elif target > 0:
            for i, x in enumerate(candidates):
                if x <= target:  # smart search
                    # this guarantee path node is appended in increasing order
                    dfs(res, candidates[i+1:], path + [x], target - x)

    if not candidates or not target:
        return []
    res, path = [], []
    # Use DFS to record results
    dfs(res, sorted(candidates), path, target)
    return res
