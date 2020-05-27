import unittest
from practice.leet.two_sum import Solution
from practice.util.driver import Driver


class TestCase(unittest.TestCase):

    def test_two_sum(self):
        driver = Driver(Solution, 'twoSum')
        return driver.run(
            nums=[2, 7, 11, 15],
            target=9, )
