from practice.frameworks.table import Table
from practice.frameworks.workflow.process import Process
from practice.frameworks.workflow import schema
from practice.frameworks import exception as ex


class Workflow:
    """ Instantiates and executes an list of tasks """
    TASKS  = []

    @classmethod
    def create(cls):
        """ creates from class variables """
        table = Table.fromList( cls.TASKS, schema.getExternalColumns() )
        return cls.fromTable( table )

    @classmethod
    def fromDF(cls, DF):
        table = Table.fromDF( DF, schema.getExternalColumns() )
        return cls.fromTable( table )

    @classmethod
    def fromTable(cls, table):
        return cls(table)

    def __init__(self, taskTable):
        self._table = taskTable.sortViaDF( schema.ORDER )
        self._tasks = Process.buildTaskIterator( self._table )

    def run(self, data=None):
        """ calls a sequence of tasks """
        while self.isRunnable():
            data = self.runNext(data)
        return data or {}

    def isRunnable(self):
        return self._tasks.isNextable()

    def runNext(self, data=None):
        currIx, *task = self._tasks.getNext()
        return self._runNext( data, currIx, task )

    def runSelected(self, i, data=None):
        order         = list( self._tasks.getPrimary( schema.ORDER ) )
        currIx, *task = self._tasks.getSelected( order.index(i) )
        return self._runNext( data, currIx, task )

    def _runNext(self, data, currIx, task):
        data       = WorkflowDict( data )
        data       = self._run( data, *task )
        nextIx, *_ = self._tasks.peekNext()

        while self.isRunnable() and currIx == nextIx:
            currIx, *task = self._tasks.getNext()
            data          = self._run( data, *task )
            nextIx, *_    = self._tasks.peekNext()

        return data.asNative()

    def _run(self, data, func, inputs, kwargs, outputs, *a, **kw):
        args   = tuple( data[k] for k in inputs )
        value  = func( *args, **kwargs )
        result = self._getResult( outputs, value )
        data.update( result )
        return data

    @staticmethod
    def _getResult(outputs, value):
        """ unpacks the calculated value """
        if not isinstance(value,(tuple, list)):
            value = (value,)
        ex.MustBeTheSameLengths.raiseIf(outputs, value)
        return { k: v for k, v in zip(outputs, value) }

    def asDag(self):
        """ represnts workflow as a dag """
        from practice.frameworks import api
        args = []
        for key in [ schema.OUTPUTS, schema.FUNCS, schema.INPUTS ]:
            val = self._tasks.getPrimary( key ).asNative()
            args.append( val )
        return api.buildDag( *args )

    def asDF(self):
        """ represents workflow as a Table """
        return self.asTable().asDF()

    def asTable(self):
        """ represents workflow as a DataFrame """
        return self._table

    def getDefaultKwargs(self):
        return self._tasks.getPrimary( schema.DEFAULT_KW ).asNative()


class WorkflowDict:
    """ wrapper around a dictionary to control access to key-value pairs """

    _SPECIALKEY = "__data__"

    def __init__(self, data=None):
        data = data or {}
        self._validate( data )
        self._data = { self._SPECIALKEY: data }

    @classmethod
    def _validate(cls, data):
        ex.MustNotContain.raiseIf( cls._SPECIALKEY, data )

    def asNative(self):
        return self._data[ self._SPECIALKEY ]

    def __getitem__(self, item):
        if item != self._SPECIALKEY:
            return self.asNative()[ item ]
        return self._data

    def __setitem__(self, key, value):
        if key != self._SPECIALKEY:
            self.asNative()[ key ] = value
        else:
            self._data = value

    def update(self, data):
        for k, v in data.items():
            self[k] = v
