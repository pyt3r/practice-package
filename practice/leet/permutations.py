"""
Permutations
============

https://leetcode.com/problems/permutations/

  Description:
    Given a collection of distinct integers, return all possible permutations.

  Example:
    Input: [1,2,3]

    Output:
        [
          [1,2,3],
          [1,3,2],
          [2,1,3],
          [2,3,1],
          [3,1,2],
          [3,2,1]
        ]
"""


class Solution:
    @staticmethod
    def permute(nums: list) -> list:
        o = HeapsAlgo()
        return o.run(nums)


class HeapsAlgo:

    def __init__(self):
        self.result = []

    def run(self, elements):
        L = len(elements)
        return self.permute(elements, L, L)

    def permute(self, a, size, n):

        if size == 1:
            self.update(a, n)
            return self.getResult()

        for i in range(size):
            self.permute(a, size - 1, n)
            y = size - 1
            x = 0 if size & 1 else i
            a[x], a[y] = a[y], a[x]

        return self.getResult()

    def update(self, a, n):
        new = ()
        for i in range(n):
            new += (a[i],)

        if new not in self.result:
            self.result.append(new)

    def getResult(self):
        return self.result
# %%


def main():
    from practice.util.driver import Driver
    driver = Driver(Solution, 'permute')

    arrOfNums = [
        [1, 2, 3],
    ]

    for nums in arrOfNums:
        print("\n\nRunning..")
        driver.run(nums=nums)


if __name__ == '__main__':
    main()
