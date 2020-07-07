"""
Zig Zag
===============

https://leetcode.com/problems/zigzag-conversion/

  Description:
    The string "PAYPALISHIRING" is written in a zigzag
    pattern on a given number of rows like this::
      P   A   H   N

      A P L S I I G

      Y   I   R

    And then read line by line: "PAHNAPLSIIGYIR"

    Write the code that will take a string and
    make this conversion given a number of rows.

  Example 1:
      Input:
        s = "PAYPALISHIRING"

        numRows = 3

      Output:
        "PAHNAPLSIIGYIR"

  Example 2:
      Input:
        s = "PAYPALISHIRING"

        numRows = 4

      Output:
        "PINALSIGYAHRPI"

      Explanation:
        P     I    N

        A   L S  I G

        Y A   H R

        P     I

One solution to this problem is posted, as follows:
"""


class Solution:

    @staticmethod
    def zigzag(s: str, numRows: int) -> str:

        if numRows == 0 or numRows == 1:
            return s

        step = -1
        rows, idx = [''] * numRows, 0

        for c in s:
            rows[idx] += c
            if idx == 0 or idx == numRows - 1:
                step = -step  # change direction
            idx += step

        return ''.join(rows)
# %%


def main():
    from practice.util import DriverFactory
    Driver = DriverFactory('basic')
    driver = Driver(Solution, 'zigzag')

    args = [
        ("PAYPALISHIRING", 3),
        ("PAYPALISHIRING", 4), ]

    for s, numRows in args:
        print("\n\nRunning...")
        driver.run(
            s=s,
            numRows=numRows, )


if __name__ == '__main__':
    main()
