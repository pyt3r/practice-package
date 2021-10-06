"""
Median Sorted Arrays
====================

https://leetcode.com/problems/median-of-two-sorted-arrays/

  Description:
    There are two sorted arrays
    nums1 and nums2 of size m and n respectively.

    Find the median of the two sorted arrays.
    The overall run time complexity should be
    O(log (m+n)).

    You may assume nums1 and nums2 cannot be both empty.

  Example 1:
    nums1 = [1, 3]

    nums2 = [2]

    The median is 2.0

  Example 2:
    nums1 = [1, 2]

    nums2 = [3, 4]

    The median is (2 + 3)/2 = 2.5


One solution to this problem is posted, as follows:
"""


class Solution:

    @staticmethod
    def medianSortedArrays(nums1: list, nums2: list) -> float:
        length = len(nums1) + len(nums2)

        if not length:
            raise ValueError(nums1, nums2)

        outlist = []
        while nums1 and nums2:

            if nums1[0] <= nums2[0]:
                new = nums1.pop(0)

            elif nums1[0] > nums2[0]:
                new = nums2.pop(0)

            outlist.append(new)

        outlist.extend(nums1)
        outlist.extend(nums2)

        middle = length // 2

        if length % 2 == 0:
            return (outlist[middle - 1] + outlist[middle]) / 2.

        else:
            return outlist[middle]
# %%


def main():

    from practice.util import DriverFactory
    Driver = DriverFactory('basic')
    driver = Driver(Solution, 'medianSortedArrays')

    args = [
        ([1, 3], [2]),
        ([1, 2], [3, 4]), ]

    for nums1, nums2 in args:
        driver.run(
            nums1=nums1,
            nums2=nums2, )


if __name__ == '__main__':
    main()
