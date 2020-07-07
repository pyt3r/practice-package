"""
Container with Most Water
=========================

https://leetcode.com/problems/container-with-most-water/

  Description:
    Given n non-negative integers a1, a2, ..., an ,
    where each represents a point at coordinate (i, ai).
    n vertical lines are drawn such that the two endpoints
    of line i is at (i, ai) and (i, 0). Find two lines,
    which together with x-axis forms a container,
    such that the container contains the most water.

    Note: You may not slant the container and n is at least 2.

  Example:
    Input: [1,8,6,2,5,4,8,3,7]

    Output: 49


One solution to this problem is posted, as follows:
"""


class Solution:

    @staticmethod
    def maxArea(height: list) -> int:
        MAX = 0
        x = len(height) - 1
        y = 0
        while x != y:
            if height[x] > height[y]:
                area = height[y] * (x - y)
                y += 1
            else:
                area = height[x] * (x - y)
                x -= 1
            MAX = max(MAX, area)
        return MAX
# %%


def main():
    from practice.util import DriverFactory
    Driver = DriverFactory('basic')
    driver = Driver(Solution, 'maxArea')

    driver.run(height=[1, 8, 6, 2, 5, 4, 8, 3, 7])


if __name__ == '__main__':
    main()
