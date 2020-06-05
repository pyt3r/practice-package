import unittest
from practice.util.driver import Driver


class MockSolution:
    @staticmethod
    def someProblem(a, b, c):
        return a + b + c


class TestCase(unittest.TestCase):

    def test_util(self):
        driver = Driver(MockSolution, 'someProblem')
        return driver.run(a=1, b=2, c=3)
