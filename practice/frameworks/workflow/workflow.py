import pandas as pd
from practice.frameworks.workflow import process, exception
from practice.frameworks.workflow.encapsulate import WorkflowDF, WorkflowDict


class Workflow:
    """ Instantiates and executes an list of tasks """
    TASKS  = []

    @classmethod
    def create(cls):
        """ creates from class variables """
        data = cls.TASKS
        cls._validate(data)
        DF = pd.DataFrame(data, columns=WorkflowDF.getColumns())
        return cls.createFromDF(DF)

    @classmethod
    def createFromDF(cls, DF):
        DF      = WorkflowDF(DF)
        order   = DF.order
        strings = DF.funcPath
        inputs  = DF.inputKeys
        kwlist  = DF.kwargs
        outputs = DF.outputKeys
        tasks   = list(zip(strings, inputs, kwlist, outputs))
        return cls(order, tasks)

    @staticmethod
    def _validate(data):
        assert isinstance(data, list)
        columns = WorkflowDF.getColumns()
        assert all(len(row) == len(columns) for row in data)

    def __init__(self, order, tasks):
        self._order = order
        self._tasks = tasks
        self.reset()

    def reset(self):
        self._nCompleted   = 0
        self._nTotal       = len(self._order)
        Process            = process.Process(self._tasks)
        self.inputs        = Process.Inputs()
        self.outputs       = Process.Outputs()
        self.strings       = Process.Strings()
        self.funcs         = Process.Funcs(self.strings)
        self.kwargs        = Process.Kwargs(self.strings, self.funcs)
        self.defaultkwargs = Process.DefaultKwargs(self.funcs, self.kwargs)
        Process.Validate(self.strings, self.funcs, self.inputs)
        self.tasks = zip(self.funcs, self.inputs, self.kwargs, self.outputs)

    def isRunnable(self):
        return self._nCompleted < self._nTotal

    def _getNextIndex(self):
        if self.isRunnable():
            return self._order[self._nCompleted]

    def run(self, data=None):
        """ calls a sequence of tasks """
        while self.isRunnable():
            data = self.runNext(data)
        return data or {}

    def runNext(self, data=None):
        data = WorkflowDict(data)
        currIx = nextIx = self._getNextIndex()
        while self.isRunnable() and nextIx == currIx:
            task   = next(self)
            data   = self._run(data, *task)
            nextIx = self._getNextIndex()

        return data.asNative()

    def __next__(self):
        task = next(self.tasks)
        self._nCompleted += 1
        return task

    def _run(self, data, func, inputs, kwargs, outputs):
        args   = tuple(data[k] for k in inputs)
        value  = func(*args, **kwargs)
        result = self._collect(outputs, value)
        data.update(result)
        return data

    def runSelected(self, i, data=None):
        """ skips until the iterator reaches the ith task """
        self.reset()
        nSkips = self._order.index(i)
        nCompleted = 0
        while nCompleted < nSkips:
            next(self)
            nCompleted = self._nCompleted
        return self.runNext(data)

    @staticmethod
    def _collect(outputs, value):
        """ unpacks the calculated value and updates results """
        if not isinstance(value,(tuple, list)):
            value = (value,)

        if len(outputs) != len(value):
            msg = f"received={len(value)}, expected={len(outputs)}, outputs={outputs}"
            raise exception.OutputLengthMismatch(msg)

        return {k: v for k, v in zip(outputs, value)}

    def buildDag(self):
        """ builds a dag representation of the workflow """
        from practice.frameworks import api
        return api.buildDag(self.outputs, self.funcs, self.inputs)
