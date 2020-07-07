"""
Minimum Path Sum
================

https://leetcode.com/problems/minimum-path-sum/

  Description:
    Given a m x n grid filled with non-negative numbers,
    find a path from top left to bottom right,
    which minimizes the sum of all numbers along its path.

  Note:
    You can only move either down or right at any point in time.

  Example:
    Input:
      [
        [1,3,1],
        [1,5,1],
        [4,2,1],
      ]
    Output:
      7

    Explanation:
      Because the path 1→3→1→1→1 minimizes the sum.
"""


class Solution:
    @staticmethod
    def minPathSum(grid: list) -> int:

        m, n = len(grid)-1, len(grid[0])-1

        if any((m<0, n<0)):
            return 0

        for i in range(n):
            grid[0][i+1] += grid[0][i]

        for i in range(m):
            grid[i+1][0] += grid[i][0]

        for i in range(m):
            for j in range(n):
                grid[i+1][j+1] += min(grid[i][j+1], grid[i+1][j])

        return grid[m][n]
# %%


def main():
    from practice.util import DriverFactory
    Driver = DriverFactory('basic')
    driver = Driver(Solution, 'minPathSum')
    driver.run(
        grid=[
            [1,3,1],
            [1,5,1],
            [4,2,1], ])


if __name__ == '__main__':
    main()
