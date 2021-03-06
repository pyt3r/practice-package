"""
Two Sum
===============

https://leetcode.com/problems/two-sum/

  Description:
    Given an array of integers,
    return indices of the two numbers,
    such that they add up to a specific target.

    You may assume that each input would have exactly one solution,
    and you may not use the same element twice.

  Example:
    Input:
      nums = [2, 7, 11, 15]

      target = 9

    Output:
      [0, 1]

    Explanation:
      nums[0] + nums[1] = 2 + 7 = 9


One solution to this problem is posted, as follows:
"""


class Solution:

    @staticmethod
    def twoSum(nums: list, target: int) -> list:
        solution = None
        for ptr in range(len(nums) - 1):
            success, solution = Solution.helper(ptr, nums, target)
            if success:
                break
        return solution

    @staticmethod
    def helper(ptr, nums, target):
        success, solution = False, None
        for i, n in enumerate(nums[ptr + 1:], 1):
            test = nums[ptr] + n
            if test == target:
                return True, [ptr, ptr + i]
        return success, solution
# %%


def main():
    from practice.util import DriverFactory
    Driver = DriverFactory('basic')
    driver = Driver(Solution, 'twoSum')
    driver.run(
        nums=[2, 7, 11, 15],
        target=9, )


if __name__ == '__main__':
    main()
