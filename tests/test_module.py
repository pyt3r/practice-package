import unittest
from practice.module import covered


class Test(unittest.TestCase):

    def test_module(self):
        import practice
        print('template_package:', practice)
        assert covered() is not None


if __name__ == '__main__':
    unittest.main()
