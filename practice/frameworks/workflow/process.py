import pydoc
from practice.frameworks import inspector
from practice.frameworks.workflow import exception


class Process:
    """ validates and processes workflow tasks and kwargs """

    def __init__(self, tasks):
        self.tasks = tasks

    def __call__(self, cls, *args):
        handler = cls(self.tasks)
        return handler.run(*args)

    def Inputs(self):
        return self(Inputs)

    def Outputs(self):
        return self(Outputs)

    def Strings(self):
        return self(Strings)

    def Funcs(self, *args):
        return self(Funcs, *args)

    def Kwargs(self, *args):
        return self(Kwargs, *args)

    def DefaultKwargs(self, *args):
        return self(DefaultKwargs, *args)

    def Validate(self, *args):
        self(ValidateArgs, *args)

    def _processXputs(self, i):
        for key in self._process(i):
            if isinstance(key, list):
                key = tuple(key)
            if not isinstance(key, tuple):
                key = (key,)
            yield tuple(k for k in key)

    def _processKwargs(self):
        return (kw or {} for kw in self._process(2))

    def _process(self, i):
        for task in self.tasks:
            yield task[i]

class Inputs(Process):
    """ processes task input keys """

    def run(self):
        return list(self._processXputs(1))

class Outputs(Process):
    """ processes task output keys """

    def run(self):
        return list(self._processXputs(3))

class Strings(Process):
    """ processes task strings """

    def run(self):
        return list(self._process(0))

class Funcs(Process):
    """ processes task funcs """

    def run(self, strings):
        err = []
        funcs = []
        for string in strings:
            func = self.importFromPath(string)
            funcs.append(func)
            if not func:
                err.append(string)

        if err:
            raise ValueError(err)

        return funcs

    @staticmethod
    def importFromPath(path):
        return pydoc.locate(path)

class Kwargs(Process):
    """ processes task kwargs """

    def run(self, strings, funcs):
        kwlist = list(self._processKwargs())

        kwargsKeys = []
        kwflags = []
        for func in funcs:
            o = inspector.Inspector(func)
            kwargsKeys.append(o.getKwargs())
            kwflags.append(o.getKwargsFlags())

        self.validate(strings, kwlist, kwargsKeys, kwflags)

        return kwlist

    @staticmethod
    def validate(strings, kwlist, kwargsKeys, kwflags):
        err = []
        for string, passed, expected, flag in zip(strings, kwlist, kwargsKeys, kwflags):
            if flag:
                unknown = set(passed.keys()) - set(expected)
                if unknown:
                    err += [(string, k, passed[k]) for k in sorted(unknown)]

        if err:
            raise exception.InvalidKwargs(err)


class DefaultKwargs(Process):
    """ processes default kwargs """

    def run(self, funcs, kwargs):
        kwlist = list(self._processKwargs())

        defaults = []
        for func, kw in zip(funcs, kwargs):
            kwargs  = inspector.Inspector(func).getKwargs()
            default = {k: v for k, v in kwargs.items() if k not in kw}
            defaults.append(default)

        return defaults


class ValidateArgs(Process):
    """ processes task args """

    def run(self, strings, funcs, inputs):
        nargs = []
        flags = []
        for func, i in zip(funcs, inputs):
            o = inspector.Inspector(func)
            narg = len(o.getArgs())
            flag = o.getArgsFlags()
            nargs.append(narg)
            flags.append(flag)

        self.validate(strings, inputs, nargs, flags)

    @staticmethod
    def validate(strings, inputs, nargs, flags):
        err = []
        for s, i, n, f in zip(strings, inputs, nargs, flags):
            if f:
                length = len(i)
                if length != n:
                    err.append(f"{s} expected={n}, received={length}")
        if err:
            raise exception.ArgsMismatch(err)
