import unittest
from practice.frameworks import dag



class DagTestCases(unittest.TestCase):
    def test_dag(self):

        o = dag.buildDag(
            outputs = [(), ("C",), ("D",), ("E",), ("F",), ],
            funcs = [fun0, fun, fun, fun, fun1, ],
            inputs = [("A", "B"), ("A", "B"), ("A",), (), ("D", "E")],
        )


def fun0(*args): pass
def fun1(*args): pass
def fun(*args): pass
