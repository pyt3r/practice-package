import unittest
from practice.frameworks import iterator


class PrimaryTestCase(unittest.TestCase):

    def test_example(self):
        p = iterator.Primary([1,2,3])
        result = [p.getNext(), p.getNext(), p.getNext(), p.getPrev(), p.getPrev()]
        self.assertListEqual([1,2,3,2,1], result)

        p.reset()
        self.assertEqual(0, p.cursor)

        self.assertEqual((1,2,3), tuple(p))


class IteratorTestCase(unittest.TestCase):
    def test_example(self):
        i = iterator.Iterator.fromDict({
            "A" : [1,2,3],
            "B" : [4,5,6],
            "C" : [7,8,9],
        })

        self.assertEqual((1,4,7), i.getNext())
        self.assertEqual((2,5,8), i.getNext())
        self.assertEqual((2,5,8), i.getSelected(1))

        i.reset()
        self.assertEqual((1,4,7), i.getNext())

        i.setViewOrder(["C", "A"])
        i.reset()
        self.assertTrue(i.isNextable())
        self.assertEqual((7,1), i.getNext())
        self.assertEqual((8,2), i.getNext())
        self.assertEqual((9,3), i.peekNext())
        self.assertEqual((9,3), i.peekNext())
        self.assertEqual((9,3), i.getNext())
        self.assertEqual((None, None), i.peekNext())
        self.assertFalse(i.isNextable())
