import unittest
from practice.frameworks.table import Table


class TestCase(unittest.TestCase):

    def test_example(self):
        rows = [
            [1,2,3,4],
            [5,6,7,8],
            [9,7,5,3], ]

        table = Table.fromList(rows, [1,2,"three",4])
        self.assertDictEqual(
            table.asNative(),
            {1: (1, 5, 9), 2: (2, 6, 7), "three": (3, 7, 5), 4: (4, 8, 3)})
