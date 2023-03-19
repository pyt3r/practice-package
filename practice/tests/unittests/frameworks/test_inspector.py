import unittest
from pprint import pprint as pp
import numpy as np
from practice.frameworks.inspector import Inspector


def fun0(): pass
def fun1(a,b,c,d): pass
def fun2(a,b,c,d=1): pass
def fun3(a,b,c,d,**kw): pass
def fun4(a,b,c=3,d=4,**kw): pass
def fun5(*args): pass
def fun6(a,b,*args): pass
def fun7(a,*args,c,d,**kw): pass
def fun8(a,*args,c=3,d=4,**kw): pass
def fun9(a,*args,c=3,d=4): pass
def fun10(a=1,b=2,c=3,d=4): pass
def fun11(a=1,b=2,c=3,d=4,**kw): pass
def fun12(**kw): pass


class TestCases(unittest.TestCase):

    def setUp(self):
        self.funs = [fun0, fun1, fun2, fun3, fun4, fun5, fun6, fun7, fun8, fun9, fun10, fun11, fun12]

    def test_view(self):
        arr = []
        for fun, handler in zip(self.funs, Inspector.getHandlers()):
            pp(handler(fun).viewConditions())

    def test_handlers(self):
        arr = []
        for fun in self.funs:
            result = [handler(fun).meetsConditions() for handler in Inspector.getHandlers()]
            arr.append(result)

        result = np.array(arr).astype(float)
        np.testing.assert_array_equal(np.identity(13), result)

    def test_case_args(self):
        results = {k: o.getArgs() for k, o in self.iterator()}
        self.assertDictEqual(
            results,
            {'fun0': [],
             'fun1': ['a', 'b', 'c', 'd'],
             'fun2': ['a', 'b', 'c'],
             'fun3': ['a', 'b', 'c', 'd'],
             'fun4': ['a', 'b'],
             'fun5': [],
             'fun6': [],
             'fun7': [],
             'fun8': [],
             'fun9': [],
             'fun10': [],
             'fun11': [],
             'fun12': [],}
        )

    def test_case_kwargs(self):
        results = {k: o.getKwargs() for k, o in self.iterator()}
        self.assertDictEqual(
            results,
            {'fun0': {},
             'fun1': {},
             'fun2': {'d': 1},
             'fun3': {},
             'fun4': {'c': 3, 'd': 4},
             'fun5': {},
             'fun6': {},
             'fun7': {},
             'fun8': {'c': 3, 'd': 4},
             'fun9': {'c': 3, 'd': 4},
             'fun10': {'a': 1, 'b': 2, 'c': 3, 'd': 4},
             'fun11': {'a': 1, 'b': 2, 'c': 3, 'd': 4},
             'fun12': {},}
        )

    def test_case_argsFlags(self):
        results = {k: o.getArgsFlags() for k, o in self.iterator()}
        self.assertDictEqual(
            results,
            {'fun0': True,
             'fun1': True,
             'fun2': True,
             'fun3': True,
             'fun4': True,
             'fun5': False,
             'fun6': False,
             'fun7': False,
             'fun8': False,
             'fun9': False,
             'fun10': True,
             'fun11': True,
             'fun12': True,}
        )

    def test_case_kwargsFlags(self):
        results = {k: o.getKwargsFlags() for k, o in self.iterator()}
        self.assertDictEqual(
            results,
            {'fun0': True,
             'fun1': True,
             'fun2': True,
             'fun3': False,
             'fun4': False,
             'fun5': True,
             'fun6': True,
             'fun7': False,
             'fun8': False,
             'fun9': True,
             'fun10': True,
             'fun11': False,
             'fun12': False,}
        )

    def iterator(self):
        for fun in self.funs:
            o = Inspector(fun)
            yield o.name, o
