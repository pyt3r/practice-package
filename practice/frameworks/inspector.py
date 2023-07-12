import inspect
import numpy as np
from practice.frameworks import exception as ex


class Inspector:
    SELECTED_CONDITIONS = [-1]*7
    ARGS_FLAG   = False  # indicates that one is able to get exact number of args from the func
    KWARGS_FLAG = False  # indicates that one is able to get all kwarg keys

    def __init__(self, fun):
        self.name = fun.__qualname__
        self.spec = inspect.getfullargspec(fun)
        self.fun  = fun

    def getName(self):
        return self.name

    def getArgs(self):
        return self.getHandler()._getArgs()

    def getKwargs(self):
        return self.getHandler()._getKwargs()

    def getArgsFlags(self):
        return self.getHandler()._getArgsFlag()

    def getKwargsFlags(self):
        return self.getHandler()._getKwargsFlag()

    def _getArgs(self):
        return []

    def _getKwargs(self):
        return {}

    def _getArgsFlag(self):
        return self.ARGS_FLAG

    def _getKwargsFlag(self):
        return self.KWARGS_FLAG

    def meetsConditions(self):
        return Conditions(self.spec).check(*self.SELECTED_CONDITIONS)

    def viewConditions(self):
        return Conditions(self.spec).conditions

    @staticmethod
    def getHandlers():
        return [
            Case0, Case1, Case2, Case3, Case4, Case5, Case6,
            Case7, Case8, Case9, Case10, Case11, Case12, Case13, ]

    def getHandler(self):
        for handler in self.getHandlers():
            o = handler(self.fun)
            if o.meetsConditions():
                return o


class Case0(Inspector):
    """ def fun0() """
    SELECTED_CONDITIONS = [0,0,0,0,0,0,1]
    ARGS_FLAG   = True # []
    KWARGS_FLAG = True # {}

    def _getArgs(self):
        return self.spec.args


class Case1(Inspector):
    """ def fun1(a,b,c,d) """
    SELECTED_CONDITIONS = [1,0,0,0,0,0,0]
    ARGS_FLAG   = True # ['a', 'b', 'c', 'd']
    KWARGS_FLAG = True

    def _getArgs(self):
        return self.spec.args


class Case2(Inspector):
    """ def fun2(a,b,c,d=1) """
    SELECTED_CONDITIONS = [1,0,0,1,0,0,0]
    ARGS_FLAG   = True # ['a', 'b', 'c']
    KWARGS_FLAG = True # {'d': 1}

    def _getArgs(self):
        defaults = self.spec.defaults
        args = self.spec.args
        index = len(args) - len(defaults)
        return args[:index]

    def _getKwargs(self):
        defaults = self.spec.defaults
        args = self.spec.args
        index = len(args) - len(defaults)
        return dict(zip(args[index:], defaults))


class Case3(Case1):
    """ def fun3(a,b,c,d,**kw) """
    SELECTED_CONDITIONS = [1,0,1,0,0,0,0]
    KWARGS_FLAG = False


class Case4(Case2):
    """ def fun3(a,b,c=3,d=4,**kw) """
    SELECTED_CONDITIONS = [1,0,1,1,0,0,0]
    KWARGS_FLAG = False


class Case5(Inspector):
    """ def fun5(*args) """
    SELECTED_CONDITIONS = [0,1,0,0,0,0,1]
    KWARGS_FLAG = True # {}


class Case6(Inspector):
    """ def fun6(a,b,*args) """
    SELECTED_CONDITIONS = [1,1,0,0,0,0,0]
    KWARGS_FLAG = True


class Case7(Inspector):
    """ def fun7(a,*args,c,d,**kw) """
    SELECTED_CONDITIONS = [1,1,1,0,1,0,0]


class Case8(Inspector):
    """ def fun8(a,*args,c=3,d=4,**kw) """
    SELECTED_CONDITIONS = [1,1,1,0,1,1,0]

    def _getKwargs(self):
        return self.spec.kwonlydefaults


class Case9(Inspector):
    """ def fun9(a,*args,c=3,d=4) """
    SELECTED_CONDITIONS = [1,1,0,0,1,1,0]
    KWARGS_FLAG = True

    def _getKwargs(self):
        return self.spec.kwonlydefaults


class Case10(Inspector):
    """ def fun10(a=1,b=2,c=3,d=4) """
    SELECTED_CONDITIONS = [1,0,0,1,0,0,1]
    ARGS_FLAG   = True
    KWARGS_FLAG = True

    def _getKwargs(self):
        defaults = self.spec.defaults
        args = self.spec.args
        return dict(zip(args, defaults))


class Case11(Case10):
    """ def fun11(a=1,b=2,c=3,d=4,**kw) """
    SELECTED_CONDITIONS = [1,0,1,1,0,0,1]
    KWARGS_FLAG = False


class Case12(Inspector):
    """ def fun12(**kw) """
    SELECTED_CONDITIONS = [0,0,1,0,0,0,1]
    ARGS_FLAG = True


class Case13(Inspector):
    """ def fun13(*args, **kw) """
    SELECTED_CONDITIONS = [0,1,1,0,0,0,1]



class Conditions:
    """ calculates the conditions for a fullargspec """
    def __init__(self, spec):
        conditions = [
            spec.args,
            spec.varargs,
            spec.varkw,
            spec.defaults,
            spec.kwonlyargs,
            spec.kwonlydefaults,
            len(spec.args) == len(spec.defaults or []),
        ]
        self.conditions = [1 if c else 0 for c in conditions]

    def check(self, *selections):

        ex.MustBeTheSameLengths.raiseIf( selections, self.conditions )

        acc = ex.Accumulator.map( selections, ex.MustContain, (0, 1) )
        acc.raiseErrorIf()

        return all( s == c for s, c in zip(selections, self.conditions) )
