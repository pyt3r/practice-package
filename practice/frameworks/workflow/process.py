import pydoc
from practice.frameworks import inspector
from practice.frameworks.table import Table
from practice.frameworks.iterator import Iterator
from practice.frameworks.workflow import schema


class Process:
    """ validates and processes workflow tasks and kwargs """

    @classmethod
    def buildTaskIterator(cls, taskTable):
        tasksIter     = taskTable.asIterator()
        process       = cls(tasksIter)
        order         = process.Order()
        inputs        = process.Inputs()
        outputs       = process.Outputs()
        strings       = process.Strings()
        funcs         = process.Funcs( strings )
        kwargs        = process.Kwargs( strings, funcs )
        defaultkwargs = process.DefaultKwargs( funcs, kwargs )
        process.Validate( strings, funcs, inputs )

        vals = [ order, funcs, inputs, kwargs, outputs, defaultkwargs ]
        cols = schema.getInternalColumns()

        tasks = Table.fromArrays( vals, cols ).asIterator()
        tasks.setViewOrder( cols )
        return tasks

    def __init__(self, tasks):
        self.tasks = tasks

    def __call__(self, cls, *args):
        handler = cls(self.tasks)
        return handler.run(*args)

    def Order(self):
        return self( Order )

    def Inputs(self):
        return self( Inputs )

    def Outputs(self):
        return self( Outputs )

    def Strings(self):
        return self( Strings )

    def Funcs(self, *args):
        return self( Funcs, *args )

    def Kwargs(self, *args):
        return self( Kwargs, *args )

    def DefaultKwargs(self, *args):
        return self( DefaultKwargs, *args )

    def Validate(self, *args):
        self( ValidateArgs, *args )

    def _processXputs(self, i):
        for key in self._process(i):

            if isinstance(key, list):
                key = tuple(key)

            if not isinstance(key, tuple):
                key = (key,)

            yield tuple( k for k in key )

    def _processKwargs(self):
        return ( kw or {} for kw in self._process( schema.KWLIST ) )

    def _process(self, i):
        return self.tasks.getPrimary(i)

class Order(Process):
    """ processes task input keys """

    def run(self):
        return list( self._process( schema.ORDER ) )

class Inputs(Process):
    """ processes task input keys """

    def run(self):
        return list( self._processXputs( schema.INPUTS ) )

class Outputs(Process):
    """ processes task output keys """

    def run(self):
        return list( self._processXputs( schema.OUTPUTS ) )

class Strings(Process):
    """ processes task strings """

    def run(self):
        return list( self._process( schema.FUNCS ) )

class Funcs(Process):
    """ processes task funcs """

    def run(self, strings):
        funcs = [ self.importFromPath(s) for s in strings ]
        error = [ s for s, f in zip(strings, funcs) if not f ]
        if error:
            raise ValueError(error)
        return funcs

    @staticmethod
    def importFromPath(path):
        return pydoc.locate(path)

class Kwargs(Process):
    """ processes task kwargs """

    def run(self, strings, funcs):
        kwlist = list( self._processKwargs() )

        keys  = []
        flags = []
        for func in funcs:
            spector = inspector.Inspector( func )
            keys.append( spector.getKwargs() )
            flags.append( spector.getKwargsFlags() )

        self.validate( Iterator.fromArrays(strings, kwlist, keys, flags) )
        return kwlist

    @staticmethod
    def validate(iterObj):
        err = []
        for string, kw, key, flag in iterObj:
            unknown = set(kw.keys()) - set(key)
            if flag and unknown:
                err += [ (string, u, kw[u]) for u in sorted(unknown) ]
        if err:
            raise InvalidKwargs(err)


class DefaultKwargs(Process):
    """ processes default kwargs """

    def run(self, funcs, kwargs):
        defaults = []
        for fun, kw in zip(funcs, kwargs):
            spector = inspector.Inspector( fun )
            kwargs  = spector.getKwargs()
            default = { k: v for k, v in kwargs.items() if k not in kw }
            defaults.append( default )
        return defaults


class ValidateArgs(Process):
    """ processes task args """

    def run(self, strings, funcs, inputs):
        nargs = []
        flags = []
        for fun, i in zip(funcs, inputs):
            spector = inspector.Inspector( fun )
            nargs.append( len(spector.getArgs()) )
            flags.append( spector.getArgsFlags() )

        self.validate( Iterator.fromArrays( strings, inputs, nargs, flags ) )

    @staticmethod
    def validate(iterObj):
        err = []
        for string, inputs, nargs, flag in iterObj:
            length = len( inputs )
            if flag and length != nargs:
                err.append( f"{string} expected={nargs}, received={length}" )
        if err:
            raise ArgsMismatch(err)


class ArgsMismatch(Exception):
    pass


class InvalidKwargs(Exception):
    pass
