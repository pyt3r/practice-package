import unittest
from practice.frameworks.workflow import workflow, exception

HERE = "practice.tests.unittests.frameworks.test_workflow"


class TestCases(unittest.TestCase):

    class Workflow(workflow.Workflow):
        TASKS = [
            [0, f"{HERE}.Calculator.calcA",         (),       {},  ("a",)],
            [1, f"{HERE}.calcB"           ,    ("a", ),       {},  ("b",)],
            [2, f"{HERE}.calcC"           , ("a", "b"), {"x": .75}, ("c11", "c12")],
            [3, f"{HERE}.calcC"           , ("a", "b"), {"z": "z"}, ( "c1",  "c2")], ]

    def test_example_workflow(self):
        results = self.Workflow.create().run()
        self.assertDictEqual(results, {'a': 2, 'b': 6, 'c1': 4.0, 'c11': 6.0, 'c12': 8, 'c2': 8})

    def test_workflow_defaultkwargs(self):
        o = self.Workflow.create()
        self.assertListEqual(o.getDefaultKwargs(),  [{}, {}, {'xx': 1}, {'x': 0.5, 'xx': 1}])

    def test_createFromDF(self):
        DF = self.Workflow.create().asDF()
        wf = workflow.Workflow.createFromDF(DF)
        results = wf.run()
        self.assertDictEqual(results, {'a': 2, 'b': 6, 'c1': 4.0, 'c11': 6.0, 'c12': 8, 'c2': 8})


class TestNextCases(unittest.TestCase):

    class Workflow(workflow.Workflow):
        TASKS = [
            [1, f"{HERE}.calcC"           , ("a", "b"), {"x": .75}, ("c11", "c12")],
            [1, f"{HERE}.calcC"           , ("a", "b"), {"z": "z"}, ( "c1",  "c2")],

            [0, f"{HERE}.Calculator.calcA",         (),       {},  ("a",)],
            [0, f"{HERE}.calcB"           ,    ("a", ),       {},  ("b",)],
        ]

    def test_runNext(self):
        workflow = self.Workflow.create()
        data = workflow.runNext()
        data = workflow.runNext(data)
        self.assertDictEqual(data, {'a': 2, 'b': 6, 'c1': 4.0, 'c11': 6.0, 'c12': 8, 'c2': 8})


class TestFreeMemoryCases(unittest.TestCase):

    class Workflow(workflow.Workflow):
        TASKS = [
            [0, f"{HERE}.Calculator.calcA",            (),             {}, ("a",)],
            [1, f"{HERE}.calcB"           ,       ("a", ),             {}, ("b",)],
            [2, f"{HERE}.calcC"           ,    ("a", "b"),     {"x": .75}, ("c11", "c12")],
            [3, f"{HERE}.delete"          , ("__data__",), {"key": "c11"}, ("deleted",)],
            [4, f"{HERE}.calcC"           ,    ("a", "b"),     {"z": "z"}, ( "c1",  "c2")], ]

    def setUp(self):
        self.workflow = self.Workflow.create()

    def test_free(self):
        data = self.workflow.run()
        self.assertDictEqual(data, {'a': 2, 'b': 6, 'c1': 4.0, 'c12': 8, 'c2': 8, "deleted": "c11"})

    def test_Dag(self):
        o = self.workflow.asDag()
        #o.view()


class TestErrorCases(unittest.TestCase):

    class ArgError(workflow.Workflow):
        TASKS = [
            [0, f"{HERE}.Calculator.calcA", (),   {}, ("a",)],
            [1, f"{HERE}.calcB",            (), None, ("b",)], ]

    def test_argError(self):
        msg = f"{HERE}.calcB expected=1, received=0"
        with self.assertRaisesRegex(exception.ArgsMismatch, msg):
            self.ArgError.create()


    class KwargError1(workflow.Workflow):
        TASKS = [
            [0, f"{HERE}.calcB", ('a',), {"x" : 1}, ("b",)], ]

    def test_kwargError1(self):
        msg = f"({HERE}.calcB', 'x', 1)"
        with self.assertRaisesRegex(exception.InvalidKwargs, msg):
            self.KwargError1.create()


    class KwargError2(workflow.Workflow):
        TASKS = [
            [0, f"{HERE}.calcC" , ("a", "b"), {"z": 1}, ("c1", "c2")],
            [1, f"{HERE}.calcD" , ("a", "b"), {"z": 1}, ("c1", "c2")], ]

    def test_kwargError2(self):
        msg = f"({HERE}.calcD', 'z', 1)"
        with self.assertRaisesRegex(exception.InvalidKwargs, msg):
            self.KwargError2.create()


    class OutputLength(workflow.Workflow):
        TASKS = [
            [0, f"{HERE}.Calculator.calcA",         (),       {},  ("a",)],
            [1, f"{HERE}.calcB"           ,    ("a", ),       {},  ("b",)],
            [2, f"{HERE}.calcC" , ("a", "b"), {"x": 1}, ("c1",)], ]

    def test_outputLength(self):
        msg = "received=2, expected=1"
        with self.assertRaisesRegex(exception.OutputLengthMismatch, msg):
            self.OutputLength.create().run()


class TestRunSelectedCases(unittest.TestCase):

    class Workflow1(workflow.Workflow):
        TASKS = [
            [1, f"{HERE}.calcC"           , ("a", "b"), {"z": "z"}, ( "c1",  "c2")],

            [0, f"{HERE}.Calculator.calcA",         (),       {},  ("a",)],
            [0, f"{HERE}.calcB"           ,    ("a", ),       {},  ("b",)],
        ]

    def test_case1(self):
        o = self.Workflow1.create()
        result = o.runSelected(1, {'a': 1, 'b': 2})
        self.assertDictEqual(result, {'a': 1, 'b': 2, 'c1': 1.5, 'c2': 3})


    class Workflow2(workflow.Workflow):
        TASKS = [
            [1, f"{HERE}.calcC"           , ("a", "b"), {"x": .75}, ("c11", "c12")],
            [1, f"{HERE}.calcC"           , ("a", "b"), {"z": "z"}, ( "c1",  "c2")],

            [0, f"{HERE}.Calculator.calcA",         (),       {},  ("a",)],
            [0, f"{HERE}.calcB"           ,    ("a", ),       {},  ("b",)],
        ]

    def test_case2(self):
        o = self.Workflow2.create()
        result = o.runSelected(1, {'a': 1, 'b': 2})
        self.assertDictEqual(result, {'a': 1, 'b': 2, 'c11': 2.25, 'c12': 3, 'c1': 1.5, 'c2': 3})


    class Workflow3(workflow.Workflow):
        TASKS = [
            [2, f"{HERE}.calcC"           , ("a", "b"), {"x": .75}, ("c111", "c222")],
            [1, f"{HERE}.calcC"           , ("a", "b"), {"x": .75}, ("c11", "c12")],
            [1, f"{HERE}.calcC"           , ("a", "b"), {"z": "z"}, ( "c1",  "c2")],

            [0, f"{HERE}.Calculator.calcA",         (),       {},  ("a",)],
            [0, f"{HERE}.calcB"           ,    ("a", ),       {},  ("b",)],
        ]

    def test_case3(self):
        o = self.Workflow3.create()
        result = o.runSelected(1, {'a': 1, 'b': 2})
        self.assertDictEqual(result, {'a': 1, 'b': 2, 'c11': 2.25, 'c12': 3, 'c1': 1.5, 'c2': 3})


class Calculator:
    @staticmethod
    def calcA():
        return 2

def calcB(a):
    return a + 4


def calcC(a, b, x=0.5, xx=1, **kw):
    return calcD(a, b, x=x, xx=xx)


def calcD(a, b, x=0.5, xx=1):
    first  = (a + b) * x
    second = (a + b)
    return first, second


def delete(data, key=None):
    data["__data__"].pop(key)
    return key
