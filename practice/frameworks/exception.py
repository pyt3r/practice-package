from collections import Counter
import json


class Accumulator:

    @classmethod
    def map(cls, data, validator, *args):
        """ map a lazy exception to an iterable"""
        TypeMismatch.raiseIf( data, (list, tuple) )
        exceptions = [ validator(e, *args) for e in data ]
        return cls.fromList( exceptions )

    @classmethod
    def fromList(cls, exceptions):
        o = cls()
        [ o.addEntry(e, i) for i, e in enumerate(exceptions) ]
        return o

    def __init__(self):
        self._entries = []
        self._indices = []

    def getEntries(self):
        return self._entries

    def getIndices(self):
        return self._indices

    def hasErrors(self):
        return len(self.getEntries()) > 0

    def addEntry(self, exception, i=None):
        if isinstance(exception, LazyException):
            exception = exception.getException()

        if exception is None:
            return

        TypeMismatch.raiseIf( exception, Exception )

        name = exception.__class__.__name__
        self._entries.append(f"{name}( {exception} )")
        self._indices.append(i)

    def raiseErrorIf(self):
        if self.hasErrors():
            self.raiseError()

    def raiseError(self):
        msg = json.dumps( self.getEntries(), indent=2 )
        raise AccumulatedErrors(msg)

    def raiseIndexErrorIf(self):
        if self.hasErrors():
            self.raiseIndexError()

    def raiseIndexError(self):
        msg = json.dumps( self.getIndices() )
        raise AccumulatedIndexErrors(msg)

    def extendEntries(self, other):
        TypeMismatch.raiseIf( other, Accumulator )
        self._entries.extend( other.getEntries() )


class AccumulatedErrors(Exception):
    pass


class AccumulatedIndexErrors(Exception):
    pass


class LazyException(Exception):

    @classmethod
    def raiseIf(cls, *args):
        exception = cls(*args).getException()
        if exception:
            raise exception

    def getException(self):
        errors = self.getErrors( *self.args )
        if errors:
            return self._getException(errors)

    @classmethod
    def _getException(cls, *args):
        return cls( cls.getMsg(*args) )

    @classmethod
    def getErrors(cls, *args):
        """ abstract method """
        raise

    @staticmethod
    def getMsg(*args):
        """ abstract method """
        raise

class MustBeUnique(LazyException):

    @classmethod
    def getErrors(cls, data):
        counter = Counter(data)
        keys    = list(counter.keys())
        counts  = counter.values()
        return [ keys[i] for i, c in enumerate( counts ) if c > 1 ]

    @staticmethod
    def getMsg(errors):
        return f"duplicates={errors}"

class MustFullyIntersect(LazyException):

    @classmethod
    def getErrors(cls, one, other):
        return set(one) ^ set(other)

    @staticmethod
    def getMsg(errors):
        return f"outliers={errors}"


class MustNotIntersect(LazyException):

    @classmethod
    def getErrors(cls, one, other):
        return set(one) & set(other)

    @staticmethod
    def getMsg(errors):
        return f"intersections={errors}"


class MustContain(LazyException):

    @classmethod
    def getErrors(cls, element, data):
        if element not in data:
            return element, data

    @staticmethod
    def getMsg(errors):
        element, data = errors
        return f"element={element} must be in data={data}"


class MustNotContain(LazyException):

    @classmethod
    def getErrors(cls, element, data):
        if element in data:
            return element, data

    @staticmethod
    def getMsg(errors):
        element, data = errors
        return f"element={element} must not be in data={data}"


class MustBeTheSame(LazyException):

    @classmethod
    def getErrors(cls, *args):
        histogram = Counter(args)
        return dict(histogram) if len(histogram) != 1 else None

    @staticmethod
    def getMsg(errors):
        return f"histogram={errors}"


class MustBeTheSameLengths(LazyException):

    @classmethod
    def getErrors(cls, *args):
        histogram = Counter([ len(a) for a in args ])
        return dict(histogram) if len(histogram) != 1 else None

    @staticmethod
    def getMsg(errors):
        return f"lengthsHistogram={errors}"

class MustBeDifferentLengths(LazyException):

    @classmethod
    def getErrors(cls, *args):
        lengths   = [ len(a) for a in args ]
        histogram = Counter(lengths)
        return dict(histogram) if len(histogram) != len(lengths) else None

    @staticmethod
    def getMsg(errors):
        return f"lengthsHistogram={errors}"


class MustBeDifferentValues(LazyException):

    @classmethod
    def getErrors(cls, *args):
        counter = Counter(*args)
        return dict(counter) if len(counter) == 1 else None

    @staticmethod
    def getMsg(errors):
        return f"lengthsHistogram={errors}"


class TypeMismatch(LazyException):

    @classmethod
    def getErrors(cls, instance, expected):
        if not isinstance(instance, expected):
            return instance, expected

    @staticmethod
    def getMsg(errors):
        instance, expected = errors
        return f"received=({instance}, {type(instance)}), expected={expected}"


class ObjectIsEmptyOrNone(LazyException):

    @classmethod
    def getErrors(cls, instance):
        if not instance:
            return instance

    @staticmethod
    def getMsg(errors):
        return f"received=({errors}, {type(errors)})"