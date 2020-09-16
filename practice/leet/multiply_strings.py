"""
Multiply Strings
=========================

https://leetcode.com/problems/multiply-strings/

    Description
      Given two non-negative integers num1 and num2
      represented as strings, return the product of num1 and num2,
      also represented as a string.

    Example 1:
      Input:
        num1 = "2"

        num2 = "3"

      Output:
        "6"

    Example 2:
      Input:
        num1 = "123"

        num2 = "456"

      Output:
        "56088"

    Note:
      The length of both num1 and num2 is < 110.

      Both num1 and num2 contain only digits 0-9.

      Both num1 and num2 do not contain any leading zero,
      except the number 0 itself.

      You must not use any built-in BigInteger library
      or convert the inputs to integer directly.
"""


class Solution:

    @staticmethod
    def multiply(num1: str, num2: str) -> str:
        return str(to_int(num1) * to_int(num2))


def to_int(num):
    j = len(num) - 1
    acc, i = 0, 0
    while j >= 0:
        acc += int(num[j]) * int("1" + "0" * i)
        j -= 1
        i += 1
    return acc
# %%


def main():
    from practice.util import DriverFactory
    Driver = DriverFactory('basic')
    driver = Driver(Solution, 'multiply')

    numbers = [
        ("3", "5"),
        ("123", "456"), ]

    for num1, num2 in numbers:
        driver.run(num1=num1, num2=num2)


if __name__ == '__main__':
    main()
