from practice.frameworks import exception as ex


class Rows:
    """ the data that populates a table """

    @classmethod
    def fromArrays(cls, arrays):
        return cls.fromDict({i: array for i, array in enumerate(arrays)})

    @classmethod
    def fromDict(cls, data):
        rows = {}
        for array in data.values():
            for i, e in enumerate(array):
                rows.setdefault(i, []).append(e)
        values = [ tuple(v) for v in rows.values() ]
        return cls.fromList( values )

    @classmethod
    def fromList(cls, values):
        """ a list of iterables [ (val1, .. valn), ... ]"""
        return cls(values)

    def __init__(self, data):
        data = self._fromList(data or [])
        self.validate(data)
        self.data  = data
        self.nrows = len(data)
        self.ncols = len(data[0]) if data else 0

    @staticmethod
    def _fromList(data):
        return [ tuple(row) for row in data ]

    @staticmethod
    def validate(data):
        ex.MustBeTheSameLengths.raiseIf( *[row for row in data] )

    def asNative(self):
        return self._fromList( self.data )

    def asRowsTyped(self):
        """ ensures that the columns in the rows are the same type """
        types = []
        for row in self.data:
            types.append( tuple(type(r) for r in row) )

        ex.MustBeTheSame.raiseIf( *types )
        return Rows( self.data )

    def asArrays(self):
        data = { i: [] for i in range(self.ncols) }
        for row in self.asNative():
            for i, e in enumerate(row):
                data[i].append(e)
        return [ tuple(v) for v in data.values() ]
