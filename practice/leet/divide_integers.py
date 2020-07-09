"""
Divide Two Integers
=========================

https://leetcode.com/problems/divide-two-integers/
  Description:
    Given two integers dividend and divisor,
    divide two integers without using multiplication,
    division and mod operator.

    Return the quotient after dividing dividend by divisor.

    The integer division should truncate toward zero,
    which means losing its fractional part.
    For example, truncate(8.345) = 8 and truncate(-2.7335) = -2.

  Example 1:
    Input:
      dividend = 10, divisor = 3

    Output:
      3

    Explanation:
      10/3 = truncate(3.33333..) = 3.

  Example 2:
    Input:
      dividend = 7, divisor = -3

    Output:
      -2

    Explanation:
      7/-3 = truncate(-2.33333..) = -2.

  Note:
    Both dividend and divisor will be 32-bit signed integers.
    The divisor will never be 0.
    Assume we are dealing with an environment
    which could only store integers within
    the 32-bit signed integer range: [−231,  231 − 1].
    For the purpose of this problem, assume that your
    function returns 231 − 1 when the division result overflows.
"""


class Solution:

    @staticmethod
    def divide(dividend: int, divisor: int) -> int:

        dividendNeg = dividend < 0
        divisorNeg = divisor < 0
        sign = -1 if dividendNeg ^ divisorNeg else 1

        dividend = abs(dividend)
        divisor = abs(divisor)

        quotient = 0
        acc = 0
        for i in range(31, -1, -1):
            """ guess == divisor*(2**i) """
            guess = divisor << i

            if acc + guess <= dividend:
                """ set the quotient bit, accumulate the guesses """
                quotient |= 1 << i
                acc += guess

        return min(max(-2**31, sign * quotient), 2**31 - 1)
# %%


def main():
    from practice.util import DriverFactory
    Driver = DriverFactory('basic')
    driver = Driver(Solution, 'divide')

    testCases = [
        ((10, 3), int(10 / 3)),
        ((7, -3), int(7 / -3)),
        ((2, 2), int(2 / 2)),
        ((-50, 3), int(-50 / 3)), ]

    err = []
    for args, expected in testCases:
        test = driver.run(dividend=args[0], divisor=args[1])
        if test != expected:
            err.append((args, expected, test))

    if err:
        print("\n\n\n----Errors:")
        for args, expected, test in err:
            print(args, expected, test)


if __name__ == '__main__':
    main()
