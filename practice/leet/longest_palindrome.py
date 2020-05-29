"""
Longest Palindromic Substring
=====================================

https://leetcode.com/problems/longest-palindromic-substring/

  Description:
    Given a string s,
    find the longest palindromic substring in s.
    You may assume that the maximum length of s is 1000.

  Example 1:
    Input: "babad"

    Output: "bab"

    Note: "aba" is also a valid answer.

  Example 2:
    Input: "cbbd"

    Output: "bb"

One solution to this problem is posted, as follows:
"""


class Solution:

    @staticmethod
    def longestPalindrome(s: str) -> str:

        length = len(s)

        if not length:
            return s

        result, lenResult = s[0], 1

        helper = make_helper(s, length)

        for i in range(length - 1):

            A, lenA = helper(i, i)
            B, lenB = helper(i, i + 1)

            if lenA > lenB:
                tmp, lenTmp = A, lenA
            else:
                tmp, lenTmp = B, lenB

            if lenTmp > lenResult:
                result, lenResult = tmp, lenTmp

        return result


def make_helper(s, length):
    '''
    make a helper function,
    which starts in the center and
    works outwards
    '''

    def helper(L, R):

        while s[L] == s[R]:
            R += 1
            L -= 1

            if R == length:
                break
            if L == -1:
                break
        L += 1
        return s[L:R], R - L

    return helper

# %%


def main():
    from practice.util.driver import Driver
    driver = Driver(Solution, 'longestPalindrome')

    strings = [
        "babad",
        "cbbd", ]

    for s in strings:
        print("\n\nRunning..")
        driver.run(s=s)


if __name__ == '__main__':
    main()
