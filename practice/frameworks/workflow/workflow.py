from practice.frameworks.table import Table
from practice.frameworks.workflow import exception
from practice.frameworks.workflow.process import Process
from practice.frameworks.workflow.encapsulate import WorkflowDict, SCHEMA


class Workflow:
    """ Instantiates and executes an list of tasks """
    TASKS  = []

    @classmethod
    def create(cls):
        """ creates from class variables """
        table = Table.createFromRows(cls.TASKS, SCHEMA.getColumns())
        return cls.createFromTable(table)

    @classmethod
    def createFromDF(cls, DF):
        table = Table.createFromDF(DF, SCHEMA.getColumns())
        return cls.createFromTable(table)

    @classmethod
    def createFromTable(cls, table):
        return cls(table)

    def __init__(self, taskTable):
        self._table = taskTable.sort(SCHEMA.ORDER)
        self._tasks = Process.buildTaskIterator(self._table)

    def run(self, data=None):
        """ calls a sequence of tasks """
        while self.isRunnable():
            data = self.runNext(data)
        return data or {}

    def isRunnable(self):
        return self._tasks.isNextable()

    def runNext(self, data=None):
        currIx, *task = self._tasks.getNext()
        return self._runNext(data, currIx, task)

    def runSelected(self, i, data=None):
        order = list(self._tasks.getPrimary(SCHEMA.ORDER))
        ix = order.index(i)
        currIx, *task = self._tasks.getSelected(ix)
        return self._runNext(data, currIx, task)

    def _runNext(self, data, currIx, task):
        data = WorkflowDict(data)
        data = self._run(data, *task)
        nextIx, *_ = self._tasks.peekNext()
        while self.isRunnable() and currIx == nextIx:
            currIx, *task = self._tasks.getNext()
            data = self._run(data, *task)
            nextIx, *_ = self._tasks.peekNext()

        return data.asNative()

    def _run(self, data, func, inputs, kwargs, outputs):
        args   = tuple(data[k] for k in inputs)
        value  = func(*args, **kwargs)
        result = self._getResult(outputs, value)
        data.update(result)
        return data

    @staticmethod
    def _getResult(outputs, value):
        """ unpacks the calculated value """
        if not isinstance(value,(tuple, list)):
            value = (value,)

        if len(outputs) != len(value):
            msg = f"received={len(value)}, expected={len(outputs)}, outputs={outputs}"
            raise exception.OutputLengthMismatch(msg)

        return {k: v for k, v in zip(outputs, value)}

    def asDag(self):
        """ represnts workflow as a dag """
        from practice.frameworks import api
        args = []
        for key in [SCHEMA.OUTPUTS, SCHEMA.FUNCS, SCHEMA.INPUTS]:
            val = self._tasks.getPrimary(key).asNative()
            args.append(val)
        return api.buildDag(*args)

    def asDF(self):
        """ represents workflow as a Table """
        return self.asTable().asDF()

    def asTable(self):
        """ represents workflow as a DataFrame """
        return self._table

    def getDefaultKwargs(self):
        col = Process.DEBUG_COLUMS[0]
        return self._tasks.getPrimary(col).asNative()
